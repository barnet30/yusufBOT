import requests
from bs4 import BeautifulSoup as BS

url = 'https://www.banki.ru/products/currency/usd/'

def get_dollar():
    r = requests.get(url)
    html = BS(r.content, 'html.parser')
    rate = html.select('div.currency-table__large-text')
    return rate[0].text


print(get_dollar())