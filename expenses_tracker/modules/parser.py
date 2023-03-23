import base64
import re

from bs4 import BeautifulSoup


class MessageParser:
    def __init__(self, messages: list[str]):
        self.msgs = messages
        self.parsed_msgs = None

    def parse_msgs(self):
        self.parsed_msgs = [MessageParser.get_processed_msg(i) for i in self.msgs]

    def extract_regex_data(self, regex_list: list[str]) -> list[list[list[str]]]:
        extracted_data = []
        if self.parsed_msgs is None:
            self.parse_msgs()
        for msg in self.parsed_msgs:
            msg_info = []
            for r in regex_list:
                msg_info.append(
                    [
                        i.strip()
                        for i in MessageParser._regex_parse(regex=r, search_exp=msg)
                    ]
                )
            extracted_data.append(msg_info)
        return extracted_data

    @staticmethod
    def get_processed_msg(body: str) -> str:
        decoded_body = MessageParser._decode_content(body)
        extracted_soup = BeautifulSoup(decoded_body, "html.parser")
        return extracted_soup.get_text().strip()

    # helper functions
    @staticmethod
    def _decode_content(content) -> str:
        return base64.urlsafe_b64decode(content.encode("ASCII")).decode("utf-8")

    @staticmethod
    def _regex_parse(regex: str, search_exp: str) -> list:
        match = re.findall(regex, search_exp)
        if match:
            return match
