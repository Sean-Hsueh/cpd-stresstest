from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


from . import project
import time, logging


class AutoAI:
    def __init__(self, name, project):
        self.name = name
        self.project = project
        self.driver = project.driver
        self.wait = project.wait

    def start_spss_flow(self):
        self.project.list()

        self.project.open(project.OVERVIEW)


    def run_experiment(self, train_file, predict_field, retry=10):
        self.project.list()

        self.project.open(project.OVERVIEW)

        self.project.add("AutoAI experiment")

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "newAutoMLNameField"))
        ).clear()
        self.driver.find_element(By.ID, "newAutoMLNameField").click()
        self.driver.find_element(By.ID, "newAutoMLNameField").send_keys(self.name)

        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='button' and text()='Create']")
            )
        ).click()

        # skip information
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Got it']"))
        ).click()

        # select assest
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[text()='Select from project']")
            )
        ).click()

        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//td[text()='%s']/preceding-sibling::td[1]" % train_file)
            )
        ).click()

        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='button' and text()='Select asset']")
            )
        ).click()

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "select-predict-col"))
        ).send_keys("%s\n" % predict_field)

        # config experiment

        for i in range(1, retry):
            s = pow(2, i)
            logging.info("sleep %d secs. for click Prediction. " % s)
            time.sleep(s)
            # self.wait.until(
            #     EC.element_to_be_clickable((By.ID, "experimentSettingCTA"))
            # ).click()
            try:
                self.driver.find_element(By.ID, "experimentSettingCTA").click()
                self.driver.find_element(By.XPATH, "//div[@title='Prediction']").click()
                break
            except Exception as e:
                self.driver.find_element(
                    By.XPATH,
                    "(//div[@id='settingsContent']/div)[2]/button[text()='Cancel']",
                ).click()

            if i == retry - 1:
                raise TimeoutError("up to retry limit")

        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//th/div[text()='Algorithm name']/../preceding-sibling::th[1]",
                )
            )
        ).click()

        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[text()='Decision Tree Classifier']/../../preceding-sibling::td[1]",
                )
            )
        ).click()

        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='button' and text()='Save settings']")
            )
        ).click()

        # run experiment
        self.wait.until(EC.element_to_be_clickable((By.ID, "runExperimentCTA"))).click()

        # wait until complete
        logging.info("wait 2 mins. for experiment finished.")
        time.sleep(120)

        for i in range(1, retry):
            s = pow(2, i)
            logging.info("wait another %d sec. for experiment finished. " % s)
            time.sleep(s)
            try:
                self.driver.find_element(
                    By.XPATH, "//div[text()='Experiment completed']"
                )
                break
            except Exception as e:
                pass

            if i == retry - 1:
                raise TimeoutError("up to retry limit")

    def saveModel(self):
        self.project.list()

        self.project.open(project.ASSETS)

        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[@class='apStyleLink' and text()='%s']" % self.name)
            )
        ).click()

        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='1']")))

        element = self.driver.find_element(
            By.XPATH,
            "//div[text()='1']/following-sibling::div[5]",
        )
        ActionChains(self.driver).move_to_element(element).click().perform()

        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Create']"))
        ).click()

    def promoteModel(self, space_name):
        self.project.list()

        self.project.open(project.ASSETS)

        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//td[descendant::a[contains(text(), 'DecisionTreeClassifierEstimator')]]/following-sibling::td[4]",
                )
            )
        ).click()

        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Promote']"))
        ).click()

        # choose differnet space
        self.wait.until(EC.element_to_be_clickable((By.ID, "spaces-dropdown"))).click()

        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='%s']" % space_name))
        ).click()

        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='button' and text()='Promote']")
            )
        ).click()
