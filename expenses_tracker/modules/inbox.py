from datetime import datetime, timedelta

from .authenticator import Authenticator
from .settings import FROM_EMAIL, USER_ID
from googleapiclient.errors import HttpError


class Inbox:
    DATE_FORMAT: str = "%Y/%m/%d"  # 2023/3/4 gmail format (year/month/day)

    def __init__(self, time_duration):
        self.authorizer = Authenticator()
        self.duration = time_duration
        self.from_date = None
        self.till_date = None

    def get_inbox_msgs_data(self) -> list[str]:
        if self.from_date is None or self.till_date is None:
            self._set_from_till_dates()
        try:
            results = (
                self.authorizer.get_service()
                .users()
                .messages()
                .list(userId=USER_ID, q=self._get_query_params()["q"])
                .execute()
            )
            msgs = results["messages"]
            msg_ids = [i["id"] for i in msgs]
            raw_msgs_data = []
            for msg in msg_ids:
                msg_result = (
                    self.authorizer.get_service()
                    .users()
                    .messages()
                    .get(userId=USER_ID, id=msg)
                    .execute()
                )
                data = msg_result.get("payload").get("body").get("data")
                raw_msgs_data.append(data)
            return raw_msgs_data
        except HttpError as error:
            print(f"An error occurred: {error}")

    def _get_query_params(self):
        # currently implemented for searching using from a sender and between two specific dates
        filter_string = (
            f"from:({FROM_EMAIL}) after:{self.from_date} before:{self.till_date}"
        )
        return {"q": filter_string}

    def _set_from_till_dates(self):
        if isinstance(self.duration, int):
            self.from_date = datetime.strftime(
                datetime.today() - timedelta(days=self.duration), Inbox.DATE_FORMAT
            )
        elif isinstance(self.duration, str):
            self.from_date = datetime.strftime(
                datetime.strptime(self.duration, Inbox.DATE_FORMAT), Inbox.DATE_FORMAT
            )
        self.till_date = datetime.strftime(
            datetime.today() + timedelta(days=1), Inbox.DATE_FORMAT
        )
