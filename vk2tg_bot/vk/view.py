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
        attachments = record.get("attachments", [])
        if reply_record is not None:
            text += View.parse_inner_message(
                reply_record, fullname_by_id, "_Reply to_:"
            )
        for fwd_record in fwd_records:
            text += View.parse_inner_message(
                fwd_record, fullname_by_id, "_Forwarded message_:"
            )
        for attachment in attachments:
            text += View.parse_attachment(attachment)

        return text

    @staticmethod
    def parse_attachment(attachment):
        attachment_type = attachment["type"]
        if attachment_type == "photo":
            photo_attachment = attachment["photo"]
            max_scale_photo = max(photo_attachment["sizes"], key=lambda p: p["height"])
            max_scale_photo_url = max_scale_photo["url"]
            return f"\nPhoto: {max_scale_photo_url}\n"

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
