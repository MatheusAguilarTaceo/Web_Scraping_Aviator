from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


from multiprocessing.pool import Pool
from multiprocessing import Process
from threading import Thread
import time
import datetime
import pytz
import mysql.connector


class BettingHouse():

    def __init__(self, callback, table):
        self.callback = callback
        self.table = table
        self.browser_chrome = None
    

    def openBrowser(self):
        user_agent = UserAgent().random
        options = Options()
        options.add_argument(f'user-agent={user_agent}')
        # options.add_argument('--headless')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-logging')
        # nonlocal self.browser_chrome
        self.browser_chrome = webdriver.Chrome(options= options)

    def closeBrowser(self):
        self.browser_chrome.quit()


    def walkToTheGame(self):
        self.callback(self.browser_chrome)

    def connectDB(self):
        db_config = {
        'host': 'localhost',
        'user': 'gg_aviator',
        'password': 'aviator_21152926',
        'database': 'app_gg_aviator'
        }

        connection = mysql.connector.connect(**db_config)
        return connection
    
    def selectDB(self, connection):
        sql = f'SELECT candle FROM {self.table} ORDER BY id DESC LIMIT 7'
        with connection.cursor() as cursor:
            old_candles = []
            cursor.execute(sql)
            result = cursor.fetchall()
            if(result):
                for candle in result:
                    old_candles.append(float(candle[0]))

                cursor.close()
                return old_candles
            old_candles = [0]
            return old_candles
    
    
    def insertDB(self, connection, candle, date_time = 'UTC_TIMESTAMP()'):
        sql = f'INSERT INTO {self.table} VALUES (default, {candle}, {date_time})'
        with connection.cursor() as cursor:
            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit()
            cursor.close()

    def dataScraping(self):

        def checkCandlesDB():
            connection = self.connectDB()
            old_candles = self.selectDB(connection)
            new_candles_hours = getCandlesAndHours()
            new_candles, new_hours = list(zip(*new_candles_hours))
        
            insert_candles_hours = filterCandlesAndHours(new_candles, old_candles, new_hours)
            if(insert_candles_hours):
                for candle, hour in reversed(insert_candles_hours):
                    self.insertDB(connection, candle, hour)
            
            connection.close()
            return new_candles        

        def getCandlesAndHours():
            candles_list = self.browser_chrome.find_elements(By.CLASS_NAME, 'payout.ng-star-inserted')
            day = datetime.datetime.now().strftime('%Y-%m-%d')
            new_candles_hours = []
            if(candles_list):
                for tag_candle in candles_list[0:7]:
                    tag_candle.click()
                    time.sleep(1)
                    candle = float(tag_candle.text.replace('x', ''))
                    
                    header_modal = self.browser_chrome.find_element(By.CLASS_NAME, 'modal-header')
                    hour =  header_modal.find_element(By.CLASS_NAME, 'header__info-time').text
                    
                    date = f"{day} {hour}"
                    date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                    date = date.astimezone(pytz.timezone('UTC'))
                    date = f"'{date.strftime('%Y-%m-%d %H:%M:%S')}'"
                    
                    button_close = header_modal.find_element(By.TAG_NAME, 'button')
                    button_close.click()
                    time.sleep(0.5)
                    
                    new_candles_hours.append([candle, date])
                return new_candles_hours   
            
        def filterCandlesAndHours(new_candles, old_candles, new_hours):  
            if(new_candles != []):
                insert_candles_hours = []
                i = 0
                for j in range(len(new_candles)):
                    if(old_candles[i] == new_candles[j]):
                        if(old_candles[i+1] == new_candles[j+1] and old_candles[i+2] == new_candles[j+2]):
                            return insert_candles_hours
                    insert_candles_hours.append([new_candles[j], new_hours[j]])

                return insert_candles_hours
            return False  
      


        def getCandles():
            candles_list = self.browser_chrome.find_elements(By.CLASS_NAME, 'payout.ng-star-inserted')
            if(candles_list):
               return [float(candle.text.replace('x','')) for candle in candles_list[0:7]]

        def filterCandles(new_candles, old_candles):  
            if(new_candles != []):
                insert_candles = []
                i = 0
                for j in range(len(new_candles)):
                    if(old_candles[i] == new_candles[j]):
                        if(old_candles[i+1] == new_candles[j+1] and old_candles[i+2] == new_candles[j+2]):
                            return insert_candles
                    insert_candles.append(new_candles[j])
                return insert_candles
            return False  
        

        old_candles = checkCandlesDB()

        while True:
            new_candles = getCandles()
            insert_candles = filterCandles(new_candles, old_candles)
            if(insert_candles):
                with self.connectDB() as connection:
                    for candle in insert_candles:
                        self.insertDB(connection, candle)
                    
                    connection.close()
                    old_candles = new_candles




def houseGoldebet(browser_chrome):
    browser_chrome.get('https://goldebet.com/casino')
    time.sleep(10)
    login_btn = browser_chrome.find_element(By.CLASS_NAME, 'login-btn')
    login_btn.click()
    time.sleep(0.5)

    [email_input, password_input] = browser_chrome.find_elements(By.CLASS_NAME, 'form-control')
    email_input.send_keys('theusaguilar2@gmail.com') 
    time.sleep(0.25)
    password_input.send_keys('Teu292112')
    time.sleep(0.25)

    login_btn = browser_chrome.find_element(By.CLASS_NAME, 'md-button')
    login_btn.click()
    time.sleep(5)

    browser_chrome.get('https://goldebet.com/casino?gameid=7339')
    time.sleep(7)
    iframe_aviator = browser_chrome.find_element(By.TAG_NAME, 'iframe').get_attribute('src')

    browser_chrome.execute_script("window.open('', '_blank');")
    handles  = browser_chrome.window_handles

    browser_chrome.switch_to.window(handles[1])
    browser_chrome.get(iframe_aviator)

    browser_chrome.switch_to.window(handles[0])
    time.sleep(1)
    
    close_btn = browser_chrome.find_element(By.CLASS_NAME, 'btn-close-modal')
    close_btn.click()

    menu = browser_chrome.find_element(By.CLASS_NAME, 'profile-btn')
    menu.click()

    close_btn = browser_chrome.find_elements(By.CLASS_NAME, 'ms-0')[7]
    close_btn.click()
    browser_chrome.close()
    browser_chrome.switch_to.window(handles[1])
    time.sleep(15)

def houseB2xbet(browser_chrome):
    browser_chrome.get('https://www.b2xbet.net/pb/?openGames=806666-real&gameNames=Aviator')
    time.sleep(15)
    browser_chrome.find_elements(By.CLASS_NAME, 'form-control-input-bc')
    [input_email, input_password] = browser_chrome.find_elements(By.CLASS_NAME, 'form-control-input-bc')
    btn_entrar = browser_chrome.find_elements(By.CLASS_NAME, 'btn.a-color')[2]
    input_email.send_keys('diversaoanimes2021@gmail.com')
    input_password.send_keys('Eighty-six3231')
    time.sleep(1)
    btn_entrar.click()
    time.sleep(10)
    browser_chrome.switch_to.frame(0)
    time.sleep(5)
    iframe_jogo_url = browser_chrome.find_element(By.TAG_NAME, 'iframe').get_attribute('src')
    browser_chrome.execute_script("window.open('', '_blank');")
    time.sleep(0.5)
    all_handles = browser_chrome.window_handles
    time.sleep(0.5)
    browser_chrome.switch_to.window(all_handles[1])
    browser_chrome.get(iframe_jogo_url)
    time.sleep(10)
    browser_chrome.switch_to.window(all_handles[0])
    time.sleep(1)
    actions = ActionChains(browser_chrome)
    actions.move_by_offset(100, 100).click().perform()
    time.sleep(0.5)
    menu = browser_chrome.find_elements(By.CLASS_NAME, 'nav-menu-sub')[1]
    browser_chrome.execute_script("arguments[0].style.visibility = 'visible';", menu)
    browser_chrome.execute_script("arguments[0].style.opacity = '1';", menu)
    btn_close = browser_chrome.find_element(By.CLASS_NAME, 'btn.ellipsis')
    time.sleep(0.5)
    btn_close.click()
    time.sleep(5)
    browser_chrome.close()
    browser_chrome.switch_to.window(all_handles[1])
    time.sleep(15)



def init(house, table):
    B = BettingHouse(house, table) 
    B.openBrowser()
    i = 0
    while i < 10:
        try:
            B.walkToTheGame()
            B.dataScraping()
        except Exception as error:
            print('Erro  = ', error)    
        
        i +=1
    B.closeBrowser()    

if __name__ == '__main__':
    with Pool(2) as p:
        p.starmap(init, [[houseB2xbet, 'b2xbet_2023'], [houseGoldebet, 'goldebet_2023']])



    
    







