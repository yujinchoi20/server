#!/usr/bin/python3
# -*- coding: utf-8 -*-
print("Content-type:application/json;charset=utf-8\r\n")

import sys
import io
import datetime
import json
import cgitb
import cgi
import codecs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

#encoding
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

form = cgi.FieldStorage()
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
cgitb.enable()
###############################################################################################

userid = None
passwd = None
ddl_place = None
ddlYear1 = None
ddlMonth1 = None
ddlDay1 = None
ddlYear2 = None
ddlMonth2 = None
ddlDay2 = None
json_Result = dict()

login_Url = 'https://sso.donga.ac.kr/svc/tk/Auth.eps?id=student&ac=Y&ifa=N&RelayState=%2f&'
overnight_Form_Url = 'http://student.donga.ac.kr/SudExam/SUD/XSUN0040.aspx'

now = datetime.datetime.now()
hour = now.hour
minute = now.minute

###############################################################################################

if hour >= 23 and minute >= 30: 
    json_Result['error'] = "-6"

else: 
    try:
        # form으로 데이터 받아오기
        userid = None
        passwd = None
        ddl_place = None
        ddlYear1 = None
        ddlMonth1 = None
        ddlDay1 = None
        ddlYear2 = None
        ddlMonth2 = None
        ddlDay2 = None
    
    except Exception as e:
        json_Result['error'] = "-2" 
    
    else:
        #selenium version 4.8.0
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True) 
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging']) 
        driver = webdriver.Chrome(service=Service('./chromedriver.exe'), options=chrome_options) 
        driver.get(login_Url)
        driver.implicitly_wait(3)

        #login
        driver.find_element(By.ID, 'display_user_id').send_keys(userid)
        driver.find_element(By.ID, 'display_user_password').send_keys(passwd)
        driver.find_element(By.CLASS_NAME, 'btn_login').click() #login btn
        driver.get(overnight_Form_Url)
        
        try:
            alert = driver.switch_to.alert
            if "대상자가 아닙니다" in alert.text:
                json_Result['error'] = "-1"
            alert.accept()
        except Exception as e:
            pass
            #place
            ddl_Place = Select(driver.find_element(By.XPATH, '//*[@id="ddl_place"]'))
            ddl_Place.select_by_visible_text(str(ddl_place)) #select_by_value -> select_by_visible_text 
            # select_by_value('01') 

            #date
            ddl_Year1 = Select(driver.find_element(By.XPATH, '//*[@id="ddlYear1"]'))
            ddl_Month1 = Select(driver.find_element(By.XPATH, '//*[@id="ddlMonth1"]'))
            ddl_Day1 = Select(driver.find_element(By.XPATH, '//*[@id="ddlDay1"]'))
            ddl_Year2 = Select(driver.find_element(By.XPATH, '//*[@id="ddlYear2"]'))
            ddl_Month2 = Select(driver.find_element(By.XPATH, '//*[@id="ddlMonth2"]'))
            ddl_Day2 = Select(driver.find_element(By.XPATH, '//*[@id="ddlDay2"]'))
            ddl_Year1.select_by_value(str(ddlYear1))
            ddl_Month1.select_by_value(str(ddlMonth1))
            ddl_Day1.select_by_value(str(ddlDay1))
            ddl_Year2.select_by_value(str(ddlYear2))
            ddl_Month2.select_by_value(str(ddlMonth2))
            ddl_Day2.select_by_value(str(ddlDay2))

            #submit
            driver.find_element(By.NAME, 'ImageButton1').click()

            try:
                alert = driver.switch_to.alert
                if "중복" in alert.text:
                    json_Result['error'] = "-3"
                elif "대상자" in alert.text:
                    json_Result['error'] = "-1"  
                else:
                    json_Result['error'] = alert.text
                alert.accept()
            except Exception as e:
                html = driver.page_source
                if "정상적으로 완료되었습니다" in html:
                    json_Result['error'] = "1" 
                elif "작을수 없습니다":
                    json_Result['error'] = "-4"
                else:
                    json_Result['error'] = "-5"
        
        ###############################################################################################
            
        driver.quit()
json_Result = json.dumps({'overnight_info_result' : json_Result}, indent=4, ensure_ascii=False)
print(json_Result)