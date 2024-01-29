from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import time, logging
from . import project


class Dashboard:
    def __init__(self, filename, f1, f2, project):
        self.filename = filename
        self.field1 = f1
        self.field2 = f2
        self.project = project
        self.driver = project.driver
        self.wait = project.wait

    def create(self):
        self.project.list()

        self.project.open(project.OVERVIEW)

        # add dashboard to project
        self.project.add("Dashboard")

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "dashboardNameField"))
        ).clear()
        self.driver.find_element(By.ID, "dashboardNameField").click()
        self.driver.find_element(By.ID, "dashboardNameField").send_keys(
            self.project.name
        )
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//button[text() = 'Create']"))
        ).click()

        retry = 4

        for i in range(1, retry):
            s = pow(2, i)
            logging.info("wait %d sec. for iframe available. " % s)
            time.sleep(s)
            try:
                self.driver.switch_to_frame(0)
                self.driver.find_element(By.XPATH, "//button[text() = 'OK']").click()
                break
            except Exception as e:
                pass
            finally:
                self.driver.switch_to.default_content()

            if i == retry - 1:
                raise TimeoutError("up to retry limit")

        self.driver.switch_to_frame(0)

        # fix: add source icon is not interactable
        # method 1: hover to icon first, then click
        element = self.wait.until(
            EC.visibility_of_element_located((By.ID, "view83addSource"))
        )
        ActionChains(self.driver).move_to_element(element).click(element).perform()
        self.driver.switch_to.default_content()

        # method 2: retry until icon interactable
        # for i in range(1, retry):
        #     s = pow(2, i)
        #     print("wait %d sec. for add source become interactable. " % s)
        #     time.sleep(s)
        #     try:
        #         self.driver.find_element(By.ID, "view83addSource").click()
        #         break
        #     except Exception as e:
        #         pass
        #     finally:
        #         self.driver.switch_to.default_content()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//span[contains(text(),'Data assets')]")
            )
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//span[contains(text(),'%s')]" % self.filename)
            )
        ).click()

        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text() = 'Select']"))
        ).click()

        self.driver.switch_to_frame(0)

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[text() = '%s']" % self.filename)
            )
        ).click()

        dd = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[text() = '%s']" % self.field1)
            )
        )

        pp = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[text() = '%s']" % self.field2)
            )
        )

        # ctrl + click
        ActionChains(self.driver).key_down(Keys.CONTROL).click(dd).key_up(
            Keys.CONTROL
        ).perform()
        ActionChains(self.driver).key_down(Keys.CONTROL).click(pp).key_up(
            Keys.CONTROL
        ).perform()

        # find correct dynamic generated id
        target_tab_id = self.driver.find_element(
            By.XPATH, "//div[contains(@id,'__tabs_1')]"
        ).get_attribute("id")
        target_element_id = target_tab_id[9:39]
        logging.info("target tab     id : %s" % target_tab_id)
        logging.info("target element id : %s" % target_element_id)

        # drag and drop

        dest_element = self.driver.find_element(By.ID, target_element_id)
        ActionChains(self.driver).drag_and_drop(dd, dest_element).perform()

        # todo: when is add completed?

        self.driver.switch_to.default_content()

        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[@data-action='save']"))
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(text(), 'Successfully saved the dashboard')]",
                )
            )
        )

        self.project.list()

        self.wait.until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()
