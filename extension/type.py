#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# region vim modline

# vim: set tabstop=4 shiftwidth=4 expandtab:
# vim: foldmethod=marker foldmarker=region,endregion:

# endregion

# region header

'''
    This module provides mostly dynamic types/classes for checking function \
    call's against a given signature. Dynamic classes means they depend on \
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

## python3.3 import builtins
import __builtin__ as builtins
import inspect
import os
import sys

'''Make boostNode packages and modules importable via relative paths.'''
for number in (3, 4):
    sys.path.append(os.path.abspath(sys.path[0] + number * ('..' + os.sep)))

# endregion


# region classes

class SelfClass:

    '''Type for defining the current object of its method.'''


class SelfClassObject:

    '''Type for defining the current object of its method.'''


class Self:

    '''Type for defining the current object of its method.'''


class MetaModel(builtins.type):

    '''Creates a model for orm based using.'''

## python3.3
##     def __new__(
##         cls: SelfClass, class_name: builtins.str, base_classes: builtins.tuple,
##         class_scope: builtins.dict,
##         *arguments: (builtins.type, builtins.object),
##         **keywords: (builtins.type, builtins.object)
##     ):
    def __new__(
        cls, class_name, base_classes, class_scope, *arguments, **keywords
    ):
##
        '''
            Triggers if a new instance is created. Set the default name for
            an orm instance.

            TODO
        '''
        class_scope['__tablename__'] = class_scope['__table__'] = \
            class_name.lower()
        return builtins.super(MetaModel, cls).__new__(
            cls, class_name, base_classes, class_scope, *arguments, **keywords)


class Model(builtins.object):

    '''Represents an abstract model for an orm base model.'''

## python3.3     def __repr__(self: Self):
    def __repr__(self):
        '''
            Describes the model as string.

            TODO
        '''
        if self.__dict__:
            property_descriptions = ''
            index = 1
            for name, value in self.__dict__.items():
                if index == builtins.len(self.__dict__):
                    property_descriptions += ' and '
                elif index != 1:
                    property_descriptions += ', '
                property_descriptions += '"%s": "%s"' % (name, value)
                index += 1
            return '%s with properties %s.' % (
                self.__class__.__name__, property_descriptions)
        return self.__class__.__name__

# endregion

# region footer

'''
    Preset some variables given by introspection letting the linter know what \
    globale variables are available.
'''
__logger__ = __exception__ = __module_name__ = __file_path__ = \
    __test_mode__ = __test_buffer__ = __test_folder__ = __test_globals__ = None
'''
    Extends this module with some magic environment variables to provide \
    better introspection support. A generic command line interface for some \
    code preprocessing tools is provided by default.
'''
if __name__ == '__main__':
    from boostNode.extension.native import Module
    Module.default(
        name=__name__, frame=inspect.currentframe(), default_caller=False)

# endregion
