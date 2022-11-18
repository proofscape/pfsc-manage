# --------------------------------------------------------------------------- #
#   Proofscape Manage                                                         #
#                                                                             #
#   Copyright (c) 2021-2022 Proofscape contributors                           #
#                                                                             #
#   Licensed under the Apache License, Version 2.0 (the "License");           #
#   you may not use this file except in compliance with the License.          #
#   You may obtain a copy of the License at                                   #
#                                                                             #
#       http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                             #
#   Unless required by applicable law or agreed to in writing, software       #
#   distributed under the License is distributed on an "AS IS" BASIS,         #
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#   See the License for the specific language governing permissions and       #
#   limitations under the License.                                            #
# --------------------------------------------------------------------------- #

import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By

import conf as pfsc_conf


def make_driver():
    """
    Construct a driver, with options such as:
      * which browser
      * whether to operate headlessly
    determined by our conf.py.
    """
    browser = pfsc_conf.SEL_BROWSER.upper()
    headless = pfsc_conf.SEL_HEADLESS
    if browser == "CHROME":
        options = ChromeOptions()
        options.headless = headless
        return webdriver.Chrome(options=options)
    elif browser == "FIREFOX":
        options = FirefoxOptions()
        options.headless = headless
        return webdriver.Firefox(options=options)
    else:
        return None


def dismiss_cookie_notice(driver):
    """
    Dismiss the cookie notice, if any.
    """
    button = driver.find_element(By.CSS_SELECTOR, "body > div.noticeBox > div.buttonRow > button")
    if button:
        button.click()


def login_as_test_user(driver, user, window_timeout=2000):
    """
    Log in as a test.user
    """
    v = {}
    
    def wait_for_window(timeout=2000):
        time.sleep(round(timeout / 1000))
        wh_now = driver.window_handles
        wh_then = v["window_handles"]
        if len(wh_now) > len(wh_then):
            return set(wh_now).difference(set(wh_then)).pop()

    # Click the user menu
    driver.find_element(By.ID, "dijit_PopupMenuBarItem_8_text").click()
    v["window_handles"] = driver.window_handles
    # Click the "Log in" option
    driver.find_element(By.ID, "dijit_MenuItem_25_text").click()
    v["popup"] = wait_for_window(window_timeout)
    v["root"] = driver.current_window_handle
    # In pop-up window, log in as the desired test user
    driver.switch_to.window(v["popup"])
    driver.find_element(By.NAME, "username").click()
    driver.find_element(By.NAME, "username").send_keys(user)
    driver.find_element(By.NAME, "password").send_keys(user)
    driver.find_element(By.CSS_SELECTOR, "p > input").click()
    driver.close()
    driver.switch_to.window(v["root"])


def open_repo(driver, repopath):
    """
    Open a content repo.
    """
    driver.find_element(By.ID, "repoInputText").click()
    driver.find_element(By.ID, "repoInputText").send_keys(repopath)
    driver.find_element(By.ID, "repoInputButton").click()
