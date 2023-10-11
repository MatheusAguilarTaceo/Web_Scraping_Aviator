from datetime import datetime, timedelta
import os
from pathlib import Path
import EnviarEmail
import mysql.connector
contador = 0
coluna = 0 


def horario():
    hora = datetime.now()
    return hora.strftime("%H:%M:%S")

def data():
    data = datetime.now()
    # return data.strftime("%d-%m-%Y")
    return data.strftime("%y-%m-%d")

def captura_10x(numero):
    global contador             
    title = 'Historico_10X'    
    if(numero >= 10) :
        caminho = Path()
        file = f"10x Contagem - {data()}.csv"
        if(not os.path.exists(f"{caminho}/{file}")):
            with open(f"{caminho}/{file}", "w") as f:
                f.write("Vela Atual\t")
                f.write("Intervalo entre 10x\t")
                f.write("Data/Hora\n")
        with open(f"{caminho}/{file}", "a") as f:
            hora = horario().strftime(("%H:%M:%S"))
            f.write(f"{numero}\t")
            f.write(f"{contador}\t")
            f.write(f"{data()} {hora}\n")       
        EnviarEmail.enviar_email(title, file) 
        contador = 0
    else:
        contador =  contador + 1
            
           
def captura_historico(numero, hora):
    global coluna
    file = f"Historico_Aviator - {data()}.csv"
    title = 'Historico Aviator Completo'       
    if(not os.path.exists (f"{file}")):
        with open(f"{file}", "w") as f:
            for i in range(16):
                f.write(f"{i+1}° Coluna\t") 
            f.write("Hora\n")    
    with open(f"{file}", "a") as f:
        f.write(f"{numero}\t")
        coluna = coluna + 1
        if(coluna == 16):
            horaAtual = horario().strftime(("%H:%M:%S"))
            f.write(f"{horaAtual}\n")
            coluna  = 0
    minuto = timedelta(hours= 0, minutes= 30, seconds= 0)
    tempo = hora + minuto
    if(horario() >= tempo):
        EnviarEmail.enviar_email(title, file)
        return horario()
    else:
        return hora

def conexao_bd(candle):
    connect = mysql.connector.connect(host='154.56.48.154', database='u114422138_gg_aviator', user='u114422138_gg_aviator', password='Teu292112@ma')
    if connect.is_connected():
        sql = f"INSERT INTO pagbet_2023_10 VALUES (default, '{candle}', '{horario()}', '{data()}')"
        cursor = connect.cursor()
        cursor.execute(sql)
        cursor.close()
        connect.close()

