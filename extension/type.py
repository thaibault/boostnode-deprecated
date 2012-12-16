#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# region header

'''
    This module provides mostly dynamic types/classes for checking function
    call's against a given signature. Dynamic classes means they depend on
    their context.
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
import library.paradigm.objectOrientation

# endregion


# region classes

class SelfClass(library.paradigm.objectOrientation.Class):
    '''Type for defining the current object of its method.'''


class SelfClassObject(library.paradigm.objectOrientation.Class):
    '''Type for defining the current object of its method.'''


class Self(library.paradigm.objectOrientation.Class):
    '''Type for defining the current object of its method.'''

# endregion

# region footer

library.extension.dependent.Resolve(
    name=__name__, frame=inspect.currentframe(), default_caller=False)

# endregion
