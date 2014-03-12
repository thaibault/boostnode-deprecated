#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# region header

'''
    This module provides mostly dynamic types/classes for checking function \
    call's against a given signature. Dynamic classes means they depend on \
    their context.
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

class Null:

    '''
        Special none type if "builtins.None" should be distinguished from a \
        real dummy value.
    '''


class SelfClass:

    '''Type for defining the current object of its method.'''


class SelfClassObject:

    '''Type for defining the current object of its method.'''


class Self:

    '''Type for defining the current object of its method.'''


class Model(builtins.type):

    '''Creates a model for orm based using.'''

    # region static methods

        # region public

            # region special

## python3.3
##     def __new__(
##         cls: SelfClass, class_name: builtins.str,
##         base_classes: builtins.tuple, class_scope: builtins.dict,
##         *arguments: (builtins.type, builtins.object),
##         **keywords: (builtins.type, builtins.object)
##     ) -> builtins.type:
    def __new__(
        cls, class_name, base_classes, class_scope, *arguments, **keywords
    ):
##
        '''
            Triggers if a new instance is created. Set the default name for \
            an orm instance.

            **class_name**   - Name of class to create.

            **base_classes** - A tuple of base classes for class to create.

            **class_scope**  - A dictionary object to define properties and \
                               methods for new class.

            Additional arguments and keywords are forwarded to python's \
            native "builtins.type" function.

            Returns the newly created class.

            Examples:

            >>> if sys.version_info.major < 3:
            ...     class UserModel: __metaclass__ = Model
            ... else:
            ...     exec('class UserModel(metaclass=Model): pass')
        '''
        from boostNode.extension.native import String

        class_scope['__tablename__'] = class_scope['__table_name__'] = \
            class_scope['db_table'] = String(
                class_name
            ).camel_case_to_delimited().content
        '''Take this method name via introspection.'''
        return builtins.getattr(
            builtins.super(Model, cls), inspect.stack()[0][3]
        )(cls, class_name, base_classes, class_scope, *arguments, **keywords)

            # endregion

        # endregion

    # endregion

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

# region vim modline

# vim: set tabstop=4 shiftwidth=4 expandtab:
# vim: foldmethod=marker foldmarker=region,endregion:

# endregion
