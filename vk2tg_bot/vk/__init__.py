from vk2tg_bot.db.db import database
from vk2tg_bot.vk.db_models import VKConversation
from vk2tg_bot.vk.db_models import VKUser

database.create_tables([VKConversation, VKUser])
