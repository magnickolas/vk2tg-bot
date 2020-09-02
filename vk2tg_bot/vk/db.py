from peewee import *

from vk2tg_bot.db.db import BaseModel


class VKConversation(BaseModel):
    id = IntegerField(unique=True)
    last_msg_id = IntegerField()


class VKUser(BaseModel):
    id = IntegerField(unique=True)
    conversation_id = IntegerField()
    first_name = TextField()
    last_name = TextField()
