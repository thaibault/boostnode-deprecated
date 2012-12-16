#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# region header

'''
    This package provides base classes and functions for implementing some
    useful programming concepts like object or aspect orientation.
'''
'''Conventions: see "../__init__.py"'''

__author__ = 'Torben Sickert'
__copyright__ = 'see ../__init__.py'
__credits__ = ('Torben Sickert',)
__license__ = 'see ../__init__.py'
__maintainer__ = 'Torben Sickert'
__maintainer_email__ = 't.sickert@gmail.com'
__status__ = 'stable'
__version__ = '1.0'

## python3.3 import builtins
pass
import inspect
import os
import sys

## python3.3 pass
builtins = sys.modules['__main__'].__builtins__

sys.path.append(os.path.abspath(sys.path[0] + 3 * ('..' + os.sep)))
sys.path.append(os.path.abspath(sys.path[0] + 4 * ('..' + os.sep)))

import library.extension.dependent

# endregion

'''Determine all modules in this folder via introspection.'''
__all__ = library.extension.dependent.Resolve.get_all()

# region footer

if __name__ == '__main__':
    from library.extension.system import CommandLine
    CommandLine.generic_package_interface(
        name=__name__, frame=inspect.currentframe())

# ednregion
