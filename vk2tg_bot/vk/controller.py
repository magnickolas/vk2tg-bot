class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def fetch_latest_messages(self, conversation_id):
        records = self.model.fetch_latest_messages_records(
            conversation_id=conversation_id
        )
        if not self.model.are_all_messages_authors_cached(
            conversation_id=conversation_id, messages_records=records
        ):
            self.model.update_conversation_members(conversation_id=conversation_id)
        members = self.model.get_conversation_members(conversation_id=conversation_id)
        return self.view.parse_messages(records=records, members=members)

    def update_conversation_members(self, conversation_id):
        self.model.update_conversation_members(conversation_id=conversation_id)
