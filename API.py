# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.
from requests import get
import json

repos = get('https://api.github.com/users/olhaexe/repos').json()
li_repos = []
for repo in repos:
    li_repos.append(repo['html_url'])
print(f'Список репозиториев для пользователя olhaexe: {li_repos}')
with open('repo.json', 'w') as f:
    f.write(json.dumps(li_repos))

# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

fmtags = get('http://ws.audioscrobbler.com/2.0/?method=track.addTags&api_key=c091708d2b2aaaf2cbcb87978a637124')
with open('response.pkl', 'w') as fm:
    fm.write(str(fmtags))

# 3. Ресурс к парсингу : https://5ka.ru/
# Задача:
# Необходимо собрать все данные с раздела товаров по акции и сохранить в json файлы: где имя файла это имя категории товара.
# Структура данных в виде:
# {category_id: str,  - уникальный идентификатор категории
# category_name: str, - человекочитаемое имя категории
# items: list - список товаров пренадлежищий к данной категории}

headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}
params = {'store':'', 'records_per_page':50, 'page':1, 'categories':''}
# , 'ordering':'', 'price_promo__lte':'', 'search':''

categories = list(get('https://5ka.ru/api/v2/categories/', headers=headers).json())

for el in categories:
    params['categories'] = el['parent_group_code']
    category_offers = get('https://5ka.ru/api/v2/special_offers/', headers=headers, params=params).json()
    results = list(category_offers['results'])
    if results:
        name = []
        for els in results:
            name.append(els['name'])
        with open(f'{el["parent_group_code"]}.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps({'category_id': str(el['parent_group_code']), 'category_name': str(el['parent_group_name']), 'items': name}))

# проверка:
with open('PUI2.json', 'r', encoding='utf-8') as test:
    data = json.load(test)
    print(data)
