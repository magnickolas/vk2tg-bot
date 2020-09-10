class View:
    @staticmethod
    def parse_messages(records, members):
        fullname_by_id = {m.id: f"{m.first_name} {m.last_name}" for m in members}
        for record in records[::-1]:
            yield View.parse_message(record, fullname_by_id)

    @staticmethod
    def parse_message(record, fullname_by_id):
        from_id = record["from_id"]
        text = View.escape_text(record["text"])
        if from_id in fullname_by_id:
            text = f"{fullname_by_id[from_id]}:\n{text}"
        reply_record = record.get("reply_message")
        fwd_records = record.get("fwd_messages", [])
        if reply_record is not None:
            text += View.parse_inner_message(
                reply_record, fullname_by_id, "_Reply to_:"
            )
        for fwd_record in fwd_records:
            text += View.parse_inner_message(
                fwd_record, fullname_by_id, "_Forwarded message_:"
            )
        return text

    @staticmethod
    def parse_inner_message(record, fullname_by_id, prefix):
        text = View.parse_message(record, fullname_by_id)
        lines = list(map(lambda line: "    " + line, text.splitlines()))
        return "\n" + prefix + "\n" + "\n".join(lines)

    @staticmethod
    def escape_text(text):
        return (
            text.replace("_", "\\_")
            .replace("*", "\\*")
            .replace("[", "\\[")
            .replace("`", "\\`")
        )
