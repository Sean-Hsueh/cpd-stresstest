from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


import time, logging

from . import data, notebook, dashboard, connection, refinery, autoai
from .. import util

OVERVIEW = "overview"
ASSETS = "assets"
ENVIRONMENTS = "environments"
JOBS = "jobs"
TAB_ID = {
    OVERVIEW: "projectDetailsOverviewContent",
    ASSETS: "projectDetailsAssets",
    ENVIRONMENTS: "projectDetailsEnvironments",
    JOBS: "projectDetailsJobs",
}


class Project:
    def __init__(self, project_name, instance):
        self.name = project_name
        self.instance = instance
        self.wait = instance.wait
        self.BASE_URL = instance.BASE_URL
        self.driver = instance.driver

    def list(self):
        PROJECT_URL = "%s/zen/#/projectList" % self.BASE_URL.strip("/")
        self.driver.get(PROJECT_URL)

        # wait for Link to target project is visible + clickable
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//td[contains(@id, '%s')]/a" % self.name)
            )
        )

    def open(self, tab_id=OVERVIEW):
        # open project
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//td[contains(@id, '%s')]/a" % self.name)
            )
        ).click()

        # open overview tab by default
        self.driver.find_element(By.ID, TAB_ID[OVERVIEW]).click()
        # self.driver.find_element(By.XPATH, "//a[@id='%s']" % TAB_ID[OVERVIEW]).click()

        # self.wait.until(
        #     EC.visibility_of_element_located((By.XPATH, "//div[text()='Admin']"))
        # )
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.dap-action-bar_add-container a.dap-action-bar_button[data-action='launch-export']"))
        )

        # go to different tab by parameter
        # go to desired tab
        # self.driver.find_element(By.XPATH, "//a[@id='%s']" % TAB_ID[tab_id]).click()
        self.driver.find_element(By.ID, TAB_ID[tab_id]).click()

    def search_and_open(self, asset_name):
        print('navigate to assets tab')
        self.navigate(ASSETS)
        
       
        util.debug(self.instance.driver, 'searching for asset: %s' % asset_name)
        search_box = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input.bx--search-input[type='text'][tabindex='0']"))
        )
        util.debug(self.instance.driver, 'found')
        search_box.click()
        util.debug(self.instance.driver, 'clicked')
        search_box.clear()
        util.debug(self.instance.driver, 'cleared')
        search_box.send_keys(asset_name)
        util.debug(self.instance.driver, 'inputed the asset name %s' % asset_name)

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//a[@title='Workshop (version 1.0)']")
            )
        ).click()
        util.debug(self.instance.driver, 'found the asset and clicked')

        
        pass

    def navigate(self, tab_id=OVERVIEW):
        print('navigating')
        self.driver.find_element(By.ID, TAB_ID[tab_id]).click()
        print('navigated')

        if tab_id == JOBS:
            self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//span[text()="You don\'t have any Jobs yet."]')
                )
            )

        if tab_id == ENVIRONMENTS:
            self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//span[text()='No environments are currently active.']")
                )
            )

        if tab_id == OVERVIEW:
            self.wait.until(
                EC.visibility_of_element_located((By.XPATH, "//div[text()='Admin']"))
            )

        if tab_id == ASSETS:
            self.wait.until(EC.visibility_of_element_located((By.ID, "ImportAssetButton")))


    def create(self):
        self.list()
        self.wait.until(
            EC.visibility_of_element_located((By.ID, "newProjectButton"))
        ).click()
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[@type='button' and text()='Next']")
            )
        ).click()
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//img[@alt='emptyProject']"))
        ).click()

        # focus on text before send key
        # https://stackoverflow.com/questions/20936403/sendkeys-are-not-working-in-selenium-webdriver
        self.wait.until(
            EC.visibility_of_element_located((By.ID, "newProjectNameField"))
        ).clear()
        self.driver.find_element(By.ID, "newProjectNameField").click()
        self.driver.find_element(By.ID, "newProjectNameField").send_keys(self.name)

        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='button' and text()='Create']")
            )
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@id='Overview-light__headerTitle___K4ujy']/div")
            )
        )
        logging.info(
            self.driver.find_element(
                By.XPATH, "//div[@id='Overview-light__headerTitle___K4ujy']/div"
            ).text
        )
        self.list()

    def delete(self, retry=6):
        PROJECT_URL = "%s/zen/#/projectList" % self.BASE_URL.strip("/")
        self.driver.get(PROJECT_URL)

        xpath_exp_menu = (
            "//button[contains(@id,'%s') and contains(@id,'menu')]" % self.name
        )
        xpath_exp_del = (
            "//button[contains(@id,'%s') and contains(@id,'Delete')]" % self.name
        )

        # click to delete project
        # retry until success

        short_wait = WebDriverWait(self.driver, 5)

        for i in range(1, retry):
            s = pow(2, i)
            logging.info("wait %d sec. for project delete complete. " % s)
            time.sleep(s)
            try:
                self.wait.until(
                    EC.visibility_of_element_located((By.XPATH, xpath_exp_menu))
                ).click()
                self.wait.until(
                    EC.visibility_of_element_located((By.XPATH, xpath_exp_del))
                ).click()
                self.wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//button[contains(text(),'Delete')]")
                    )
                ).click()
                if short_wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//div[contains(text(), 'successfully deleted')]")
                    )
                ):
                    break
            except TimeoutException as e:
                pass
            if i == retry - 1:
                raise TimeoutError("up to retry limit")

    def add(self, type):
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[text()='Admin']"))
        )
        self.driver.find_element(By.LINK_TEXT, "Add to project").click()
        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//span[@class='AddToProjectModalContent-light__assetName___3N938' and text()='%s']"
                    % type,
                )
            )
        ).click()

    def notebook(self, notebook_name):
        return notebook.Notebook(notebook_name, self)

    def data(self, path):
        return data.Data(path, self)

    def dashboard(self, filename, f1, f2):
        return dashboard.Dashboard(filename, f1, f2, self)

    def connection(self, name):
        return connection.Connection(name, self)

    def refinery(self):
        return refinery.Refinery(self)

    def autoai(self, name):
        return autoai.AutoAI(name, self)
