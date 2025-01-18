import csv, requests
from bs4 import BeautifulSoup
from random import choice

urls = [f'https://parsinger.ru/html/index{x}_page_1.html' for x in range(1, 6)]

pages_list = []

with open('res.csv', 'w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file, delimiter=';')

    for url in urls:
        response = requests.get(url)
        response.encoding = 'utf-8'
        html = response.text

        soup = BeautifulSoup(html, 'lxml')
        schema = url.replace('1.html', '')
        pagen = [f'{schema}{link.text}.html' for link in soup.find('div', class_='pagen').find_all('a')]


        for url in pagen:
            names = []
            response = requests.get(url)
            response.encoding = 'utf-8'
            html = response.text
            soup = BeautifulSoup(html, 'lxml')

            print(url)

            for item in soup.find_all('div', class_="item"):

                name = item.find('a', class_='name_item').text.strip()
                description = item.find('div', class_='description').find_all('li')
                price = item.find('p', class_='price').text.strip()


                flatten = name, *[x.text.split(':')[1].strip() for x in description], price
                writer.writerow(flatten)


            print('Файл res.csv создан')