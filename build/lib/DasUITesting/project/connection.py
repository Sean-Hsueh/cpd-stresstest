from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from . import project


class Connection:
    def __init__(self, name, project):
        self.name = name
        self.project = project
        self.driver = project.driver
        self.wait = project.wait

    def create(self, type, metadata):
        self.project.list()

        self.project.open(project.OVERVIEW)

        self.project.add("Connection")

        if type == "MySQL":
            self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//span[text()='%s']" % type)
                )
            ).click()
            self.createMysql(metadata)
        else:
            raise Exception("not support connection type")

    def createMysql(self, metadata):
        # connection name
        self.wait.until(
            EC.visibility_of_element_located((By.ID, "txtInput-ConnectionName"))
        ).send_keys(self.name)

        # todo: read from paramater
        # database
        self.wait.until(
            EC.visibility_of_element_located((By.ID, "txtInput-database"))
        ).send_keys(metadata["database"])

        # host
        self.wait.until(
            EC.visibility_of_element_located((By.ID, "txtInput-host"))
        ).send_keys(metadata["host"])

        # port
        self.wait.until(
            EC.visibility_of_element_located((By.ID, "intInput-port"))
        ).send_keys(metadata["port"])

        # username
        self.wait.until(
            EC.visibility_of_element_located((By.ID, "txtInput-username"))
        ).send_keys(metadata["username"])

        # password
        self.wait.until(
            EC.visibility_of_element_located((By.ID, "txtInput-password"))
        ).send_keys(metadata["password"])

        # click test
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Test']"))
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//p[text()='The test was successful.']")
            )
        )

        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Create']"))
        ).click()

        # todo: wait until connection assest appear
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//td//a[text()='%s']" % self.name)
            )
        )
