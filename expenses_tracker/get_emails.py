from datetime import datetime, timedelta
import json
from parse_msg import regex_parse
from parse_msg import parse_all

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials

from environs import Env

# load_dotenv()
#
# USER_ID = os.getenv("USER_ID")
# TOKEN = os.getenv("TOKEN")
# REDIRECT_URI = os.getenv("REDIRECT_URI")
# CLIENT_ID = os.getenv("CLIENT_ID")
# CLIENT_SECRET = os.getenv("CLIENT_SECRET")
# AUTH_URI = os.getenv("AUTH_URI")
# TOKEN_URI = os.getenv("TOKEN_URI")
# SCOPES = os.getenv("SCOPES")
# AUTH_TOKEN = json.loads(os.getenv("AUTH_TOKEN"))


# TODO OOP based (scalable and loosely coupled for further use)
# TODO include time zone conversion
# TODO time based filtering (epoch ms) - on hold (maybe - too specific)
# TODO saving to database (sqlite3 (KISS), api - sqlalchemy) and further usage (visualisation - plotly)
# TODO create category for each transaction to track the type of spending (hint -spendee)


env = Env()
env.read_env()

USER_ID = env.str("USER_ID")
FROM_EMAIL = env.str("FROM_EMAIL")


def fetch_data(given_date: str = ""):
    # 2023/3/4 gmail format (year, month, day)
    # reference_date = datetime.strftime(datetime.today(), "%y/%m/%d")
    past_date = datetime.strftime(datetime.strptime(given_date, "%Y/%m/%d"), "%Y/%m/%d")
    if not given_date:
        past_date = datetime.strftime(datetime.today() - timedelta(days=3), "%Y/%m/%d")
    future_date = datetime.strftime(datetime.today() + timedelta(days=1), "%Y/%m/%d")
    q_params = {"q": f"from:({FROM_EMAIL}) after:{past_date} before:{future_date}"}
    creds = Credentials.from_authorized_user_file('../token.json', SCOPES)
    # request
    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId=USER_ID, q=q_params["q"]).execute()
        msgs = results["messages"]
        msg_ids = [i["id"] for i in msgs]
        msg_data = []
        for m in msg_ids:
            msg_result = service.users().messages().get(userId=USER_ID, id=m).execute()
            data = msg_result.get("payload").get("body").get("data")
            msg_data.append(parse_all(data))
        return msg_data
        # for i in msg_data:
        #     print(i)
        #     print("-------------")
    except HttpError as error:
        print(f"An error occurred: {error}")
    # r = auth_client.get(mail_url, params=q_params)
    # if r.status_code == 200:
    #     content = r.content.decode("utf-8")
    #     msg_ids = [i["id"] for i in json.loads(content)["messages"]]
    #     msg_data = []
    #     for m in msg_ids:
    #         msg_url = os.path.join(mail_url, m)
    #         mr = auth_client.get(msg_url)
    #         msg_data.append(mr.content)
    #
    #     return msg_data


if __name__ == '__main__':
    # base_url = "https://gmail.googleapis.com/gmail/v1/users/"
    # mail_url = os.path.join(base_url, USER_ID, "messages")
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
    email_contents = fetch_data(given_date="2023/2/23")

    # regex
    amt_regex = r"[A-Z]{3}\s\d+\.?\d+[\.?|\s]"
    date_regex = r"\s\d+-[A-Z]{3}-\d{2}\s"
    time_regex = r"\s\d{2}:\d{2}\s[AP][M]"
    location_regex = r"[AP][M]\s[a][t][\w\s]{1,150}\s*"

    info = []
    regex_list = [amt_regex, date_regex, time_regex, location_regex]
    for msg in email_contents:
        msg_info = []
        for r in regex_list:
            msg_info.append([i.strip() for i in regex_parse(regex=r, search_exp=msg)])
        info.append(msg_info)

    for i in info:
        print(i)
