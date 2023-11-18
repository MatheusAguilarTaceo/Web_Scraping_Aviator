from  datetime import datetime
import mysql.connector
from mysql.connector import pooling
import pytz
import time
import random


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

connection_pool = pooling.MySQLConnectionPool(**db_config, **pool_config)

connect = connection_pool.get_connection()




def insertCandle(candle):
    try:
        connection = connection_pool.get_connection()
        print('Conectado')
        sql = f"INSERT INTO teste VALUES (default, '{candle}', '{hour()}', '{date()}')"
        cursor = connection.cursor()
        cursor.execute(sql)
        cursor.close()
        connection.close()
    except mysql.connector.Error as error:
        print('ERRO = ', error)
        time.sleep(0.5)
        insertCandle(candle)
    finally:
        print(candle)   



def hour():
    hour = datetime.now(pytz.utc)
    return hour.strftime('%H:%M:%S')
def date():
    date = datetime.now(pytz.utc)
    return date.strftime('%Y-%m-%d')

i = 0
while True:
    candle  = random.randint(1,1000)
    insertCandle(candle)
    i += 1
    time.sleep(5)
    if i > 10:
        break

# print(date())
# print(hour())
