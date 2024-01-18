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
import random
import uuid


FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

# + pycharm={"name": "#%%\n"}
# get env var
BASE_URL = os.environ.get('DAS_INSTANCE')
USER = os.environ.get('DAS_USER')
PASSWORD = os.environ.get('DAS_PASSWORD')
EXECUTOR = os.environ.get('REMOTE_EXECUTOR')

# BASE_URL = "https://lab.das.twcc.ai"
# USER = "das"
# PASSWORD = "NchcDAS@2020"
# EXECUTOR = "http://140.110.136.74:30052/wd/hub"

# + pycharm={"name": "#%%\n"}
#now = datetime.datetime.now(pytz.timezone('Asia/Taipei'))
# project_name = now.strftime('notebook-by-selenium-at-%Y%m%d-%H%M%S')
prj_id = uuid.uuid4()
project_name = "selenium-%s" % prj_id


start = time.time()
# -

try:
    instance = instance.Instance(EXECUTOR,wait_timeout=120)
    instance.login(BASE_URL, USER, PASSWORD)
    aa = time.time()
    logging.info("login：%f 秒" % (aa - start))

    proj = instance.project(project_name)

    # think
    bbs = random.expovariate(0.02)
    time.sleep(bbs)
    bb_start = time.time()
    proj.create()
    bb_end = time.time()
    logging.info("create project：%f 秒" % (bb_end - bb_start))

    # think
    bbs = random.expovariate(0.02)
    time.sleep(bbs)
    cc_start = time.time()
    proj.open("overview")
    proj.list()
    cc_end = time.time()
    logging.info("navigate to overview：%f 秒" % (cc_end - cc_start))

    # think
    bbs = random.expovariate(0.02)
    time.sleep(bbs)
    dd_start = time.time()
    proj.open("assets")
    proj.list()
    dd_end = time.time()
    logging.info("navigate to asset：%f 秒" % (dd_end - dd_start))

    # think
    bbs = random.expovariate(0.02)
    time.sleep(bbs)    
    ee_start = time.time()
    proj.open("environments")
    proj.list()
    ee_end = time.time()    
    logging.info("navigate to env：%f 秒" % (ee_end - ee_start))

    #think
    bbs = random.expovariate(0.02)
    time.sleep(bbs)    
    ff_start = time.time()
    proj.delete()
    ff_end = time.time()    
    logging.info("delete project：%f 秒" % (ff_end - ff_start))
    
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


