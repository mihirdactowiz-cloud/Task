from  datetime  import datetime, date

from dateutil.rrule import weekday
from future.backports.datetime import timedelta

now  = datetime.now() # Output: 2026-04-06 16:52:32 (YYYY-MM-DD HH-MM-SS format)
today  = date.today()

# print(now)
# print(today)

specific = datetime(2024, 12, 25, 10, 30)
str_date = now.strftime("%Y-%m-%d   %H:%M")
obj = datetime.strptime("2026-02-02", "%Y-%m-%d")

week_later  = now + timedelta(days=7)
diff  =  datetime(2024, 1, 1)

ts = now.timestamp()
iso =  now.isoformat()
weekday = now.weekday()

# print(specific)
# print(today)
# print(str_date)
# print(week_later.date())
# print(obj)
print(ts)
print(iso)
print(weekday)