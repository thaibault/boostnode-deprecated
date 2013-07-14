#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-

# region vim modline

# vim: set tabstop=4 shiftwidth=4 expandtab:
# vim: foldmethod=marker foldmarker=region,endregion:

# endregion

# region header

'''
    This package hold all needed aspects for an aspect orientated way of
    programming.
'''
'''
    For conventions see "boostNode/__init__.py" on
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

## python2.7 pass
import builtins
import inspect
import os
import sys

## python2.7 builtins = sys.modules['__main__'].__builtins__
pass

for number in (3, 4):
    sys.path.append(os.path.abspath(sys.path[0] + number * ('..' + os.sep)))

import boostNode.extension.dependent

# endregion

'''Determine all modules in this folder via introspection.'''
__all__ = boostNode.extension.dependent.Resolve.get_all()

 # region footer

if __name__ == '__main__':
    from boostNode.extension.system import CommandLine
    '''
        Extends this module with some magic environment variables to provide
        better introspection support. A generic command line interface for some
        code preprocessing tools is provided by default.
    '''
    CommandLine.generic_package_interface(
        name=__name__, frame=inspect.currentframe())

# endregion
