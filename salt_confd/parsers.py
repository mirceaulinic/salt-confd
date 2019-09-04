# -*- coding: utf-8 -*-

import sys
import logging
import optparse
import multiprocessing

import salt_confd.version

from salt.ext import six
import salt.version
import salt.utils.args
import salt.utils.parsers
import salt.config as config


def salt_information():
    '''
    Return version of Salt and salt-sproxy.
    '''
    yield 'Salt', salt.version.__version__
    yield 'Salt Confd', salt_confd.version.__version__


def dependency_information(include_salt_cloud=False):
    '''
    Report versions of library dependencies.

    This function has been ported from
    https://github.com/saltstack/salt/blob/develop/salt/version.py
    and extended here to collect the version information for several more
    libraries that may be necessary for various Proxy (or Execution) Modules.
    '''
    libs = [
        ('Python', None, sys.version.rsplit('\n')[0].strip()),
        ('timelib', 'timelib', 'version'),
        ('dateutil', 'dateutil', '__version__'),
        ('gitpython', 'git', '__version__'),
    ]
    if include_salt_cloud:
        libs.append(('Apache Libcloud', 'libcloud', '__version__'))

    for name, imp, attr in libs:
        if imp is None:
            yield name, attr
            continue
        try:
            imp = __import__(imp)
            version = getattr(imp, attr)
            if callable(version):
                version = version()
            if isinstance(version, (tuple, list)):
                version = '.'.join(map(str, version))
            yield name, version
        except Exception:
            yield name, None

salt.version.salt_information = salt_information
salt.version.dependency_information = dependency_information


class SaltConfdOptionParser(six.with_metaclass(salt.utils.parsers.OptionParserMeta,
                                              salt.utils.parsers.OptionParser,
                                              salt.utils.parsers.ConfigDirMixIn,
                                              salt.utils.parsers.ExecutorsMixIn,
                                              salt.utils.parsers.MergeConfigMixIn,
                                              salt.utils.parsers.LogLevelMixIn,
                                              salt.utils.parsers.OutputOptionsMixIn,
                                              salt.utils.parsers.HardCrashMixin,
                                              salt.utils.parsers.SaltfileMixIn,
                                              salt.utils.parsers.ArgsStdinMixIn,
                                              salt.utils.parsers.ProfilingPMixIn,
                                              salt.utils.parsers.NoParseMixin,
                                              salt.utils.parsers.CacheDirMixIn)):

    VERSION = salt_confd.version.__version__

    epilog = (
        'You can find additional help about %prog at '
        'https://salt-confd.readthedocs.io/en/latest/'
    )

    description = (
        'salt-confd is used to manage configuration files for local apps'
    )

    usage = '%prog [options]'

    # ConfigDirMixIn config filename attribute
    _config_filename_ = 'confd.yml'

    # LogLevelMixIn attributes
    _default_logging_level_ = config.DEFAULT_MINION_OPTS['log_level']
    _default_logging_logfile_ = config.DEFAULT_MINION_OPTS['log_file']

    def _mixin_setup(self):
        self.add_option(
            '--return',
            default='',
            metavar='RETURNER',
            help=('Set salt-call to pass the return data to one or many '
                  'returner interfaces.')
        )
        self.add_option(
            '--file-root',
            default=None,
            help='Set this directory as the base file root.'
        )
        self.add_option(
            '--pillar-root',
            default=None,
            help='Set this directory as the base pillar root.'
        )
        self.add_option(
            '--confdir',
            default='/etc/salt/confd',
            help='The Salt confd conf directory'
        )
        self.add_option(
            '--retcode-passthrough',
            default=False,
            action='store_true',
            help=('Exit with the salt call retcode and not the salt binary '
                  'retcode.')
        )
        self.add_option(
            '--metadata',
            default=False,
            dest='print_metadata',
            action='store_true',
            help=('Print out the execution metadata as well as the return. '
                  'This will print out the outputter data, the return code, '
                  'etc.')
        )
        self.add_option(
            '--set-metadata',
            dest='metadata',
            default=None,
            metavar='METADATA',
            help=('Pass metadata into Salt, used to search jobs.')
        )
        self.add_option(
            '--skip-grains',
            default=False,
            action='store_true',
            help=('Do not load grains.')
        )
        self.add_option(
            '--refresh-grains-cache',
            default=False,
            action='store_true',
            help=('Force a refresh of the grains cache.')
        )
        self.add_option(
            '--test', '--dry-run', '--noop',
            dest='test',
            action='store_true',
            default=False,
            help=('Dry run, show pending changes.')
        )
        self.add_option(
            '--onetime',
            dest='onetime',
            action='store_true',
            default=False,
            help=('Run once and exit.')
        )

    def setup_config(self):
        return config.minion_config(self.get_config_file_path(),
                                    cache_minion_id=True)
