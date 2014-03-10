#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# region header

'''
    This package hold all needed aspects for an aspect orientated way of \
    programming.
'''
'''
    For conventions see "boostNode/__init__.py" on \
    https://github.com/thaibault/boostNode
'''

__author__ = 'Torben Sickert'
__copyright__ = 'see boostNode/__init__.py'
__credits__ = 'Torben Sickert',
__license__ = 'see boostNode/__init__.py'
__maintainer__ = 'Torben Sickert'
__maintainer_email__ = 't.sickert@gmail.com'
__status__ = 'stable'
__version__ = '1.0'

import inspect
import os
import sys

'''Make boostNode packages and modules importable via relative paths.'''
for number in (3, 4):
    sys.path.append(os.path.abspath(sys.path[0] + number * ('..' + os.sep)))

from boostNode import __get_all_modules__

# endregion

__all__ = __get_all_modules__()
'''Determine all modules in this folder via introspection.'''

 # region footer

'''
    Preset some variables given by introspection letting the linter know what \
    globale variables are available.
'''
__logger__ = __exception__ = __module_name__ = __file_path__ = \
    __test_mode__ = __test_buffer__ = __test_folder__ = __test_globals__ = None
if __name__ == '__main__':
    from boostNode.extension.system import CommandLine
    '''
        Extends this module with some magic environment variables to provide \
        better introspection support. A generic command line interface for \
        some code preprocessing tools is provided by default.
    '''
    CommandLine.generic_package_interface(
        name=__name__, frame=inspect.currentframe())

# endregion

# region vim modline

# vim: set tabstop=4 shiftwidth=4 expandtab:
# vim: foldmethod=marker foldmarker=region,endregion:

# endregion
