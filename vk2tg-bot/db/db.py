from peewee import *

database = SqliteDatabase("database/database.db")


class BaseModel(Model):
    class Meta:
        database = database
