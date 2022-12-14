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

import os

import click

MISSING_CONF_ERR_MSG = """
Did not find conf.py. You should copy the file sample_conf.py

    $ cp sample_conf.py conf.py

and then adapt conf.py as desired.
"""
try:
    import conf
except ModuleNotFoundError:
    print(MISSING_CONF_ERR_MSG)
    import sys
    sys.exit(1)

PFSC_MANAGE_ROOT = os.path.dirname(__file__)
# In the standard, recommended installation, the top-level directory
# of this project lives directly under the Proofscape root dir. Users
# may configure a different location if they wish.
PFSC_ROOT = getattr(conf, 'PFSC_ROOT', None) or os.path.dirname(PFSC_MANAGE_ROOT)


@click.group()
def cli():
    pass

# These imports define all the commands.
import tools.basic
import tools.build
import tools.deploy
import tools.gdb
#import tools.install
import tools.license
import tools.make
import tools.repo
import tools.update
import tools.release
import tools.grep
import tools.get
