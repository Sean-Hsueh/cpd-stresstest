from . import space


class Deployment:
    def __init__(self, instance):
        self.instance = instance
        self.wait = instance.wait
        self.BASE_URL = instance.BASE_URL
        self.driver = instance.driver

    def list(self):
        DEPLOYMENT_URL = "%s/ml-runtime" % self.BASE_URL.strip("/")
        self.driver.get(DEPLOYMENT_URL)

    def space(self, name):
        return space.Space(name, self)
