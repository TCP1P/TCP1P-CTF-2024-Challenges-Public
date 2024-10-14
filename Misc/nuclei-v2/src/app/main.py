from flask import Flask, render_template, redirect, url_for, session, flash, request
from internal import internal_bp
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os
import re
import uuid
import subprocess

app = Flask(__name__)

app.secret_key = os.urandom(32)

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)

app.register_blueprint(internal_bp)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            url = request.form['url']
            template = request.form['template']

            if not re.match(r'^[a-zA-Z0-9:/\.]+$', url):
                return render_template('index.html', error='Invalid URL format.')

            filename = str(uuid.uuid4())
            with open(f'/tmp/{filename}.yaml', 'w') as f:
                f.write(template)

            validate_template = subprocess.Popen(
                ['nuclei', '-nc', '-duc', '-t', f'/tmp/{filename}.yaml', '--validate'],
                stderr=subprocess.PIPE
            )
            _, stderr = validate_template.communicate()

            if "Error occurred parsing template" not in stderr.decode('utf-8'):
                process = subprocess.Popen(
                    ['nuclei', '-nc', '-duc', '-t', f'/tmp/{filename}.yaml', '-u', url],
                    stdout=subprocess.PIPE
                )
                stdout, _ = process.communicate()

                os.remove(f'/tmp/{filename}.yaml')

                if stdout.decode('utf-8'):
                    return render_template('index.html', output=stdout.decode('utf-8'))
                else: 
                    return render_template('index.html', output="Not Found")
            else:
                os.remove(f'/tmp/{filename}.yaml')
                return render_template('index.html', output="Error when parsing the template")

        except Exception as e:
            return render_template('index.html', error=f'An unexpected error occurred: {str(e)}')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
