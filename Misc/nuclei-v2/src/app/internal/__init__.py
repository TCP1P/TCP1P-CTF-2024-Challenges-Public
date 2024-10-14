from flask import Blueprint, render_template, redirect, url_for, session, flash, request, abort
from functools import wraps
from flask_mysqldb import MySQL
import MySQLdb.cursors
import subprocess

internal_bp = Blueprint('internal', __name__, url_prefix='/internal')

mysql = MySQL()

ALLOWED_IPS = {'127.0.0.1', '::1'}

def ip_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_ip = request.remote_addr
        if client_ip not in ALLOWED_IPS:
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function

@internal_bp.route('/')
@ip_required
def home():
    if 'loggedin' in session:
        return render_template('home/home.html', username=session['username'], title="Home")
    return redirect(url_for('internal.login'))

@internal_bp.route('/login', methods=['GET', 'POST'])
@ip_required
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('internal.profile'))
        else:
            flash("Incorrect username/password!", "danger")

    return render_template('auth/login.html', title="Login")

import os
from flask import render_template, session, redirect, url_for

@internal_bp.route('/profile')
@ip_required
def profile():
    if 'loggedin' in session:
        is_admin = (session['username'] == 'admin')

        if is_admin:
            # Using subprocess.run to execute the command
            result = subprocess.run(['/readflag'], capture_output=True, text=True)
            command_output = result.stdout
        else:
            # Using subprocess.run to echo "No!"
            result = subprocess.run(['echo', 'No!'], capture_output=True, text=True)
            command_output = result.stdout

        return render_template('auth/profile.html', 
                               username=session['username'], 
                               title="Profile",
                               command_output=command_output)
    return redirect(url_for('internal.login'))

@internal_bp.route('/logout')
@ip_required
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('internal.login'))
