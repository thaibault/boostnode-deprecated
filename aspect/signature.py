#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# region header

'''
    This module provides functions for checking function call's against a
    given signature.
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

## python3.3
## import builtins
## import collections
pass
##
import copy
import functools
import inspect
import os
import sys
## python3.3 import types
pass

## python3.3 pass
builtins = sys.modules['__main__'].__builtins__

sys.path.append(os.path.abspath(sys.path[0] + 3 * ('..' + os.sep)))
sys.path.append(os.path.abspath(sys.path[0] + 4 * ('..' + os.sep)))

import boostNode.extension.dependent
import boostNode.extension.native
import boostNode.extension.system
import boostNode.extension.type
import boostNode.paradigm.aspectOrientation

# endregion


# region functions

@boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
## def add_check(point_cut: builtins.str) -> builtins.list:
def add_check(point_cut):
##
    '''
        Adds signature checking in functions and methods for given point cuts.

        Examples:

        >>> add_check(point_cut='^.*test$') # doctest: +ELLIPSIS
        [...]
        >>> @boostNode.paradigm.aspectOrientation.JointPoint
        ... def test():
        ...     pass
    '''
## python3.3
##     boostNode.paradigm.aspectOrientation.ASPECTS.append(
##         {'advice': (
##             {'callback': CheckArguments,
##              'event': 'call'},
##             {'callback': CheckReturnValue,
##              'event': 'return'}),
##          'point_cut': point_cut})
    pass
##
    return boostNode.paradigm.aspectOrientation.ASPECTS

# endregion


# region abstract classes

## python3.3 class CheckObject:
class CheckObject(builtins.object):
    '''
        Checks a function call against a given specification. This class serves
        as helper class.
    '''

    # region dynamic properties

        # region public properties

    '''
        Holds informations about the function and their bounding that is to be
        checked.
    '''
    class_object = object = function = None

        # endregion

        # region protected properties

    '''
        Saves informations in which way the give method is used. It could by
        something like "builtins.staticmethod" or "builtins.classmethod".
    '''
    _method_type = None

        # endregionza

    # endregion

    # region static methods

        # region protected methods

            # region boolean functions

    @builtins.classmethod
## python3.3
##     def _is_multiple_type(
##         cls: boostNode.extension.type.SelfClass,
##         type: (builtins.object, builtins.type)
##     ) -> builtins.bool:
    def _is_multiple_type(cls, type):
##
        '''
            Check wether a given specification allows multiple types.
        '''
        return(
            builtins.isinstance(type, (builtins.tuple, builtins.list)) and
            builtins.len(type) > 1 and
            builtins.isinstance(type[0], builtins.type))

    @builtins.classmethod
## python3.3
##     def _is_right_type(
##         cls: boostNode.extension.type.SelfClass, given_type: builtins.type,
##         expected_type: builtins.type
##     ) -> builtins.bool:
    def _is_right_type(cls, given_type, expected_type):
##
        '''
            Check wether a given type is expected type or given type is a
            subclass of expected type.

            Fixes bug that "bool" is a subtype of "int".
        '''
        return (given_type is expected_type or
                builtins.issubclass(given_type, expected_type) and
                not (given_type is builtins.bool and
                     expected_type is builtins.int))

            # endregion

        # endregion

    # endregion

    # region dynamic methods

        # region public methods

            # region special methods

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def __init__(cls: boostNode.extension.type.SelfClass) -> None:
    def __init__(cls):
##
        '''
            If this method wasn't be overwridden an exception is raised.

            Examples:

            >>> CheckObject() # doctest: +ELLIPSIS
            Traceback (most recent call last):
            ...
            NotImplementedError: Method "__init__" wasn't implemented by "Ob...
        '''
        raise boostNode.extension.native.Object\
            .determine_abstract_method_exception(
                abstract_class_name=CheckObject.__name__)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def __repr__(self: boostNode.extension.type.Self) -> builtins.str:
    def __repr__(self):
##
        '''
            Describes current properties of analysing object.

            Examples:

            >>> def test(self):
            ...     pass
            >>> class A(CheckObject):
            ...     def __init__(self):
            ...         self.function = test
            ...         self._method_type = staticmethod
            >>> repr(A()) # doctest: +ELLIPSIS
            'Object of "A" with class object "None", object "None", called...'
        '''
        class_name = 'None'
        if self.__class__ is not None:
            class_name = self.__class__.__name__
        class_object_name = 'None'
        if self.class_object is not None:
            class_object_name = self.class_object.__name__
        return ('Object of "{class_name}" with class object "'
                '{class_object_name}", object "{object}", called function '
                '"{function}" and method type "{method_type}".'.format(
                    class_name=class_name,
                    class_object_name=class_object_name,
                    object=builtins.repr(self.object),
                    function=builtins.str(self.function),
                    method_type=builtins.str(self._method_type)))

            # endregion

        # endregion

    # region getter methods

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def get_function_path(
##         self: boostNode.extension.type.Self
##     ) -> builtins.str:
    def get_function_path(self):
##
        '''
            Returns an object depended function description.

            Examples:

            >>> def test():
            ...     pass
            >>> class A(CheckObject):
            ...     def __init__(self):
            ...         self.function = test
            ...         self._method_type = staticmethod
            >>> a = A()

            >>> a.get_function_path()
            'test'
        '''
## python3.3
##         return self.function.__qualname__
        if self.class_object is not None:
            return self.class_object.__name__ + '.' + self.function.__name__
        return self.function.__name__
##

        # endregion

        # region protected methods

## python3.3
##     def _handle_multiple_types(
##         self: boostNode.extension.type.Self, value: builtins.object,
##         given_type: builtins.type,
##         expected_types: (builtins.tuple, builtins.list), name='return value'
##     ) -> boostNode.extension.type.Self:
    def _handle_multiple_types(
        self, value, given_type, expected_types, name='return value'
    ):
##
        '''
            Check an argument which is specified with multiple types.
        '''
        if(builtins.isinstance(expected_types, builtins.tuple) and
           not self._check_again_multiple_types(
               value, given_type, expected_types)):
            raise __exception__(
                '"{function_path}()" expects one instance of '
                '{types} for "{name}" but received "{type_name}".'.format(
                    function_path=self.get_function_path(),
                    types=self._join_types(types=expected_types),
                    name=name, type_name=given_type.__name__))
        elif(builtins.isinstance(expected_types, builtins.list) and
             not value in expected_types):
            raise __exception__(
                '"{function_path}()" expects one value of '
                '{types} for "{name}" but received "{type_name}".'.format(
                    function_path=self.get_function_path(),
                    types=self._join_types(types=expected_types),
                    name=name, type_name=given_type.__name__))
        return self

## python3.3
##     def _check_type(
##         self: boostNode.extension.type.Self, expected_type: builtins.type,
##         given_type: builtins.type, value: builtins.object,
##         name='return value'
##     ) -> boostNode.extension.type.Self:
    def _check_type(
        self, expected_type, given_type, value, name='return value'
    ):
##
        '''
            Checks if the given value is of its specified type.
        '''
        if not (expected_type is builtins.type(None) or
                expected_type is given_type or
                builtins.issubclass(given_type, expected_type)):
            if expected_type is boostNode.extension.type.Self:
                self._handle_self(name, value)
            elif(expected_type is boostNode.extension.type.SelfClass or
                 expected_type is boostNode.extension.type.SelfClassObject):
                self._handle_self_class(expected_type, given_type, name, value)
            else:
                raise __exception__(
                    '"{function_path}()" expects instance of '
                    '"{object}" for "{name}" but received "{type}" '
                    '({value}).'.format(
                        function_path=self.get_function_path(),
                        object=expected_type.__name__, name=name,
                        type=given_type.__name__, value=builtins.repr(value)))
        return self

## python3.3
##     def _handle_self(
##         self: boostNode.extension.type.Self, name: builtins.str,
##         value: builtins.object
##     ) -> boostNode.extension.type.Self:
    def _handle_self(self, name, value):
##
        '''
            Checks given argument value against the methods bounded object.

            Examples:

            >>> def test():
            ...     pass
            >>> class A(CheckObject):
            ...     def __init__(self):
            ...         self.function = test
            ...         self._method_type = staticmethod
            >>> a = A()

            >>> a._handle_self(
            ...     'argument_name', 'value'
            ... ) # doctest: +ELLIPSIS +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            boostNode.extension.native.SignatureError: ...instance so "self" ...

            >>> a.object = A()
            >>> a._handle_self(
            ...     'argument_name', 'value'
            ... ) # doctest: +ELLIPSIS +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            boostNode.extension.native.SignatureError:... but received "'value'".

            >>> b = A()
            >>> a.object = b
            >>> a._handle_self(
            ...     'argument_name', b
            ... ) # doctest: +ELLIPSIS +IGNORE_EXCEPTION_DETAIL
            Object of "A" with class object "None", object "Object...
        '''
        if self.object is None:
            raise __exception__(
                '"{function_path}()" wasn\'t called from '
                'an instance so "self" for "{name}" couldn\'t be '
                'determined.'.format(
                    function_path=self.get_function_path(), name=name))
        elif value is not self.object:
            raise __exception__(
                '"{function_path}()" expects "{object} '
                '(self)" for "{name}" but received "{value}".'.format(
                    function_path=self.get_function_path(),
                    object=builtins.repr(self.object), name=name,
                    value=builtins.repr(value)))
        return self

## python3.3
##     def _handle_self_class(
##         self: boostNode.extension.type.Self,
##         expected_type: [boostNode.extension.type.SelfClass,
##                         boostNode.extension.type.SelfClassObject],
##         given_type: builtins.type, name: builtins.str,
##         value: builtins.object
##     ) -> boostNode.extension.type.Self:
    def _handle_self_class(self, expected_type, given_type, name, value):
##
        '''
            Checks given argument value against the methods bounded class.

            Examples:

            >>> def test():
            ...     pass
            >>> class A(CheckObject):
            ...     def __init__(self):
            ...         self.function = test
            ...         self._method_type = staticmethod
            >>> a = A()

            >>> a._handle_self_class(
            ...     boostNode.extension.type.SelfClass, str, 'argument_name',
            ...     'value') # doctest: +ELLIPSIS +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            boostNode.extension.native.SignatureError:..." wasn't called from ...

            >>> a.class_object = A
            >>> a._handle_self_class(
            ...     boostNode.extension.type.SelfClass, str, 'argument_name',
            ...     'value') # doctest: +ELLIPSIS +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            boostNode.extension.native.SignatureError: "A.test()" expects ...

            >>> a.class_object = A
            >>> a._handle_self_class(
            ...     boostNode.extension.type.SelfClassObject, str,
            ...     'argument_name', 'value'
            ... ) # doctest: +ELLIPSIS +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            boostNode.extension.native.SignatureError: "A.test()" expects inst...

            >>> a.class_object = A
            >>> a._handle_self_class(
            ...     boostNode.extension.type.SelfClass, A, 'argument_name', A
            ... ) # doctest: +ELLIPSIS
            Object of "A" with class object "A", object "None", called func...

            >>> a.class_object = A
            >>> a._handle_self_class(
            ...     boostNode.extension.type.SelfClassObject, A, 'argument_name',
            ...     a) # doctest: +ELLIPSIS
            Object of "A" with class object "A", object "None", called funct...
        '''
        if self.class_object is None:
            raise __exception__(
                '"{function_path}()" wasn\'t called from '
                'a class so "self class" for "{name}" couldn\'t be '
                'determined.'.format(
                    function_path=self.get_function_path(), name=name))
        elif(expected_type is boostNode.extension.type.SelfClass and
             value is not self.class_object):
            raise __exception__(
                '"{function_path}()" expects "{object} '
                '(self class)" for "{name}" but "{type}" ({value}) '
                'received.'.format(
                    function_path=self.get_function_path(),
                    object=self.class_object, name=name,
                    type=given_type.__name__,
                    value=builtins.repr(value)))
        elif(expected_type is
             boostNode.extension.type.SelfClassObject and
             given_type is not self.class_object):
            raise __exception__(
                '"{function_path}()" expects instance of '
                '"{object} (self class)" for "{name}" but "{type}" '
                '({value}) received.'.format(
                    function_path=self.get_function_path(),
                    object=self.class_object, name=name,
                    type=given_type.__name__,
                    value=builtins.repr(value)))
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _check_again_multiple_types(
##         self: boostNode.extension.type.Self, value: builtins.object,
##         given_type: builtins.type, expected_types: collections.Iterable
##     ) -> builtins.bool:
    def _check_again_multiple_types(
        self, value, given_type, expected_types
    ):
##
        '''
            Checks if given value is one of a set of types.
        '''
        for expected_type in expected_types:
            if self._is_right_type(given_type, expected_type):
                return True
        return(boostNode.extension.type.Self in expected_types and
               value is self.object or
               boostNode.extension.type.SelfClass in expected_types and
               value is self.class_object or
               boostNode.extension.type.SelfClassObject in expected_types and
               given_type is self.class_object)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _join_types(
##         self: boostNode.extension.type.Self, types: collections.Iterable
##     ) -> builtins.str:
    def _join_types(self, types):
##
        '''
            Join given types for pretty error message presentation.
        '''
        if builtins.len(types) < 2:
            return types[0]
        output = ''
        for type in types:
            if type is boostNode.extension.type.Self:
                output += '"' + builtins.str(self.object) + ' (self)"'
            elif type is boostNode.extension.type.SelfClass:
                output += '"' + self.class_object.__name__ + ' (self class)"'
            elif type is boostNode.extension.type.SelfClassObject:
                output += '"' + self.class_object.__name__ +\
                    ' (self class object)"'
            else:
                output += '"' + type.__name__ + '"'
            if type is types[-2]:
                output += ' or '
            elif type is not types[-1]:
                output += ', '
        return output

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _check_value(
##         self: boostNode.extension.type.Self,
##         expected_value: builtins.object, value: builtins.object,
##         name='return value'
##     ) -> boostNode.extension.type.Self:
    def _check_value(self, expected_value, value, name='return value'):
##
        '''
            Checks if the given argument value is equal the specified
            argument value.
        '''
        if expected_value != value:
            raise __exception__(
                '"{function_path}()" expects value '
                '"{expected_value}" for "{name}" but received '
                '"{value}".'.format(
                    function_path=self.get_function_path(),
                    expected_value=expected_value, name=name, value=value))
        return self

        # endregion

    # endregion

# endregion


# region classes

class Check(boostNode.paradigm.aspectOrientation.FunctionDecorator):
## python3.3
##     '''
##         This function provides function and method signature checking.
##         An exception is raised on invalid signature implementation.
##
##         There are several possibilities to specify a given argument or
##         the return value:
##
##         1. Specify a type.
##         2. Specify a number of types via a tuple.
##         3. Specify a number of types expected as values explicit via list.
##         4. Specify an explicit value.
##         5. Specify type implicit by setting a default value.
##         6. Specify current instance via "boostNode.extension.type.Self".
##         7. Specify any instance of the current class via
##            "boostNode.extension.type.SelfClassObject".
##         8. Specify the current Class type (interpret as value) for static
##            methods via "boostNode.extension.type.SelfClass".
##
##         Examples:
##
##         >>> @Check
##         ... def test(num: builtins.int, name: builtins.str) -> tuple:
##         ...     return num, name
##         >>> test(3, 'hans')
##         (3, 'hans')
##
##         >>> test('hans', 'hans') # doctest: +ELLIPSIS
##         Traceback (most recent call last):
##         ...
##         boostNode.extension.native.SignatureError: ..."int" for "num" b...
##
##         >>> @Check
##         ... def test() -> builtins.int:
##         ...     return 'hans'
##         >>> test() # doctest: +ELLIPSIS
##         Traceback (most recent call last):
##         ...
##         boostNode.extension.native.SignatureError: ...int" for "return ...
##
##         >>> @Check
##         ... def test(param: 5) -> None:
##         ...     variable = param * 2
##         >>> test(4) # doctest: +ELLIPSIS
##         Traceback (most recent call last):
##         ...
##         boostNode.extension.native.SignatureError: ...m" but received "4".
##
##         >>> @Check
##         ... def test(param: (builtins.str, builtins.bool)) -> True:
##         ...     return True
##         >>> test(True)
##         True
##         >>> test('hans')
##         True
##         >>> test(5) # doctest: +ELLIPSIS
##         Traceback (most recent call last):
##         ...
##         boostNode.extension.native.SignatureError: ...r" or "bool" for ...
##
##         >>> @Check
##         ... def test(param='hans') -> builtins.str:
##         ...     return param
##         >>> test('peter')
##         'peter'
##         >>> test('hans')
##         'hans'
##         >>> test(param='klaus')
##         'klaus'
##         >>> test(4) # doctest: +ELLIPSIS
##         Traceback (most recent call last):
##         ...
##         boostNode.extension.native.SignatureError: ...tr" for "param" b...
##
##         >>> @Check
##         ... def test(a='hans', b='and peter') -> builtins.str:
##         ...     return a + ' ' + b
##         >>> test('klaus')
##         'klaus and peter'
##         >>> test('hans', 'and fritz')
##         'hans and fritz'
##         >>> test('peter', b='and hans')
##         'peter and hans'
##         >>> test(b='and hans')
##         'hans and hans'
##
##         >>> @Check
##         ... def test() -> None:
##         ...     pass
##         >>> test('klaus') # doctest: +ELLIPSIS
##         Traceback (most recent call last):
##         ...
##         TypeError: too many positional arguments
##         >>> test(b='and hans')
##         Traceback (most recent call last):
##         ...
##         TypeError: too many keyword arguments
##         >>> test()
##
##         >>> @Check
##         ... def test(*args: builtins.str, **kw: builtins.str) -> None:
##         ...     pass
##         >>> test('klaus')
##         >>> test()
##         >>> test('hans', 5) # doctest: +ELLIPSIS
##         Traceback (most recent call last):
##         ...
##         boostNode.extension.native.SignatureError: ... for "2. argument" ...
##         >>> test('hans', a='peter')
##         >>> test(a='peter', b=5) # doctest: +ELLIPSIS
##         Traceback (most recent call last):
##         ...
##         boostNode.extension.native.SignatureError: ..."str" for "b" but...
##
##         >>> @Check
##         ... def test(*args: (builtins.str, builtins.int)) -> None:
##         ...     pass
##         >>> test('klaus', 5)
##         >>> test(True) # doctest: +ELLIPSIS
##         Traceback (most recent call last):
##         ...
##         boostNode.extension.native.SignatureError: ...r" or "int" for "...
##
##         >>> @Check
##         ... def test(**kw: (builtins.str, builtins.int)) -> None:
##         ...     pass
##         >>> test(a='klaus', b=5)
##         >>> test(a=True) # doctest: +ELLIPSIS
##         Traceback (most recent call last):
##         ...
##         boostNode.extension.native.SignatureError: ...r" or "int" for "...
##
##         >>> @Check
##         ... def test(give) -> (builtins.str, builtins.int):
##         ...     return give
##         >>> test('klaus')
##         'klaus'
##         >>> test(5)
##         5
##         >>> test(True) # doctest: +ELLIPSIS
##         Traceback (most recent call last):
##         ...
##         boostNode.extension.native.SignatureError: ...r" or "int" for "...
##
##         >>> class test:
##         ...     @Check
##         ...     def method(self) -> boostNode.extension.type.Self:
##         ...         return 5
##         >>> test().method() # doctest: +ELLIPSIS
##         Traceback (most recent call last):
##         ...
##         boostNode.extension.native.SignatureError: ...self...turn value...
##
##         >>> class test:
##         ...     @Check
##         ...     def method(self) -> boostNode.extension.type.Self:
##         ...         return self
##         >>> test().method() # doctest: +ELLIPSIS
##         <...test object at 0x...>
##
##         >>> class test:
##         ...     @Check
##         ...     def method(self) -> boostNode.extension.type.Self:
##         ...         return test()
##         >>> test().method() # doctest: +ELLIPSIS
##         Traceback (most recent call last):
##         ...
##         boostNode.extension.native.SignatureError: ...method()" expects...
##
##         >>> class test:
##         ...     @Check
##         ...     def m(self) -> boostNode.extension.type.SelfClassObject:
##         ...         return test()
##         >>> test().m() # doctest: +ELLIPSIS
##         <...test object at 0x...>
##
##         >>> class test:
##         ...     @Check
##         ...     def method(self) -> boostNode.extension.type.Self:
##         ...         return self
##         >>> test().method() # doctest: +ELLIPSIS
##         <...test object at 0x...>
##     '''
    '''
       This class is needed to be compatiable with future implementations.
    '''
##

    # region dynamic methods

        # region protected methods

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def get_wrapper_function(
##         self: boostNode.extension.type.Self
##     ) -> (types.FunctionType, types.MethodType):
##         '''
##             Returns a wrapper function for the function to be checked.
##
##             Examples:
##
##             >>> def a(a: int):
##             ...     return a
##             >>> Check(a).get_wrapper_function() # doctest: +ELLIPSIS
##             <function a at ...>
##
##             >>> Check(a).get_wrapper_function()(5)
##             5
##
##             >>> Check(a).get_wrapper_function()(
##             ...     'hans') # doctest: +ELLIPSIS +IGNORE_EXCEPTION_DETAIL
##             Traceback (most recent call last):
##             ...
##             boostNode.extension.native.SignatureError: "a()" expects instan...
##         '''
##         @functools.wraps(self.function)
##         def wrapper_function(
##             *arguments: builtins.object, **keywords: builtins.object
##         ) -> builtins.object:
##             '''
##                 Wrapper function for function to be checked.
##                 Does the argument and return value checks.
##                 Runs the function to be checked and returns their return
##                 value.
##             '''
##             arguments = self._determine_arguments(arguments)
##             CheckArguments(
##                 self.class_object, self.object, self.function, arguments,
##                 keywords
##             ).aspect()
##             return_value = self.function(*arguments, **keywords)
##             return CheckReturnValue(
##                 self.class_object, self.object, self.function, arguments,
##                 keywords, return_value
##             ).aspect()
##         return wrapper_function
    def get_wrapper_function(self):
        '''
           Dummy method to be compatible to newer features.

           Examples:

           >>> def a(a):
           ...     return a
           >>> Check(a).get_wrapper_function() # doctest: +ELLIPSIS
           <function a at ...>

           >>> Check(a).get_wrapper_function()(5)
           5
        '''
        return self.function
##

        # endregion

    # endregion


class CheckArguments(
    boostNode.paradigm.aspectOrientation.CallJointPoint, CheckObject
):
    '''Checks arguments given to a function again their specification.'''

    # region dynamic methods

        # region public methods

## python3.3
##     def aspect(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def aspect(self):
##
        '''
            This functions could be used as decorator function or aspects to
            implement argument type check for each function call.
        '''
        if builtins.hasattr(self.function, '__annotations__'):
            '''
                If there aren't any specifications (signature), the given
                function could be given back unmodified.
            '''
            for argument in self.argument_specifications:
                self._check_argument(argument)
        return self

        # endregion

        # region protected methods

## python3.3
##     def _check_argument_cases(
##         self: boostNode.extension.type.Self,
##         argument: boostNode.paradigm.aspectOrientation.Argument,
##     ) -> boostNode.extension.type.Self:
    def _check_argument_cases(self, argument):
##
        '''
            Handles the different possibilities an argument could be
            specified. It could be specified by a given type, multiple
            types, implicit type through an default value or an explicit
            value.
        '''
        if builtins.isinstance(argument.annotation, builtins.type):
            return self._check_type(
                expected_type=argument.annotation,
                given_type=builtins.type(argument.value),
                value=argument.value, name=argument.name)
        elif self._is_multiple_type(type=argument.annotation):
            return self._handle_multiple_types(
                value=argument.value, given_type=builtins.type(argument.value),
                expected_types=argument.annotation, name=argument.name)
        return self._check_value(
            expected_value=argument.annotation, value=argument.value,
            name=argument.name)

## python3.3
##     def _check_argument(
##         self: boostNode.extension.type.Self,
##         argument: boostNode.paradigm.aspectOrientation.Argument
##     ) -> boostNode.extension.type.Self:
    def _check_argument(self, argument):
##
        '''
            Checks an argument. No matter if argument was given by
            its keyword or not.
        '''
        if argument.default is inspect.Parameter.empty:
            if argument.annotation is not inspect.Parameter.empty:
                self._check_argument_cases(argument)
        else:
            self._check_type(
                expected_type=builtins.type(argument.default),
                given_type=builtins.type(argument.value),
                value=argument.value, name=argument.name)
        return self

        # endregion

    # endregion


class CheckReturnValue(
    boostNode.paradigm.aspectOrientation.ReturnJointPoint, CheckObject
):
    '''Checks return value from a function again their specification.'''

    # region dynamic methods

        # region public methods

## python3.3
##     def aspect(self: boostNode.extension.type.Self) -> builtins.object:
    def aspect(self):
##
        '''
            Checks the given return value.

            Returns the original value of the given wrapped function if
            everything goes right.
        '''
## python3.3
##         if 'return' in self.function.__annotations__:
##             expected_return = self.function.__annotations__['return']
##             given_return_type = builtins.type(self.return_value)
##             if builtins.isinstance(expected_return, builtins.type):
##                 self._check_type(
##                     given_type=given_return_type,
##                     expected_type=expected_return, value=self.return_value)
##             elif self._is_multiple_type(type=expected_return):
##                 self._handle_multiple_types(
##                     value=self.return_value, given_type=given_return_type,
##                     expected_types=expected_return)
##             else:
##                 self._check_value(
##                     expected_value=expected_return, value=self.return_value)
        pass
##
        return self.return_value

        # endregion

    # endregion

# endregion

# region footer

boostNode.extension.dependent.Resolve(
    name=__name__, frame=inspect.currentframe(), default_caller=False)

# endregion
