from flask import Flask, request, render_template
from scripts.today import get_today
from scripts.utils import weekday


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "GET":
        return render_template("home.html")
    else:
        authenticate()
    

def authenticate():
    pass

def generate_days_timeslots():

    curr_day, curr_hr = get_today()
    if curr_day == 1 or curr_day == 7:
        #Generate for whole week
        pass
    
    for k,v in weekday.items():

        if k == curr_day:
            # Create a day object
            # Create the hours from curr_hour
            pass

        elif k > curr_day:
            # Create a day
            # Create the hours from 8am
            pass
    


    




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5500, debug=True)
