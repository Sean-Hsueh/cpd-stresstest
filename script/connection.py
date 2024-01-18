# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.1
#   kernelspec:
#     display_name: 'Python 3.9.2 64-bit (''selenium-venv'': venv)'
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
# -

# get env var
BASE_URL = os.environ.get('DAS_INSTANCE')
USER = os.environ.get('DAS_USER')
PASSWORD = os.environ.get('DAS_PASSWORD')
EXECUTOR = os.environ.get('REMOTE_EXECUTOR')
#
# BASE_URL = "https://lab.das.twcc.ai"
# USER = "das"
# PASSWORD = "NchcDAS@2020"
# EXECUTOR = "http://140.110.136.74:30052/wd/hub"

# +
now = datetime.datetime.now(pytz.timezone('Asia/Taipei'))
name_suffix = now.strftime('by-selenium-at-%Y%m%d-%H%M%S')
project_name = "connection-%s" % name_suffix


start = time.time()
# -

try:
    instance = instance.Instance(EXECUTOR)
    instance.login(BASE_URL, USER, PASSWORD)
    proj = instance.project(project_name)
    proj.create()
    conn = proj.connection(project_name)
    metadata={
        'database':'dasdata',
        'host':'103.124.72.160',
        'port':'3306',
        'username':'das140read',
        'password':'Nchc@2020'
    }
    conn.create("MySQL", metadata)
    proj.delete()
    instance.logout()
    instance.close()
except Exception as e:
    util.print_image_base64_encoding(instance.driver, "/tmp/%s.png" % project_name)
    raise



# +

end = time.time()
logging.info("執行時間：%f 秒" % (end - start))
# -


