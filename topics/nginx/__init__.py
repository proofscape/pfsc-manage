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
import jinja2

import conf as pfsc_conf
from tools.util import squash

this_dir = os.path.dirname(__file__)
templates_dir = os.path.join(this_dir, 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_dir))

def write_nginx_conf(
        listen_on=80, server_name='localhost',
        ssl=False, basic_auth_title=None,
        static_redir=None, static_acao=False,
        redir_http=False, twin_server_name=None,
        hsts_seconds=None,
        **kwargs):
    # Define mapping {URL_path_extension: nginx_subdir}.
    # This means URLs pointing to
    #   {{app_url_prefix}}/static{{path_ext}}
    # will be served from the directory
    #   /usr/share/nginx{{subdir}}
    # in the Nginx container.
    # Note: originally, this was not the identity map! Could maybe turn into
    # a mere list now, but for the moment I'm keeping it as a map.
    loc_map = {
        '/PDFLibrary': '/PDFLibrary',
        f'/pdfjs/v{pfsc_conf.CommonVars.PDFJS_VERSION}': f'/pdfjs/v{pfsc_conf.CommonVars.PDFJS_VERSION}',
        '/whl': '/whl',
        f'/pyodide/v{pfsc_conf.CommonVars.PYODIDE_VERSION}': f'/pyodide/v{pfsc_conf.CommonVars.PYODIDE_VERSION}',
        '/css': '/css',
        '/img': '/img',
        f'/elk/v{pfsc_conf.CommonVars.ELKJS_VERSION}': f'/elk/v{pfsc_conf.CommonVars.ELKJS_VERSION}',
        f'/mathjax/v{pfsc_conf.CommonVars.MATHJAX_VERSION}': f'/mathjax/v{pfsc_conf.CommonVars.MATHJAX_VERSION}',
        '/dojo': '/dojo',
        f'/ise/v{pfsc_conf.CommonVars.ISE_VERSION}': f'/ise/v{pfsc_conf.CommonVars.ISE_VERSION}',
    }
    template = jinja_env.get_template('nginx.conf')
    return squash(template.render(
        listen_on=listen_on,
        redir_http=redir_http,
        twin_server_name=twin_server_name,
        hsts_seconds=hsts_seconds,
        server_name=server_name,
        ssl=ssl,
        basic_auth_title=basic_auth_title,
        static_redir=static_redir, static_acao=static_acao,
        loc_map=loc_map,
        **kwargs
    ))


def write_maintenance_nginx_conf(
        listen_on=80,
        ssl=False, basic_auth_title=None,
        redir_http=False,
        **kwargs):
    template = jinja_env.get_template('maintenance_nginx.conf')
    return squash(template.render(
        listen_on=listen_on,
        redir_http=redir_http,
        ssl=ssl,
        basic_auth_title=basic_auth_title,
        **kwargs
    ))
