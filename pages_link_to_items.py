import csv, requests
from bs4 import BeautifulSoup
from random import choice

urls = 'https://parsinger.ru/html/index1_page_1.html'
headers = ['Наименование', 'Артикул', 'Бренд', 'Модель', 'Тип', 'Технология экрана', 'Материал корпуса', 'Материал браслета', 'Размер', 'Сайт производителя', 'Наличие', 'Цена', 'Старая цена', 'Ссылка на карточку с товаром']
with open('res.csv', 'w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(headers)

response = requests.get(url)
response.encoding = 'utf-8'
html = response.text

soup = BeautifulSoup(html, 'lxml')
schema = 'https://parsinger.ru/html/index1_page_'
pagen = [f'{schema}{link.text}.html' for link in soup.find('div', class_='pagen').find_all('a')]

pages_list = []

for url in pagen:
    names = []
    response = requests.get(url)
    response.encoding = 'utf-8'
    html = response.text
    soup = BeautifulSoup(html, 'lxml')

    tags = soup.findAll('a', class_="name_item")
    #print(soup.text)
    for tag in tags:

        names.append(tag['href'])

    pages_list.extend(names)

print(pages_list)

with open('res.csv', 'a', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    for page in pages_list:
        url = f'https://parsinger.ru/html/{page}'
        print(url)
        response = requests.get(url)
        response.encoding = 'utf-8'
        html = response.text
        soup = BeautifulSoup(html, 'lxml')


        name = soup.find('p', id='p_header').text
        article = int(soup.find('p', class_='article').text.replace('Артикул: ', ''))
        description = soup.find('ul', id='description').find_all('li')
        in_stock = int(soup.find('span', id='in_stock').text.replace('В наличии: ', ''))
        price = soup.find('span', id='price').text
        old_price = soup.find('span', id='old_price').text

        flatten = name, article, *[x.text.split(':')[1].strip() for x in description], in_stock, price, old_price, url
        writer.writerow(flatten)
        print('Файл res.csv создан')