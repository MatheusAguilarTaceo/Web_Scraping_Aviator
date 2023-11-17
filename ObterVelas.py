from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome import options #busca dos elementos na tela
from selenium.webdriver.chrome.options import Options #opções para o navegador
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
 
import time
import os
import mysql.connector
from datetime import datetime, timedelta





class Utilizar:
    def __init__(self):            
        self.login = None
        self.senha = None
        self.site = None
        self.contador = 0
        self.i = True       
        self.navegador = None
        self.candle_list = None
        self.candle_list_previous = None
    

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
    btn_entrar = use.navegador.find_element(By.CLASS_NAME, 'btn.a-color ')
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
    print("IFRAME AVIATOR", iframe_jogo_url)




    while True:
        use.candle_list = obter_vela()
        if(use.candle_list != use.candle_list_previous):
            conexao_bd(use.candle_list[0])
            use.candle_list_previous = use.candle_list
            os.system('cls')
           
            

def obter_vela():
    try:
        candle_list = use.navegador.find_elements(By.CLASS_NAME, 'payout.ng-star-inserted')
        return [float(candle.text.replace("x","")) for candle in candle_list[0:5]]
    except:
        use.navegador.refresh()
        time.sleep(10)
        use.navegador.switch_to.default_content()
        time.sleep(3)
        use.navegador.switch_to.frame(0)
        time.sleep(2)
        iframe = use.navegador.switch_to.frame(0)
        print("IFRAME AVIATOR", iframe)
        return obter_vela()


def conexao_bd(candle):
    connect = mysql.connector.connect(host='154.56.48.154', database='u114422138_app_gg_aviator', user='u114422138_gg_aviator', password='Users21152926')
    if connect.is_connected():
        sql = f"INSERT INTO b2xbet_2023_11 VALUES (default, '{candle}', '{horario()}', '{data()}')"
        cursor = connect.cursor()
        cursor.execute(sql)
        cursor.close()
        connect.close()



def horario():
    hora = datetime.now()
    return hora.strftime("%H:%M:%S")

def data():
    data = datetime.now()
    return data.strftime("%y-%m-%d")        

iniciar_programa()
