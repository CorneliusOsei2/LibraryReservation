from flask import Flask, request, render_template


app = Flask(__name__)

def populate_day():
    pass

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5500, debug=True)
