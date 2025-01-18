import random

from bs4 import BeautifulSoup
import requests
from random import choice

url = 'https://parsinger.ru/html/index3_page_1.html'

with open('user_agent.txt') as file:
    lines = file.read().split('\n')
#for line in lines:
user_agent = {'user-agent': choice(lines)}

response = requests.get(url, user_agent)
response.encoding = 'utf-8'
html = response.text

soup = BeautifulSoup(html, 'lxml')
schema = 'https://parsinger.ru/html/index3_page_'
pagen = [link.text for link in soup.find('div', class_='pagen').find_all('a')]

pages_list = []

for page in pagen:
    url = f'{schema}{page}.html'
    #print(url )
    response = requests.get(url, user_agent)
    response.encoding = 'utf-8'
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    names = []
    tags = soup.findAll('a', class_="name_item")
    #print(soup.text)
    for tag in tags:

        names.append(tag.text)
    pages_list.append(names)

print(pages_list)