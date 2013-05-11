#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-

# vim: set tabstop=4 shiftwidth=4 expandtab:
# vim: foldmethod=marker foldmarker=region,endregion:

# region header

'''
    This package provides a number of extension by dealing with often used
    things like underlying operating system, file objects, python modules,
    or I/O operations.
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

# endregion

'''Determine all modules in this folder via introspection.'''
__all__ = builtins.list(builtins.set(builtins.map(
    lambda name: name[:name.rfind('.')],
    builtins.filter(
        lambda name: ((name.endswith('.py') or
                      name.endswith('.pyc')) and
                      not name.startswith('__init__.')),
        os.listdir(
            sys.path[0][:- 1 -builtins.len(os.path.basename(sys.path[0]))] if
            os.path.isfile(sys.path[0]) else sys.path[0])))))

# region footer

if __name__ == '__main__':
    from boostNode.extension.system import CommandLine
    CommandLine.generic_package_interface(
        name=__name__, frame=inspect.currentframe())

# endregion
