import sys
import io
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

#encoding
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')
###############################################################################################

login_Url = 'https://sso.donga.ac.kr/svc/tk/Auth.eps?id=student&ac=Y&ifa=N&RelayState=%2f&'
overnight_Form_Url = 'http://student.donga.ac.kr/SudExam/SUD/XSUN0040.aspx'

userid = None
passwd = None
ddl_place = '동아리방'
ddlYear1 = 2023
ddlMonth1 = 2
ddlDay1 = 9
ddlYear2 = 2023
ddlMonth2 = 2
ddlDay2 = 10

###############################################################################################

#selenium version 4.8.0
chrome_options = Options()
chrome_options.add_experimental_option("detach", True) #브라우저 꺼짐 방지
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging']) #불필요한 에러 메시지 없애기 
driver = webdriver.Chrome(service=Service('./chromedriver.exe'), options=chrome_options) #브라우저 연결
driver.get(login_Url)
driver.implicitly_wait(3)

#login
driver.find_element(By.ID, 'display_user_id').send_keys(userid)
driver.find_element(By.ID, 'display_user_password').send_keys(passwd)
driver.find_element(By.CLASS_NAME, 'btn_login').click() #login btn
driver.get(overnight_Form_Url)

###############################################################################################

#place
ddl_Place = Select(driver.find_element(By.XPATH, '//*[@id="ddl_place"]'))
ddl_Place.select_by_visible_text(str(ddl_place)) #select_by_value -> select_by_visible_text 수정
# select_by_value('01') 이런 형식으로 사용해야됨. html 코드를 보면 알 수 있음. 

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

###############################################################################################

