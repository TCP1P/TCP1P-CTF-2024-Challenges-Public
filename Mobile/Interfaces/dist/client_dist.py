from time import sleep
from type import Status, Queue

from utils import *

import uuid
import re

MAIN_PACKAGE_NAME ="app.aimar.id.interfaces"
PROCESS_TIMEOUT = 5*60

FLAG = 'REDACTED'

def callback(package_name: str, q: Queue):
    q.status = Status.RUNNING_PROOF_OF_CONCEPT

    out, _ = run_adb(['shell', 'dumpsys', 'package', MAIN_PACKAGE_NAME])
    app_uid = re.search(r"userId=(.+)", out).group(1)

    run_adb(['shell', 'rm', '-rf', f'/data/data/{MAIN_PACKAGE_NAME}/files/*'])
    run_adb(['shell', 'mkdir', '-p', f'/data/data/{MAIN_PACKAGE_NAME}/files/'])
    run_adb(['shell', 'echo', FLAG, '>', f'/data/data/{MAIN_PACKAGE_NAME}/files/flag.txt'])
    run_adb(['push', f'challenges/{CHALLENGE_NAME}/pwds.yml', f'/data/data/{MAIN_PACKAGE_NAME}/files/pwds.yml'])
    run_adb(['shell', 'chown', '-R', f'{app_uid}:{app_uid}', f'/data/data/{MAIN_PACKAGE_NAME}/files'])  

    start_app(package_name)

    sleep(10)