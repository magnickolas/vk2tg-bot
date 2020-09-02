from peewee import *

from vk_tg_resender.db.db import BaseModel


class VKConversation(BaseModel):
    id = IntegerField(unique=True)
    last_msg_id = IntegerField()
