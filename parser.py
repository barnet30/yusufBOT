import requests
from bs4 import BeautifulSoup as BS

r = requests.get('https://www.banki.ru/products/currency/usd/')

html = BS(r.content, 'html.parser')

rate = html.select('div.currency-table__large-text')
print(rate[1].text)

