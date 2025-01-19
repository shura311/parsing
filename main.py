import requests

url = 'https://parsinger.ru/4.6/1/res.json'
r = dict()

response = requests.get(url=url).json()
for item in response:
    if item['categories'] in r:
        r[item['categories']] = r[item['categories']] + int(item['article']) * int(item['description']['rating'])
    else:
        r[item['categories']] = int(item['article']) * int(item['description']['rating'])
print(f'Результат: {r}')
