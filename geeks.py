# используя bs4, ресурс: https://geekbrains.ru/posts, пройти ленту, статей блога, получить страницу с статьей,
# извлечь след данные: заголовок статьи, дата публикации, url статьи, список тегов, имя автора, url автора
# при помощи sqlalchemy сохранить данные в базу.
# обязательно теги и автор должны существовать отдельными таблицами, и должны быть корректно реализованы соответствующие связи.

import requests
import re
from bs4 import BeautifulSoup as BS
import pandas as pd

from database.models import (
    Base,
    BlogPost,
    Writer,
    Tag,
)

from database.db import BlogDb

start_url = 'https://geekbrains.ru/posts/'

db_url = 'sqlite:///blogpost.sqlite'
db = BlogDb(db_url)

def get_page_content(url):
    link = url
    html_content = requests.get(link).text
    return html_content

def title_link_get(start_url):
    html_content = get_page_content(start_url)
    soup = BS(html_content, 'html.parser')
    title_example = """<a href="/posts/[^\"]">...</a>"""
    refs = str(soup.find_all('a'))
    titles = re.findall('href=\"/posts/([^\"]+)\"', refs)
    return titles

title_set = set(title_link_get(start_url))
link_list = []
for t in title_set:
    u = start_url + t
    link_list.append(u)
#print(link_list)

def get_info(url):
    article_content = get_page_content(url)
    writer_url_id = re.findall('\"(/users/[0-9]+)\"', article_content)
    if writer_url_id:
        title = re.findall('<meta name=\"title\" content=\"([^\"]+)\"', article_content)
        date_publ = re.findall('<meta name=\"mediator_published_time\" content=\"([^\"]+)\"', article_content)
        article_url = url
        tags = re.findall('<meta name=\"keywords\" content=\"([^\"]+)\"', article_content)
        writer = re.findall('<meta name=\"mediator_author\" content=\"([^\"]+)\"', article_content)
        writer_url = 'https://geekbrains.ru' + str(writer_url_id[0])
        df_article = pd.DataFrame({'title':title[0], 'date_publ':date_publ[0], 'url':url, 'tags':tags[0], 'writer':writer[0], 'writer_url':[writer_url]},
                                columns=['title', 'date_publ', 'url', 'tags', 'writer', 'writer_url'])
        return df_article

df = pd.DataFrame(columns=['title', 'date_publ', 'url', 'tags', 'writer', 'writer_url'])

for u in link_list:
    df = pd.concat([df, get_info(u)], axis=0, ignore_index=True)

#print(df)

tags = list(df['tags'])
tag_list = []
for s in tags:
    tag_list.extend(s.split(', '))
tag_set = set(tag_list)
#tag_set.remove('')
#print(tag_set)

tags_class = [Tag(f'{el}') for el in tag_set]
#print(tags_class)

writer_list = list(df['writer'])
writer_url_list = (df['writer_url'])
writers = []
for i in range(len(writer_list)):
    writers.append([writer_list[i], writer_url_list[i]])
writers_unique = []
for el in writers:
    if el not in writers_unique:
        writers_unique.append(el)
#print(writers_unique)

writers_class = [Writer(f'{el[0]}', el[1]) for el in writers_unique]
#print(writers_class[0].name) #разные имена при каждом запуске, видимо, из-за set

db.session.add(tags_class)
db.session.add(writers_class)
print(writers_class[0].id)

title_list = list(df['title'])
posts_list = []
for i in range(len(title_list)):
    posts_list.append([title_list[i], link_list[i], writer_list[i], tags[i].split(', ')])
#for i in range(len(posts_list)):
 #   print(posts_list[i])

#posts_class = [BlogPost(el[0], el[1], el[2], el[3]) for el in posts_list]
#print(posts_class)
#    title = Column(String)
#    url = Column(String, unique=True)
#    writer_id = Column(Integer, ForeignKey('writer.id'))
#    writer = relationship('Writer', backref='blogposts')
#    tags = relationship('Tag', secondary=assoc_post_tag, backref='blogposts')