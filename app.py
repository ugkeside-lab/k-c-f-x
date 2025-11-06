from flask import Flask, render_template, request, redirect, url_for, session
from strategy import analyze_gold
from scheduler import start_scheduler
import json, os, datetime

app = Flask(__name__)
app.secret_key = "kcfx_secret_key"

# Load basic config
with open("config.json") as f:
    config = json.load(f)

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = config.get('users', {})
        if username in users:
            return "User already exists!"
        users[username] = password
        config['users'] = users
        with open("config.json", "w") as f:
            json.dump(config, f)
        return redirect(url_for('home'))
    return render_template('signup.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    users = config.get('users', {})
    if username in users and users[username] == password:
        session['user'] = username
        return redirect(url_for('dashboard'))
    return "Invalid credentials!"

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('home'))
    with open("signals.json", "r") as f:
        signals = json.load(f)
    return render_template('dashboard.html', signals=signals)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    start_scheduler()  # Starts auto hourly analysis
    app.run(host='0.0.0.0', port=5000)
