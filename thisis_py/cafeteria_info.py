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

cur = db.cursor()

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
	cafe_Rows_Sh = cafe_Table_Sh.find_all('tr')
	#cafe_Rows_Sh[1], [2], [3]

	setmenu = list()
	onemenu = list()
	snackmenu = list()

	for row_Idx in range(1, len(cafe_Rows_Sh)): #정식, 일품, 양분식
		cafe_Cols_Sh = cafe_Rows_Sh[row_Idx].find_all('td')

		for col_Idx in range(1, len(cafe_Cols_Sh)): #교수회관, 학생회관, 도서관
			if col_Idx is 3: #공과대학 pass
				continue

			if row_Idx is 1:
				setmenu.append(cafe_Cols_Sh[col_Idx].text)
			elif row_Idx is 2:
				onemenu.append(cafe_Cols_Sh[col_Idx].text)
			elif row_Idx is 3:
				snackmenu.append(cafe_Cols_Sh[col_Idx].text)

	for idx in range(len(setmenu)):
		if idx is 0:
			print(setmenu[idx] + ", " + onemenu[idx] + ", " + snackmenu[idx] + "<br>")
		elif idx is 1:
			print(setmenu[idx] + ", " + onemenu[idx] + ", " + snackmenu[idx] + "<br>")
		elif idx is 2:
			print(setmenu[idx] + ", " + onemenu[idx] + ", " + snackmenu[idx] + "<br>")
			
	#######################################################

	for idx in range(len(setmenu)):
		if idx is 0: #교수회관
			sql = f"INSERT INTO cafe_professor_CYJ(setmenu, onemenu, snackmenu, date) VALUES('{setmenu[idx]}', '{onemenu[idx]}', '{snackmenu[idx]}', '20221207')"
			cur.execute(sql)
			db.commit()
		elif idx is 1:
			sql = f"INSERT INTO cafe_student_CYJ(setmenu, onemenu, snackmenu, date) VALUES('{setmenu[idx]}', '{onemenu[idx]}', '{snackmenu[idx]}', '20221207')"
			cur.execute(sql)
			db.commit()
		elif idx is 2:
			sql = f"INSERT INTO cafe_library_CYJ(setmenu, onemenu, snackmenu, date) VALUES('{setmenu[idx]}', '{onemenu[idx]}', '{snackmenu[idx]}', '20221207')"
			cur.execute(sql)
			db.commit()
	#######################################################

db.close()