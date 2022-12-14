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

from manage import cli, PFSC_ROOT
from tools.util import trymakedirs

log = click.echo

@cli.command()
def makestruct():
    """
    Build the directory structure for Proofscape.

    In order to build the directory structure for Proofscape, `pfsc-manage` needs
    to know where the root directory is to be located.

    By default, `pfsc-manage` is expected to live directly under the root dir itself,
    and so the root is assumed to be the parent dir of `pfsc-manage`.

    For example, in a normal installation the root dir might be `~/proofscape`,
    and the `pfsc-manage` repo would be at `~/proofscape/pfsc-manage`.

    If you want to override the default behavior, you may set the location of the
    root directory in the variable `PFSC_ROOT` in your `conf.py`.
    """
    if PFSC_ROOT is None or (isinstance(PFSC_ROOT, str) and len(PFSC_ROOT) == 0):
        raise click.UsageError('PFSC_ROOT undefined.')

    click.confirm(f'Do you want to install Proofscape in {PFSC_ROOT}?', abort=True)

    if os.path.exists(PFSC_ROOT):
        log(f'Found existing directory {PFSC_ROOT}.')
    else:
        log(f'Making directory {PFSC_ROOT}.')
        trymakedirs(PFSC_ROOT)

    for name in "lib build PDFLibrary graphdb deploy/.ssl src/tmp".split():
        path = os.path.join(PFSC_ROOT, name)
        if os.path.exists(path):
            log(f'Directory {path} already exists.')
        else:
            log(f'Making directory {path}.')
            trymakedirs(path, exist_ok=True)
