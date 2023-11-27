from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import time
import datetime
import pytz
import mysql.connector


def driver():
    user_agent = UserAgent().random

    options  = Options()
    options.add_argument(f'user-agent={user_agent}')
    # options.add_argument('--headless')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-logging')
    
    driver_chrome = webdriver.Chrome(options= options)
    driver_chrome.get('https://goldebet.com/casino')
    time.sleep(10)

    login_btn = driver_chrome.find_element(By.CLASS_NAME, 'login-btn')
    login_btn.click()
    time.sleep(0.5)

    [email_input, password_input] = driver_chrome.find_elements(By.CLASS_NAME, 'form-control')
    email_input.send_keys('theusaguilar2@gmail.com') 
    time.sleep(0.25)
    password_input.send_keys('Teu292112')
    time.sleep(0.25)

    login_btn = driver_chrome.find_element(By.CLASS_NAME, 'md-button')
    login_btn.click()
    time.sleep(5)

    driver_chrome.get('https://goldebet.com/casino?gameid=7339')
    time.sleep(5)
    iframe_aviator = driver_chrome.find_element(By.TAG_NAME, 'iframe').get_attribute('src')
    print(iframe_aviator)
    driver_chrome.execute_script("window.open('', '_blank');")
    handles  = driver_chrome.window_handles
    driver_chrome.switch_to.window(handles[1])
    driver_chrome.get(iframe_aviator)
    driver_chrome.switch_to.window(handles[0])
    close_btn = driver_chrome.find_element(By.CLASS_NAME, 'btn-close-modal')
    close_btn.click()
    driver_chrome.switch_to.window(handles[1])
    return driver_chrome

def obterVelas():
    candle_list = driver_chrome.find_elements(By.CLASS_NAME, 'payout.ng-star-inserted')
    return [float(candle.text.replace('x','')) for candle in candle_list[0:7]]


def firstCandles():
    candle_date_time = []
    day = datetime.datetime.now().strftime('%Y-%m-%d')

    candle_list = driver_chrome.find_elements(By.CLASS_NAME, 'payout.ng-star-inserted')
    candle_list_previous = selectCandle()
    for tag_candle in candle_list[0:7]:
        tag_candle.click()
        time.sleep(0.5)
        candle = float(tag_candle.text.replace('x', ''))
        
        header_modal = driver_chrome.find_element(By.CLASS_NAME, 'modal-header')
        hour =  header_modal.find_element(By.CLASS_NAME, 'header__info-time').text
        
        date = f"{day} {hour}"
        date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').astimezone()
        date = date.astimezone(pytz.timezone('UTC'))
        date = f"'{date.strftime('%Y-%m-%d %H:%M:%S')}'"
        
        button_close = header_modal.find_element(By.TAG_NAME, 'button')
        button_close.click()
        time.sleep(0.5)
        
        candle_date_time.insert(0, [candle, date])
        candle_list.append(candle)

    candle_list_insert = filterCandles(candle_list, candle_list_previous)
    
    if(candle_list_insert):
        for list in candle_date_time:
            for candle in candle_list_insert:
                if(candle == list[0]):
                    insertCandle(candle, list[1])
                    candle_list_insert.pop(0)
                break
        candle_list_insert = []    
    
    return candle_list

def selectCandle():
    db_config = {
        'host': '154.56.48.154',
        'user': 'u114422138_gg_aviator',
        'password': 'Aviator_21152926',
        'database': 'u114422138_app_gg_aviator'
    }

    connection = 0
    cursor = 0
    candle_list_previous = []
    try:
        connection = mysql.connector.connect(**db_config)
        sql = "SELECT candle from b2xbet_2023 ORDER BY id DESC LIMIT 7"
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        if(result):
            for candle in result:
                candle_list_previous.append(float (candle[0]))
            cursor.close()
            connection.close()
            return
        candle_list_previous = [0]    
        cursor.close()
        connection.close()
    except Exception as error:
        if(cursor):
            cursor.close()
        if(connection):
            connection.close()
        candle_list_previous = []
        print(error)
        selectCandle()    

def insertCandle(candle , date_time = 'UTC_TIMESTAMP()'):
    db_config = {
        'host': '154.56.48.154',
        'user': 'u114422138_gg_aviator',
        'password': 'Aviator_21152926',
        'database': 'u114422138_app_gg_aviator'
    }
    connection = 0
    cursor = 0

    try:
        connection = mysql.connector.connect(**db_config)
        sql = f"INSERT INTO b2xbet_2023 VALUES ( default, {candle}, {date_time})"
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
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

def filterCandles(candle_list, candle_list_previous):
    if(candle_list != []):
        candle_list_insert = []
        for i in  range(len(candle_list_previous)):
            for j in range(len(candle_list)):
                if(candle_list_previous[i] == candle_list[j]):
                    if(candle_list_previous[i+1] == candle_list[j+1] and candle_list_previous[i+1] == candle_list[j+1]):
                        return candle_list_insert
                candle_list_insert.insert(0, candle_list[j])
        return candle_list_insert
    return False  



driver_chrome = driver()
candle_list_previous = firstCandles()

while True:
    candle_list = obterVelas()
    if(candle_list):
        for candle in candle_list:
            insertCandle(candle)

    



