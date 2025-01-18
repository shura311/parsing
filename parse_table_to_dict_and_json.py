from bs4 import BeautifulSoup
import requests, json

url = 'https://parsinger.ru/4.8/6/index.html'


response = requests.get(url)
response.encoding = 'utf-8'
html = response.text

soup = BeautifulSoup(html, 'html.parser')

headings = ['Марка Авто', 'Год выпуска', 'Тип двигателя', 'Стоимость авто']

# tags = soup.find(attrs={"colspan": True})
table = soup.find('tbody')
list_of_cars_dict = []

for tag in table.find_all('tr'):
    car = tag.find_all('td')
    make = car[0].text
    year = int(car[1].text)
    engine = car[4].text
    price = int(car[7].text)
    list_of_cars_dict.append({headings[0] : make, headings[1] : year, headings[2] : engine, headings[3] : price})

filtered = list(filter(lambda x: x['Стоимость авто'] <= 4000000, list_of_cars_dict))
filtered = list(filter(lambda x: x['Год выпуска'] >= 2005, filtered))
filtered = list(filter(lambda x: x['Тип двигателя'] == 'Бензиновый', filtered))

sorted_list = sorted(filtered, key=lambda x: x["Стоимость авто"])

print(json.dumps(sorted_list, indent=4, ensure_ascii=False))



