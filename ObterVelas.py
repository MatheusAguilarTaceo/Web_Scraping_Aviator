from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options #opções para o navegador
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
 
import time
import os
import datetime
import pytz
import mysql.connector
from mysql.connector import pooling




class Utilizar:
    def __init__(self):            
        self.login = None
        self.senha = None
        self.site = None
        self.connection_pool = None
        self.contador = 0
        self.i = True       
        self.navegador = None
        self.candle_list = []
        self.candle_list_previous = []
        self.candle_list_insert = []
    

use = Utilizar()
    
def iniciar_programa():
    try:
        options = Options()  
        user_agent = UserAgent().random
        options.add_argument(f'user-agent={user_agent}')
    # options.add_argument("--headless")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-logging")
        use.navegador = webdriver.Chrome(options = options)

        link_site = 'https://b2xbet.com/'
        use.navegador.get("https://b2xbet.com/")
        time.sleep(10)
        btn_entrar = use.navegador.find_element(By.CLASS_NAME, 'btn.s-small.sign-in')
        btn_entrar.click()
        time.sleep(10)
        use.navegador.find_elements(By.CLASS_NAME, 'form-control-input-bc')
        [input_email, input_password] = use.navegador.find_elements(By.CLASS_NAME, 'form-control-input-bc')
        btn_entrar = use.navegador.find_elements(By.CLASS_NAME, 'btn.a-color')[2]
        input_email.send_keys('theusaguilar2@gmail.com')
        input_password.send_keys('Teu292112')
        btn_entrar.click()
        time.sleep(5)
        use.navegador.get('https://www.b2xbet.net/pb/?openGames=806666-real&gameNames=Aviator')
        time.sleep(15)
        use.navegador.switch_to.frame(0)
        time.sleep(10)
        iframe_jogo_url = use.navegador.find_element(By.TAG_NAME, 'iframe').get_attribute('src')
        use.navegador.get(iframe_jogo_url)
        time.sleep(10)


        db_config = {
            'host': '154.56.48.154',
            'user': 'u114422138_gg_aviator',
            'password': 'Aviator_21152926',
            'database': 'u114422138_app_gg_aviator'
        }

        pool_config = {
            'pool_name': 'pool_b2xbet',
            'pool_size': 5,
            'autocommit': True
        }

        use.connection_pool = pooling.MySQLConnectionPool(**db_config, **pool_config)

        firstCandles()
        while True:
            use.candle_list = obterVela()
            if(filterCandles()):
                for candle in use.candle_list_insert:
                    insertCandle(candle)
                    
                use.candle_list_insert = []
    except:
        use.connection_pool.stop()  

def firstCandles():
    try:
        candle_list = use.navegador.find_elements(By.CLASS_NAME, 'payout.ng-star-inserted')
        candle_date_time = []
        day = datetime.datetime.now().strftime('%Y-%m-%d')
        selectCandle()
        for tag_candle in candle_list[0:7]:
            tag_candle.click()
            time.sleep(0.5)
            header_modal = use.navegador.find_element(By.CLASS_NAME, 'modal-header')
            candle = float(tag_candle.text.replace('x', ''))

            hour =  header_modal.find_element(By.CLASS_NAME, 'header__info-time').text
            date = f"{day} {hour}"
            date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').astimezone()
            date = date.astimezone(pytz.timezone('UTC'))
            date = f"'{date.strftime('%Y-%m-%d %H:%M:%S')}'"
            button_close = header_modal.find_element(By.TAG_NAME, 'button')
            button_close.click()
            time.sleep(0.5)
            candle_date_time.insert(0, [candle, date])
            use.candle_list.append(candle)
        if(filterCandles()):
            for list in candle_date_time:
                for candle in use.candle_list_insert:
                    if(candle == list[0]):
                        insertCandle(candle, list[1])
                        use.candle_list_insert.pop(0)
                    break
            use.candle_list_insert = []    
        return 

    except Exception  as error:
        print('ERRO = ', error)
        use.navegador.get('https://www.b2xbet.net/pb/?openGames=806666-real&gameNames=Aviator')
        time.sleep(15)
        use.navegador.switch_to.frame(0)
        iframe_jogo_url = use.navegador.find_element(By.TAG_NAME, 'iframe').get_attribute('src')
        use.navegador.get(iframe_jogo_url)
        time.sleep(10)
        return firstCandles()


def obterVela():
    try:
        candle_list = use.navegador.find_elements(By.CLASS_NAME, 'payout.ng-star-inserted')
        return [float(candle.text.replace('x','')) for candle in candle_list[0:7]]
    except:
        use.navegador.get('https://www.b2xbet.net/pb/?openGames=806666-real&gameNames=Aviator')
        time.sleep(15)
        use.navegador.switch_to.frame(0)
        iframe_jogo_url = use.navegador.find_element(By.TAG_NAME, 'iframe').get_attribute('src')
        use.navegador.get(iframe_jogo_url)
        time.sleep(10)
        return obterVela()
    
def insertCandle(candle , date_time = 'UTC_TIMESTAMP()'):
    connection = 0
    cursor = 0
    try:
        connection = use.connection_pool.get_connection()
        sql = f"INSERT INTO b2xbet_2023 VALUES ( default, {candle}, {date_time})"
        cursor = connection.cursor()
        cursor.execute(sql)
        cursor.close()
        connection.close()
    except mysql.connector.Error as error:
        if(cursor):
            cursor.close()
        if(connection):
            connection.close()
        print('ERRO = ', error)
        time.sleep(0.5)
        insertCandle(candle)

def selectCandle():
    connection = 0
    cursor = 0
    try:
        sql = "SELECT candle from b2xbet_2023 ORDER BY id DESC LIMIT 7"
        connection = use.connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        if(result):
            for candle in result:
                use.candle_list_previous.append(float (candle[0]))
                cursor.close()
                connection.close()
            return
        use.candle_list_previous = [0]    
        cursor.close()
        connection.close()
    except Exception as error:
        if(cursor):
            cursor.close()
        if(connection):
            connection.close()
        use.candle_list_previous = []
        print(error)
        selectCandle()

        
def filterCandles():
    if(use.candle_list != []):
        for i in  range(len(use.candle_list_previous)):
            for j in range(len(use.candle_list)):
                if(use.candle_list_previous[i] == use.candle_list[j]):
                    if(use.candle_list_previous[i+1] == use.candle_list[j+1] and use.candle_list_previous[i+1] == use.candle_list[j+1]):
                        use.candle_list_previous = use.candle_list
                        return True
                use.candle_list_insert.insert(0, use.candle_list[j])
        use.candle_list_previous = use.candle_list
        return True
    return False     
       
iniciar_programa()
