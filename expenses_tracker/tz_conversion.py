from datetime import datetime, timedelta
from pytz import timezone
import pytz

utc = pytz.utc
given_date = "2023/02/24 08:55PM"
# new_date = datetime.strftime(datetime.strptime(given_date, "%Y/%m/%d %I:%M%p"), "%Y/%m/%d %H:%M")
new_date1 = datetime.strptime(given_date, "%Y/%m/%d %I:%M%p")
india_tz = timezone("Asia/Kolkata")
germany_tz = timezone("Europe/Berlin")
local = india_tz.localize(new_date1)
germany_time = local.astimezone(germany_tz)
print(germany_time)
