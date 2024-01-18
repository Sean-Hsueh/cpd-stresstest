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

# +
from DasUITesting import instance, util
import time
import os
import datetime
import pytz
import logging

FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

# +
BASE_URL   = os.environ.get('DAS_INSTANCE')    if os.environ.get('DAS_INSTANCE')    is not None else "https://lab.das.twcc.ai"
USER       = os.environ.get('DAS_USER')        if os.environ.get('DAS_USER')        is not None else "das"
PASSWORD   = os.environ.get('DAS_PASSWORD')    if os.environ.get('DAS_PASSWORD')    is not None else "NchcDAS@2020"
EXECUTOR   = os.environ.get('REMOTE_EXECUTOR') if os.environ.get('REMOTE_EXECUTOR') is not None else "http://140.110.136.74:30052/wd/hub"
MEAN_THINK = os.environ.get('MEAN_THINK')      if os.environ.get('MEAN_THINK')      is not None else ""
DURATION   = os.environ.get('DURATION')        if os.environ.get('DURATION')        is not None else "1"

# get env var
# BASE_URL = os.environ.get('DAS_INSTANCE')
# USER = os.environ.get('DAS_USER')
# PASSWORD = os.environ.get('DAS_PASSWORD')
# EXECUTOR = os.environ.get('REMOTE_EXECUTOR')
#
# BASE_URL = "https://lab.das.twcc.ai"
# USER = "das"
# PASSWORD = "NchcDAS@2020"
# EXECUTOR = "http://140.110.136.74:30052/wd/hub"

# +
now = datetime.datetime.now(pytz.timezone('Asia/Taipei'))
project_name = now.strftime('dashboard-by-selenium-at-%Y%m%d-%H%M%S')

start = time.time()
# -

try:
    instance = instance.Instance(EXECUTOR)
    instance.login(BASE_URL, USER, PASSWORD)
    proj = instance.project(project_name)
    proj.create()
    proj.data("/tmp/sample/area_trend_data/area_trend_v2_utf8.csv").upload()
    filename = "area_trend_v2_utf8.csv"
    field1 = "Date"
    field2 = "PM"
    proj.dashboard(filename, field1, field2).create()
    proj.delete()
    instance.logout()
    instance.close()
except Exception as e:
    util.print_image_base64_encoding(instance.driver, "/tmp/%s.png" % project_name)
    raise



end = time.time()
logging.info("執行時間：%f 秒" % (end - start))




