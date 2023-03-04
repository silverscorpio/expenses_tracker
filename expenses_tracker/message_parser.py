import base64
from bs4 import BeautifulSoup


# TODO variable declaration inside classes
class MessageParser:

    def __init__(self, messages: list[str]):
        self.msgs = messages

    def parse_msgs(self):
        return [MessageParser.get_processed_msg(i) for i in self.msgs]

    @staticmethod
    def get_processed_msg(body: str) -> str:
        decoded_body = MessageParser._decode_content(body)
        extracted_soup = BeautifulSoup(decoded_body, 'html.parser')
        return extracted_soup.get_text().strip()

    # helper functions
    @staticmethod
    def _decode_content(content) -> str:
        return base64.urlsafe_b64decode(content.encode("ASCII")).decode("utf-8")

    def regex_parser(self, regex_list: list[str], parsed_msgs: list[str]):
        info = []
        for msg in parsed_msgs:
            msg_info = []
            for r in regex_list:
                msg_info.append([i.strip() for i in regex_parse(regex=r, search_exp=msg)])
            info.append(msg_info)
        return info
