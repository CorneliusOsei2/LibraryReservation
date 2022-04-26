from crypt import methods
from flask import Flask, request, render_template
from scripts.helpers import gen_weekdays, gen_hours, get_today
from scripts.utils import response
from db import db,Week, Day, Time
import requests, json
from flask_cors import CORS

# Initialize Flask
app = Flask(__name__)
CORS(app)

# DB config
db_filename = "library.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()


# Helper Functions and Generators

@app.route("/", methods=["GET"])
def greet():
    return "HI", 200
    
@app.route("/library/gen/", methods=["GET"])
def gen_all_days_hours():
    '''
    Generate 17 weeks, 7 days for each week, and timeslots from 8am to 10pm
    for each day
    '''
    weekdays = gen_weekdays()
    hours = gen_hours()
    
    # Generate weeks
    for i in range(17):
        week = Week(number = i+1, active = True)
        db.session.add(week)
        db.session.commit()

    # Generate days
    weeks = Week.query.all()
    for wk in weeks:
        for dy in weekdays.values():
            day = Day(name=dy, active=True, week_id = wk.id, week=wk)
            wk.days.append(day)
            db.session.add(day)
            db.session.commit()


    # Generate hours for each day
    days = Day.query.all()
    for day in days:
        for hr in hours:
            time = Time(start=hr, booked=False, day_id=day.id, day=day)
            day.timeslots.append(time)
            db.session.add(time)
            db.session.commit()
    

    out = [wk.serialize_for_week() for wk in weeks]
    return response(res=out, success=True, code=200)
            

def check_day_active(day):
    '''
    Check if day has active/free timeslots or can be booked
    '''
    timeslots = day.timeslots
    for time in timeslots:
        if time.active:
            return True
    
    return False

        
# Routes
@app.route("/", methods=["GET", "POST"])
def home():
    '''
    Homepage
    '''
    if request.method == "GET":
        return render_template("home.html")
    else:
        authenticate()
    

@app.route("/library/weeks/", methods=["GET"])
def get_all_weeks():
    '''
    Get all weeks: active and inactive
    '''
    weeks = Week.query.all()
    return response(
        res={"weeks": [wk.serialize_for_week() for wk in weeks]}, success=True, code=200)

@app.route("/library/weeks/active/", methods=["GET"])
def get_active_week_days(week):
    '''
    Get only days that can be booked/have free timeslots
    '''
    days = week.days
    res = []

    for day in days:
        if day.active:
            res.append(day)
    
    return response(res=res, success=True, code=200)


@app.route("/library/days/", methods=["GET"])
def get_all_days():
    '''
    Get all days: active and inactive
    '''
    days = Day.query.all()

    return response(res={"days":[day.serialize_for_day() for day in days]}, success=True, code=200)

@app.route("/library/<int:week_id>/<int:day_id>/", methods=["GET"])
def get_active_day_times(week_id, day_id):
    '''
    Get only active/free timeslots
    '''
    day = Day.query.filter_by(id=day_id).first()
    timeslots = day.timeslots
    res = []

    for time in timeslots:
        if not time.booked:
            res.append(time.serialize_for_day())
    
    return response(res={"timeslots": res}, success=True, code=200)


@app.route("/library/<int:week_id>/<int:day_id>/<int:time_id>/", methods=["GET", "POST"])
def book_time(week_id, day_id, time_id):
    
    # POST
    timeslot = Time.query.filter_by(id= time_id).first()
    if not timeslot: return response(res={"error": "No such timeslot"}, success=False, code=400)

    if request.method == "POST":
        body = json.loads(request.data)
        timeslot.booked, timeslot.description = body.get("booked"), body.get("description", "")
        return response(res=timeslot.serialize_for_time(), success=True, code=201)
    
    #GET
    return response(res=timeslot.serialize_for_time(), success=True, code=200)



def authenticate():
    pass




# Added for testing purposes
@app.route("/library/drop/", methods=["POST"])
def drop_table():
    db.drop_all(bind=None)

    return response(res=[], success=True, code=201)



# @app.route("/library/weeks/", methods=["DELETE"])
# def delete_all_weeks():
#     weeks = Week.delete()
#     db.session.commit()

#     return response(res=[wk.serialize_for_week() for wk in weeks], success=True, code=200)


# @app.route("/library/days/", methods=["DELETE"])
# def delete_all_days():
#     db.session.delete(Day)
#     db.session.commit()
#     days = Day.query.all()
#     return response(res=[day.serialize_for_day() for day in days], success=True, code=200)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500)