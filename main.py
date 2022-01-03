# -*- coding: utf-8 -*-
from selenium import webdriver
import random
from selenium.webdriver.firefox.service import Service
from bs4 import BeautifulSoup
import json
import time
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def get_sms(id, count = 0, mod = 0):
    url1 = 'https://onlinesim.ru/api/getState.php?apikey=96ad76d72c908e689ce8712bc4b6fc2b'
    param = {
        'message_to_code': True,
        'msg_list': True,
        'tzid': id,
    }
    req = requests.get(url=url1, params=param, verify=False)
    todos = json.loads(req.text)
    cod = ''
    passwor = ''
    print(todos)
    print(todos[0]['response'])
    try:
        if (todos[0]['response'] == 'TZ_NUM_WAIT'):
            time.sleep(10)
            if(count == 20):
                exit()
            cod,passwor = get_sms(id, count=count+1, mod=mod)
        if (todos[0]['response'] == 'TZ_NUM_ANSWER' and mod == 1):
            count = 0
            print(todos[0]['msg'][0]['msg'])
            try:
                print(todos[0]['msg'][1]['msg'])
                passwor = str(todos[0]['msg'][1]['msg'])
            except:
                time.sleep(10)
                if (count == 20):
                    exit()
                cod,passwor = get_sms(id, count=count + 1, mod=mod)
        if (todos[0]['response'] == 'TZ_NUM_ANSWER' and mod == 0):
            print(todos[0]['msg'][0]['msg'])
            cod = str(todos[0]['msg'][0]['msg'])
    except:
        print("Ошибка!")
    return cod,passwor
def buy_number():
    url1 = 'https://onlinesim.ru/api/getNum.php?apikey=96ad76d72c908e689ce8712bc4b6fc2b&service=Kopilka'
    param = {
        'number': True
    }
    req = requests.get(url=url1, params=param, verify=False)
    todos = json.loads(req.text)
    print(todos)
    print(todos['response'])
    number = str(todos['number'])
    id = str(todos['tzid'])
    try:
        if (todos['response'] == 'TZ_NUM_WAIT'):
            print('Ожидаем ответа')
            time.sleep(10)
        if (todos['response'] == '1'):
            print('Номер успешно куплен')
            number2 = todos['number']
            id2 = todos['tzid']
    except:
        print("Ошибка!")
    print(number + " " + id)
    return number,id

def get_inf_numbers_api():
    url = 'https://api-conserver.onlinesim.ru/stubs/handler_api.php'
    settings = {
        "api_key": '96ad76d72c908e689ce8712bc4b6fc2b',
        "action": 'getNumbersStatus',
        "country": "7",
    }
    head = {
        "Content-Type': 'application/json"
    }
    req = requests.post(url, params=settings, headers=head)
    print(req.text)


def get_person():
    file1 = open("persons.txt", "r")
    len = file1.readline()
    count = 0
    name = ''
    famaly_name = ''
    otc = ''
    find = random.randint(0, int(len)-1)
    while True:
        if(count == find):
            line = file1.readline()
            if not line:
                break
            famaly_name = line.rpartition(' ')[0]
            famaly_name = famaly_name.rpartition(' ')[0]
            name = line.partition(' ')[2]
            name = name.rpartition(' ')[0]
            otc = line.partition(' ')[2]
            otc = otc.partition(' ')[2]
            count = count + 1
            break
        temp = file1.readline()
        if not temp:
            break
        count = count + 1
    file1.close
    return famaly_name, name, otc

def get_key():
    file1 = open("keys.txt", "r")
    count = 0
    find = random.randint(1, 198)
    key = ''
    while True:
        if(count == find):
            line = file1.readline()
            key = line
            if not line:
                break
            count = count + 1
            break
        temp = file1.readline()
        if not temp:
            break
        count = count + 1
    file1.close
    if(len(key) > 8):
        key = get_key()
    return key
def get_area():
    k = random.randint(1, 4)
    print(k)
    if(k == 1):
        area = 'Иркутская Область\n'
        city = 'Ангарск'
        return area, city
    if(k == 2):
        area = 'Красноярский Край\n'
        city = 'Минусинск'
        return area, city
    if(k == 3):
        area = 'Красноярский Край\n'
        city = 'Канск'
        return area, city
    if(k == 4):
        area = 'Красноярский Край\n'
        city = 'Красноярск'
        return area, city
def push_next(driver):
    next_btn = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[1]/div/form/div[6]/div/div[8]/span/input')
    next_btn.click()
def get_card():
    file1 = open("cards.txt", "r")
    line_get = file1.readline()
    file1.close()
    file1 = open("cards.txt", "r")
    lines = file1.readlines()
    file1.close()

    file1 = open("cards.txt", "w")
    pattern = re.compile(re.escape(line_get))
    for line in lines:
        result = pattern.search(line)
        if result is None:
            file1.write(line)
    file1.close()
    return line_get
def save_acc(number, passw):
    file1 = open("new_acc.txt", "a")  # режим добавления
    file1.write(number + ":" + passw + '\n')
    file1.close()
def reg(rep = 0, number = '', id = '', card = 0):
    famaly_name = ''
    name = ''
    otc = ''
    famaly_name1, name1, otc1 = get_person()
    famaly_name = famaly_name1
    famaly_name1, name1, otc1 = get_person()
    name = name1
    famaly_name1, name1, otc1 = get_person()
    otc = otc1
    key = get_key()
    ser = Service("/home/danil/PycharmProjects/Koplka/geckodriver")
    op = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(executable_path="/home/danil/PycharmProjects/Koplka/geckodriver")
    driver.get('https://kopilkaclub.ru/register/card')
    last_name_btn = driver.find_element_by_xpath("//input[@name='inp[ln]']")
    last_name_btn.send_keys(famaly_name)
    name_btn = driver.find_element_by_xpath("//input[@name='inp[fn]']")
    name_btn.send_keys(name)
    otces_btn = driver.find_element_by_xpath("//input[@name='inp[mn]']")
    otces_btn.send_keys(otc)
    data_btn = driver.find_element_by_xpath("//input[@name='inp[dob]']")
    dates = '0601' + str(random.randint(1987, 2004))
    data_btn.send_keys(dates)
    if(rep == 0):
        number, id = buy_number()
    for_text = number # Дальше буду использовать этот вариант для поиска ошибок
    print(number + ' ' + id)
    number = number[2:]
    print(number + ' ' + id)
    phone_btn = driver.find_element_by_xpath("//input[@name='inp[phone]']")
    phone_btn.send_keys(number)
    # email_btn = driver.find_element_by_xpath("//input[@name='inp[email]']")
    # email_btn.send_keys('homefg@mail.ru')
    card_btn = driver.find_element_by_xpath("//input[@name='inp[card]']")
    if(card == 0):
        card_btn.send_keys(get_card())
    else:
        card_btn.send_keys(card)
    #     2282696 2282700 2282701 2282702 2282703 2282705 2282707
    secret_btn = driver.find_element_by_xpath("//input[@name='inp[secret]']")
    secret_btn.send_keys(key)
    iwant_sms_btn = driver.find_element_by_xpath("//input[@id='inp[iwant_sms]']")
    iwant_sms_btn.click()
    iwant_email_btn = driver.find_element_by_xpath("//input[@id='inp[iwant_email]']")
    iwant_email_btn.click()
    next_btn = driver.find_element_by_xpath("//input[@class='btn btn-success btn-lg next-step']");
    next_btn.click()
    area, city = get_area()
    oblast_btn = driver.find_element_by_xpath("//span[@id='select2-inpregion-container']")
    oblast_btn.click()
    oblast_btn = driver.find_element_by_xpath("//input[@class='select2-search__field']")
    oblast_btn.send_keys(area)

    gorod_btn = driver.find_element_by_xpath("//span[@id='select2-inpcity-container']")
    gorod_btn.click()
    gorod_btn = driver.find_element_by_xpath("//input[@class='select2-search__field']")
    gorod_btn.send_keys(city)
    time.sleep(3)
    gorod_btn.send_keys(city + '\n')

    uliza_btn = driver.find_element_by_xpath("//span[@id='select2-inpstreet-container']")
    uliza_btn.click()
    try:
        uliza_btn = driver.find_element_by_xpath("//input[@class='select2-search__field']")
        alf = 'абвгдежзиклмнопрстуфхцчшщэюя'
        bukv = alf[random.randint(0, len(alf)-1)]
        uliza_btn.send_keys(bukv)
        time.sleep(4)
        uliza_btn.send_keys(bukv + '\n')
    except:
        reg(rep=1, number=number, id=id)

    dom_btn = driver.find_element_by_xpath("//input[@id='inp[house]']")
    dom_btn.send_keys(str(random.randint(1, 99)))

    time.sleep(3)
    try:
        push_next(driver) #Кнопка далее(вторая)
    except:
        time(4)
        push_next(driver)
    try:
        mistake = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[1]/div/form/div[4]/p') #текс что нужно вести код подтверждения
        #/html/body/div[3]/div/div/div[1]/div/form/div[4]/p[3]

        print('Ошибка регистрации')
        #reg(rep=0, number=number, id=id)
    except:
        print('')
    try:
        bad_card = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[1]/div/form/div[4]/p/span') # Ошибка если карта уже используется
        if(bad_card.text == 'номер карты :'):
            driver.quit()
            reg(rep=1,number=for_text, id=id,card=0)
        else:
            print('Номер карты уникальный')
    except:
        print('Номер карты уникальный')
    try:
        bad_phone = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[1]/div/form/div[4]/p/span') # Ошибка если номер уже используется
        if (bad_phone.text == 'телефон : '):
            driver.quit()
            reg(rep=0, card=card)
    except:
        print('Номер телефона уникальный')
    try:
        next_btn = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[1]/div/form/div[5]/div/input')
    except:
        reg(rep=1, number=for_text, id=id)
    cod, passwor = get_sms(id, mod=0)
    finil = driver.find_element_by_xpath("//*[@id='confirmCode']")
    finil.send_keys(cod)
    next_btn.click()
    cod, passwor = get_sms(id, mod=1)
    save_acc(number, passwor)
    driver.quit()
    reg()
    # try:
    #     succses = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[1]/div/form/div[3]/div/p[1]')

class Kopilka_aut:
    def __init__(self):
        self.driver = webdriver.Firefox(executable_path="/home/danil/PycharmProjects/Koplka/geckodriver")
    def __del__(self):
        self.driver.quit()

    def enter_btn(self):
        element = self.driver.find_element_by_link_text("Войти")
        element.click()

    def get_data(self, number):
        file1 = open("sample.txt", "r")
        count = 0
        password = 'null'
        login = 'null'
        while True:
            if (count == number):
                count = count + 1
                line = file1.readline()
                if not line:
                    break
                password = line[line.find(":") + 1:]
                login = line.partition(':')[0]
                print(line.strip())
                continue
            # считываем строку
            buff = file1.readline()
            # прерываем цикл, если строка пустая
            count = count + 1
            if not buff:
                break
            # выводим строку

        # закрываем файл
        file1.close
        return login, password
    def login_btn(self, login):
        element = self.driver.find_element_by_xpath("//input[@name='card_no']");
        element.send_keys(login)
    def passw_btn(self, password):
        element = self.driver.find_element_by_xpath("//input[@name='pin']");
        element.send_keys(password)
    def next_btn(self):
        button = self.driver.find_element_by_xpath("//button[@class='btn btn-success']");
        button.click()
    def get_balance(self, number):
        try:
            balance = self.driver.find_element_by_xpath("//span[@class='lk-card-balance']")
            print(balance.text)
        except:
            print(str(number) + " Ошибка!")

    def aut(self):
        for number in range(28):
            self.driver.get('https://kopilkaclub.ru/')
            self.enter_btn()
            login, password = self.get_data(number=number)
            pageSource = self.driver.page_source
            self.login_btn(login)
            self.passw_btn(password)
            self.next_btn()
            time.sleep(12)
            self.get_balance(number=number)
            self.driver.delete_all_cookies()

print('If you want to cheak accaunts, push 1\nIf you want to reg accaunt, push 0 ')
mod = int(input())
if(mod == 1):
    start = Kopilka_aut()
    start.aut()
if(mod == 0):
    reg()

