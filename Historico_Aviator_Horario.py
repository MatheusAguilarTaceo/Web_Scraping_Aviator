from datetime import datetime, timedelta
from pathlib import Path
import numpy as np
import pandas as pd

import Utils 

def validate_time(variable_test):
    try:
        datetime.strptime(variable_test, "%H:%M:%S")
        return True
    except:
        return False
def preencher_lista(lista):
    tamanho = len(lista)
    tamanho = 200 - tamanho
    for i in range(tamanho):
        lista.append(np.nan)
    return lista    
def inicializar_variaveis():
    tempo = timedelta(hours= 1, minutes= 00, seconds= 00)
    hora = "00:00:00"
    hora = datetime.strptime(hora, "%H:%M:%S") 

    dicionario = {}
    hora_aux = hora
    for i in range(24):
        dicionario[hora_aux.strftime("%H:%M:%S")] = []
        hora_aux = hora_aux + tempo
    return dicionario, hora, tempo


def historico_horario(file, use):
    dicionario, hora , tempo = inicializar_variaveis()
    df = pd.read_excel(file, engine = "odf")

    for indice, linha in  df.iterrows():
        for coluna in df.columns:
            if(validate_time(linha[coluna])):   
                print(linha[coluna])
                if(datetime.strptime(linha[coluna], "%H:%M:%S") >= hora+tempo):
                    dicionario[hora.strftime("%H:%M:%S")] = preencher_lista(dicionario[hora.strftime("%H:%M:%S")])
                    hora = hora + tempo 
            else:
                if pd.isna(linha[coluna]) and df.shape[0]-1 ==indice:
                    dicionario[hora.strftime("%H:%M:%S")] = preencher_lista(dicionario[hora.strftime("%H:%M:%S")])
                elif not pd.isna(linha[coluna]):    
                    dicionario[hora.strftime("%H:%M:%S")].append(linha[coluna])

    caminho = use.caminho_historico_horario
    nome_arquivo = f'{caminho}\{caminho.name} - {file.name.split()[2].split(".")[0]}.xlsx'
    df = pd.DataFrame(dicionario)
    df.to_excel(nome_arquivo, index=False)
    df.to_excel()
    print(f'O DataFrame foi salvo em "{nome_arquivo}"')


def iniciar():
    use = Utils.Caminhos_APP()
    lista_arquivos = Utils.listar_Arquivos(use.caminho_historico)
    caminho = use.caminho_historico_horario
    for file in lista_arquivos:
        if (not  Path(f'{caminho}/{caminho.name} - {file.name.split()[2].split(".")[0]}.xlsx').exists() ):
            historico_horario(file, use)
