from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


from . import project


class Data:
    def __init__(self, path, project):
        self.path = path
        self.project = project
        self.driver = project.driver
        self.wait = project.wait

    def upload(self):
        self.project.list()

        self.project.open(project.OVERVIEW)

        # add notebook to project
        self.project.add("Data")

        self.wait.until(
            EC.presence_of_element_located((By.ID, "osFileWidget"))
        ).send_keys(self.path)

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//span[contains(text(), 'Upload successful')]")
            )
        )
