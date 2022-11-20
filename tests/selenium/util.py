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
import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

import conf as pfsc_conf

BASIC_WAIT = pfsc_conf.SEL_BASIC_WAIT


def make_driver():
    """
    Construct a driver, with options such as:
      * which browser
      * whether to operate headlessly
    determined by our conf.py.
    """
    browser = pfsc_conf.SEL_BROWSER.upper()
    headless = pfsc_conf.SEL_HEADLESS

    driver = None
    if browser == "CHROME":
        options = ChromeOptions()
        options.headless = headless
        if pfsc_conf.SEL_STAY_OPEN:
            options.add_experimental_option("detach", True)
        return webdriver.Chrome(options=options)
    elif browser == "FIREFOX":
        options = FirefoxOptions()
        options.headless = headless
        return webdriver.Firefox(options=options)

    return driver


def load_page(driver, url):
    driver.get(url)
    driver.set_window_size(pfsc_conf.SEL_WINDOW_WIDTH, pfsc_conf.SEL_WINDOW_HEIGHT)


def dismiss_cookie_notice(driver):
    """
    Dismiss the cookie notice, if any.
    """
    button = driver.find_element(By.CSS_SELECTOR, "body > div.noticeBox > div.buttonRow > button")
    if button:
        button.click()
        logging.info("Dismissed cookie notice")
    else:
        logging.info("Found no cookie notice")


def login_as_test_user(driver, user, wait=BASIC_WAIT):
    """
    Log in as a test.user
    """
    v = {}
    
    def wait_for_window(wait=BASIC_WAIT):
        time.sleep(wait)
        wh_now = driver.window_handles
        wh_then = v["window_handles"]
        if len(wh_now) > len(wh_then):
            return set(wh_now).difference(set(wh_then)).pop()
    logging.info("Logging in...")
    # Click the user menu
    driver.find_element(By.ID, "dijit_PopupMenuBarItem_8_text").click()
    v["window_handles"] = driver.window_handles
    # Click the "Log in" option
    driver.find_element(By.ID, "dijit_MenuItem_25_text").click()
    v["popup"] = wait_for_window(wait)
    v["root"] = driver.current_window_handle
    # In pop-up window, log in as the desired test user
    driver.switch_to.window(v["popup"])
    driver.find_element(By.NAME, "username").click()
    driver.find_element(By.NAME, "username").send_keys(user)
    driver.find_element(By.NAME, "password").send_keys(user)
    driver.find_element(By.CSS_SELECTOR, "p > input").click()
    driver.close()
    driver.switch_to.window(v["root"])
    # User menu text should now say our username
    WebDriverWait(driver, wait).until(expected_conditions.text_to_be_present_in_element((By.ID, "dijit_PopupMenuBarItem_8_text"), f"test.{user}"))
    assert driver.find_element(By.ID, "dijit_PopupMenuBarItem_8_text").text == f"test.{user}"
    logging.info(f"Logged in as test.{user}")


def wait_for_element(driver, selector, wait=BASIC_WAIT):
    WebDriverWait(driver, wait).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, selector)))
    return driver.find_element(By.CSS_SELECTOR, selector)


def wait_for_element_with_text(driver, selector, text, wait=BASIC_WAIT):
    WebDriverWait(driver, wait).until(expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR, selector), text))
    return driver.find_element(By.CSS_SELECTOR, selector)


def wait_for_element_visible(driver, selector, wait=BASIC_WAIT):
    WebDriverWait(driver, wait).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, selector)))
    return driver.find_element(By.CSS_SELECTOR, selector)


def wait_for_element_invisible(driver, selector, wait=BASIC_WAIT):
    WebDriverWait(driver, wait).until(expected_conditions.invisibility_of_element_located((By.CSS_SELECTOR, selector)))


def inner_html(element):
    return element.get_attribute('innerHTML')


def open_repo(driver, repopath, selector, wait=BASIC_WAIT, select_tab=None):
    """
    Open a content repo.

    selector: for the tree node element whose text will be the repopath, after
        the repo loads
    wait: max seconds to wait for repo to load
    """
    logging.info(f"Opening repo {repopath}...")
    driver.find_element(By.ID, "repoInputText").click()
    driver.find_element(By.ID, "repoInputText").send_keys(repopath)
    driver.find_element(By.ID, "repoInputButton").click()
    if select_tab:
        tab_sel = {
            'fs': '#dijit_layout_TabContainer_0_tablist_fsTab',
            'build': '#dijit_layout_TabContainer_0_tablist_buildTab',
            'struct': '#dijit_layout_TabContainer_0_tablist_buildTab',
        }[select_tab]
        tab = wait_for_element(driver, tab_sel, wait=wait)
        tab.click()
    root_node = wait_for_element(driver, selector, wait=wait)
    # Strangely, for this element it's not the inner text, but inner HTML that
    # is equal to the repopath.
    #print("=" * 80)
    #print('text', root_node.text)
    #print('html', root_node.get_attribute('innerHTML'))
    assert inner_html(root_node) == repopath
    logging.info(f"Opened repo {repopath}.")


def click(driver, selector, button='l'):
    """
    Click element by selector.

    button: 'l' or 'r', default 'l'
    """
    elt = driver.find_element(By.CSS_SELECTOR, selector)
    actions = ActionChains(driver)
    actions.move_to_element(elt)
    if button == 'r':
        actions.context_click()
    else:
        actions.click()
    actions.perform()


def right_click(driver, selector):
    """
    Right-click element by selector.
    """
    return click(driver, selector, button='r')


class Tester:

    def setup_method(self, method):
        self.driver = make_driver()

    def teardown_method(self, method):
        if pfsc_conf.SEL_HEADLESS or not pfsc_conf.SEL_STAY_OPEN:
            self.driver.quit()

    def load_page(self, url):
        return load_page(self.driver, url)

    def find_element(self, selector):
        return self.driver.find_element(By.CSS_SELECTOR, selector)

    def dismiss_cookie_notice(self):
        return dismiss_cookie_notice(self.driver)

    def login_as_test_user(self, user, wait=BASIC_WAIT):
        return login_as_test_user(self.driver, user, wait=wait)

    def open_repo(self, repopath, selector, wait=BASIC_WAIT, select_tab=None):
        return open_repo(self.driver, repopath, selector, wait=wait, select_tab=select_tab)

    def click(self, selector, button='l'):
        return click(self.driver, selector, button=button)

    def right_click(self, selector):
        return right_click(self.driver, selector)

    def wait_for_element(self, selector, wait=BASIC_WAIT):
        return wait_for_element(self.driver, selector, wait=wait)

    def wait_for_element_visible(self, selector, wait=BASIC_WAIT):
        return wait_for_element_visible(self.driver, selector, wait=wait)

    def wait_for_element_invisible(self, selector, wait=BASIC_WAIT):
        return wait_for_element_invisible(self.driver, selector, wait=wait)

    def wait_for_element_with_text(self, selector, text, wait=BASIC_WAIT):
        return wait_for_element_with_text(self.driver, selector, text, wait=wait)
