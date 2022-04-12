from datetime import datetime
import calendar

def get_today():

    today = datetime.now()
    hour = today.hour
    day = today.isoweekday()

    return day, hour


get_today()