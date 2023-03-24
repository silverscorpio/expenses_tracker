from modules.inbox import Inbox
from modules.parser import MessageParser


def get_regexp_list() -> list[str]:
    regex_data = {
        "MONEY_SPENT": r"[A-Z]{3}\s\d+\.?\d+",
        "TRANSACTION_DATE": r"\s\d+-[A-Z]{3}-\d{2}\s",
        "TRANSACTION_TIME": r"\s\d{2}:\d{2}\s[AP][M]",
        "MERCHANT": r"[AP][M]\s[a][t][\w\s]{1,150}\s*",
    }
    return [value for value in regex_data.values()]


def main(duration: int | str, regexp_list: list[str]):
    raw_messages = Inbox(time_duration=duration).get_inbox_msgs_data()
    parser = MessageParser(messages=raw_messages)
    parser.parse_msgs()
    parser.extract_regex_data(regex_list=regexp_list)
    print(parser.extracted_regex_info)


if __name__ == "__main__":
    main(duration=2, regexp_list=get_regexp_list())
