# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.4
#   kernelspec:
#     display_name: 'Python 3.9.0 64-bit (''selenium-venv'': venv)'
#     name: python3
# ---

# !pip install selenium


# + pycharm={"name": "#%%\n"}
from DasUITesting import instance, util
import time
import os
import datetime
import pytz
import logging
import uuid


FORMAT = "%(asctime)s %(levelname)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)

# + pycharm={"name": "#%%\n"}
# get env var
BASE_URL = os.environ.get("DAS_INSTANCE")
USER = os.environ.get("DAS_USER")
PASSWORD = os.environ.get("DAS_PASSWORD")
EXECUTOR = os.environ.get("REMOTE_EXECUTOR")

print('>>> BASE_URL: %s, %s, %s, %s' %(BASE_URL, USER, PASSWORD, EXECUTOR))

# + pycharm={"name": "#%%\n"}
now = datetime.datetime.now(pytz.timezone("Asia/Taipei"))
prj_id = uuid.uuid1()
project_name = "notebook-selenium-%s" % prj_id

start = time.time()

# + tags=[]
try:
    print('starting')
    instance = instance.Instance(EXECUTOR, wait_timeout=120)
    print('login')
    instance.login(BASE_URL, USER, PASSWORD)
    print('login done')
    proj = instance.project(project_name)
    proj.create()
    proj.open("overview")
    proj.list()
    proj.open("assets")
    proj.list()
    proj.open("environments")
    proj.list()
    proj.delete()
    instance.logout()
    instance.close()
except Exception as e:
    print('closing')
    util.print_image_base64_encoding(instance.driver, "/tmp/%s.png" % project_name)
    raise

# + pycharm={"name": "#%%\n"}


# + pycharm={"name": "#%%\n"}
end = time.time()
logging.info("執行時間：%f 秒" % (end - start))

# -
