#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# region vim modline

# vim: set tabstop=4 shiftwidth=4 expandtab:
# vim: foldmethod=marker foldmarker=region,endregion:

# endregion

# region header

'''
    This module implements features like joint points, point cuts and advices
    for implementing aspect orientated code.
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

import atexit
## python3.3
## import builtins
## import collections
import __builtin__ as builtins
##
import functools
import inspect
import os
import re
import sys
import types

'''Make boostNode packages and modules importable via relative paths.'''
for number in (3, 4):
    sys.path.append(os.path.abspath(sys.path[0] + number * ('..' + os.sep)))

from boostNode.paradigm.objectOrientation import Class
## python3.3 from boostNode.extension.type import Self, SelfClass
pass

# endregion

# region constants

    # region public constants

'''
    Saves all aspects for cross cutting concerns for whole library and
    program code that uses this feature.

    Examples:

    >>> ASPECTS.append(
    ...     {'advice': ({'callback': check_arguments,
    ...                  'event': 'call'},
    ...                 {'callback': check_return_value,
    ...                  'event': 'return'}),
    ...      'point_cut': '^library\..+$'},
    ...     {'advice': ({'callback': log_call,
    ...                  'event': 'call'},
    ...                 {'callback': log_return,
    ...                  'event': 'return'}),
    ...      'point_cut': '^.+$'})
'''
ASPECTS = []

    # endregion

# endregion


# region abstract classes

class FunctionDecorator(Class):
    '''Abstract class and interface for function decorator classes.'''

    # region properties

    '''
        This constant holds a list of python decorators which could be emulated
        by this function wrapper instances.
    '''
    MANAGEABLE_DECORATORS = [builtins.classmethod, builtins.staticmethod]
    '''This property hold a list of common python's native decorators.'''
    COMMON_DECORATORS = [
        builtins.property, builtins.super, atexit.register,
        Class.pseudo_property]

    # endregion

    # region dynamic methods

        # region public

            # region  special

## python3.3
##     def __init__(
##         self: Self, method: (types.FunctionType, types.MethodType),
##         function=None
##     ) -> None:
    def __init__(self, method, function=None):
##
        '''
            Collects informations about wrapped method.

            Examples:

            >>> def a(): pass

            >>> FunctionDecorator(a) # doctest: +ELLIPSIS
            Object of "FunctionDecorator" with called function "a", wrapped...

            >>> FunctionDecorator(5) # doctest: +ELLIPSIS
            Traceback (most recent call last):
            ...
            TypeError: First ... but "int" (5) given.
        '''

                # region properties

        '''Properties of function calls.'''
        self.class_object = self.object = self.function = self.return_value = \
            self.wrapped_decorator = None
        '''Saves method types like static or class bounded.'''
        self.method_type = None
        '''
            Determines if class or object references for a wrapped method are
            already determined.
        '''
        self.arguments_determines = False
        '''
            NOTE: We can't use "self.__class__" because this points usually to
            a subclass of this class.
        '''
        if(method in self.COMMON_DECORATORS + self.MANAGEABLE_DECORATORS or
           builtins.isinstance(method, builtins.type) and
           builtins.issubclass(method, FunctionDecorator)):
            self._handle_given_decorator(function, method)
        elif builtins.isinstance(method, FunctionDecorator):
            '''
                If we are wrapping a nested instance of this class we propagate
                inspected informations to lower decorator.
                This case is given if one instances of this class wraps another
                one.
            '''
            self.wrapped_decorator = method
            self.function = method.function
            self.method_type = method.method_type
        elif(builtins.isinstance(
            method, (types.FunctionType, types.MethodType))
        ):
            self.function = method
        else:
            raise builtins.TypeError(
                'First argument for initializing "{class_name}" must be '
                '"{common_methods}", "{function_type}" or '
                '"{method_type}" but "{type}" ({value}) given.'.format(
                    class_name=self.__class__.__name__,
                    common_methods='", "'.join(builtins.map(
                        lambda decorator: decorator.__name__,
                        self.COMMON_DECORATORS + self.MANAGEABLE_DECORATORS +
                        [FunctionDecorator])),
                    function_type=types.FunctionType.__name__,
                    method_type=types.MethodType.__name__,
                    type=builtins.type(method).__name__,
                    value=builtins.str(method)))
        '''Necessary for providing python's native function properties.'''
        self.__func__ = self.function

                # endregion

## python3.3     def __repr__(self: Self) -> builtins.str:
    def __repr__(self):
        '''
            Describes current function wrapper.

            Examples:

            >>> function_decorator = FunctionDecorator(
            ...     FunctionDecorator.__repr__)
            >>> function_decorator.class_object = FunctionDecorator
            >>> repr(function_decorator) # doctest: +ELLIPSIS
            'Object of "FunctionDecorator" ... "__repr__" ... (NoneType).'
        '''
        if self.class_object:
            return ('Object of "{class_name}" with class object '
                    '"{class_object}", object "{object}", called function '
                    '"{function}", wrapped function "{wrapped_function}" '
                    'and return value "{value}" ({type}).'.format(
                        class_name=self.__class__.__name__,
                        class_object=self.class_object.__name__,
                        object=builtins.repr(self.object),
                        function=self.function.__name__,
                        wrapped_function=self.__func__.__name__,
                        value=builtins.str(self.return_value),
                        type=builtins.type(self.return_value).__name__))
        return ('Object of "{class_name}" with called function '
                '"{function}", wrapped function "{wrapped_function}" and '
                'return value "{value}" ({type}).'.format(
                    class_name=self.__class__.__name__,
                    function=self.function.__name__,
                    wrapped_function=self.__func__.__name__,
                    value=builtins.str(self.return_value),
                    type=builtins.type(self.return_value).__name__))

## python3.3
##     def __call__(
##         self: Self, *arguments: builtins.object, **keywords: builtins.object
##     ) -> builtins.object:
    def __call__(self, *arguments, **keywords):
##
        '''This method is triggered if wrapped function was called.'''
        if self.function and self.object is None and self.class_object is None:
            '''A standalone function was wrapped.'''
            return self.get_wrapper_function()(*arguments, **keywords)
        '''A object bounded method was wrapped.'''
        return self.__class__(
            method=self.method_type, function=arguments[0])

## python3.3
##     def __get__(
##         self: Self, object: builtins.object, class_object=None
##     ) -> (types.FunctionType, types.MethodType):
    def __get__(self, object, class_object=None):
##
        '''
            If same function was called twice in same context (recursion)
            create a new instance for it manually.

            Examples:

            >>> function_decorator = FunctionDecorator(
            ...     FunctionDecorator.__get__)
            >>> function_decorator.__get__(
            ...     function_decorator
            ... ) # doctest: +ELLIPSIS
            <...FunctionDecorator.__get__...>
        '''
        if self.wrapped_decorator is not None:
            self.function = builtins.getattr(
                self.wrapped_decorator, inspect.stack()[0][3]
            )(object, class_object)
        if self.object is not None:
            '''
                Restore old information about given class to function
                (method_type).
            '''
            method_type = self.method_type
            self = self.__class__(self.function)
            self.method_type = method_type
        self.class_object = class_object
        self.object = object
        if self.class_object is None:
            self.class_object = object.__class__
        return self.get_wrapper_function()

            # endregion

## python3.3
##     def get_wrapper_function(
##         self: Self
##     ) -> (types.FunctionType, types.MethodType):
    def get_wrapper_function(self):
##
        '''
            This method should usually be overridden. It serves the wrapper
            function to manipulate decorated function calls.
        '''
        return self.function

        # endregion

        # region protected

## python3.3
##     def _handle_given_decorator(
##         self: Self, function: (types.FunctionType, types.MethodType),
##         method: (builtins.object, builtins.type)
##     ) -> Self:
    def _handle_given_decorator(self, function, method):
##
        '''
            Another decorator was given to this instance. This decorator should
            additionally be used on given function.
        '''
        self.function = function
        self.method_type = method
        if self.function is not None:
            if builtins.isinstance(self.function, FunctionDecorator):
                '''
                    If we are wrapping a nested instance of this class we
                    propagate inspected informations to lower decorator. This
                    case is given if one instances of this class wraps another
                    one. The last wrapping instance additionally uses a common
                    or manageable wrapper.
                '''
                self.wrapped_decorator = self.function
                self.method_type = self.function.method_type
                self.function = self.function.function
            elif(builtins.isinstance(method, builtins.type) and
                 builtins.issubclass(method, FunctionDecorator)):
                '''
                    If we are wrapping a nested instance of this class we
                    propagate inspected informations to lower decorator. This
                    case is given if one instances of this class wraps another
                    one and the lower one is given via argument.
                '''
                self.wrapped_decorator = self.method_type(function)
                self.method_type = self.wrapped_decorator.method_type
                self.function = self.wrapped_decorator.function
            elif self.method_type in self.COMMON_DECORATORS:
                self.function = self.method_type(self.function)
        return self

## python3.3
##     def _determine_arguments(
##         self: Self, arguments: collections.Iterable
##     ) -> builtins.tuple:
    def _determine_arguments(self, arguments):
##
        '''Determine right set of arguments for different method types.'''
        '''Avoid to add object or class references twice.'''
        # TODO workaround for argument forwarding.
        """if not self.determined:
            if self.method_type is builtins.classmethod:
                arguments = [self.class_object] + builtins.list(arguments)
            elif not (self.object is None or
                      self.method_type is builtins.staticmethod):
                arguments = [self.object] + builtins.list(arguments)
        if self.wrapped_decorator is not None:
            self.wrapped_decorator.determined = True"""
        if(self.method_type is builtins.classmethod and
           (not arguments or arguments[0] is not self.class_object)):
            arguments = [self.class_object] + builtins.list(arguments)
        elif(not (self.object is None or
                  self.method_type is builtins.staticmethod) and
             (not arguments or arguments[0] is not self.object)):
            arguments = [self.object] + builtins.list(arguments)
        return builtins.tuple(arguments)

        # endregion

    # endregion


class JointPointHandler(Class):
    '''Abstract class for joint point implementations.'''

    # region dynamic methods

        # region public

            # region special

## python3.3
##     def __init__(
##         self: Self, class_object: builtins.type, object: builtins.object,
##         function: (types.FunctionType, types.MethodType),
##         arguments: collections.Iterable, keywords: builtins.dict
##     ) -> None:
    def __init__(self, class_object, object, function, arguments, keywords):
##
        '''
            Saves function call properties.

            Examples:

            >>> class A:
            ...     def a(self): pass

            >>> JointPointHandler(A, A(), A().a, (), {}) # doctest: +ELLIPSIS
            Object of "JointPointHandler" with class object "A", object "...".
        '''

                # region properties

        self.class_object = class_object
        self.object = object
        self.function = function
        self.arguments = arguments
        self.keywords = keywords
        self.argument_specifications = []
## python3.3
##         argument_specifications = inspect.signature(
##             self.function
##         ).parameters
##         bound_arguments = inspect.signature(self.function).bind(
##             *self.arguments, **self.keywords)
##         for name, value in bound_arguments.arguments.items():
##             if(argument_specifications[name].kind is
##                inspect.Parameter.VAR_POSITIONAL):
##                 for index, positional_value in builtins.enumerate(
##                     value
##                 ):
##                     self.argument_specifications.append(Argument(
##                         parameter=argument_specifications[name],
##                         value=positional_value, function=self.function,
##                         name=builtins.str(index + 1) + '. argument'))
##             elif(argument_specifications[name].kind is
##                  inspect.Parameter.VAR_KEYWORD):
##                 for keyword_name, keyword_value in value.items():
##                     self.argument_specifications.append(Argument(
##                         parameter=argument_specifications[name],
##                         value=keyword_value, function=self.function,
##                         name=keyword_name))
##             else:
##                 self.argument_specifications.append(Argument(
##                     parameter=argument_specifications[name],
##                     value=value, function=self.function))
        pass
##

                # endregion

## python3.3     def __repr__(self: Self) -> builtins.str:
    def __repr__(self):
        '''Represents the given function call properties.'''
        return ('Object of "{class_name}" with class object "{class_object}", '
                'object "{object}", function "{function}", arguments '
                '"{arguments}" and keywords "{keywords}".'.format(
                    class_name=self.__class__.__name__,
                    class_object=self.class_object.__name__,
                    object=builtins.repr(self.object),
                    function=self.function.__name__,
                    arguments='", "'.join(self.arguments),
                    keywords=builtins.str(self.keywords)))

            # endregion

    @classmethod
## python3.3     def aspect(cls: SelfClass) -> None:
    def aspect(cls):
        '''
            This method should be overwritten to provide the essential aspect
            for handled function call.

            Examples:

            >>> class A:
            ...     def a(self): pass

            >>> JointPointHandler(
            ...     A, A(), A().a, (), {}
            ... ).aspect() # doctest: +ELLIPSIS
            Traceback (most recent call last):
            ...
            NotImplementedError: Method "aspect" wasn't implemented by "...".
        '''
        from boostNode.extension.native import Object
        raise Object.determine_abstract_method_exception(
            abstract_class_name=JointPointHandler.__name__,
            class_name=cls.__name__)

        # endregion

    # endregion


class ReturnAspect(Class):
    '''Abstract class for aspects dealing with function's return value.'''

    # region dynamic methods

        # region public

            # region special

## python3.3     def __init__(self: Self) -> None:
    def __init__(self):
        '''Initializes instance properties.'''

                # region properties

        self.class_object = self.object = self.function = self.arguments = \
            self.keywords = self.return_value = None

                # endregion

## python3.3     def __repr__(self: Self) -> builtins.str:
    def __repr__(self):
        '''
            Represents the current handled function call.

            Examples:

            >>> class A:
            ...     def a(self): pass
            >>> return_aspect = ReturnAspect()
            >>> return_aspect.class_object = A
            >>> return_aspect.object = A()
            >>> return_aspect.function = A().a
            >>> return_aspect.arguments = ()
            >>> return_aspect.keywords = {}

            >>> repr(return_aspect) # doctest: +ELLIPSIS
            'Object of "ReturnAspect" with class object "A", object "...'
        '''
        return ('Object of "{class_name}" with class object "{class_object}", '
                'object "{object}", function "{function}", arguments '
                '"{arguments}", keywords "{keywords}" and return value '
                '"{value}" ({type}).'.format(
                    class_name=self.__class__.__name__,
                    class_object=self.class_object.__name__,
                    object=builtins.repr(self.object),
                    function=self.function.__name__,
                    arguments='", "'.join(self.arguments),
                    keywords=builtins.str(self.keywords),
                    value=builtins.str(self.return_value),
                    type=builtins.str(builtins.type(self.return_value))))

            # endregion

        # endregion

    # endregion


class CallJointPoint(JointPointHandler):
    '''Abstract class for joint points dealing with function calls.'''
    pass


class ReturnJointPoint(JointPointHandler, ReturnAspect):
    '''Abstract class for joint points dealing with function's return value.'''

    # region dynamic methods

        # region public

            # region special

## python3.3
##     def __init__(
##         self: Self, *arguments: builtins.object, **keywords: builtins.object
##     ) -> None:
    def __init__(self, *arguments, **keywords):
##
        '''
            Initializes a joint point for saved function call.

            Examples:


            >>> class A:
            ...     def a(self): pass

            >>> ReturnJointPoint(
            ...     A, A(), A().a, (), {}, return_value=None
            ... ) # doctest: +ELLIPSIS
            Object of "ReturnJointPoint" with class object "A", object "...".

            >>> ReturnJointPoint(
            ...     A, A(), A().a, (), {}, None
            ... ) # doctest: +ELLIPSIS
            Object of "ReturnJointPoint" with class object "A", object "...".
        '''
        '''Take this method via introspection from super classes.'''
        builtins.getattr(
            ReturnAspect, inspect.stack()[0][3]
        )(self)

                # region properties

        if keywords:
            self.return_value = keywords['return_value']
            del keywords['return_value']
        else:
            self.return_value = arguments[-1]
            arguments = arguments[:-1]

                # endregion

        '''Take this method via introspection from super classes.'''
        return builtins.getattr(
            JointPointHandler, inspect.stack()[0][3]
        )(self, *arguments, **keywords)

            # endregion

        # endregion

    # endregion

# endregion


# region classes

## python3.3 pass
"""


class Argument(Class):
    '''Represents a given argument given to a function.'''

    # region dynamic methods

        # region public

            # region special

## python3.3
##     def __init__(
##         self: Self, parameter: inspect.Parameter,
##         value: (builtins.object, builtins.type),
##         function: (types.MethodType, types.FunctionType),
##         name=None
##     ) -> None:
    def __init__(self, parameter, value, function, name=None):
##
        '''
            Collects information about argument.

            Examples:

            >>> def mocup(a: int): pass

            >>> argument = Argument(
            ...     inspect.signature(mocup).parameters['a'], 5, mocup)
            >>> argument.kind
            <_ParameterKind: 'POSITIONAL_OR_KEYWORD'>
            >>> argument.empty
            <class 'inspect._empty'>
            >>> argument.default
            <class 'inspect._empty'>
            >>> argument.annotation
            <class 'int'>
            >>> argument.value
            5
            >>> argument.name
            'a'
            >>> argument.function # doctest: +ELLIPSIS
            <function mocup at ...>

            >>> Argument(
            ...     inspect.signature(mocup).parameters['a'], 5, mocup, 'b'
            ... ).name
            'b'
        '''

                # region properties

        '''
            Holds some informations about arguments passing through the
            function.
        '''
        self.kind = parameter.kind
        self.empty = parameter.empty
        self.default = parameter.default
        self.annotation = parameter.annotation
        self.value = value
        self.name = parameter.name
        if name is not None:
            self.name = name
        self.function = function

                # endregion

## python3.3     def __repr__(self: Self) -> builtins.str:
    def __repr__(self):
        '''
            Represents current instance as string.

            Examples:

            >>> def mocup(a: str): pass

            >>> Argument(
            ...     inspect.signature(mocup).parameters['a'], 5, mocup
            ... ) # doctest: +ELLIPSIS
            Object of "Argument" (POSITIONAL_OR_KEYWORD) bounded to "mocup"...
        '''
        default_value = 'default value "%s", ' % builtins.str(self.default)
        if self.default is inspect.Signature.empty:
            default_value = ''
## python3.3         function_path = self.function.__qualname__
        function_path = self.function.__name__
        return (
            'Object of "{name}" ({kind}) bounded to "{function_path}" '
            'with name "{argument_name}", {default_value}annotation '
            '"{annotation}" and value "{value}".'
        ).format(
            name=self.__class__.__name__, kind=builtins.str(self.kind),
            function_path=function_path, argument_name=self.name,
            default_value=default_value,
            annotation=builtins.str(self.annotation),
            value=builtins.str(self.value))

            # endregion

        # endregion

    # endregion

## python3.3 pass
"""


class PointCut(ReturnAspect):
    '''Generic way to handle point cuts.'''

    # region dynamic methods

        # region public

            # region special

## python3.3
##     def __init__(
##         self: Self, class_object: builtins.type, object: builtins.object,
##         function: (types.FunctionType, types.MethodType),
##         arguments: collections.Iterable, keywords: builtins.dict
##     ) -> None:
    def __init__(self, class_object, object, function, arguments, keywords):
##
        '''
            Initializes a point cut object for implementing the aspect
            orientated model.
        '''
        '''Take this method via introspection from super classes.'''
        builtins.getattr(
            builtins.super(self.__class__, self), inspect.stack()[0][3]
        )()

                # region properties

        self.class_object = class_object
        self.object = object
        self.function = function
        self.arguments = arguments
        self.keywords = keywords

                # endregion

            # endregion

## python3.3     def handle_call(self: Self) -> builtins.bool:
    def handle_call(self):
        '''
            Implementation of point cut for the aspect orientated way. Filters
            all functions calls and run given advice on given event.
        '''
## python3.3         def call_handler(advice: builtins.dict) -> builtins.bool:
        def call_handler(advice):
            '''
                Supports classes, simple functions or methods as triggered call
                handler.
            '''
            if 'call' == advice['event']:
                result = advice['callback'](
                    self.class_object, self.object, self.function,
                    self.arguments, self.keywords)
                if(builtins.hasattr(advice['callback'], 'aspect') and
                   builtins.isinstance(
                       builtins.getattr(advice['callback'], 'aspect'),
                       (types.MethodType, types.FunctionType))):
                    result = result.aspect()
                return result is not False
            return True
        return self._handle_aspects(handler=call_handler)

## python3.3
##     def handle_return(
##         self: Self, return_value: builtins.object
##     ) -> builtins.object:
    def handle_return(self, return_value):
##
        '''
            Implementation of point cut for the aspect orientated way. Filters
            all functions calls and run given advice on given event.
        '''
## python3.3         def return_handler(advice: builtins.dict) -> None:
        def return_handler(advice):
            '''
                Supports classes, simple functions or methods as triggered
                return handler.
            '''
            if 'return' == advice['event']:
                self.return_value = advice['callback'](
                    self.class_object, self.object,
                    self.function, self.arguments, self.keywords,
                    return_value)
                if(builtins.hasattr(advice['callback'], 'aspect') and
                   builtins.callable(
                       builtins.getattr(advice['callback'], 'aspect'))):
                    self.return_value = self.return_value.aspect()
        self.return_value = return_value
        self._handle_aspects(handler=return_handler)
        return self.return_value

        # endregion

        # region protected

## python3.3
##     def _handle_aspects(
##         self: Self, handler: types.MethodType
##     ) -> builtins.bool:
    def _handle_aspects(self, handler):
##
        '''Iterates through each aspect matching current function call.'''
        from boostNode.extension.native import Module
        context_path = Module.get_context_path(path=inspect.getfile(
            self.function))
        if self.class_object:
            context_path += '.' + self.class_object.__name__
        context_path += '.' + self.function.__name__
        result = True
        for aspect in ASPECTS:
            if(not 'point_cut' in aspect or
               re.compile(aspect['point_cut']).match(context_path)):
                for advice in aspect['advice']:
                    if handler(advice) is False:
                        result = False
        return result

        # endregion

    # endregion


if sys.flags.optimize:
## python3.3
##     def JointPoint(
##         function: (types.FunctionType, types.MethodType)
##     ) -> (types.FunctionType, types.MethodType):
    def JointPoint(function):
##
        '''
            Dummy function for simply return given function to avoid
            JointPoints in high performance mode.
        '''
        return function
else:
    class JointPoint(FunctionDecorator):
        '''
            Implementation of joint point for the aspect orientated way.
            Triggers every function call and look for aspects to wrap around.

            Examples:

            >>> @JointPoint
            ... def test(a):
            ...     return a

            >>> def call_handler(
            ...     class_object, object, function, arguments, keywords
            ... ): return True
            >>> def return_handler(
            ...     class_object, object, function, arguments, keywords,
            ...     return_value
            ... ): return 'wrapped_result'
            >>> __test_globals__['ASPECTS'] = [{
            ...     'advice': (
            ...         {'callback': call_handler, 'event': 'call'},
            ...         {'callback': return_handler, 'event': 'return'}),
            ...     'point_cut': '^.+\.((A\.b)|a)$'}]

            >>> class A:
            ...     @JointPoint
            ...     def b(self): pass
            >>> A().b()
            'wrapped_result'

            >>> @JointPoint
            ... def a():
            ...     pass
            >>> a()
            'wrapped_result'

            >>> @JointPoint
            ... def b(): return 'not_wrapped'
            >>> b()
            'not_wrapped'

            >>> def call_handler(
            ...     class_object, object, function, arguments, keywords
            ... ): return False
            >>> __test_globals__['ASPECTS'][0]['advice'][0]['callback'] = (
            ...     call_handler)
            >>> @JointPoint
            ... def a(): return 'wrapper_prevents_calling'
            >>> a()

            >>> def a(): pass
            >>> def b(): pass
            >>> b.__func__ = a
            >>> a = JointPoint(b)
            >>> a()

            >>> class CallHandler(CallJointPoint):
            ...     def aspect(self): return True
            >>> class ReturnHandler(ReturnJointPoint):
            ...     def aspect(self): return 'class_wrapped_result'
            >>> __test_globals__['ASPECTS'][0]['advice'][0]['callback'] = (
            ...     CallHandler)
            >>> __test_globals__['ASPECTS'][0]['advice'][1]['callback'] = (
            ...     ReturnHandler)

            >>> A().b()
            'class_wrapped_result'
        '''

    # region dynamic methods

        # region public

## python3.3
##         def get_wrapper_function(
##             self: Self
##         ) -> (types.FunctionType, types.MethodType):
        def get_wrapper_function(self):
##
            '''This methods returns the joint point's wrapped function.'''
            @functools.wraps(self.function)
            def wrapper_function(*arguments, **keywords):
                '''
                    Wrapper function for doing the aspect orientated stuff
                    before and after a function call.
                '''
                '''Unpack wrapper methods.'''
                self.__func__ = self.function
                while builtins.hasattr(self.__func__, '__func__'):
                    self.__func__ = self.__func__.__func__
                arguments = self._determine_arguments(arguments)
                point_cut = PointCut(
                    self.class_object, self.object, function=self.__func__,
                    arguments=arguments, keywords=keywords)
                if point_cut.handle_call():
                    self.return_value = point_cut.handle_return(
                        return_value=self.function(*arguments, **keywords))
                return self.return_value
## python3.3             pass
            wrapper_function.__wrapped__ = self.function
            return wrapper_function

        # endregion

    # endregion

# endregion

# region footer

'''
    Preset some variables given by introspection letting the linter know what
    globale variables are available.
'''
__logger__ = __exception__ = __module_name__ = __file_path__ = \
    __test_mode__ = None
'''
    Extends this module with some magic environment variables to provide better
    introspection support. A generic command line interface for some code
    preprocessing tools is provided by default.
'''
if __name__ == '__main__':
    from boostNode.extension.native import Module
    Module.default(
        name=__name__, frame=inspect.currentframe(), default_caller=False)

# endregion
