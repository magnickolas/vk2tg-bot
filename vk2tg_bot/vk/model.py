from time import sleep

from vk_api.exceptions import ApiError

from vk2tg_bot.vk.api import get_api
from vk2tg_bot.vk.db_models import VKConversation
from vk2tg_bot.vk.db_models import VKUser


class Model:
    def __init__(self):
        self.api = get_api()

    def fetch_latest_messages_records(self, conversation_id):
        conversation = VKConversation.get_or_none(id=conversation_id)
        if not conversation:
            records = self.fetch_latest_messages_with_offset(
                conversation_id=conversation_id, offset=0, count=5
            )
            last_msg_id = records[0]["id"]
            VKConversation.create(id=conversation_id, last_msg_id=last_msg_id)
            return records
        else:
            all_records = []
            from_msg_id = conversation.last_msg_id + 1
            offset = 0
            while True:
                records = self.fetch_latest_messages_with_offset(
                    conversation_id=conversation_id, offset=offset, count=200,
                )
                first_history_message = records[-1]
                all_records.extend(
                    filter(lambda record: record["id"] >= from_msg_id, records)
                )
                if from_msg_id >= first_history_message["id"]:
                    break
                offset += len(records)
            if all_records:
                last_msg_id = all_records[0]["id"]
                query = VKConversation.update(last_msg_id=last_msg_id).where(
                    VKConversation.id == conversation_id
                )
                query.execute()
            return all_records

    def fetch_latest_messages_with_offset(self, conversation_id, offset, count):
        messages = None
        while True:
            try:
                messages = self.api.messages.getHistory(
                    offset=offset, peer_id=conversation_id, count=count
                )["items"]
                break
            except ApiError as ex:
                sleep(5)
        return messages

    def get_conversation_members(self, conversation_id):
        query = VKUser.select(VKUser.id, VKUser.first_name, VKUser.last_name).where(
            VKUser.conversation_id == conversation_id
        )
        return [member for member in query]

    def update_conversation_members(self, conversation_id):
        response = self.api.messages.getConversationMembers(
            peer_id=conversation_id, fields="id,first_name,last_name"
        )
        profiles = response["profiles"]
        for profile in profiles:
            id = profile["id"]
            first_name = profile["first_name"]
            last_name = profile["last_name"]
            VKUser.get_or_create(
                id=id,
                conversation_id=conversation_id,
                first_name=first_name,
                last_name=last_name,
            )

    def are_all_messages_authors_cached(self, conversation_id, messages_records):
        authors_ids = set([record["from_id"] for record in messages_records])
        num_authors_ids = len(authors_ids)
        num_cached_authors_ids = (
            VKUser.select()
            .where(
                VKUser.id.in_(authors_ids) & (VKUser.conversation_id == conversation_id)
            )
            .count()
        )
        return num_authors_ids == num_cached_authors_ids
