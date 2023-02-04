from selenium import webdriver
from selenium.webdriver.common.by import By
import time

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome("./chromedriver.exe", options=options)

driver.get('https://www.google.co.kr/')
time.sleep(3)