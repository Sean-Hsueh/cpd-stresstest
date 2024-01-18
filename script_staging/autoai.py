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
from DasUITesting import instance, project, util
import time
import os
import datetime
import pytz
import logging
import requests, json


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

def get_token(user, password):
    header = {
        "cache-control": "no-cache",
        "Content-Type": "application/json",
    }


    post_data = {
        "username": user,
        "password": password,
    }

    response = requests.post(
        "%s/icp4d-api/v1/authorize" % BASE_URL.strip("/"),
        json=post_data,
        headers=header,
    )

    res = json.loads(response.text)
    return res["token"]        


def verify_deployment(token, endpoint, field, value):

    header = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
    }

    payload_scoring = {
        "input_data": [
            {
                "fields": field,
                "values": [value],
            }
        ]
    }

    response_scoring = requests.post(
        endpoint,
        json=payload_scoring,
        headers=header,
    )

    logging.info(json.loads(response_scoring.text))


now = datetime.datetime.now(pytz.timezone('Asia/Taipei'))
name_suffix = now.strftime('by-selenium-at-%Y%m%d-%H%M%S')
project_name = "autoai-%s" % name_suffix
autoai_name = "autoai-%s" % name_suffix
space_name="space-%s" % name_suffix
deployment_name = "deployment-%s" % name_suffix

start = time.time()

try:
    instance = instance.Instance(EXECUTOR)
    instance.login(BASE_URL, USER, PASSWORD)
    deployment = instance.deployment()
    project = instance.project(project_name)
    project.create()

    logging.info("upload test data")
    project.data("/tmp/sample/go_sales_data/GoSales.csv").upload()
    space = deployment.space(space_name)
    space.create()
    autoai = project.autoai(autoai_name)

    logging.info("run autoai experiment")
    autoai.run_experiment("GoSales.csv", "IS_TENT")
    
    logging.info("save optimized model")
    autoai.saveModel()
    logging.info("promote optimized model")
    autoai.promoteModel(space_name)

    logging.info("deploy to space")
    space.deploy(deployment_name)

    logging.info("verify deployed model")
    endpoint = space.get_endpoint(deployment_name)
    token = get_token(USER,PASSWORD)
    field = ["GENDER","AGE","MARITAL_STATUS","PROFESSION","PRODUCT_LINE","PURCHASE_AMOUNT"]
    value = ["M", 27, "Single", "Professional", "Camping Equipment", 144.78]
    verify_deployment(token, endpoint, field, value)
    
    logging.info("tear down created resource")
    space.undeploy(deployment_name)
    space.delete()
    project.delete()
    instance.logout()
    instance.close()
except Exception as e:
    util.print_image_base64_encoding(instance.driver, "/tmp/%s.png" % project_name)
    raise    

# +

end = time.time()
logging.info("執行時間：%f 秒" % (end - start))
# -


