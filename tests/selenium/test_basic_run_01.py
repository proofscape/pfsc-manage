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

from tests.selenium.util import Tester


class TestBasicRun01(Tester):
    """Log in as test.hist, and load the test.hist.lit repo @WIP."""

    def test_basic_run_01(self, caplog, pise_url, selenium_logging_level):
        logger = logging.getLogger(__name__)
        self.logger_name = __name__
        # https://docs.pytest.org/en/6.2.x/logging.html#caplog-fixture
        caplog.set_level(selenium_logging_level, logger=__name__)

        self.load_page(pise_url)
        time.sleep(1)
        self.dismiss_cookie_notice()
        self.check_user_menu()
        self.login_as_test_user('hist', wait=1)

        repopath = "test.hist.lit"

        s_repo_root_node = "#dijit__TreeNode_0_label"
        s_feedback_area = "#feedback"
        s_prog_bar = "#feedback > div.progbar > div.nanobar > div.bar"

        self.open_repo(repopath, s_repo_root_node, select_tab='fs')

        prog_bar = self.find_element(s_prog_bar)

        # Open context menu and click "build recursive" option.
        self.click_nth_context_menu_option(s_repo_root_node, "dijit_Menu_1", 7, "Build Recursive")
        t0 = time.time()
        logger.info("Starting build...")

        # Watch the feedback monitor, and sample the width of the progress bar.
        self.wait_for_element_visible(s_feedback_area)
        logger.info("Feedback monitor is visible.")
        logger.info("Sampling prog bar width for 3 seconds...")
        widths = set()
        for i in range(30):
            w_str = prog_bar.value_of_css_property('width')
            w_flt = float(w_str.replace('px', ''))
            logger.debug(f'Prog bar width: {w_flt:.2f}')
            widths.add(w_flt)
            time.sleep(0.1)
        # Probably got 20 or more different values,
        # but we'll just look for two distinct non-zero values.
        n = len(widths - {0})
        logger.info(f"Got {n} different nonzero prog bar widths.")
        assert n >= 2

        # Feedback monitor should be hidden after build completes.
        self.wait_for_element_invisible(s_feedback_area, wait=30)
        dt = time.time() - t0
        logger.info(f'Feedback monitor hidden. Build took {dt:.2f}s.')

        # Wait a second and log out
        time.sleep(1)
        self.log_out()
