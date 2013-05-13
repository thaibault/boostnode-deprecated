#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# vim: set tabstop=4 shiftwidth=4 expandtab:
# vim: foldmethod=marker foldmarker=region,endregion:

# region header

'''
    This module implements features like getter and setter methods
    for implementing object orientated code.
'''
'''
    For conventions see "boostNode/__init__.py" on
    https://github.com/thaibault/boostNode
'''
'''
    The concept

    Interface class is a high level interface support for interaction with
    objects. This class transmits a full object oriented way to handle object
    oriented concepts fast and efficient.

    Getter and setter

    If you let transmit your class from the "Class" class you can use a
    getter or setter method for every property you need. A user of your class
    doesn't have to know which property has its own getter/setter, an
    universal getter/setter or nothing of them. A user can always try to access
    any property defined with an underscore at the beginning of the class with
    no underscore. If it's necessary to use a function to get or set the
    property it will be executed, otherwise not.
    If no explicit or general getter/setter is provided, the property still
    takes inaccessible. Properties which should be accessible and doesn't need
    any getter or setter method can be implemented without any underscore.
    Doing that way saves your application performance because no needless
    function calls are done.

    Getter/setter examples:

    >>> def get_example(self):
    ...     """
    ...         A special getter method for protected property "_example" which
    ...         only should read by "value = object.example".
    ...
    ...         Returns the actual value of "self._example".
    ...     """
    ...     """Do something depending on "self._example"."""
    ...     self.__dict__['_example'] += '_special_modified'
    ...     return self.__dict__['_example']

    >>> def set_example(self, value):
    ...     """
    ...         A special setter method for protected property "_example" which
    ...         should only be accessed by "object.example = some_value".
    ...
    ...         "value" The new value for "self._example".
    ...
    ...         Returns the new value of "self._example".
    ...     """
    ...     """Do something depending on "self._example"."""
    ...     self.__dict__['_example'] = value
    ...     return value

    >>> def get(self, name: builtins.str):
    ...     """
    ...         General getter method for all properties with no special getter
    ...         method.
    ...
    ...         "name" The property name which should be returned.
    ...
    ...         Returns the current value of the given property.
    ...     """
    ...     """Do something general depending on properties."""
    ...     self.__dict__[name] += '_general_modified'
    ...     return self.__dict__[name]

    >>> def set(self, name: builtins.str, value):
    ...     """
    ...         General setter method for all properties with no special setter
    ...         method.
    ...
    ...         "name" The property name which should be overwritten.
    ...         "value" The new value for the given property name.
    ...
    ...         Returns the new value of the given property.
    ...     """
    ...     """Do something general depending on properties."""
    ...     self.__dict__[name] = value
    ...     return value
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
pass
import inspect
import os
import sys

## python3.3 pass
builtins = sys.modules['__main__'].__builtins__

for number in (3, 4):
    sys.path.append(os.path.abspath(sys.path[0] + number * ('..' + os.sep)))

import boostNode.extension.dependent

# endregion


# region abstract classes

## python3.3 class Class:
class Class(builtins.object):
    '''
        The main class which is intended for passing on other class.
        It serves a scope for one application to minimize conflicts with other
        classes in the global scope.
    '''

    # region static methods

        # region public methods

            # region special methods

    @builtins.classmethod
## python3.3     def __repr__(cls: builtins.type) -> builtins.str:
    def __repr__(cls):
        '''
            Invokes if this object should describe itself by a string.

            Examples:

            >>> repr(Class())
            'Object of "Class".'
        '''
        return 'Object of "%s".' % cls.__name__

    @builtins.classmethod
## python3.3     def __str__(cls: builtins.type) -> builtins.str:
    def __str__(cls):
        '''
            Is triggered if the current object is tried to be converted into a
            string object.

            It returns the output buffer as string.

            Examples:

            >>> class Test(Class):
            ...     def __init__(self):
            ...         pass
            >>> Test()
            Object of "Test".
        '''
        return cls.__name__

            # endregion

        # endregion

    # endregion

    # region dynamic methods

        # region public method

            # region special methods

## python3.3
##     def __getattr__(
##         self: builtins.object, name: builtins.str
##     ) -> builtins.object:
    def __getattr__(self, name):
##
        '''
            Is triggered if a property was tried to be read but is
            inaccessible.

            "name" is the inaccessible property name.

            Should return the current value of the given
            property name depends on its getter method.
            Returns "None" if no getter method is accessible.

            Examples:

            >>> class TestA(Class):
            ...     _a = 'hans'
            ...     def get_a(self):
            ...         return self._a
            >>> TestA().a
            'hans'
            >>> class TestB(Class):
            ...     _a = ''
            ...     _b = ''
            ...     def __init__(self):
            ...         self._a = 'hans'
            ...         self._b = 'also hans'
            ...     def get(self, name):
            ...         if name in ('_a', '_b'):
            ...             return self.__dict__[name]
            ...         return None
            >>> TestB().b
            'also hans'
        '''
        if self.is_property(name='_' + name):
            if self.is_method(name='get_' + name):
                return builtins.getattr(self, 'get_' + name)()
            elif self.is_method(name='get'):
                return self.get(name='_' + name)
        return None

## python3.3
##     def __setattr__(
##         self, name: builtins.str, value: builtins.object
##     ) -> builtins.object:
    def __setattr__(self, name, value):
##
        '''
            Is triggered if a property was tried to overwrite but is
            inaccessible.

            "name" is the inaccessible property name.
            "value" is the new value for the given property name.

            Returns the new value of the given property name
            depending on the presence of setter method
            otherwise "None" is returned.

            Examples:

            >>> class TestA(Class):
            ...     _a = 'hans'
            ...     def set_a(self, value):
            ...         self._a = 'Not only ' + value + '. Also hans.'
            >>> test_a = TestA()
            >>> test_a.a = 'peter'
            >>> test_a._a
            'Not only peter. Also hans.'
            >>> class TestB(Class):
            ...     _a = ''
            ...     _b = ''
            ...     def __init__(self):
            ...         self._a = 'hans'
            ...         self._b = 'also hans'
            ...     def set(self, name, value):
            ...         if name in ('_a', '_b'):
            ...             self.__dict__[name] = 'hans and ' + value
            >>> test_b = TestB()
            >>> test_b.a = 'peter'
            >>> test_b._a
            'hans and peter'
        '''
        if self.is_property(name):
            if not self._setattr_helper(name, value):
                self.__dict__[name] = value
            return None
        if self.is_property(name='_' + name):
            self._setattr_helper(name, value)
            return value

            # endregion

            # region boolean methods

## python3.3     def is_method(self, name: builtins.str) -> builtins.bool:
    def is_method(self, name):
        '''
            Determines if the given class attribute is a callable method or
            something else.

            Returns "True" if the given attribute is a method or "False"
            otherwise.

            "is_property()"

            Examples:

            >>> Class().is_method('is_method')
            True
            >>> Class().is_method('not existing')
            False
        '''
        return (name in self.__class__.__dict__.keys() and
                builtins.hasattr(self.__class__.__dict__[name], '__call__'))

## python3.3     def is_property(self, name: builtins.str) -> builtins.bool:
    def is_property(self, name):
        '''
            Determines if the given class attribute is a property or
            something else.

            Returns "True" if the given attribute is a property or "False"
            otherwise.

            Examples:

            >>> Class().is_property('is_property')
            False
            >>> Class.test = 'A'
            >>> Class().is_property('test')
            True
        '''
        return (name in self.__class__.__dict__ and
                not builtins.hasattr(
                    self.__class__.__dict__[name], '__call__'))

            # endregion

        # endregion

        # region protected methods.

## python3.3
##     def _setattr_helper(
##         self, name: builtins.str, value: builtins.object
##     ) -> builtins.bool:
    def _setattr_helper(self, name, value):
##
        '''
            Helper method for "self.__setattr__()". Does the actual overwrite
            process on the given property.

            "name" is the inaccessible property name.
            "value" is the new value for the given property name.

            Returns "True" if the given property was successful overwritten or
            "False" otherwise.
        '''
        setter_name = 'set_' + name
        if self.is_method(name=setter_name):
            builtins.getattr(self, setter_name)(value)
            return True
        elif self.is_method(name='set'):
            self.set('_' + name, value)
            return True
        return False

        # endregion

    # endregion

# endregion

# region footer

boostNode.extension.dependent.Resolve(
    name=__name__, frame=inspect.currentframe(), default_caller=False)

# endregion
