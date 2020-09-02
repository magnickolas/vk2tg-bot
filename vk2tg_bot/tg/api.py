from telegram.bot import Bot
from telegram.utils.request import Request

from vk2tg_bot.config import CONFIG


class Api:
    def __init__(self, token, *, proxy_url, white_list=None, **kwargs):
        request = Request(proxy_url=proxy_url)
        self.bot = Bot(token, request=request)
        self.white_list = white_list

    def check_white_list(self, chat_id: int):
        return self.white_list is None or chat_id in self.white_list

    def send_message(self, chat_id: int, msg_text: str):
        if self.check_white_list(chat_id):
            self.bot.send_message(chat_id=chat_id, text=msg_text)


def get_api():
    tg_bot_config = CONFIG["tg_bot"]

    bot_token = tg_bot_config["bot_token"]
    proxy_url = tg_bot_config["proxy_url"]
    white_list = tg_bot_config["white_list"]

    api = Api(token=bot_token, proxy_url=proxy_url, white_list=white_list)

    return api
