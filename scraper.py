import os
os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"

from bs4 import BeautifulSoup
from datetime import datetime
import requests
import scraperwiki

today = datetime.today()

url = 'https://www.bawbawshire.vic.gov.au/Plan-and-Build/Planning-permits/Advertised-Planning-Applications'
r = requests.get(url)
soup = BeautifulSoup(r.content, 'lxml')

table = soup.find('tbody')
rows = table.find_all('tr')

for row in rows:
    record = {}
    record['address'] = row.find_all('td')[1].text.strip().replace('\xa0', ' ')
    record['date_scraped'] = today.strftime("%Y-%m-%d")
    record['description'] = row.find_all('td')[2].text.strip()
    record['council_reference'] = row.find('a').text.split('(P')[0]
    record['info_url'] = 'https://www.bawbawshire.vic.gov.au' + str(row.find('a')).split('"')[3]
    record['on_notice_to'] = row.find_all('td')[3].text.strip()
    scraperwiki.sqlite.save(
        unique_keys=['council_reference'], data=record, table_name="data")
