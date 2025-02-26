# Assumptions
# The database for storing credentials is fully fledged out and secure
# Sessions are being properly handled, CSRF protection is in place, etc.

from flask import Flask, render_template, session, redirect, url_for, request
from flask_session import Session
import datetime

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem' 
app.config['SESSION_PERMANENT'] = False  
app.config['SESSION_USE_SIGNER'] = True  
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'

Session(app)

mockDB = {
    'john': 'password123',  
    'alice': 'securePass',  
    'bob': 'myPassword',    
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in mockDB:
            return render_template('signup.html', error="Username already in use!")
        else:
            mockDB[username] = password
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in mockDB and mockDB[username] == password:
            session['user'] = username  
            return redirect(url_for('home'))  
        else:
            return render_template('login.html', error="Invalid username or password.") 
    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user', None) 
    return redirect(url_for('home'))

@app.route('/health-check', methods=['GET', 'POST'])
def tools():
    if 'user' in session:
        if request.method == 'POST':
            arg = requests.form.get('arg')
            check = "ping" + arg + "127.0.0.1:19032"
            result = subprocess.run(check, shell=True, text=True, capture_output=True, check=True)
            output = result.stdout
        elif request.method == 'GET':
            return render_template('health.html')
        else:
            resp = make_response("Incompatible Method!", 405)
            return resp
    return redirect(url_for('login'))  

if __name__ == '__main__':
    app.run(debug=True)
