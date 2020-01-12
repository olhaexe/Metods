from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    String,
    Integer
)

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

assoc_post_tag = Table(
    'post_tag',
    Base.metadata,
    Column('blogpost', Integer, ForeignKey('blogpost.id')),
    Column('tag', Integer, ForeignKey('tag.id'))
)

# todo класс записи в блоге
class BlogPost(Base):
    __tablename__ = 'blogpost'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    date = Column(String)
    url = Column(String, unique=True)
    writer_id = Column(Integer, ForeignKey('writer.id'))
    writer = relationship('Writer', backref='blogposts')
    tags = relationship('Tag', secondary=assoc_post_tag, backref='blogposts')

    def __init__(self, title: str, date: str, url: str, writer, tags=[]):
        self.title = title
        self.date = date
        self.url = url
        self.writer = writer
        if tags:
            self.tags.extend(tags)

# todo класс для объекта тега
class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)

    def __init__(self, name: str):
        self.name = name

# todo класс для автора
class Writer(Base):
    __tablename__ = 'writer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    url = Column(String, unique=True)

    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url
