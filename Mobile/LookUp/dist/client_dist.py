"""
You can use https://github.com/TCP1P/Mobile-POC-Tester to simulate server behaviour
"""
from time import sleep
from type import Status, Queue

from utils import *

import uuid

MAIN_PACKAGE_NAME ="com.dimas.lookup"
PROCESS_TIMEOUT = 5*60

FLAG = "fake{flag}"

def callback(package_name: str, q: Queue):
    q.status = Status.RUNNING_PROOF_OF_CONCEPT

    flag = "flag_" + str(uuid.uuid4()) + ".txt"
    out, _ = run_adb(['shell', 'dumpsys', 'package', MAIN_PACKAGE_NAME])
    app_uid = re.search(r"userId=(.+)", out).group(1)

    run_adb(['shell', 'rm', '-rf', f'/data/data/{MAIN_PACKAGE_NAME}/files/'])

    run_adb(['shell', 'mkdir', '-p', f'/data/data/{MAIN_PACKAGE_NAME}/files/'])
    run_adb(['shell', 'chmod', '777', f'/data/data/{MAIN_PACKAGE_NAME}/files/'])

    run_adb(['shell', 'echo', FLAG, '>', f'/data/data/{MAIN_PACKAGE_NAME}/files/{flag}'])
    run_adb(['shell', 'chmod', '777', f'/data/data/{MAIN_PACKAGE_NAME}/files/{flag}'])

    run_adb(['shell', 'chown', '-R', f'{app_uid}:{app_uid}', f'/data/data/{MAIN_PACKAGE_NAME}/files'])

    start_app(package_name)

    sleep(5)

    stop_app(package_name)

    sleep(2.5)
