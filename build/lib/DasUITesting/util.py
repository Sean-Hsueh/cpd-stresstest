import base64, logging
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def take_sceenshot(driver, path):
    driver.save_screenshot(path)


def print_image_base64_encoding(driver, path):
    driver.save_screenshot(path)
    with open(path, "rb") as img_file:
        my_string = base64.b64encode(img_file.read())

    logging.info("screenshot base64 encoding: \n" + my_string.decode("utf-8"))


def debug(driver, msg='debug'):
    print(msg)
    driver.save_screenshot('/tmp/selenium-script/debug.png')


def debug2(driver, msg='debug', condition_func=None):
    print(msg)
    driver.save_screenshot('/tmp/selenium-script/debug.png')

    if condition_func:
        while True:
            result = condition_func()  # 调用条件函数
            if result:
                print("条件满足，结束循环。")
                break  # 如果条件函数返回True，则退出循环
            else:
                print(".", end='', flush=True)  # 条件函数返回False，打印点并等待
                time.sleep(1)  # 等待一秒

