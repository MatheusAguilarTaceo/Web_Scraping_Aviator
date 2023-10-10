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
import PySimpleGUI as sg
import sys
import Alerta
import threading

import CapturaDados 

def Tela_configuracao():
    lista = []
    layout = [
        [sg.Text('Configurações', font=('Helvetica', 14, 'bold'), justification='center')],
        [sg.HorizontalSeparator()],
        [sg.Text("Login"), sg.Input(key = "_LOGIN_")],
        [sg.Text("Senha"), sg.Input(key = "_SENHA_")],
        [sg.Button('Salvar', key='_SALVAR_'), sg.Text('Nome do Arquivo', size=(14,1)), sg.Input(key='_ARQUIVO_', size=(20, 1))],
        [sg.HorizontalSeparator()],
        [sg.Button('Escolher Site', key='_ESCOLHER_'), sg.Combo(lista, key='_LISTA_', size=(20, 1))]
    ]
    return sg.Window('Configurações', layout, font=('Helvetica', 11), element_justification='', margins=(10, 10)).finalize()

def Tela_espera():
    layout = [
        [sg.Text('ESPERE FAZER O LOGIN, DEPOIS APERTE O BOTÃO')],
        [sg.Button('Espere', key = '_ESPERE_')]
    ]
    return sg.Window('Tela de Espera', layout, font=('Helvetica', 11), element_justification= '', margins= (10, 10)).finalize()



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
# janela = Tela_configuracao()

while False:
    events, value = janela.read()
    if events == sg.WIN_CLOSED or janela == "Exit":
        sys.exit()
        break
    
    match events:    
        case "_ESCOLHER_":
            use.site = value["_LISTA-SITE_"]
            with open(f"{caminho}/{use.site}", "r") as f:
                use.link_site = f.readlines()
            use.login = value["_LOGIN_"]
            use.senha = value["_SENHA_"] 
            use.i = True
    if (use.i == True):
        threading.Thread(target = captura_10x).start()
        use.i = False
        break
             


def iniciar_programa():
    options = Options()  
    user_agent = UserAgent().random
    options.add_argument(f'user-agent={user_agent}')
    options.headless = False 
    options.add_argument("--disable-popup-blocking")
    use.navegador = webdriver.Chrome(options = options)

    link_site = 'https://b2xbet.com/'
    use.navegador.get("https://b2xbet.com/")
    time.sleep(10)
    btn_entrar = use.navegador.find_element(By.CLASS_NAME, 'btn.s-small.sign-in')
    btn_entrar.click()
    time.sleep(10)
    use.navegador.find_elements(By.CLASS_NAME, 'orm-control-input-bc')
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
    iframe = use.navegador.switch_to.frame(0)
    print("IFRAME AVIATOR", iframe)



    janela = Tela_espera()
    
    while True:
        events, values = janela.read()
        match events:
            case '_ESPERE_':
                janela.close()
                break
    
    
    while True:
        use.candle_list = obter_vela()
        if(use.candle_list != use.candle_list_previous):
            # CapturaDados.conexao_bd(use.candle_list[0])
            use.candle_list_previous = use.candle_list
            print('VELA = ', use.candle_list[0])

def obter_vela():
    try:
        candle_list = use.navegador.find_elements(By.CLASS_NAME, 'payout.ng-star-inserted')
        return [float(candle.text.replace("x","")) for candle in candle_list[0:5]]
    except:
        use.navegador.refresh()
        time.sleep(6)
        return obter_vela()




iniciar_programa()
