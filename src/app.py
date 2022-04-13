from flask import Flask, request, render_template
from scripts.utils import gen_weekdays, gen_hours, get_today
from db import Day, Time

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("home.html")
    else:
        authenticate()
    

def authenticate():
    pass

# def generate_days_timeslots():

#     curr_day, curr_hr = get_today()
#     if curr_day == 1 or curr_day == 7:
#         #Generate for whole week
#         pass
    
#     for k,v in weekdays.items():

#         if k == curr_day:
#             # Create a day object
#             day = Day()
#             # Create the hours from curr_hour
#             pass

#         elif k > curr_day:
#             # Create a day
#             # Create the hours from 8am
#             pass

def gen_all_days_hours():
    weekdays = gen_weekdays()
    hours = gen_hours()

    for k,v in weekdays.items():
        day = Day(name=v, active=True)

        for hr in hours:
            time = Time(start=hr, booked=False)
            day.timeslots.append(time)


    




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5500, debug=True)
