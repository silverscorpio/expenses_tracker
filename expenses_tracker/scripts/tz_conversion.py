# Timezone conversion

from datetime import datetime

import pytz
from pytz import timezone


# (default: from India to Germany)
def convert_tz(
    given_datetime_12: str,
    given_tz: str = "Asia/Kolkata",
    new_tz: str = "Europe/Berlin",
) -> str:
    if all([tz in pytz.all_timezones for tz in (given_tz, new_tz)]):
        # input datetime format "2023/02/24 08:55 PM"
        # example - convert_tz(given_datetime_12="2023/02/24 08:55 PM")
        formatted_datetime_24 = datetime.strptime(
            given_datetime_12, "%Y/%m/%d %I:%M %p"
        )
        given_tz = timezone(given_tz)
        new_tz = timezone(new_tz)
        local_given_tz_time = given_tz.localize(formatted_datetime_24)
        return datetime.strftime(
            local_given_tz_time.astimezone(new_tz), "%Y/%m/%d %I:%M %p"
        )


if __name__ == "__main__":
    pass
