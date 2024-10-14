"""
You can use https://github.com/TCP1P/Mobile-POC-Tester to simulate server behaviour
"""
from time import sleep
from type import Status, Queue

from utils import *

MAIN_PACKAGE_NAME ="com.dimas.lookdown"
PROCESS_TIMEOUT = 60

FLAG = "TCP1P{e9dbd49b4cc177d6823054a00ffe943f5fbd8e7750d3bec03564f4684cf6a0b9}"

def callback(package_name: str, q: Queue):
    q.status = Status.RUNNING_PROOF_OF_CONCEPT

    grant_all_permission(MAIN_PACKAGE_NAME)

    out, _ = run_adb(['shell', 'dumpsys', 'package', MAIN_PACKAGE_NAME])
    app_uid = re.search(r"userId=(.+)", out).group(1)

    run_adb(['shell', 'rm', '-rf', f'/data/data/{MAIN_PACKAGE_NAME}/files/'])

    run_adb(['shell', 'mkdir', '-p', f'/data/data/{MAIN_PACKAGE_NAME}/files/'])
    run_adb(['shell', 'chmod', '777', f'/data/data/{MAIN_PACKAGE_NAME}/files/'])

    run_adb(['shell', 'echo', FLAG, '>', f'/data/data/{MAIN_PACKAGE_NAME}/files/flag.txt'])
    run_adb(['shell', 'chmod', '777', f'/data/data/{MAIN_PACKAGE_NAME}/files/flag.txt'])

    run_adb(['shell', 'chown', '-R', f'{app_uid}:{app_uid}', f'/data/data/{MAIN_PACKAGE_NAME}/files'])

    start_app(package_name)

    sleep(15)

    stop_app(package_name)

    run_adb(['shell', 'rm', '/sdcard/Download/*'])

    sleep(2.5)
