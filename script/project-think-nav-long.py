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
from DasUITesting import instance
import time
import os
import logging
import random



FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.WARN, format=FORMAT)

# + pycharm={"name": "#%%\n"}
# get env var
BASE_URL   = os.environ.get('DAS_INSTANCE')    if os.environ.get('DAS_INSTANCE')    is not None else "https://das.edu-cloud.nchc.org.tw/"
USER       = os.environ.get('DAS_USER')        if os.environ.get('DAS_USER')        is not None else "usera"
PASSWORD   = os.environ.get('DAS_PASSWORD')    if os.environ.get('DAS_PASSWORD')    is not None else "keip3Rea"
EXECUTOR   = os.environ.get('REMOTE_EXECUTOR') if os.environ.get('REMOTE_EXECUTOR') is not None else "http://140.110.136.74:30052/wd/hub"
MEAN_THINK = os.environ.get('MEAN_THINK')      if os.environ.get('MEAN_THINK')      is not None else ""
DURATION   = os.environ.get('DURATION')        if os.environ.get('DURATION')        is not None else "1"

# + pycharm={"name": "#%%\n"}
project_name = "selenium-jimmy"


# -

def all(proj):
    # think
    if MEAN_THINK != "":
        mean = float(MEAN_THINK)
        bbs = random.expovariate(1/mean)
        time.sleep(bbs)

    all_start = time.time()
    proj.list()
    all_end = time.time()
    all_time = all_end - all_start
    return all_time



def overview(proj):
    if MEAN_THINK != "":
        mean = float(MEAN_THINK)
        bbs = random.expovariate(1/mean)
        time.sleep(bbs)

    overview_start = time.time()
    proj.open("overview")
    overview_end = time.time()
    overview_time = overview_end - overview_start
    return overview_time


def asset(proj):
    # think
    if MEAN_THINK != "":
        mean = float(MEAN_THINK)
        bbs = random.expovariate(1/mean)
        time.sleep(bbs)

    assets_start = time.time()
    proj.navigate("assets")
    assets_end = time.time()
    assets_time = assets_end - assets_start
    return assets_time


def environment(proj):
    if MEAN_THINK != "":
        mean = float(MEAN_THINK)
        bbs = random.expovariate(1/mean)
        time.sleep(bbs)

    environments_start = time.time()
    proj.navigate("environments")
    environments_end = time.time()    
    environments_time = environments_end - environments_start
    return environments_time


def job(proj):
    if MEAN_THINK != "":
        mean = float(MEAN_THINK)
        bbs = random.expovariate(1/mean)
        time.sleep(bbs)

    job_start = time.time()
    proj.navigate("jobs")
    job_end = time.time()    
    job_time = job_end - job_start    
    return job_time


def overview2(proj):
    if MEAN_THINK != "":
        mean = float(MEAN_THINK)
        bbs = random.expovariate(1/mean)
        time.sleep(bbs)
            
    overview2_start = time.time()
    proj.navigate("overview")
    overview2_end = time.time()    
    overview2_time = overview2_end - overview2_start    
    return overview2_time


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
bbs = random.expovariate(0.2)
time.sleep(bbs)

login_start = time.time()
instance.login(BASE_URL, USER, PASSWORD)
login_end = time.time()
login_time = login_end - login_start


proj = instance.project(project_name)

# +
timeout = time.time() + 60* int(DURATION)   # 1 minutes from now


while True:
    if time.time() > timeout:
        break

    all_time = all(proj)
    overview_time = overview(proj)
    assets_time = asset(proj)
    environments_time = environment(proj)
    job_time = job(proj)
    overview2_time = overview2(proj)

    print(">, %f, %f, %f,  %f,  %f,  %f,  %f" % (login_time,all_time, overview_time, assets_time, environments_time,job_time,overview2_time),flush=True)


# -

instance.logout()
instance.close()


