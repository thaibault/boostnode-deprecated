#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

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
__credits__ = ('Torben Sickert',)
__license__ = 'see boostNode/__init__.py'
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

boostNode.extension.dependent.Resolve(
    name=__name__, frame=inspect.currentframe(), default_caller=False)

# endregion
