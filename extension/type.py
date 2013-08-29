#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-

# region vim modline

# vim: set tabstop=4 shiftwidth=4 expandtab:
# vim: foldmethod=marker foldmarker=region,endregion:

# endregion

# region header

'''
    This module provides mostly dynamic types/classes for checking function
    call's against a given signature. Dynamic classes means they depend on
    their context.
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

## python2.7 import __builtin__ as builtins
import builtins
import inspect
import os
import sys

'''Make boostNode packages and modules importable via relative paths.'''
for number in (3, 4):
    sys.path.append(os.path.abspath(sys.path[0] + number * ('..' + os.sep)))

import boostNode.extension.dependent
import boostNode.paradigm.objectOrientation

# endregion


# region classes

class SelfClass(boostNode.paradigm.objectOrientation.Class):
    '''Type for defining the current object of its method.'''


class SelfClassObject(boostNode.paradigm.objectOrientation.Class):
    '''Type for defining the current object of its method.'''


class Self(boostNode.paradigm.objectOrientation.Class):
    '''Type for defining the current object of its method.'''

# endregion

# region footer

'''
    Preset some variables given by introspection letting the linter know what
    globale variables are available.
'''
__logger__ = __test_mode__ = __exception__ = __module_name__ = \
    __file_path__ = None
'''Resolve cyclic dependency issues.'''
boostNode.extension.dependent.Resolve(
    name=__name__, frame=inspect.currentframe(), default_caller=False)

# endregion
