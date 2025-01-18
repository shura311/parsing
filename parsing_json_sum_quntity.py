import requests

url = 'https://parsinger.ru/downloads/get_json/res.json'
r = dict()

response = requests.get(url=url).json()
for item in response:
    if item['categories'] in r:
        r[item['categories']] = r[item['categories']] + int(item['count'])
    else:
        r[item['categories']] = int(item['count'])
print(r)