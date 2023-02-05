from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome("./chromedriver.exe", options=options)

driver.get('https://www.google.co.kr/')
time.sleep(3)

#search_box = driver.find_element(By.CSS_SELECTOR, 'input.gLFyf')
search_box = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')

search_box.send_keys('Python')
search_box.send_keys(Keys.RETURN)
time.sleep(3)