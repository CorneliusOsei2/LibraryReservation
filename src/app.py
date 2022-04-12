from flask import Flask, request, render_template
from scripts.today import get_today



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

    




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5500, debug=True)
