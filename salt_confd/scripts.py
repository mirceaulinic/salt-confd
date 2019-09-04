# -*- coding: utf-8 -*-

import sys

from salt.scripts import _install_signal_handlers


def salt_confd():
    '''
    Execute a salt convenience routine.
    '''
    import salt_confd.cli

    if '' in sys.path:
        sys.path.remove('')
    client = salt_confd.cli.SaltConfd()
    _install_signal_handlers(client)
    client.run()


if __name__ == '__main__':
    salt_confd()
