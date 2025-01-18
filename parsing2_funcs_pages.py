import csv, requests, json
from bs4 import BeautifulSoup
from random import choice

from parse_to_list_of_dicts_filter_sort import price

urls = [f'https://parsinger.ru/html/index{x}_page_1.html' for x in range(1, 6)]

# Список страниц с разделами, можно взять тот, что сверху. В данном случае один раздел
# urls = ['https://parsinger.ru/html/index4_page_1.html', ]

def get_pagen(url):
    '''Передаем url страницы с карточками получаем список url всех pages'''
    response = requests.get(url)
    response.encoding = 'utf-8'
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    schema = url.replace('1.html', '')
    pagen = [f'{schema}{link.text}.html' for link in soup.find('div', class_='pagen').find_all('a')]
    return pagen

def get_pages_from_url(url):
    '''Передаем url страницы c карточками получаем спимок ссылок на карточки'''
    shema = f'{url.split('html')[0]}html/'
    response = requests.get(url)
    response.encoding = 'utf-8'
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    names = []
    tags = soup.findAll('a', class_="name_item")
    # print(soup.text)
    for tag in tags:
        names.append(f'{shema}{tag['href']}')
    return names

def get_info_from_card(url):
    '''Работает со ссылкой на карточку. Возвращает словарь с данными'''

    headers = ['Наименование', 'Бренд', 'Форм-фактор', 'Ёмкость', 'Объем буферной памяти', 'Цена']
    response = requests.get(url)
    response.encoding = 'utf-8'
    html = response.text
    soup = BeautifulSoup(html, 'lxml')

    name = soup.find('p', id='p_header').text.strip()
    description = soup.find('ul', id='description').find_all('li')
    price = soup.find('span', id='price').text.strip()
    descr = [x.text.split(':')[1].strip() for x in description]

    flatten = name, descr[0], descr[2], descr[3], descr[4] , price

    return dict(zip(headers, flatten))

def get_info_from_page(url):
    '''Собирает информацию о товаре со страницы с карточками. Возвращает список словарей'''
    result_list = []
    headers = ['Наименование', 'Бренд', 'Форм-фактор', 'Ёмкость', 'Объем буферной памяти', 'Цена']
    response = requests.get(url)
    response.encoding = 'utf-8'
    html = response.text
    soup = BeautifulSoup(html, 'lxml')

    for item in soup.find_all('div', class_="item"):
        name = item.find('a', class_='name_item').text.strip()
        description = item.find('div', class_='description').find_all('li')
        price = item.find('p', class_='price').text.strip()
        desc_dict = {x.text.split(':')[0].strip() : x.text.split(':')[1].strip()  for x in description}
        # flatten = name, *[x.text.split(':')[1].strip() for x in description], price
        # headers[1:4] = [x.text.split(':')[0].strip() for x in description]
        result = {headers[0] : name}
        result.update(desc_dict)
        result[headers[5]] = price
        result_list.append(result)

    return result_list

pages = []
for url in urls:
    #собрали пагинацию
    pages.extend(get_pagen(url))

print(pages)

result = []
for page in pages:
    result.extend(get_info_from_page(page))

with open('res.json', 'w', encoding='utf-8-sig', newline='') as file:
#
    json.dump(result, file, indent=4, ensure_ascii=False)


print('Файл res.json создан')