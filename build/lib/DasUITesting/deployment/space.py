from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


import logging, time


class Space:
    def __init__(self, space_name, deployment):
        self.name = space_name
        self.deployment = deployment
        self.wait = deployment.wait
        self.BASE_URL = deployment.BASE_URL
        self.driver = deployment.driver

        self.deployment.list()
        self.wait.until(EC.element_to_be_clickable((By.ID, "mlRuntimeSpaces"))).click()
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Maybe later']"))
        ).click()

    def create(self):

        self.deployment.list()

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "mlruntime-create-space-Button"))
        ).click()

        # todo: sometimes not clickable
        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//img[@src='/ml-runtime/graphics/empty_deployment_space.svg']",
                )
            )
        )
        self.driver.find_element(
            By.XPATH,
            "//img[@src='/ml-runtime/graphics/empty_deployment_space.svg']/../..",
        ).click()
        # ActionChains(self.driver).move_to_element(element).click().perform()

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "newSpaceNameField"))
        ).clear()
        self.driver.find_element(By.ID, "newSpaceNameField").click()
        self.driver.find_element(By.ID, "newSpaceNameField").send_keys(self.name)

        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='button' and text()='Create']")
            )
        ).click()

        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[text()='is ready']"))
        )

        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='button' and text()='Close']")
            )
        ).click()

    def delete(self):
        self.deployment.list()

        self.wait.until(EC.element_to_be_clickable((By.ID, "mlRuntimeSpaces"))).click()

        self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//td/div/button/div/a[text()='%s']/../../../../following-sibling::td[6]/div/button"
                    % self.name,
                )
            )
        ).click()

        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Delete']"))
        ).click()

        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Delete']"))
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@title='Successfully deleted %s.']" % self.name)
            )
        )

    def deploy(self, deploy_name, retry=10):
        self.deployment.list()

        self.wait.until(EC.element_to_be_clickable((By.ID, "mlRuntimeSpaces"))).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//td/div/button/div/a[text()='%s']" % self.name,
                )
            )
        ).click()

        self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "(//td[text()='wml-hybrid_0.1']/following-sibling::td[3]/div/button)[1]",
                )
            )
        ).click()

        self.driver.switch_to_frame(0)

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[text()='Online']",
                )
            )
        ).click()

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "newDeploymentNameField"))
        ).clear()
        self.driver.find_element(By.ID, "newDeploymentNameField").click()
        self.driver.find_element(By.ID, "newDeploymentNameField").send_keys(deploy_name)

        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='button' and text()='Create']")
            )
        ).click()

        self.driver.switch_to.default_content()

        # Model should be deployed after 5 mins, don't to raise another exception
        # to interrupt process
        for i in range(1, 5):
            try:
                self.wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//div[text()='Asset deployed']")
                    )
                )
                break
            except Exception as e:
                logging.warning(
                    "retry %d times for model deployed. " % i, exc_info=True
                )

        for i in range(1, retry):
            try:
                self.wait.until(
                    EC.element_to_be_clickable((By.ID, "spaceDeployments"))
                ).click()
                break
            except Exception as e:
                logging.warning(
                    "retry %d times for click deployment tab. " % i, exc_info=True
                )

            if i == retry - 1:
                raise TimeoutError("up to retry limit")

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//td//a[text()='%s']/../../../../../following-sibling::td[2]//span[text()='Deployed']"
                    % deploy_name,
                )
            )
        )

    def undeploy(self, deploy_name, retry=10):
        self.deployment.list()

        self.wait.until(EC.element_to_be_clickable((By.ID, "mlRuntimeSpaces"))).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//td/div/button/div/a[text()='%s']" % self.name,
                )
            )
        ).click()

        for i in range(1, retry):
            try:
                self.wait.until(
                    EC.element_to_be_clickable((By.ID, "spaceDeployments"))
                ).click()
                break
            except Exception as e:
                logging.warning(
                    "retry %d times for click deployment tab. " % i, exc_info=True
                )

            if i == retry - 1:
                raise TimeoutError("up to retry limit")

        # self.wait.until(EC.element_to_be_clickable((By.ID, "spaceDeployments"))).click()

        self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//td//a[text()='%s']/../../../../../following-sibling::td[5]"
                    % deploy_name,
                )
            )
        ).click()

        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@title='Delete']"))
        ).click()

        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Delete']"))
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@title='Your deployment was successfully removed.']")
            )
        )

    def get_endpoint(self, deploy_name, retry=10):
        self.deployment.list()

        self.wait.until(EC.element_to_be_clickable((By.ID, "mlRuntimeSpaces"))).click()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//td/div/button/div/a[text()='%s']" % self.name,
                )
            )
        ).click()

        for i in range(1, retry):
            try:
                self.wait.until(
                    EC.element_to_be_clickable((By.ID, "spaceDeployments"))
                ).click()
                break
            except Exception as e:
                logging.warning(
                    "retry %d times for click deployment tab. " % i, exc_info=True
                )

            if i == retry - 1:
                raise TimeoutError("up to retry limit")

        # self.wait.until(EC.element_to_be_clickable((By.ID, "spaceDeployments"))).click()

        self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//td//a[text()='%s']" % deploy_name,
                )
            )
        ).click()

        ep_element = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div/div[text()='Endpoint']/../following-sibling::div[1]//pre",
                )
            )
        )

        return ep_element.text
