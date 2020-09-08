import vk_api

from vk2tg_bot.config import CONFIG


def get_api():
    vk_config = CONFIG["vk"]

    TOKEN = vk_config["token"]
    APP_ID = vk_config["app-id"]

    vk_session = vk_api.VkApi(
        token=TOKEN,
        app_id=APP_ID,
    )

    return vk_session.get_api()
