from peewee import Model, CharField, DateTimeField
import datetime
from dao.database import db


class User(Model):
    username = CharField(unique=True)
    password = CharField()
    created = DateTimeField(default=datetime.datetime.now)
    last_login = DateTimeField(null=True)

    class Meta:
        database = db
