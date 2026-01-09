import requests
from bs4 import BeautifulSoup
BASE = "https://cricsheet.org"
URL="https://cricsheet.org/matches/"
response=requests.get(URL)
data=response.text
soup=BeautifulSoup(data,'html.parser')
dt=soup.find_all('dt')
for t in dt:
    if 'Indian Premier League' in t:
        dd=t.find_next_sibling("dd")
        link=dd.find('a')
        downloadURL=BASE+link['href']
        print(downloadURL)        
        response = requests.get(downloadURL)

        with open("ipl_json.zip", "wb") as f:
            f.write(response.content)

        print("Download completed")