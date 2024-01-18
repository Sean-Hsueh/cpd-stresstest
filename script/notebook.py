# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.1
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


FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

# + pycharm={"name": "#%%\n"}
BASE_URL   = os.environ.get('DAS_INSTANCE')    if os.environ.get('DAS_INSTANCE')    is not None else "https://das.edu-cloud.nchc.org.tw/"
USER       = os.environ.get('DAS_USER')        if os.environ.get('DAS_USER')        is not None else "usera"
PASSWORD   = os.environ.get('DAS_PASSWORD')    if os.environ.get('DAS_PASSWORD')    is not None else "keip3Rea"
EXECUTOR   = os.environ.get('REMOTE_EXECUTOR') if os.environ.get('REMOTE_EXECUTOR') is not None else "http://140.110.136.74:30052/wd/hub"
MEAN_THINK = os.environ.get('MEAN_THINK')      if os.environ.get('MEAN_THINK')      is not None else ""
DURATION   = os.environ.get('DURATION')        if os.environ.get('DURATION')        is not None else "1"

# get env var
# BASE_URL = os.environ.get('DAS_INSTANCE')
# USER = os.environ.get('DAS_USER')
# PASSWORD = os.environ.get('DAS_PASSWORD')
# EXECUTOR = os.environ.get('REMOTE_EXECUTOR')

# BASE_URL = "https://das.edu-cloud.nchc.org.tw/"
# USER = "usera"
# PASSWORD = "keip3Rea"
# EXECUTOR = "http://140.110.136.74:30052/wd/hub"

# + pycharm={"name": "#%%\n"}
now = datetime.datetime.now(pytz.timezone('Asia/Taipei'))
project_name = now.strftime('notebook-by-selenium-at-%Y%m%d-%H%M%S')

start = time.time()
# -

try:
    instance = instance.Instance(EXECUTOR,wait_timeout=120)
    instance.login(BASE_URL, USER, PASSWORD)
    proj = instance.project(project_name)
    proj.create()
    nb = proj.notebook(project_name)
    nb.create("Default Python 3.7 (1 vCPU, 2 GB RAM)")
    nb.run_cell("print(\"hello world\")", "hello world")
    nb.delete(USER)
    proj.delete()
    instance.logout()
    instance.close()
except Exception as e:
    util.print_image_base64_encoding(instance.driver, "/tmp/%s.png" % project_name)
    raise    

# + pycharm={"name": "#%%\n"}


# + pycharm={"name": "#%%\n"}
end = time.time()
logging.info("執行時間：%f 秒" % (end - start))

# -


