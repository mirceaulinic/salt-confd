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

from salt_confd.parsers import SaltConfdOptionParser


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

        if self.options.states_dir:
            # check if the argument is pointing to a file on disk
            states_dir = os.path.abspath(self.options.states_dir)
            self.config['states_dirs'] = [states_dir]

        # Always local client
        self.config['file_client'] = 'local'

        # Setup file logging!
        self.setup_logfile_logger()
        verify_log(self.config)

        caller = salt.cli.caller.Caller.factory(self.config)

        caller.run()
