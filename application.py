from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
app.config['MYSQL_DB'] = 'sd3a_registrants_23'

app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")
app.config["MAIL_PASSWORD"] = os.getenv("GMAIL_APP_PASSWORD")
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")

mail = Mail(app)


mysql = MySQL(app)

SPORTS = ["Basketball", "Soccer", "Tennis", "Snooker"]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", sports=SPORTS)
    elif request.method == "POST":
        return render_template("greet.html", name=request.form.get("name", "world"))


@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    if not email:
        return render_template("error.html", message="Missing email")
    sport = request.form.get("sport")
    if not sport:
        return render_template("error.html", message="Missing sport")
    if sport not in SPORTS:
        return render_template("error.html", message="Stop hacking my site")
    cursor = mysql.connection.cursor()
    cursor.execute('''insert into registrants(name, sport) values (%s, %s)''', (email, sport))
    mysql.connection.commit()
    cursor.close()
    message = Message("You are registered", recipients=[email])
    mail.send(message)
    return redirect("/registrants")


@app.route("/registrants")
def registrants():
    cur = mysql.connection.cursor()
    cur.execute("select * from registrants")
    registrants = cur.fetchall()
    return render_template("registrants.html", registrants=registrants)


if __name__ == '__main__':
    app.run()
