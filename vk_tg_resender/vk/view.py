class View:
    @staticmethod
    def parse_messages(records):
        for record in records[::-1]:
            yield record["text"]
