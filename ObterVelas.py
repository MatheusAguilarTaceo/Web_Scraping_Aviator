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
        self.numeroAnterior = 0
    

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

    janela = Tela_espera()
    
    while True:
        events, values = janela.read()
        match events:
            case '_ESPERE_':
                janela.close()
                break

    use.navegador.switch_to.window(use.navegador.window_handles[1])

    use.navegador.switch_to.frame(0)
    
    # candle_list = use.navegador.find_elements(By.CLASS_NAME, 'bubble-multiplier')
    
    # for candle in candle_list:
    #     print(candle.text)

    
    hora = CapturaDados.horario()
    while True:
        numero = obter_vela()
        if(numero != use.numeroAnterior):
            # CapturaDados.captura_10x(numero)
            # hora = CapturaDados.captura_historico(numero, hora)
            # Alerta.alerta_1x(numero)
            CapturaDados.conexao_bd(numero)
            use.numeroAnterior = numero

def obter_vela():
    # try:
        candle_list = use.navegador.find_elements(By.CLASS_NAME, 'payout.ng-star-inserted')
        # for candle in candle_list:
        #     print(candle.text)
        candle = candle_list[0].text.replace("x", "")                             
        if (candle == ''):
            return  0
        else:
            return  float(candle)
    # except:
    #     use.navegador.refresh()
    #     time.sleep(6)
    #     return obter_vela()




iniciar_programa()
# Abra o link em uma nova aba
# use.navegador.execute_script('window.open(arguments[0]);', link_url)
# WebDriverWait(use.navegador, 30).until(EC.presence_of_element_located((By.TAG_NAME, "button"))