from peewee import Model, IntegerField, CharField, TimestampField, DateTimeField
import datetime
from dao.database import db


class Post(Model):
    id = IntegerField(primary_key=True)
    content = CharField()
    created = DateTimeField()
    visible = DateTimeField()
    deleted = DateTimeField(null=True)
    edited = TimestampField(default=datetime.datetime.now)

    class Meta:
        database = db
