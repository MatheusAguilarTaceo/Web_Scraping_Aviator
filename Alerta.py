import os
import EnviarEmail
from CapturaDados import horario
from CapturaDados import data

contador = 0
def alerta_1x(numero):
    file = f'1X_Contador - {data()}.csv'
    if(numero < 2):
        global contador
        contador =+ 1
        if(not os.path.exists(f"{file}")):
            with open(f"{file}", "w") as f:
                f.write("Quantidades Maxima de 1x Maior ou Igual a 10\n")
        with open(f"{file}", "a") as f:
            f.write(f"{numero}\t")        
        if(contador >= 10):
            EnviarEmail.enviar_email('Alerta 1X', file)
    else:
        contador  = 0
        with open(f"{file}", "a") as f:
            horaAtual = horario().strftime(("%H:%M:%S"))
            f.write(f"{horaAtual}\n")
                