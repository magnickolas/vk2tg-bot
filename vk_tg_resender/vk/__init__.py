from vk_tg_resender.db.db import database
from vk_tg_resender.vk.db import VKConversation

database.create_tables([VKConversation])
