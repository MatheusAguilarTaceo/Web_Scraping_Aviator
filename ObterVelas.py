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

    first_candles()
    
    while True:
        print('PREVIOUSS', use.candle_list_previous)
        use.candle_list = obter_vela()
        print('NEXT', use.candle_list)
        if(use.candle_list != []):
            for i in  range(len(use.candle_list_previous)):
                for j in range(len(use.candle_list)):
                    if(use.candle_list_previous[i] == use.candle_list[j]):
                        if(use.candle_list_previous[i+1] == use.candle_list[j+1] and use.candle_list_previous[i+1] == use.candle_list[j+1]):
                            break
                    use.candle_list_insert.append(use.candle_list[j])    
                else:
                    continue
                break  
            for candle in reversed(use.candle_list_insert):
                insertCandle(candle)
                
            print('Parece que n esta entrando aqui')
            use.candle_list_previous = use.candle_list
            use.candle_list_insert= []

def first_candles():
    try:
        candle_list = use.navegador.find_elements(By.CLASS_NAME, 'payout.ng-star-inserted')
        connect = use.connection_pool.get_connection()
        cursor = connect.cursor()
        day = datetime.datetime.now().strftime('%Y-%m-%d')

        for candle in reversed(candle_list[0:7]):
            candle.click()
            time.sleep(0.5)
            header_modal = use.navegador.find_element(By.CLASS_NAME, 'modal-header')
            candle = float(candle.text.replace('x', ''))
            hour =  header_modal.find_element(By.CLASS_NAME, 'header__info-time').text
            date = f'{day} {hour}'
            date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').astimezone()
            date = date.astimezone(pytz.timezone('UTC'))
            date = date.strftime('%Y-%m-%d %H:%M:%S')
            print(candle, ' ', date)
            sql = f" INSERT INTO b2xbet_2023 values (default, {candle}, '{date}')"
            cursor.execute(sql)

            button_close = header_modal.find_element(By.TAG_NAME, 'button')
            button_close.click()
            use.candle_list_previous.insert(0, candle)
            time.sleep(0.5)
        cursor.close() 
        connect.close()  
        return 

    except Exception  as error:
        print(error)
        use.navegador.get('https://www.b2xbet.net/pb/?openGames=806666-real&gameNames=Aviator')
        time.sleep(15)
        use.navegador.switch_to.frame(0)
        iframe_jogo_url = use.navegador.find_element(By.TAG_NAME, 'iframe').get_attribute('src')
        use.navegador.get(iframe_jogo_url)
        time.sleep(10)
        return first_candles()


def obter_vela():
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
        return obter_vela()
    



def insertCandle(candle , ):
    try:
        connection = use.connection_pool.get_connection()
        sql = f"INSERT INTO b2xbet_2023 VALUES ( default, {candle}, UTC_TIMESTAMP() )"
        cursor = connection.cursor()
        cursor.execute(sql)
        cursor.close()
        connection.close()
    except mysql.connector.Error as error:
        print('ERRO = ', error)
        time.sleep(0.5)
        insertCandle(candle)

        
iniciar_programa()
