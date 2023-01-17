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

def CLEANUP_DATE_STRING(row_Date):
    row_Clean_Date = row_Date.split('-')
    result_Clean_Date = ""
    day_List = ['(월)','(화)','(수)','(목)','(금)','(토)','(일)']

    if len(row_Clean_Date) > 3: #년도가 바뀔 경우
        row_Clean_Text = row_Clean_Date[0] + '-' + row_Clean_Date[1] + '-' + row_Clean_Date[2]
        row_Clean_Datetime = datetime.strptime(row_Clean_Text, '%Y-%m-%d')
        row_Clean_Text = row_Clean_Datetime.strftime('%Y-%m-%d')
        row_Clean_Day = row_Clean_Datetime.weekday()
        row_Clean_Text += day_List[row_Clean_Day]
        result_Clean_Date = row_Clean_Text

    else: #년도가 바뀌지 않을 경우
        row_Clean_Text = row_Clean_Date[0] + '-' + row_Clean_Date[1] 
        row_Clean_Datetime = datetime.strptime(row_Clean_Text, '%m-%d')
        row_Clean_Text = row_Clean_Datetime.strftime('%m-%d')
        row_Clean_Day = row_Clean_Datetime.weekday()
        row_Clean_Text += day_List[row_Clean_Day]
        result_Clean_Date = row_Clean_Text

    return result_Clean_Date


def MAKE_DATE_STRING(row_Text):
    row_Text = row_Text.replace(".", "-")
    row_Text = row_Text.replace(" ", "")
    row_Text = row_Text.replace("∙", "")
    row_List = row_Text.split("~")

    result_Date_String = ""
    if len(row_List) > 1: #날짜가 2개일 경우
        row_First = CLEANUP_DATE_STRING(row_List[0])
        row_Second = CLEANUP_DATE_STRING(row_List[1])
        result_Date_String = row_First + "~" + row_Second

    else: #날짜가 1개일 경우
        row_First = CLEANUP_DATE_STRING(row_List[0])
        result_Date_String = row_First

    return result_Date_String

#######################################################

url = 'https://www.donga.ac.kr/WebApp/BOARD/BASIC/Read.asp?BIDX=19&CAT=&PG=1&ORD=&KEY=&NUM=7291200&KWD='

try:
    response = requests.get(url, timeout=15)
    response.encoding = None
except requests.exceptions.Timeout:
    print("Timeout Error")    
else:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser', from_encoding = 'utf-8')
    
    cal_Tables = soup.find('table', attrs={'border':'1', 'cellspacing':'1', 'cellpadding':'3', 'width':'99%'})
    cal_Table = cal_Tables.find_all('table')
    
    semester_List = []
    date_List = []
    work_List = []

    for row_Idx in range(len(cal_Table)):
        if row_Idx % 2 == 0:
            cal_Date_Row = cal_Table[row_Idx].find_all('td')
            for row in cal_Date_Row:
                date_List.append(MAKE_DATE_STRING(row.text))
                if row_Idx is 0:
                    semester_List.append(1)
                else:
                    semester_List.append(2)

        else:
            cal_Work_Row = cal_Table[row_Idx].find_all('td')
            for row in cal_Work_Row:
                work_List.append(row.text.strip())



    for list_Idx in range(len(date_List)):
        print(semester_List[list_Idx])
        print(" ")
        print(date_List[list_Idx])
        print(" ")
        print(work_List[list_Idx])
        print("<br>")