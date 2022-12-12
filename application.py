from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
import json
import bcrypt
from flask_sqlalchemy import SQLAlchemy
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import os
import pathlib

app = Flask(__name__)

alive = 0
data = {}

#db = SQLAlchemy(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = 'y3monitoring'

mysql = MySQL(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:NDTJ9876!@localhost/y3monitoring"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://localhost"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#GOOGLE_CLIENT_ID = "10191242350-p4had4h1o1s7jq78keq9psl6fnqjfitd.apps.googleusercontent.com"

#client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

# flow = Flow.from_client_secrets_file(
#     client_secrets_file=client_secrets_file,
#     scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
#     redirect_uri="https://127.0.0.1:5000/callback"
# )

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        return render_template("greet.html")

# @app.route("/googlelogin")
# def googlelogin():
#     authorization_url, state = flow.authorization_url()
#     session["state"] = state
#     return redirect(authorization_url)

def login_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401) # Authorization required
        else:
            return function()
    return wrapper

@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/secure_area")

@app.route("/secure_area")
@login_required
def secure_area():
    my_db.add_user_and_login(session["name"], session["google_id"])
    return render_template("index.html", user_id=session["google_id"], online_users=my_db.get_all_logged_in_users())

@app.route("/login", methods=["GET","POST"])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()

        if user:
            realPassword = user[2]

            userBytes = password.encode('ascii')

            check = bcrypt.checkpw(userBytes, realPassword.encode('ascii'))
            print(check)

            return render_template('logged_in.html')
        else:
            message = 'Incorrect email / password !'
    return render_template('login.html', message = message)


@app.route('/register', methods =['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'password' in request.form and 'email' in request.form:
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = % s', (email,))
        user = cursor.fetchone()
        if user:
            message = 'Account exists!'
            return render_template('signup.html', message=message)
        elif not password or not email:
            message = 'Please fill out form!'
            return render_template('signup.html', message=message)
        else:
            bytes = password.encode('ascii')

            salt = bcrypt.gensalt()

            hash = bcrypt.hashpw(bytes, salt)
            cursor.execute('INSERT INTO users VALUES (NULL, %s, %s)', (email, hash))
            mysql.connection.commit()
            cursor.close()
            message = 'You have registered!'
            return render_template('logged_in.html', message=message)
    elif request.method == 'POST':
        message = 'Please fill out form!'
    return render_template('signup.html', message = message)

@app.route('/addHomePod', methods =['GET', 'POST'])
def addHomePod():
    message = ''
    if request.method == 'POST' and 'ip' in request.form and 'location' in request.form:
        ip = request.form['ip']
        location = request.form['location']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM camera WHERE ip = % s', (ip,))
        sensors = cursor.fetchone()
        if sensors:
            message = 'HomePod already Added!'
        elif not ip or not location:
            message = 'Please fill out form!'
        else:
            cursor.execute('INSERT INTO camera VALUES (NULL, %s, %s)', (ip, location))
            cursor.execute('INSERT INTO motion_sensor VALUES (NULL, %s, %s)', (ip, location))
            cursor.execute('INSERT INTO sound_sensor VALUES (NULL, %s, %s)', (ip, location))
            mysql.connection.commit()
            cursor.close()
            message = 'You have added the Homepod!'
            return render_template('logged_in.html', message=message)
    elif request.method == 'POST':
        message = 'Please fill out form!'
    return render_template('index.html', message = message)

@app.route("/keep_alive")
def keep_alive():
    global alive, data
    alive += 1
    keep_alive_count = str(alive)
    data['keep_alive'] = keep_alive_count
    parsed_json = json.dumps(data)
    print(parsed_json)
    return str(parsed_json)
@app.route("/live_video")
def live_video():
    global alive, data
    alive += 1
    live_video_count = str(alive)
    data['live_video'] = live_video_count
    parsed_json = json.dumps(data)
    print(parsed_json)
    return str(parsed_json)
@app.route("/logout")
def logout():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()
