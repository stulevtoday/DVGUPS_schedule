import timetable
from datetime import date

day = timetable.parse_date(date(2022, 10, 7))

filename = timetable.collect_timetable(date_of=day)

print(timetable.for_timetable(filename))