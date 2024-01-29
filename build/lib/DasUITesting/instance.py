from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# import time
from .project import project
from .deployment import deployment


class Instance:
    def __init__(self, executor, headless=False, wait_timeout=60):
        # full screen chrome
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors-spki-list')
        print('here: ', options)

        # enable headless mode
        if headless:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")

        # connect to remote driver
        driver = webdriver.Remote(
            command_executor=executor,
            options=options,
        )

        self.driver = driver
        self.wait = WebDriverWait(driver, wait_timeout)
        self.BASE_URL = None

    def login(self, base, user, password):
        self.BASE_URL = base

        LOGIN_URL = "%s/auth/login/sso?logged_out=true" % self.BASE_URL.strip("/")

        self.driver.get(LOGIN_URL)
        self.driver.find_element(By.ID, "username-textinput").send_keys(user)
        self.driver.find_element(By.ID, "password-textinput").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, "#signInButton > span").click()
        self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, "walkme-balloon-5426948-focusable-element-5")
            )
        ).click()

    def logout(self):
        self.driver.find_element(
            By.CSS_SELECTOR, ".profile-toggle-parent .icon-profile"
        ).click()
        self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "#dap-open-logout-modal > span")
            )
        ).click()
        self.wait.until(
            EC.visibility_of_element_located((By.ID, "logout-modal-commit"))
        ).click()

    def close(self):
        self.driver.close()

    def project(self, project_name):
        prj = project.Project(project_name, self)
        return prj

    def deployment(self):
        return deployment.Deployment(self)
