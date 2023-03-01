# #!/usr/bin/python3
# # -*- coding: utf-8 -*-
# print("Content-type:application/json;charset=utf-8\r\n")

import sys
import io
import datetime
import json
import cgitb
import cgi
import codecs
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

# login_Url = 'https://sso.donga.ac.kr/svc/tk/Auth.eps?id=student&ac=Y&ifa=N&RelayState=%2f&' #통합 로그인
login_Url = 'https://hanlim.donga.ac.kr/subLogin/hanlim/view.do' #한림생활관 로그인
overnight_Form_Url = 'http://student.donga.ac.kr/SudExam/SUD/XSUN0040.aspx' #외박신청

now = datetime.datetime.now()
hour = now.hour
minute = now.minute

#외박신청 기간이 아닐경우 False, 외박신청 기간이 맞는 경우 True 반환
def check_Exists_By_XPATH_1(xpath):
    try:
        Select(driver.find_element(By.XPATH, xpath))
    except Exception as e: 
        return False
    return True

###############################################################################################

if hour >= 23 and minute >= 30: 
    json_Result['error'] = "-6"

else: 
    try:
        # form으로 데이터 받아오기
        # userid = form['userid'].value
        # passwd = form['passwd'].value
        # ddl_place = form['ddl_place'].value
        # ddlYear1 = form['ddlYear1'].value
        # ddlMonth1 = form['ddlMonth1'].value
        # ddlDay1 = form['ddlDay1'].value
        # ddlYear2 = form['ddlYear2'].value
        # ddlMonth2 = form['ddlMonth2'].value
        # ddlDay2 = form['ddlDay2'].value
        userid = '2024354'
        passwd = 'tusocl0710*^^*'
        ddl_place = '동아리방'
        ddlYear1 = '2023'
        ddlMonth1 = '2'
        ddlDay1 = '27'
        ddlYear2 = '2023'
        ddlMonth2 = '3'
        ddlDay2 = '1'
    
    except Exception as e:
        json_Result['error'] = "-2" # 데이터 제대로 안옴
    
    else:
        #selenium version 4.8.0
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True) 
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging']) 
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=Service('./chromedriver.exe'), options=chrome_options) 
        driver.get(login_Url)
        driver.implicitly_wait(3)

        #login (통합로그인 -> 한림생활관, 로그인 창 변경) 
        driver.find_element(By.ID, 'userId').send_keys(userid)
        driver.find_element(By.ID, 'userPwd').send_keys(passwd)
        driver.find_element(By.CLASS_NAME, '_loginSubmit').click() #login btn
        driver.get(overnight_Form_Url)
        driver.implicitly_wait(3)
            
        # 이름 자체가 공백이여도 대상자가 아니라는 의미 
        if(driver.find_element(By.XPATH, '/html/head/script')):
            json_Result['error'] = "-1"
        
        else:
            #place
            # 여기서 막히는 거면 외박신청 기간이 아니라는 의미 
            # -7 -> 외박신청 기간이 아님 
            # xpath의 존재 여부를 check_Exists_By_XPATH() 메소드를 통해 확인 -> False/True를 반환
            
            ddl_Chk = check_Exists_By_XPATH_1('//*[@id="ddl_place"]')
            # print(ddl_Chk)
            
            if ddl_Chk:      
                ddl_Place = Select(driver.find_element(By.XPATH, '//*[@id="ddl_place"]'))
                ddl_Place.select_by_visible_text(str(ddl_place)) #select_by_value -> select_by_visible_text 

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
            else:
                json_Result['error'] = "-7"
        ###############################################################################################
            
        driver.quit()
json_Result = json.dumps({'overnight_info_result' : json_Result}, indent=4, ensure_ascii=False)
print(json_Result)