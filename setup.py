from setuptools import setup

setup(
    name="DasUITesting",
    version="0.1.0",
    description="Selenium based package for test CPD",
    url="https://github.com/shuds13/pyexample",
    author="Jimmy Chuang",
    author_email="jimmy_chuang@narlabs.org.tw",
    packages=["DasUITesting", "DasUITesting.deployment", "DasUITesting.project", "DasUITesting.catalog"],
    install_requires=["selenium", "requests", "pytz"],
    classifiers=[],
)
