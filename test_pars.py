
# shop_scraper.py
import requests
from bs4 import BeautifulSoup

url = 'https://scrapingclub.com/exercise/list_basic/?page=1'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
items = soup.find_all('div', class_='w-full rounded border')

for n, i in enumerate(items, start=1):
    itemName = i.find('h4', class_='p-4').text.strip()
    itemPrice = i.find('h5').text
    print(f'{n}:  {itemPrice} за {itemName}')