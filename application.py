from flask import Flask, render_template, request

app = Flask(__name__)

SPORTS = ["Basketball", "Soccer", "Tennis", "Snooker"]

REGISTRANTS = {}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", sports=SPORTS)
    elif request.method == "POST":
        return render_template("greet.html", name=request.form.get("name", "world"))


@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    if not name:
        return render_template("error.html", message="Missing name")
    sport = request.form.get("sport")
    if not sport:
        return render_template("error.html", message="Missing sport")
    if sport not in SPORTS:
        return render_template("error.html", message="Stop hacking my site")
    REGISTRANTS[name] = sport
    return render_template("registrants.html", registrants = REGISTRANTS)


if __name__ == '__main__':
    app.run()
