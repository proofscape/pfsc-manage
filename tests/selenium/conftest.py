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

import logging
import time

import pytest
import requests
from requests.exceptions import ConnectionError

import conf as pfsc_conf
from tests.selenium.util import make_driver


@pytest.fixture
def pise_url():
    url = pfsc_conf.SEL_PISE_URL
    url = url.replace("<MCA_PORT>", str(pfsc_conf.PFSC_ISE_MCA_PORT))
    return url


@pytest.fixture
def pise_server_status(pise_url):
    """
    Try to connect to the PISE server for up to SEL_SERVER_READY_TIMEOUT seconds.
    Return a pair (code, message) indicating the result.
    code ranges from 0 to 4 incl., 4 means the server appears to be ready,
    anything less means it is not ready.
    """
    expected_text = '<title>Proofscape ISE</title>'
    result = 0, 'unknown issue'
    for i in range(int(pfsc_conf.SEL_SERVER_READY_TIMEOUT)):
        try:
            r = requests.get(pise_url)
        except ConnectionError:
            result = 1, 'could not connect'
        else:
            if r.status_code == 200:
                if r.text.find(expected_text) >= 0:
                    result = 4, 'status 200, and found expected text'
                    break
                else:
                    result = 3, f'status 200, but did not find expected text, "{expected_text}"'
            else:
                result = 2, f'status {r.status_code}'
        time.sleep(1)
    return result


@pytest.fixture
def pise_server_ready(pise_server_status):
    """
    Require a ready server, raising an exception otherwise.
    """
    code, message = pise_server_status
    if code < 4:
        raise Exception('PISE Server not ready: ' + message)
    return pise_server_status


@pytest.fixture
def driver():
    return make_driver()


@pytest.fixture
def selenium_logging_level():
    return getattr(logging, pfsc_conf.SEL_LOG_LEVEL)
