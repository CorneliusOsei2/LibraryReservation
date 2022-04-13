from flask import Flask, request, render_template
from scripts.helpers import gen_weekdays, gen_hours, get_today
from scripts.utils import response
from db import db,Week, Day, Time

# Initialize Flask
app = Flask(__name__)

# DB config
db_filename = "library.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()


# Helper Functions and Generators
@app.route("/library/gen/", methods=["GET"])
def gen_all_days_hours():
    weekdays = gen_weekdays()
    hours = gen_hours()

    for i in range(17):
        week = Week(number=i+1)
        db.session.add(week)
        db.session.commit()

    for v in weekdays.values():
        day = Day(name=v, active=True)
        db.session.add(day)
        db.session.commit()

    days = Day.query.all()
    for day in days:
        for hr in hours:
            time = Time(start=hr, booked=False, day_id=day.id, day=day)
            day.timeslots.append(time)
            db.session.add(time)
            db.session.commit()
    
    weeks = Week.query.all()
    days = Day.query.all()
    for wk in weeks:
        for day in days:
            day.week_id = week.id
            day.week = week
            wk.days.append(day)
        
    db.session.commit()

    out = [day.serialize_for_day() for day in days]
    return response(res=out, success=True, code=200)
            
        
        
    


# Routes
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("home.html")
    else:
        authenticate()
    

@app.route("/library/weeks/", methods=["GET"])
def get_all_weeks():
    weeks = Week.query.all()

    return response(res=[wk.serialize_for_week() for wk in weeks], success=True, code=200)


@app.route("/library/days/", methods=["GET"])
def get_all_days():
    days = Day.query.all()

    return response(res=[day.serialize_for_day() for day in days], success=True, code=200)





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

    


# Added for testing purposes
@app.route("/library/drop/", methods=["POST"])
def drop_table():
    db.drop_all(bind=None)

    return response(res=[], success=True, code=201)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5500, debug=True)
