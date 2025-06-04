from appium import webdriver
from appium.options.android import UiAutomator2Options

def get_driver():
    options = UiAutomator2Options()
    options.platform_name = 'Android'
    options.platform_version = '16.0'
    options.device_name = 'Android Emulator'
    options.app = '/Users/eliram/Downloads/app-v5.44.1412-debug.apk'  # Update this path
    options.automation_name = 'UiAutomator2'

    driver = webdriver.Remote('http://localhost:4723', options=options)
    return driver
