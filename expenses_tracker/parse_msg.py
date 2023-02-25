import base64
import json
import re

from bs4 import BeautifulSoup


def decode_content(content) -> str:
    return base64.urlsafe_b64decode(content.encode("ASCII")).decode("utf-8")


# step 2 (inside step 1)
def save_json(name: str, data_val):
    with open(name, "w") as f:
        json.dump(data_val, f)


# step 1
def parse_data(mail: bytes):
    data_json = json.loads(mail.decode("utf-8"))
    # save_json(file, data_json)
    return data_json


# step 3
def bs_data(req_data):
    # TODO add check on size and body data
    conv_data = decode_content(req_data.get("payload").get("body").get("data"))
    conv_bs_data = BeautifulSoup(conv_data, 'html.parser')
    value = conv_bs_data.get_text()
    return value.strip()


# ans = (json.loads(data[0].decode("utf-8")))

# with open("file.json", "w") as f:
#     json.dump(ans, f)

def parse_all(body: str) -> str:
    x = decode_content(body)
    conv_bs_data = BeautifulSoup(x, 'html.parser')
    value = conv_bs_data.get_text()
    return value.strip()


# parsed_data = decode_content(ans.get("payload").get("body").get("data"))
# # print(parsed_data)
# bs_data = BeautifulSoup(parsed_data, 'html.parser')
# val = bs_data.get_text()
# print(val.strip())
# # print(bs_data.find("body"))

amt_regex = r"[A-Z]{3}\s\d+\.?\d+[\.?|\s]"
date_regex = r"\s\d+-[A-Z]{3}-\d{2}\s"
time_regex = r"\s\d{2}:\d{2}\s[AP][M]"
location_regex = r"[AP][M]\s[a][t][\w\s]{1,150}\s*\.{1}"


#### multiple parsing
def msg_parse(fetched_data: list[bytes]) -> list:
    emails = []
    for ind, val in enumerate(fetched_data):
        d = parse_data(val, f"file_{ind + 1}.json")
        emails.append(bs_data(d))
    return emails


def regex_parse(regex: str, search_exp: str) -> list:
    match = re.findall(regex, search_exp)
    if match:
        return match


if __name__ == '__main__':
    msg_parse(fetched_data=data)
