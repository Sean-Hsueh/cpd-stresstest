# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import time
import random
import logging
import os


FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

# +
# get env var
BASE_URL = os.environ.get('DAS_INSTANCE')
USER = os.environ.get('DAS_USER')
PASSWORD = os.environ.get('DAS_PASSWORD')
EXECUTOR = os.environ.get('REMOTE_EXECUTOR')


# EXECUTOR = "http://140.110.136.74:30052/wd/hub"
# BASE_URL = ""
# USER=""
# PASSWORD=""

# +
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")


# connect to remote driver
driver = webdriver.Remote(
    command_executor=EXECUTOR,
    desired_capabilities=DesiredCapabilities.CHROME,
    options=options,
)

wait = WebDriverWait(driver, 60)

# +

driver.get(BASE_URL)
# -

wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, '//a[text()="htpasswd_provider"]')
    )
).click()






# +
login_start = time.time()

driver.find_element(By.ID, "inputUsername").send_keys(USER)
driver.find_element(By.ID, "inputPassword").send_keys(PASSWORD)
wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, '//button[text()="Log in"]')
    )
).click()

# wait until Control Plane button show up
wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, '//button[text()="Control Plane"]')
    )
).click()

login_end = time.time()
login_time = login_end - login_start

logging.info("login：%f 秒" % (login_time))

# -







# +

# Open default project
project_start = time.time()

wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, '//a[text()="Projects"]')
    )
).click()


wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, '//a[text()="default"]')
    )
).click()

# wait until Active message is showup
wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, '(//span[text()="Active"])[2]')
    )
).click()

project_end = time.time()
project_time = project_end - project_start
logging.info("open project：%f 秒" % (project_time))




# +




# +

# Navigate to Detail Tab
detail_start = time.time()

wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, '//a[text()="Details"]')
    )
).click()

# wait until Active message is showup
wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, '(//span[text()="Active"])[2]')
    )
).click()
detail_end = time.time()

detail_time = detail_end - detail_start
logging.info("detail tab：%f 秒" % (detail_time))


# +

# Navigate to Workloads Tab
workload_start = time.time()

wait.until(
    EC.visibility_of_element_located(
        (By.XPATH,  '//a[text()="Workloads"]')
    )
).click()


# wait until Wuick Starts block is showup
wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, '//h1[text()="Quick Starts"]')
    )
).click()
workload_end = time.time()

workload_time = workload_end - workload_start
logging.info("workload tab：%f 秒" % (workload_time))



# +

# Navigate to Overview Tab
overview_start = time.time()

wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, '(//a[text()="Overview"])[2]')
    )
).click()

# wait until Active message is showup
wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, '(//span[text()="Active"])[2]')
    )
).click()
overview_end = time.time()

overview_time = overview_end - overview_start
logging.info("overview tab：%f 秒" % (overview_time))

# +

# logout
wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, '//span[text()="%s"]/../../..' % USER)
    )
).click()

driver.find_element(By.XPATH, '//button[text()="Log out"]').click()


# -



driver.close()

logging.info("\n  login,  project,  detail,  workload,  overview \n%f, %f, %f, %f, %f " % (login_time, project_time, detail_time, workload_time, overview_time))











