class View:
    @staticmethod
    def parse_messages(records, members):
        fullname_by_id = {m.id: f"{m.first_name} {m.last_name}" for m in members}
        for record in records[::-1]:
            from_id = record["from_id"]
            text = record["text"]
            if from_id in fullname_by_id:
                text = f"{fullname_by_id[from_id]}:\n{text}"
            yield text
