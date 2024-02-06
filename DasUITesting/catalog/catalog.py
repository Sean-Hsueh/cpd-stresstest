from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class Catalog:
    def __init__(self, catalog_name, instance):
        self.name = catalog_name
        self.instance = instance
        self.wait = instance.wait
        self.BASE_URL = instance.BASE_URL
        self.driver = instance.driver

    def open(self):
        CATALOGS_URL = "%s/data/catalogs/" % self.BASE_URL.strip("/")
        print('going to: ', CATALOGS_URL)
        self.driver.get(CATALOGS_URL)

        # wait for Link to target catalog is visible + clickable
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//h4[contains(@id, 'catalogCard-catalogName') and text()='CL_Preview']"))
        ).click()

    # sample link: https://cpd-cpd-instance.apps.cp4d2.hosp.ncku.edu.tw/data/catalogs/e292c730-2cc4-4a81-91a8-03da6ed59363/asset/adcbe5b7-a559-43e6-8088-7de56ea4bed3/asset-preview?context=icp4data
    def gotoAsset(self, assetLink):
        self.driver.get(assetLink)

        # wait for the text 'Schema:'
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'GridPreview-light__schemaTitleContainer___') and contains(text(), 'Schema:')]"))
        )



