from datetime import datetime, timedelta

def gen_weekdays():
    return {
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
        7: "Sunday"
    }

def gen_hours():
    def datetime_range(start, end, delta):
        current = start
        while current < end:
            yield current
            current += delta

    dts = [dt.strftime('%H:%M') for dt in 
        datetime_range(datetime(2016, 9, 1, 8), datetime(2016, 9, 1, 23), 
        timedelta(hours=1))]
    
    return dts


def get_today():

    today = datetime.now()
    hour = today.hour
    day = today.isoweekday()

    return day, hour

