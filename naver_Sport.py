import requests
from bs4 import BeautifulSoup

url = "https://sports.news.naver.com/volleyball/record/index?category=kovo&year=2022" 
#url = "https://sports.news.naver.com/volleyball/record/index?category=wkovo&year=2022" 

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
    
    record = []
    record.append([])
    
    for idx in range(1, len(title)):
        record[0].append(title[idx].text)   

    Record_Body = Record_Table.find('tbody')
    score = Record_Body.find_all('tr')
    
    for tr in range(len(score)):
        team = score[tr].find_all('td')
        
        record.append([])
        for td in range(len(team)):            
            if td == 0:
                team_Record = team[td].find_all('span')
                str = team_Record[1].text.strip()
                record[tr+1].append(str)
            elif td == 2:
                team_Record = team[td].find('strong')
                str = team_Record.text.strip()
                record[tr+1].append(str)
            else:
                team_Record = team[td].find('span')
                str = team_Record.text.strip()
                record[tr+1].append(str)
    
    for tr in range(len(record)):
        for td in range(len(record[0])):
            print(record[tr][td], end=' ')
        print()