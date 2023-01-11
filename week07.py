#!/usr/bin/python3
# -*- coding: utf-8 -*-
print("Content-type:text/html;charset=utf-8\r\n")

# text/html -> 일반 html
# application/json -> json 출력 시

#######################################################

import sys
import codecs
import cgi
import cgitb
import requests
import json
import re
from bs4 import BeautifulSoup
from datetime import datetime
import pymysql
sys.path.insert(0,'/var/www/html/thisis_py/db')
from db_proc import db

sys.stdout = codecs.getwriter("utf-8") (sys.stdout.detach())
cgitb.enable()

#######################################################

url = 'https://www.donga.ac.kr/gzSub_007005005.aspx?DT=20221207#mt'

try:
	response = requests.get(url, timeout = 15)
	response.encoding = None
except requests.exceptions.Timeout:
	print("ERROR")
else:
	html = response.text
	soup = BeautifulSoup(html, 'html.parser', from_encoding = 'utf-8')
 
    cafe_Table_Sh = soup.find('table', attrs={'class':'gzTable', 'width':'100%', 'cellpadding':'0', 'cellspacing':'0', 'summary':'승학캠퍼스 식단표'})
    
    