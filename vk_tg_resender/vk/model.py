from vk_tg_resender.vk.api import get_api
from vk_tg_resender.vk.db import VKConversation


class Model:
    def __init__(self):
        self.api = get_api()

    def fetch_latest_messages_records(self, conversation_id):
        conversation = VKConversation.get_or_none(VKConversation.id == conversation_id)
        if not conversation:
            records = self.api.messages.getHistory(
                offset=0, peer_id=conversation_id, count=5
            )["items"]
            last_msg_id = records[0]["id"]
            VKConversation.create(id=conversation_id, last_msg_id=last_msg_id)
            return records
        else:
            all_records = []
            from_msg_id = conversation.last_msg_id + 1
            offset = 0
            while True:
                records = self.api.messages.getHistory(
                    peer_id=conversation_id, offset=offset, count=200,
                )["items"]
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
