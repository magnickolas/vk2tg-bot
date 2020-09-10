from time import sleep

from telegram import ParseMode
from telegram.bot import Bot
from telegram.error import RetryAfter
from telegram.utils.request import Request

from vk2tg_bot.config import CONFIG


class Api:
    def __init__(self, token, *, proxy_url, **kwargs):
        request = Request(proxy_url=proxy_url)
        self.bot = Bot(token, request=request)

    def send_message(self, chat_id: int, msg_text: str):
        while True:
            try:
                return self.bot.send_message(
                    chat_id=chat_id, text=msg_text, parse_mode=ParseMode.MARKDOWN
                )
            except RetryAfter as ex:
                sleep(ex.retry_after)


def get_api():
    tg_bot_config = CONFIG["tg-bot"]

    bot_token = tg_bot_config["bot-token"]
    proxy_url = tg_bot_config["proxy-url"]

    api = Api(token=bot_token, proxy_url=proxy_url)

    return api
