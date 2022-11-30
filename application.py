from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
import json
app = Flask(__name__)
alive = 0
data = {}

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = 'y3monitoring'

mysql = MySQL(app)

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
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email,password,))
        user = cursor.fetchone()

        if user:
            # hashed = user['password']
            # bcrypt.checkpw(password, hashed);
            message = 'Logged in successfully !'
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
            # Hashing the password
            # salt = bcrypt.gensalt()
            # password = bcrypt.hashpw(password.encode('utf-8'), salt)
            cursor.execute('INSERT INTO users VALUES (NULL, %s, %s)', (email, password))
            mysql.connection.commit()
            cursor.close()
            message = 'You have registered!'
            return render_template('logged_in.html', message=message)
    elif request.method == 'POST':
        message = 'Please fill out form!'
    return render_template('signup.html', message = message)

# @app.route('/forgotPassword', methods =['GET', 'POST'])
# def forgotPassword():
#     message = ''
#     if request.method == 'POST' and 'password' in request.form and 'email' in request.form:
#         password = request.form['password']
#         email = request.form['email']
#         cursor = mysql.connection.cursor()
#         cursor.execute('SELECT * FROM users WHERE email = % s', (email,))
#         user = cursor.fetchone()
#         if user:
#             message = 'Account exists!'
#         elif not password or not email:
#             message = 'Please fill out form!'
#         else:
#             cursor.execute('INSERT INTO users VALUES (NULL, %s, %s)', (email, password))
#             mysql.connection.commit()
#             cursor.close()
#             message = 'You have registered!'
#     elif request.method == 'POST':
#         message = 'Please fill out form!'
#     return render_template('message.html', message = message)

@app.route('/addCamera', methods =['GET', 'POST'])
def addCamera():
    message = ''
    if request.method == 'POST' and 'ip' in request.form and 'location' in request.form:
        ip = request.form['ip']
        location = request.form['location']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE ip = % s', (ip,))
        camera = cursor.fetchone()
        if camera:
            message = 'Camera exists!'
        elif not ip or not location:
            message = 'Please fill out form!'
        else:
            cursor.execute('INSERT INTO camera VALUES (NULL, %s, %s)', (ip, location))
            mysql.connection.commit()
            cursor.close()
            message = 'You have added the camera!'
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

@app.route("/logout")
def logout():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()
