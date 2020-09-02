class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def fetch_latest_messages(self, conversation_id):
        records = self.model.fetch_latest_messages_records(
            conversation_id=conversation_id
        )
        return self.view.parse_messages(records=records)
