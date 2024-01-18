from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


import time, logging
from . import project


class Notebook:
    def __init__(self, name, project):
        self.name = name
        self.project = project
        self.driver = project.driver
        self.wait = project.wait

    def create(self, environment, retry=10):
        self.project.list()

        self.project.open(project.OVERVIEW)

        # add notebook to project
        self.project.add("Notebook")

        # enter notebook name
        self.wait.until(EC.visibility_of_element_located((By.ID, "nameNew"))).clear()
        self.driver.find_element(By.ID, "nameNew").click()
        self.driver.find_element(By.ID, "nameNew").send_keys(self.name)

        # select environment
        select = Select(self.driver.find_element_by_id("instanceNew"))
        select.select_by_visible_text(environment)

        # launch notebook
        self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, "newNotebook_newNotebookForm_submitButton")
            )
        ).click()

        # wait for iframe appear
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//iframe[@id='guest']"))
        )

        # wait unit notebook ready
        for i in range(1, retry):
            s = pow(2, i)
            logging.info("wait %d sec. for notebook ready. " % s)
            time.sleep(s)
            try:
                self.driver.switch_to_frame("guest")
                self.driver.find_element(By.XPATH, "//div[@id='notebook-container']")
                break
            except Exception as e:
                pass
            finally:
                self.driver.switch_to.default_content()

            if i == retry - 1:
                raise TimeoutError("up to retry limit")

    def delete(self, user):
        self.project.list()

        self.project.open(project.ENVIRONMENTS)

        # then delete notebook runtime
        # self.wait.until(
        #     EC.visibility_of_element_located((By.XPATH, "//div[text()='Admin']"))
        # )
        # self.driver.find_element(
        #     By.XPATH, "//a[@id='projectDetailsEnvironments']"
        # ).click()
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//td/div[text()='%s']/../following-sibling::td[1]" % user)
            )
        ).click()
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button/div[text()='Stop']/..")
            )
        ).click()
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//button[text()='Stop']"))
        ).click()

    def run_cell(self, cmd, expected):
        # reference:
        # https://www.jianshu.com/p/9ac7a17d6e3c
        # https://stackoverflow.com/questions/58527543/use-selenium-to-write-in-and-run-a-code-cell-in-jupyterlab
        self.driver.switch_to.default_content()
        self.driver.switch_to_frame("guest")
        e = self.driver.find_element(By.CSS_SELECTOR, ".CodeMirror textarea")
        p = self.driver.find_element(By.CSS_SELECTOR, "pre.CodeMirror-line")
        p.click()
        e.send_keys(cmd)
        self.driver.find_element(By.ID, "celllink").click()
        self.driver.find_element(By.XPATH, "//li[@id='run_cell']/a/span").click()

        output = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".output_text"))
        )
        assert output.text.strip() == expected

        # save notebook avoid alarm to interrupt project_list() flow
        self.driver.find_element(By.ID, "filelink").click()
        self.driver.find_element(By.XPATH, "//li[@id='save_notebook']/a").click()
        # wait until notebook is saved
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//span[contains(text(), 'Notebook saved')]")
            )
        )
