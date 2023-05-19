import datetime



def get_first_and_last_week_of_month(year, month):
    # Calculate the first day of the ISO year
    jan4 = datetime.date(year, 1, 4)
    
    # Calculate the first day of the first week of the ISO year
    delta = datetime.timedelta(days=7-jan4.weekday())
    first_day_of_first_week = jan4 + delta
    
    # Calculate the date of the first day of the specified month
    first_day_of_month = datetime.date(year, month, 1)
    
    # Calculate the number of days between the first day of the first week and the first day of the month
    days_between = (first_day_of_month - first_day_of_first_week).days
    
    # Calculate the number of weeks between the first day of the first week and the first day of the month
    weeks_between = int(days_between / 7)
    
    # Calculate the first day of the first week of the specified month
    first_day_of_first_week_of_month = first_day_of_first_week + datetime.timedelta(days=weeks_between*7)+datetime.timedelta(days=7)
    
    # Calculate the last day of the last week of the specified month
    last_day_of_month = datetime.date(year, month, 28)
    while last_day_of_month.month == month:
        last_day_of_month += datetime.timedelta(days=1)
    last_day_of_month -= datetime.timedelta(days=7-last_day_of_month.weekday())
    
    return first_day_of_first_week_of_month, last_day_of_month+datetime.timedelta(days=7)-datetime.timedelta(days=1)

def get_month_from_year_week(year, week):
    # Calculate the first day of the ISO year
    jan4 = datetime.date(year, 1, 4)

    # Calculate the first day of the first week of the ISO year
    delta = datetime.timedelta(days=-jan4.weekday())
    first_day_of_first_week = jan4 + delta
    
    # Calculate the date of the first day of the specified week
    first_day_of_week = first_day_of_first_week + datetime.timedelta(weeks=week-1)

    # Extract the month number from the first day of the week
    month = first_day_of_week.month
    
    return month

def get_week_numbers(daterange):
    weeklist = []
    for date in daterange:
        weeklist.append(date.isocalendar().week)
    return list(set(weeklist))
    
def get_month_name_from_number(month):
    months = ["Januari","Februari","Mars","April","Maj","Juni","Juli","Augusti","September","Oktober","November","December"]
    return months[month-1]

def get_month_from_week(year, week_number):
    # Create a datetime object for the given year and week number
    if not year: year="2023"
    dt = datetime.datetime.strptime(f'{year}-W{week_number}-1', '%Y-W%W-%w')

    # Get the month in the ISO format
    month = dt.strftime('%Y-%m')

    return month
def first_day_from_week(year,week):
    # Create a date object for January 4th of the given year, which is always in week 1
    jan_4 = datetime.date(year, 1, 4)

    # Calculate the number of days to add to January 4th to get to the first day of the given week
    days_to_add = (week - 1) * 7 - jan_4.weekday()

    # Calculate the date of the first day of the given week
    first_day = jan_4 + datetime.timedelta(days=days_to_add)

    return first_day