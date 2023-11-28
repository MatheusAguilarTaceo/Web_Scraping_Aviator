from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


import time
import datetime
import pytz
import mysql.connector
from multiprocessing import ProcessS


def bettingHouse(url, table):
    browser_chrome = None
    
    def openHouse():
        user_agent = UserAgent().random()
        options = Options()
        options.add_argument(f'user-agent = {user_agent}')
        # options.add_argument('--headless')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-logging')

        browser_chrome = webdriver.Chrome(options= options)
        return

    def closeHouse():
        browser_chrome.quit()


    def walkToTheGame(callback):
        callback()

    def connectDB():
        db_config = {
        'host': 'localhost',
        'user': 'gg_aviator',
        'password': 'aviator_21152926',
        'database': 'app_gg_aviator'
        }

        connection = mysql.connector.connect(db_config)
        return connection
    
    def selectDB(connection):
        sql = f'SELECT candle FROM {table} ORDER BY id DESC LIMIT 7'
        cursor = connection.cursor()
        old_candles = []
        result = cursor.execute(sql)
        for candle in result:
            old_candles.append(float(candle))
        cursor.close()

        return old_candles
        
    def insertDB(connection, candle, date_time = 'UTC_TIMESTAMP()'):
        sql = f'INSERT INTO {table} VALUES (default, {candle}, {date_time})'
        cursor = connection.cursor()
        cursor.execute(sql)
        cursor.close()

    def dataScraping():

        def checkCandlesDB():
            connection = connectDB()
            old_candles = selectDB(connection)
            new_candles_hours = getCandlesAndHours()
            for canndle
            #AQUII COMEÇAR
            insert_candles = filterCandles(new_candles_hours, old_candles)
            for candle in insert_candles:
                insertDB(candle)

        def getCandlesAndHours():
            candles_list = browser_chrome.find_elements(By.CLASS_NAME, 'payout.ng-star-inserted')
            day = datetime.datetime.now().strftime('%Y-%m-%d')
            new_candles_hours = []
            if(candles_list):
                for tag_candle in candles_list[0:7]:
                    tag_candle.click()
                    time.sleep(0.5)
                    candle = float(tag_candle.text.replace('x', ''))
                    
                    header_modal = browser_chrome.find_element(By.CLASS_NAME, 'modal-header')
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

        def getCandles():
            candles_list = browser_chrome.find_elements(By.CLASS_NAME, 'payout.ng-star-inserted')
            if(candles_list):
               return [float(candle.text.replace('x','')) for candle in candles_list[0:7]]

        def filterCandles():  