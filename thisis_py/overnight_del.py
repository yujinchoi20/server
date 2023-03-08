#!/usr/bin/python3
# -*- coding: utf-8 -*-
# print("Content-type:application/json;charset=utf-8\r\n")

import cgitb
import cgi
import codecs
import sys
import datetime
import json
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

form = cgi.FieldStorage()
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
cgitb.enable()

userid = None
passwd = None
year = None
month = None
day = None
tr_Init = 3
td_Init = None
json_Result = dict()

login_Url = 'https://sso.donga.ac.kr/svc/tk/Auth.eps?id=student&ac=Y&ifa=N&RelayState=%2f&'
calendar_Url = f"https://student.donga.ac.kr/SudExam/SUD/XSUN0120.aspx"

year_Now = datetime.datetime.today().year
month_Now = datetime.datetime.today().month
date = datetime.date(year_Now, month_Now, 1).weekday()
# 0123456 -> 월화수목금토일

if date == 6: #일
    td_Init = 1
elif date == 0:
    td_Init = 2
elif date == 1:
    td_Init = 3
elif date == 2:
    td_Init = 4
elif date == 3:
    td_Init = 5
elif date == 4:
    td_Init = 6
elif date == 5:
    td_Init  =7

# print(tr_Init, " " , td_Init)
###############################################################################################

try:
    userid = form['userid'].value
    passwd = form['passwd'].value
    year = form['year'].value
    month = form['month'].value
    day = form['day'].value

except Exception as e:
    json_Result['error'] = "-2"

else:
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option(
        'excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(
        './chromedriver.exe'), options=chrome_options)
    driver.implicitly_wait(3)
    driver.get(login_Url)

    driver.find_element(By.ID, 'display_user_id').send_keys(userid)
    driver.find_element(By.ID, 'display_user_password').send_keys(passwd)
    driver.find_element(By.CLASS_NAME, 'btn_login').click()  # login btn

    try:
        alert = driver.switch_to.alert
        if "대상자가 아닙니다." in alert.text:
            json_Result['error'] = "-1"
        alert.accept

    except Exception as e:
        driver.get(calendar_Url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        json_Result['error'] = "-1" # 기본값
        
        # day+신청중
        tr_All = soup.find_all('tr')
        for tr_Idx in range(3, len(tr_All)):
            for td_Idx in tr_All[tr_Idx]:
                if td_Idx.text == day+"신청중":
                    # print(td_Idx.text)
                    try:
                        td_Init = td_Init + int(day) - 1
                        tr_Init = tr_Init + int(td_Init / 7)
                        td_Init = td_Init % 7
                        # print(tr_3, " ", td_3)
                    except Exception as e:
                        json_Result['error'] = "-1"
                    else:
                        # tr, td 값을 날짜에 맞게 바꿔주면 됨
                        # 문제는 매월 날짜에 따른 tr, td값이 바뀐다는 것...
                        driver.find_element(
                            By.XPATH, '//*[@id="cal"]/tbody/tr[{tr}]/td[{td}]/a'.format(tr=tr_Init, td=td_Init)).click()
                        driver.find_element(
                            By.XPATH, '//*[@id="Button1"]').click()

                        alert = driver.switch_to.alert
                        alert.accept()

                        confirm = driver.switch_to.alert
                        confirm.accept()
                        json_Result['error'] = "1"
                    
###################################################################################

driver.quit()
json_Result = json.dumps(
    {'overnight_info_result': json_Result}, indent=4, ensure_ascii=False)
print(json_Result)
