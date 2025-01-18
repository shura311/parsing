import csv, requests, json
from bs4 import BeautifulSoup
from random import choice

# urls = [f'https://parsinger.ru/html/index{x}_page_1.html' for x in range(1, 6)]

# Список страниц с разделами, можно взять тот, что сверху. В данном случае один

urls = ['https://parsinger.ru/html/index2_page_1.html', ]

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
    description = soup.find('ul', id='description').find_all('li')
    desc_dict = {x['id'] : x.text.split(':')[1].strip() for x in description}
    result = dict()
    result['categories'] = 'mobile'
    result['name'] = soup.find('p', id='p_header').text.strip()
    result['article'] = soup.find('p', class_='article').text.replace('Артикул: ', '').strip()
    result['description'] = desc_dict
    result['count'] = soup.find('span', id="in_stock").text.replace('В наличии: ', '')
    result['price'] = soup.find('span', id='price').text.strip()
    result['old_price'] = soup.find('span', id='old_price').text.strip()
    result['link'] = url

    return result

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

pagen = []
for url in urls:
    #собрали пагинацию
    pagen.extend(get_pagen(url))
print(pagen)

p_list = []
for p in pagen:
    p_list.extend(get_pages_from_url(p))
print(p_list)

result = []
for page in p_list:
    result.append(get_info_from_card(page))


with open('res.json', 'w', encoding='utf-8-sig', newline='') as file:
#
    json.dump(result, file, indent=4, ensure_ascii=False)


print('Файл res.json создан')