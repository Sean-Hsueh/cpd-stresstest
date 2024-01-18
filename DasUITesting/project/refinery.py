from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from . import project
import time, logging


class Refinery:
    def __init__(self, project):
        self.project = project
        self.driver = project.driver
        self.wait = project.wait

    def build_flow(self, retry=5):
        self.project.list()

        self.project.open(project.OVERVIEW)

        # add refinery to project
        self.project.add("Data Refinery flow")

        # load data
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//span[contains(text(),'Data assets')]")
            )
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//span[contains(text(),'%s')]" % "airline-data.csv")
            )
        ).click()

        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//button[text() = 'Add']"))
        ).click()

        # operation > filter
        self.ready_for_next_operation(retry)

        self.wait.until(EC.visibility_of_element_located((By.ID, "filter"))).click()

        # choose column
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//span[text()='Column']/following-sibling::div[1]/div")
            )
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[text()='UniqueCarrier']")
            )
        ).click()

        # choose operator
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//span[text()='Operator']/following-sibling::div[1]/div")
            )
        ).click()

        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[text()='Is equal to']"))
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, "ColumnValueToggle_TextFieldID_filterInputText01")
            )
        ).send_keys("UA")

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//button[@class='CustomOperations__opsPanelSingleOpButton___2mlJe bx--btn bx--btn--primary']",
                )
            )
        ).click()

        # operation > calculate
        self.ready_for_next_operation(retry)

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "calculateNewColumn"))
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[@placeholder='Select column']")
            )
        ).click()

        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[text()='ArrDelay']"))
        ).click()

        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//button[text()='Next']"))
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//label[@for='ColumnValueToggle_SwitchCalculate_ColumnValueTogglecolumn']",
                )
            )
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[@placeholder='Select column']")
            )
        ).click()

        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[text()='DepDelay']"))
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//span[text()='Create new column for results']")
            )
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, "NewColNameWidget_TextCalculateOp")
            )
        ).send_keys("TotalDelay")

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//button[@class='CustomOperations-light__opsPanelSingleOpButton___VB9qL bx--btn bx--btn--primary']",
                )
            )
        ).click()

        # code input > select
        self.ready_for_next_operation(retry)

        op_input = self.wait.until(
            EC.visibility_of_element_located((By.ID, "operation-input"))
        )
        op_input.clear()
        op_input.click()
        op_input.send_keys("select(Year, Month, DayofMonth, TotalDelay)")

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "command-editor-apply"))
        ).click()

        # code input > group_by
        self.ready_for_next_operation(retry)

        op_input = self.wait.until(
            EC.visibility_of_element_located((By.ID, "operation-input"))
        )
        op_input.clear()
        op_input.click()
        op_input.send_keys("group_by(Year, Month, DayofMonth)")
        self.wait.until(
            EC.visibility_of_element_located((By.ID, "command-editor-apply"))
        ).click()

        # operation > aggregate
        self.ready_for_next_operation(retry)

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "aggregateOp"))
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//span[text()='Column']/following-sibling::div[1]/div")
            )
        ).click()

        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[text()='TotalDelay']"))
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//span[text()='Operator']/following-sibling::div[1]/div")
            )
        ).click()

        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[text()='Mean']"))
        ).click()

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "newColumnTextField01"))
        ).send_keys("mean_Delay")

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//button[@class='CustomOperations-light__opsPanelSingleOpButton___VB9qL bx--btn bx--btn--primary']",
                )
            )
        ).click()

        # sort
        # Because the sort menu can be showed if windows is too small , open operation menu and close right away.
        self.ready_for_next_operation(retry)
        self.ready_for_next_operation(retry)

        self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "svg.Shaper-light__actionButton___3IEqm")
            )
        ).click()

        element = self.driver.find_element(
            By.XPATH,
            "//div[@id='shaper-data-grid-column.columnHeader_3']/div/div[2]/div",
        )
        ActionChains(self.driver).move_to_element(element).perform()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[@id='shaper-data-grid-column.columnHeader_3']/div/div[2]/div/div",
                )
            )
        ).click()

        self.driver.find_element(
            By.XPATH, "//li/button/div[@title='Sort descending']"
        ).click()

        # save flow
        self.ready_for_next_operation(retry)

        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//a[@data-action='save']"))
        ).click()

        self.ready_for_next_operation(retry)

        self.project.list()

    def ready_for_next_operation(self, retry=5):
        for i in range(1, retry):
            try:
                self.wait.until(
                    EC.element_to_be_clickable((By.ID, "applyOperation"))
                ).click()
                break
            except Exception as e:
                logging.warning(
                    "retry %d times for operation ready. " % i, exc_info=True
                )

            if i == retry - 1:
                raise TimeoutError("up to retry limit")

    def create_job(self, job_name, retry=5):
        self.project.list()

        self.project.open(project.ASSETS)

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//td/div[text()='Data Refinery flow']/../following-sibling::td[3]",
                )
            )
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//button/div[text()='Create job']/..",
                )
            )
        ).click()

        for i in range(1, retry):
            s = pow(2, i)
            logging.info("wait %d sec. for page load. " % s)
            time.sleep(s)
            try:
                # step 1
                # time.sleep(s)
                self.wait.until(
                    EC.visibility_of_element_located((By.ID, "nameField"))
                ).send_keys(job_name)

                self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Next']"))
                ).click()

                # step 2
                # time.sleep(s)
                self.wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//div[text()='airline-data.csv']")
                    )
                )

                self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Next']"))
                ).click()

                # step 3
                # time.sleep(s)
                self.wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, " //span[text()='Schedule off']")
                    )
                )

                self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Next']"))
                ).click()

                # Step 4
                # time.sleep(s)
                self.wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[text()='Create and run']")
                    )
                ).click()
                break
            except Exception as e:
                logging.info("screen seems empty, refresh and try again")
                self.driver.refresh()

            if i == retry - 1:
                raise TimeoutError("up to retry limit")

        status_element = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//td[text()='das']/preceding-sibling::td[2]")
            )
        )

        while status_element.text == "Running":
            time.sleep(5)
            logging.info("Job is %s" % status_element.text)

        assert status_element.text.strip() == "Completed"

        duration_element = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//td[text()='das']/preceding-sibling::td[1]")
            )
        )

        logging.info("Job compeleted in %s." % duration_element.text)

    def cleanup(self):
        self.project.list()

        self.project.open(project.ENVIRONMENTS)

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//td/div[text()='das']/../following-sibling::td[1]")
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
