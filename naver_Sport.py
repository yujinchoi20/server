import requests
from bs4 import BeautifulSoup

url = "https://sports.news.naver.com/volleyball/record/index?category=kovo&year=2022" #남자부
#url = "https://sports.news.naver.com/volleyball/record/index?category=wkovo&year=2022" #여자부

try:
    response = requests.get(url, timeout=15)
    response.encoding = None
except requests.exceptions.Timeout:
    print("Timeout Error")
else:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    
    Record_Table = soup.find('table', attrs={"cellspacing":"0", "cellpadding":"0"})
    Record_Title = Record_Table.find('thead')
    title = Record_Title.find_all('strong')
    
    for idx in range(1, len(title)):
        print(title[idx].text, end=' ')
    
    print()    
    print("-----------------------------------------------------------------------------------------------------")
    
    Record_Body = Record_Table.find('tbody')
    score = Record_Body.find_all('tr') #len = 7
    
    for tr in range(len(score)):
        team = score[tr].find_all('td')
        
        for td in range(len(team)):            
            if td == 0:
                team_Record = team[td].find_all('span')
                print(team_Record[1].text.strip(), end=' ')
            elif td == 2:
                team_Record = team[td].find('strong')
                print(team_Record.text.strip(), end=' ')
            else:
                team_Record = team[td].find('span')
                print(team_Record.text.strip(), end=' ')
        
        print()
        