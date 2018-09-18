import os
import sys

from commons import debug
from immutable import change

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from settings import engine

from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()


class Article(Base):
    __tablename__ = 'Articles'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), default='')
    content = Column(String(255), default='')

    comments = relationship("Comment", backref="article")

class Comment(Base):
    __tablename__ = 'Comments'
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer,ForeignKey('Articles.id'))
    comment = Column(String(255), default='')



Session = sessionmaker(bind=engine)


def get_database_object(state):
    debug(get_database_object.__name__, "json:", state.json)
    database_obj=None
    json = state.json
    if json.has_key("id") and (isinstance(json["id"],int) or isinstance(json["id"],long)):
        database_obj = state.session.query(state.type).get(json["id"])

    if not database_obj:
        database_obj = state.type()

    return change("data", database_obj)(state)


def save_database_object(state):
    raise NotImplementedError


def save_database_object(state):
    debug(save_database_object.__name__, "obj:", state.data)
    obj = state.data
    if not obj.id:
        state.session.add(obj)
    state.session.commit()
    state.session.refresh(obj)
    return change("data", obj)(state)
