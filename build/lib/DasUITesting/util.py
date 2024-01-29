import base64, logging


def take_sceenshot(driver, path):
    driver.save_screenshot(path)


def print_image_base64_encoding(driver, path):
    driver.save_screenshot(path)
    with open(path, "rb") as img_file:
        my_string = base64.b64encode(img_file.read())

    # logging.info("screenshot base64 encoding: \n" + my_string.decode("utf-8"))


def debug(driver, msg='debug'):
    print(msg)
    driver.save_screenshot('/tmp/selenium-script/debug.png')
  


def base64_to_image():
    pass
