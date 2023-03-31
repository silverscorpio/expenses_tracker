from datetime import datetime, timedelta

from database.db_schemas import Expenses, db
from database.db_utils import db_store
from modules.cmdline import args_parser
from modules.inbox import Inbox
from modules.parser import MessageParser


def get_regexp_list() -> list[str]:
    # eur as guaranteed primary currency
    regex_data = {
        "MONEY_SPENT": r"[EUR]{3}\s\d+\.?\d+",
        "TRANSACTION_DATE": r"\s\d+-[A-Z]{3}-\d{2}\s",
        "TRANSACTION_TIME": r"\s\d{2}:\d{2}\s[AP][M]",
        "MERCHANT": r"[AP][M]\s[a][t][\w\s]{1,150}\s*",
    }
    return [value for value in regex_data.values()]


def main(
    regexp_list: list[str],
    duration: int
    | str = (datetime.today().date() - timedelta(days=1)).strftime("%Y/%m/%d"),
):
    with db:
        raw_messages = Inbox(time_duration=duration).get_inbox_msgs_data()
        parser = MessageParser(messages=raw_messages)
        parser.parse_msgs()
        parser.extract_regex_data(regex_list=regexp_list)
        parser.process_data()
        db_store(
            database=db, model=Expenses, data=parser.processed_data, loop_over=True
        )


if __name__ == "__main__":
    # 2023 transactions (27.03)
    # date format - 2023/3/4

    # cmdline part
    # time_duration = args_parser()

    main(duration=1, regexp_list=get_regexp_list())
