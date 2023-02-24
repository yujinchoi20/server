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
import selenium
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

#�ܹڽ�û �Ⱓ�� �ƴҰ�� False, �ܹڽ�û �Ⱓ�� �´� ��� True ��ȯ
def check_Exists_By_XPATH(xpath):
    try:
        driver.find_element(xpath)
    except Exception as e: 
        return False
    return True

###############################################################################################

if hour >= 23 and minute >= 30: 
    json_Result['error'] = "-6"

else: 
    try:
        # form���� ������ �޾ƿ���
        # userid = form['userid'].value
        # passwd = form['passwd'].value
        # ddl_place = form['ddl_place'].value
        # ddlYear1 = form['ddlYear1'].value
        # ddlMonth1 = form['ddlMonth1'].value
        # ddlDay1 = form['ddlDay1'].value
        # ddlYear2 = form['ddlYear2'].value
        # ddlMonth2 = form['ddlMonth2'].value
        # ddlDay2 = form['ddlDay2'].value
        userid = None
        passwd = None
        ddl_place = '���Ƹ���'
        ddlYear1 = '2023'
        ddlMonth1 = '2'
        ddlDay1 = '22'
        ddlYear2 = '2023'
        ddlMonth2 = '2'
        ddlDay2 = '23'
    
    except Exception as e:
        json_Result['error'] = "-2" # ������ ����� �ȿ�
    
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

        #login
        driver.find_element(By.ID, 'display_user_id').send_keys(userid)
        driver.find_element(By.ID, 'display_user_password').send_keys(passwd)
        driver.find_element(By.CLASS_NAME, 'btn_login').click() #login btn
        driver.get(overnight_Form_Url)
        
        try:
            alert = driver.switch_to.alert() 
            # ����(02.24) �� ������ �ܹڽ�û �Ⱓ�� �ƴ϶� ��������� �ƴ��� �˷��ִ� alertâ�� �� �ߴ� �� �� ��������.
            # ����ڰ� �ƴϸ� alert â�� �ߴµ�, ���� ����ڰ� ������ alert â�� �� ��!
            # �׷��� ����� ���̵�� �α����ϸ� �� �κп��� ���� �߻� 
            if "����ڰ� �ƴմϴ�" in alert.text:
                json_Result['error'] = "-1"
            alert.accept()
            
        except Exception as e:
            pass
            #place
            # ���⼭ ������ �Ÿ� �ܹڽ�û �Ⱓ�� �ƴ϶�� �ǹ� 
            # -7 -> �ܹڽ�û �Ⱓ�� �ƴ� 
            # xpath�� ���� ���θ� check_Exists_By_XPATH() �޼ҵ带 ���� Ȯ�� -> False/True�� ��ȯ
            
            ddl_Chk = check_Exists_By_XPATH('//*[@id="ddl_place"]')
            # print(ddl_Chk)
            
            if ddl_Chk:      
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
                    if "�ߺ�" in alert.text:
                        json_Result['error'] = "-3"
                    elif "�����" in alert.text:
                        json_Result['error'] = "-1"  
                    else:
                        json_Result['error'] = alert.text
                    alert.accept()
                except Exception as e:
                    html = driver.page_source
                    if "���������� �Ϸ�Ǿ����ϴ�" in html:
                        json_Result['error'] = "1" 
                    elif "������ �����ϴ�":
                        json_Result['error'] = "-4"
                    else:
                        json_Result['error'] = "-5"
            else:
                json_Result['error'] = "-7"
        ###############################################################################################
            
        driver.quit()
json_Result = json.dumps({'overnight_info_result' : json_Result}, indent=4, ensure_ascii=False)
print(json_Result)