# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

from requests import get
import json

repos = get('https://api.github.com/users/olhaexe/repos').json()
for repo in repos:
    print(repo['html_url'])
with open('repo.json', 'w') as f:
    f.write(json.dumps(repo['html_url']))

# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

fmtags = get('http://ws.audioscrobbler.com/2.0/?method=track.addTags&api_key=c091708d2b2aaaf2cbcb87978a637124')
with open('response.pkl', 'w') as fm:
    fm.write(str(fmtags))

