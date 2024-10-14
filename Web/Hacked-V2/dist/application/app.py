from flask import Flask, request, Response, jsonify, redirect, url_for, render_template_string, abort
from util import is_from_localhost, proxy_req, url_decode
from flask import request, abort
import random, os

app = Flask(__name__)

# I BLACKLIST EVERY CHAR :)

blacklist = ["debug", "args", "headers", "cookies", "environ", "values", "query",
    "data", "form", "os", "system", "popen", "subprocess", "globals", "locals",
    "self", "lipsum", "cycler", "joiner", "namespace", "init", "join", "decode",
    "module", "config", "builtins", "import", "application", "getitem", "read",
    "getitem", "mro", "endwith", " ", "'", '"', "_", "{{", "}}", "[", "]", "\\", "x"]

def check_forbidden_input(func):
    def wrapper(*args, **kwargs):
        for header, value in request.headers.items():
            decoded_value = url_decode(value)
            for forbidden_str in blacklist:
                if forbidden_str in decoded_value:
                    abort(400, f"Forbidden: '{forbidden_str}' not allowed in {header} header")

        for key, value in request.args.items():
            decoded_key = url_decode(key)
            decoded_value = url_decode(value)
            for forbidden_str in blacklist:
                if forbidden_str in decoded_key or forbidden_str in decoded_value:
                    abort(400, f"Forbidden: '{forbidden_str}' not allowed in URL parameter '{key}'")

        try:
            if request.is_json:
                json_data = request.get_json()
                if json_data:
                    for key, value in json_data.items():
                        decoded_key = url_decode(key)
                        decoded_value = url_decode(value)
                        for forbidden_str in blacklist:
                            if forbidden_str in decoded_key or forbidden_str in decoded_value:
                                abort(400, f"Forbidden: '{forbidden_str}' not allowed in JSON request body key '{key}'")
            else:
                body = request.get_data(as_text=True)
                decoded_body = url_decode(body)
                for forbidden_str in blacklist:
                    if forbidden_str in decoded_body:
                        abort(400, f"Forbidden: '{forbidden_str}' not allowed in request body")
        except Exception as e:
            pass

        return func(*args, **kwargs)
    return wrapper

@app.route('/', methods=['GET'])
@check_forbidden_input
def proxy():
    url = request.args.get('url')

    list_endpoints = [
        '/about/',
        '/portfolio/',
    ]

    if not url:
        endpoint = random.choice(list_endpoints)
        # Construct the URL with query parameter
        return redirect(f'/?url={endpoint}')
    
    target_url = "http://daffa.info" + url

    if target_url.startswith("http://daffa.info") and any(target_url.endswith(endpoint) for endpoint in list_endpoints):
        response, headers = proxy_req(target_url)

        return Response(response.content, response.status_code, headers.items())
    else:
        abort(403)

@app.route('/secret', methods=['GET', 'POST'])
@is_from_localhost
def dev_secret():
    admin = "daffainfo"
    css_url = url_for('static', filename='css/main.css')

    if request.args.get('admin') is not None:
        admin = request.args.get('admin')
        print(admin)

    if not admin:
        abort(403)

    template = '''<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Admin Notes Preview</title>
            <link rel="stylesheet" href="{}">
        </head>
        <body>
            <h1>NOTES!! ONLY ADMIN CAN ACCESS THIS AREA!</h1>
            <form action="" method="GET">
                <label for="admin">Admin:</label>
                <input type="text" id="admin" name="admin" required>
                <br>
                <input type="submit" value="Preview!">
            </form>
            <p>Admin: {}<span id="adminName"></span></p>
        </body>
        </html>'''.format(css_url, admin)
    return render_template_string(template)

app.run(host='0.0.0.0', port=1337)