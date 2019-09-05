# -*- coding: utf-8 -*-
# Copyright 2019 Mircea Ulinic. All rights reserved.
#
# The contents of this file are licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
'''
The CLI entry point module.
'''
from __future__ import absolute_import, print_function, unicode_literals

# stdlib
import re
import os
import sys
import copy
import logging

# local modules
from salt_confd.parsers import SaltConfdOptionParser

# Salt modules
import salt.loader
import salt.cli.caller
import salt.utils.jinja
import salt.utils.stringio
import salt.utils.templates
from salt.utils.verify import verify_log

# 3rd party libs
import jinja2


log = logging.getLogger(__name__)


def getv(self, value, sort_keys=True, indent=None):
    return jinja2.Markup(value)


def parse(self, parser):
    log.error(self.environment.filters)
    self.environment.filters.update({
        'getv': self.getv
    })
    if parser.stream.current.value == 'import_yaml':
        return self.parse_yaml(parser)
    elif parser.stream.current.value == 'import_json':
        return self.parse_json(parser)
    elif parser.stream.current.value == 'import_text':
        return self.parse_text(parser)
    elif parser.stream.current.value in self._load_parsers:
        return self.parse_load(parser)
    parser.fail('Unknown format ' + parser.stream.current.value,
                parser.stream.current.lineno)

salt.utils.jinja.SerializerExtension._load_parsers.update(['getv'])
salt.utils.jinja.SerializerExtension.tags.update(['getv'])
setattr(salt.utils.jinja.SerializerExtension, 'getv', getv)
setattr(salt.utils.jinja.SerializerExtension, 'parse', parse)


class SaltConfd(SaltConfdOptionParser):
    '''
    Render the template(s) to generate the configuration files.
    '''

    def run(self):
        '''
        Execute a lightweight salt-call with bespoken options.
        '''
        self.parse_args()

        if self.options.file_root:
            # check if the argument is pointing to a file on disk
            file_root = os.path.abspath(self.options.file_root)
            self.config['file_roots'] = {'base': _expand_glob_path([file_root])}

        if self.options.pillar_root:
            # check if the argument is pointing to a file on disk
            pillar_root = os.path.abspath(self.options.pillar_root)
            self.config['pillar_roots'] = {'base': _expand_glob_path([pillar_root])}

        # Always local client
        self.config['file_client'] = 'local'
        self.config['transport'] = 'tcp'

        if not self.config.get('confdir'):
            self.config['confdir'] = os.path.join(self.config['config_dir'], 'confd')

        confd_dir = os.path.join(self.config['confdir'], 'conf.d')
        templates_dir = os.path.join(self.config['confdir'], 'templates')

        self.config['file_roots']['base'].append(os.path.dirname(__file__))
        self.config['file_roots']['base'].append(templates_dir)

        # Setup file logging!
        self.setup_logfile_logger()
        verify_log(self.config)

        self.config['fun'] = 'state.apply'
        self.config['arg'] = ['confd']
        self.config['confd'] = {}

        minion_mods = salt.loader.minion_mods(self.config)
        renderers = salt.loader.render(self.config, minion_mods)

        kwargs = {}
        path_or_string = ':string:'
        rgx = re.compile(r'^(.*):\/\/(.*)$')

        for file_ in os.listdir(confd_dir):
            confd_file = os.path.join(confd_dir, file_)
            if not os.path.isfile(confd_file):
                continue
            with salt.utils.files.fopen(confd_file, 'r') as fp_:
                string = fp_.read()
                kwargs['input_data'] = string
                ret = salt.template.compile_template(
                    path_or_string,
                    renderers,
                    self.config.get('default_renderer', 'jinja|yaml'),
                    self.config.get('renderer_blacklist'),
                    self.config.get('renderer_whitelist'),
                    **kwargs
                )
                res = ret.read() if salt.utils.stringio.is_readable(ret) else ret
                if not rgx.match(res['src']):
                    res['src'] = 'salt://' + res['src']
                if not res.get('template'):
                    res['template'] = 'jinja'
                item = os.path.splitext(file_)[0]
                self.config['confd'][item] = res

        caller = salt.cli.caller.Caller.factory(self.config)
        caller.run()
