from vk2tg_bot.db.db import database
from vk2tg_bot.vk.db import VKConversation
from vk2tg_bot.vk.db import VKUser

database.create_tables([VKConversation, VKUser])
