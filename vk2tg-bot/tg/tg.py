from vk_tg_resender.tg.api import get_api


class Sender:
    def __init__(self):
        self.api = get_api()

    def send_message(self, chat_id: str, msg_text: str):
        if msg_text.strip():
            self.api.send_message(chat_id=chat_id, msg_text=msg_text)
