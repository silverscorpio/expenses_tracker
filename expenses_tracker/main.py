from modules.inbox import Inbox
from modules.parser import MessageParser

from expenses_tracker.database.db_schemas import db


def get_regexp_list() -> list[str]:
    regex_data = {
        "MONEY_SPENT": r"[A-Z]{3}\s\d+\.?\d+",
        "TRANSACTION_DATE": r"\s\d+-[A-Z]{3}-\d{2}\s",
        "TRANSACTION_TIME": r"\s\d{2}:\d{2}\s[AP][M]",
        "MERCHANT": r"[AP][M]\s[a][t][\w\s]{1,150}\s*",
    }
    return [value for value in regex_data.values()]


def main(duration: int | str, regexp_list: list[str]):
    with db:
        raw_messages = Inbox(time_duration=duration).get_inbox_msgs_data()
        parser = MessageParser(messages=raw_messages)
        parser.parse_msgs()
        parser.extract_regex_data(regex_list=regexp_list)
        parser.process_data()
        print(parser.processed_data)


if __name__ == "__main__":
    main(duration=2, regexp_list=get_regexp_list())
