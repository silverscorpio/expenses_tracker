import base64
import re
from enum import Enum, unique

from bs4 import BeautifulSoup

from .datetime_utils import change_date_format, convert_tz


class MessageParser:
    @unique
    class Tag(Enum):
        FOOD_DRINKS_GROCERIES = 1
        EDUCATION_AND_LEARNING = 2
        BILLS = 3
        TRAVEL = 4
        UTILITIES = 5
        SHOPPING = 6
        SALARY = 7
        EXTRA_INCOME = 8
        OTHERS = 9

    def __init__(self, messages: list[str]):
        self.msgs = messages
        self.parsed_msgs = None
        self.extracted_regex_info = None
        self.processed_data = None

    def parse_msgs(self):
        self.parsed_msgs = [MessageParser.get_processed_msg(i) for i in self.msgs]

    def extract_regex_data(self, regex_list: list[str]):
        extracted_data = []
        if self.parsed_msgs is None:
            self.parse_msgs()
        for msg in self.parsed_msgs:
            msg_info = []
            for r in regex_list:
                msg_info.extend(
                    [
                        i.strip()
                        for i in MessageParser._regex_parse(regex=r, search_exp=msg)
                    ]
                )
            extracted_data.append(msg_info)
        self.extracted_regex_info = extracted_data

    def process_data(self):
        db_data = []
        for transaction in self.extracted_regex_info:
            ger_datetime = MessageParser.get_ger_datetime(
                date_val=transaction[2], time_val=transaction[3]
            ).split()
            ger_date = ger_datetime[0]
            ger_time = " ".join(ger_datetime[1:])
            db_row = {
                "merchant": " ".join(transaction[-1].split()[2:]).lower(),
                "money_spent": float(transaction[0].split()[1]),
                "current_balance": float(transaction[1].split()[1]),
                "transaction_date_ger": ger_date,
                "transaction_time_ger": ger_time,
                "old_balance": (
                    float(transaction[0].split()[1]) + float(transaction[1].split()[1])
                ),
                "tag": self.tag_transaction(),
                "transaction_date_ind": transaction[2],
                "transaction_time_ind": transaction[3],
            }
            db_data.append(db_row)
        self.processed_data = db_data

    def tag_transaction(self):
        pass

    # helper functions
    @staticmethod
    def get_ger_datetime(date_val: str, time_val: str) -> str:
        ind_datetime = change_date_format(given_date=date_val) + " " + time_val
        return convert_tz(given_datetime_12=ind_datetime)

    @staticmethod
    def get_processed_msg(body: str) -> str:
        decoded_body = MessageParser._decode_content(body)
        extracted_soup = BeautifulSoup(decoded_body, "html.parser")
        return extracted_soup.get_text().strip()

    @staticmethod
    def _decode_content(content) -> str:
        return base64.urlsafe_b64decode(content.encode("ASCII")).decode("utf-8")

    @staticmethod
    def _regex_parse(regex: str, search_exp: str) -> list | str:
        match = re.findall(regex, search_exp)
        if match:
            return match
        return ""  # credited
