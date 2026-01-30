from datetime import date, timedelta
import calendar

today = date.today()
year = today.year
month = today.month

# Get number of days in current month
_, days_in_month = calendar.monthrange(year, month)

menu = {}

# Day indexes
today_day = today.day
tomorrow_day = today_day + 1

for day in range(1, days_in_month + 1):
    menu[day] = "TBD"

# Apply rules
menu[today_day] = "Chicken Nuggets"
if today_day + 1 <= days_in_month:
    menu[today_day + 1] = "Pizza"
if today_day + 2 <= days_in_month:
    menu[today_day + 2] = "Pizza"

# Second day of chicken nuggets (after pizza if possible)
second_nugget_day = today_day + 3
if second_nugget_day <= days_in_month:
    menu[second_nugget_day] = "Chicken Nuggets"

# Output
print(f"Dinner Menu for {calendar.month_name[month]} {year}\n")
for day in range(1, days_in_month + 1):
    print(f"{month:02d}/{day:02d}: {menu[day]}")
