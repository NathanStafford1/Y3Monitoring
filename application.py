from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from flask_session import Session
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = 'y3monitoring'

app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")
app.config["MAIL_PASSWORD"] = os.getenv("GMAIL_APP_PASSWORD")
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")

mail = Mail(app)

mysql = MySQL(app)
Session(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        return render_template("greet.html")

@app.route("/login", methods=["GET","POST"])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password,))
        user = cursor.fetchone()
        if user:
            password_rs = user['password']
            print(password_rs)
            if check_password_hash(password_rs, password):
                message = 'Logged in successfully !'
                return render_template('error.html', message=message)
        else:
            message = 'Incorrect email / password !'
    return render_template('error.html', message = message)

@app.route('/register', methods =['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'password' in request.form and 'email' in request.form:
        password = request.form['password']
        _hashed_password = generate_password_hash(password)
        email = request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = % s', (email,))
        user = cursor.fetchone()
        if user:
            message = 'Account exists!'
        elif not password or not email:
            message = 'Please fill out form!'
        else:
            cursor.execute('INSERT INTO users VALUES (NULL, %s, %s)', (email, password))
            mysql.connection.commit()
            cursor.close()
            message = 'You have registered!'
    elif request.method == 'POST':
        message = 'Please fill out form!'
    return render_template('error.html', message = message)

@app.route("/logout")
def logout():
    # session["email"] = None
    return redirect("/")

if __name__ == '__main__':
    app.run()
