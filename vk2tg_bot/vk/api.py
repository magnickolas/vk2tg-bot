import vk_api

from vk2tg_bot.config import CONFIG


def get_api():
    vk_config = CONFIG["vk"]

    LOGIN = vk_config["login"]
    TOKEN = vk_config["token"]
    PASSWORD = vk_config["password"]
    APP_ID = vk_config["app-id"]

    def auth_handler():
        code = input("Enter authentication code: ")
        remember_device = True
        return code, remember_device

    vk_session = vk_api.VkApi(
        login=LOGIN,
        password=PASSWORD,
        token=TOKEN,
        auth_handler=auth_handler,
        app_id=APP_ID,
    )
    vk_session.auth()

    return vk_session.get_api()
