# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.1
#   kernelspec:
#     display_name: Python 3.9.0 64-bit
#     name: python3
# ---

# +
# # !pip install selenium
# -



# + pycharm={"name": "#%%\n"}
from DasUITesting import instance
import time
import os
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
MEAN_THINK = os.environ.get('MEAN_THINK')

# BASE_URL = "https://das.edu-cloud.nchc.org.tw/"
# USER = "usera"
# PASSWORD = "keip3Rea"
# EXECUTOR = "http://140.110.136.74:30052/wd/hub"
# MEAN_THINK = "10"


# + pycharm={"name": "#%%\n"}
#now = datetime.datetime.now(pytz.timezone('Asia/Taipei'))
# project_name = now.strftime('notebook-by-selenium-at-%Y%m%d-%H%M%S')
prj_id = uuid.uuid4()
project_name = "selenium-jimmy"


# -

for i in range(1, 10):
    s = pow(2, i)
    logging.info("wait %d sec. for EXECUTOR to ready. " % s)
    time.sleep(s)
    try:
        instance = instance.Instance(EXECUTOR,wait_timeout=120)
        break
    except Exception as e:
        logging.info("connect to DRIVER fail")


# +

login_start = time.time()
instance.login(BASE_URL, USER, PASSWORD)
login_end = time.time()
login_time = login_end - login_start
logging.info("login：%f 秒" % login_time)


# +

proj = instance.project(project_name)

# think
if MEAN_THINK != "":
    mean = float(MEAN_THINK)
    bbs = random.expovariate(1/mean)
    time.sleep(bbs)

all_start = time.time()
proj.list()
all_end = time.time()
all_time = all_end - all_start
logging.info("list all project：%f 秒" % all_time)


# +


# think
if MEAN_THINK != "":
    mean = float(MEAN_THINK)
    bbs = random.expovariate(1/mean)
    time.sleep(bbs)

overview_start = time.time()
proj.open("overview")
overview_end = time.time()
overview_time = overview_end - overview_start
logging.info("navigate to overview：%f 秒" % overview_time)


# +

# think
if MEAN_THINK != "":
    mean = float(MEAN_THINK)
    bbs = random.expovariate(1/mean)
    time.sleep(bbs)

assets_start = time.time()
proj.navigate("assets")
assets_end = time.time()
assets_time = assets_end - assets_start
logging.info("navigate to asset：%f 秒" % assets_time)


# +

# think
if MEAN_THINK != "":
    mean = float(MEAN_THINK)
    bbs = random.expovariate(1/mean)
    time.sleep(bbs)

environments_start = time.time()
proj.navigate("environments")
environments_end = time.time()    
environments_time = environments_end - environments_start
logging.info("navigate to env：%f 秒" % environments_time)



# +

# think
if MEAN_THINK != "":
    mean = float(MEAN_THINK)
    bbs = random.expovariate(1/mean)
    time.sleep(bbs)

job_start = time.time()
proj.navigate("jobs")
job_end = time.time()    
job_time = job_end - job_start
logging.info("navigate to job：%f 秒" % job_time)



# +

#think
if MEAN_THINK != "":
    mean = float(MEAN_THINK)
    bbs = random.expovariate(1/mean)
    time.sleep(bbs)
        
overview2_start = time.time()
proj.navigate("overview")
overview2_end = time.time()    
overview2_time = overview2_end - overview2_start
logging.info("navigate to overview：%f 秒" % overview2_time)


# +

instance.logout()
instance.close()
logging.info("\n  login,  list all, overview,  assets,  environments,   job  , overview \n%f, %f, %f,  %f,  %f,  %f,  %f" % (login_time,all_time, overview_time, assets_time, environments_time,job_time,overview2_time))
# -


