import tempfile, subprocess
from base64 import b64encode
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

class Input(BaseModel):
    code: bytes

class Output(BaseModel):
    output: bytes

app = FastAPI()

@app.get("/")
def index():
    return FileResponse("index.html")

@app.post("/api/run")
def run(input: Input):
    code = input.code
    with tempfile.NamedTemporaryFile() as fp:
        fp.write(code)
        fp.seek(0)
        output = subprocess.check_output(["/home/ctf/minivm/build/bin/minivm", fp.name], stderr=subprocess.STDOUT, timeout=300)
    return Output(output=b64encode(output))
