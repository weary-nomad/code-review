from flask import Flask, render_template, session, redirect, url_for, request, subprocess, make_response
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

# Assume this is not a cleartext DB and is fully fledged out.
mockDB = {
    'john@example.com': 'password123',  
    'alice@example.com': 'securePass',  
    'bob@example.com': 'myPassword',    
}

@app.route('/')
def home():
    return render_template('home.html')

# Assume 2FA is setup and enforced, and the email is verified before the account becomes active. Also assume protection is in place at the network level for DoS.
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email in mockDB:
            return render_template('signup.html', error="Email already in use!")
        else:
            mockDB[email] = password
            return redirect(url_for('login'))
    return render_template('signup.html')

# Assume 2FA from signup is required to login and protection is in place at the network level for DoS. Sessions regenerate once someone logs back in, so old session cookies are nullified.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email in mockDB and mockDB[email] == password:
            session['user'] = email
            app.session_interface.regenerate(session)
            return redirect(url_for('home'))  
        else:
            return render_template('login.html', error="Invalid email or password.") 
    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user', None) 
    return redirect(url_for('home'))

@app.route('/health-check', methods=['GET', 'POST'])
def tools():
    if 'user' in session:
        if request.method == 'POST':
            arg = request.form.get('arg')
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
