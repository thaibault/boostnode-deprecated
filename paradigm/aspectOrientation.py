#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-

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

## python2.7
## pass
import builtins
import collections
##
import functools
import inspect
import os
import re
import sys
import types

## python2.7 builtins = sys.modules['__main__'].__builtins__
pass

for number in (3, 4):
    sys.path.append(os.path.abspath(sys.path[0] + number * ('..' + os.sep)))

import boostNode.extension.dependent
import boostNode.extension.native
import boostNode.extension.type

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

## python2.7 class FunctionDecorator(builtins.object):
class FunctionDecorator:
    '''Abstract class and interface for function decorator classes.'''

    # region dynamic properties

        # region public properties

            # region special properties

    '''Necessary for providing python's native function properties.'''
    __func__ = None

            # endregion

    '''Properties of function calls.'''
    class_object = object = function = return_value = None

        # endregion

        # region protected properties

    '''Saves method types like static or class bounded.'''
    _method_type = None

        # endregion

    # endregion

    # region dynamic methods

        # region public methods

            # region special methods

## python2.7
##     def __init__(self, method, function=None):
    def __init__(
        self: boostNode.extension.type.Self,
        method: (types.FunctionType, types.MethodType), function=None
    ) -> None:
##
        '''
            Collects informations about wrapped method.

            Examples:

            >>> def a():
            ...     pass

            >>> FunctionDecorator(a) # doctest: +ELLIPSIS
            Object of "FunctionDecorator" with called function "a", wrapped...

            >>> FunctionDecorator(5) # doctest: +ELLIPSIS
            Traceback (most recent call last):
            ...
            TypeError: First ... but "int" (5) given.
        '''
        self.class_object = self.object = self.function =\
            self.return_value = None
        self._method_type = None

        if method in (builtins.classmethod, builtins.staticmethod):
            self.function = function
            self._method_type = method
        elif(builtins.isinstance(
            method, (types.FunctionType, types.MethodType))
        ):
            self.function = method
        else:
            raise builtins.TypeError(
                'First argument for initializing "{class_name}" must be '
                '"{classmethod}", "{staticmethod}", "{function_type}" or '
                '"{method_type}" but "{type}" ({value}) given.'.format(
                    class_name=self.__class__.__name__,
                    classmethod=builtins.classmethod.__name__,
                    staticmethod=builtins.staticmethod.__name__,
                    function_type=types.FunctionType.__name__,
                    method_type=types.MethodType.__name__,
                    type=builtins.type(method).__name__,
                    value=builtins.str(method)))
        self.__func__ = self.function

## python2.7
##     def __repr__(self):
    def __repr__(self: boostNode.extension.type.Self) -> builtins.str:
##
        '''
            Describes current function wrapper.

            Examples:

            >>> fD = FunctionDecorator(FunctionDecorator.__repr__)
            >>> fD.class_object = FunctionDecorator
            >>> repr(fD) # doctest: +ELLIPSIS
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

## python2.7
##     def __call__(self, *arguments, **keywords):
    def __call__(
        self: boostNode.extension.type.Self, *arguments: builtins.object,
        **keywords: builtins.object
    ) -> builtins.object:
##
        '''
            This method is triggered if wrapped function was called.
        '''
        if self.function and self.object is None and self.class_object is None:
            '''A standalone function was wrapped.'''
            return self.get_wrapper_function()(*arguments, **keywords)
        '''A object bounded method was wrapped.'''
        return self.__class__(
            method=self._method_type, function=arguments[0])

## python2.7
##     def __get__(self, object, class_object=None):
    def __get__(
        self: boostNode.extension.type.Self, object: builtins.object,
        class_object=None
    ) -> (types.FunctionType, types.MethodType):
##
        '''
            If same function was called twice in same context (recursion)
            create a new instance for it manually.

            Examples:

            >>> fD = FunctionDecorator(FunctionDecorator.__get__)
            >>> fD.__get__(fD) # doctest: +ELLIPSIS
            <...FunctionDecorator.__get__...>
        '''
        if self.object is not None:
            '''Restore old information about given class to function.'''
            method_type = self._method_type
            self = self.__class__(self.function)
            self._method_type = method_type
        self.class_object = class_object
        self.object = object
        if self.class_object is None:
            self.class_object = object.__class__
        return self.get_wrapper_function()

            # endregion

## python2.7
##     def get_wrapper_function(self):
    def get_wrapper_function(
        self: boostNode.extension.type.Self
    ) -> (types.FunctionType, types.MethodType):
##
        '''
            This method should ususally be overwridden. It serves the wrapper
            function to manipulate decorated function calls.
        '''
        return self.function

        # endregion

        # region protected methods

## python2.7
##     def _determine_arguments(self, arguments):
    def _determine_arguments(
        self: boostNode.extension.type.Self, arguments: collections.Iterable
    ) -> builtins.tuple:
##
        '''
            Determine right set of arguments for different method types.
        '''
        if self._method_type is builtins.classmethod:
            arguments = [self.class_object] + builtins.list(arguments)
        elif not (self.object is None or
                  self._method_type is builtins.staticmethod):
            arguments = [self.object] + builtins.list(arguments)
        return builtins.tuple(arguments)

        # endregion

    # endregion


## python2.7 class JointPointHandler(builtins.object):
class JointPointHandler:
    '''Abstract class for joint point implementations.'''

    # region dynamic properties

        # region public properties

    class_object = object = function = arguments = keywords = None
    argument_specifications = []

        # endregion

    # endregion

    # region dynamic methods

        # region public methods

            # region special methods

## python2.7
##     def __init__(self, class_object, object, function, arguments, keywords):
    def __init__(
        self: boostNode.extension.type.Self, class_object: builtins.type,
        object: builtins.object,
        function: (types.FunctionType, types.MethodType),
        arguments: collections.Iterable, keywords: builtins.dict
    ) -> None:
##
        '''
            Saves function call properties.
        '''
        self.class_object = class_object
        self.object = object
        self.function = function
        self.arguments = arguments
        self.keywords = keywords
## python2.7
##         pass
        argument_specifications = inspect.signature(
            self.function
        ).parameters
        bound_arguments = inspect.signature(self.function).bind(
            *self.arguments, **self.keywords)
        self.argument_specifications = []
        for name, value in bound_arguments.arguments.items():
            if(argument_specifications[name].kind is
               inspect.Parameter.VAR_POSITIONAL):
                for index, positional_value in builtins.enumerate(
                    value
                ):
                    self.argument_specifications.append(Argument(
                        parameter=argument_specifications[name],
                        value=positional_value, function=self.function,
                        name=builtins.str(index + 1) + '. argument'))
            elif(argument_specifications[name].kind is
                 inspect.Parameter.VAR_KEYWORD):
                for keyword_name, keyword_value in value.items():
                    self.argument_specifications.append(Argument(
                        parameter=argument_specifications[name],
                        value=keyword_value, function=self.function,
                        name=keyword_name))
            else:
                self.argument_specifications.append(Argument(
                    parameter=argument_specifications[name],
                    value=value, function=self.function))
##

## python2.7
##     def __repr__(self):
    def __repr__(self: boostNode.extension.type.Self) -> builtins.str:
##
        '''
            Represents the given function call properties.
        '''
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

## python2.7     def aspect(self):
    def aspect(self: boostNode.extension.type.Self) -> None:
##
        '''
            This method should be overwridden to provide the essentiel aspect
            for handled function call.
        '''
        raise boostNode.extension.native.Object\
            .determine_abstract_method_exception(
                abstract_class_name=JointPointHandler.__name__)

        # endregion

    # endregion


## python2.7 class ReturnAspect(builtins.object):
class ReturnAspect:
    '''Abstract class for aspects dealing with function's return value.'''

    # region dynamic properties

        # region public properties

    class_object = object = function = arguments = keywords = return_value =\
        None

        # endregion

    # endregion

    # region dynamic methods

        # region public methods

            # region special methods

## python2.7
##     def __repr__(self):
    def __repr__(self: boostNode.extension.type.Self) -> builtins.str:
##
        '''
            Represents the current handled function call.
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

    # region dynamic properties

        # region public properties

    return_value = None

        # endregion

    # endregion

    # region dynamic methods

        # region public methods

            # region special methods

## python2.7
##     def __init__(self, *arguments, **keywords):
    def __init__(
        self: boostNode.extension.type.Self, *arguments: builtins.object,
        **keywords: builtins.object
    ) -> None:
##
        if keywords:
            self.return_value = keywords['return_value']
            del keywords['return_value']
        else:
            self.return_value = arguments[-1]
            arguments = arguments[:-1]
        '''Take this method via introspection.'''
        return builtins.getattr(
            JointPointHandler, inspect.stack()[0][3]
        )(self, *arguments, **keywords)

            # endregion

        # endregion

    # endregion

# endregion


# region classes

## python2.7 """
pass


class Argument(inspect.Parameter):
    '''Represents a given argument given to a function.'''

    # region dynamic properties

        # region public properties

    '''Holds some informations about arguments passing through the function.'''
    empty = default = annotation = kind = value = function = None
    name = ''

        # endregion

    # endregion

    # region dynamic methods

        # region public methods

            # region special methods

## python2.7
##     def __init__(self, parameter, value, function, name=None):
    def __init__(
        self: boostNode.extension.type.Self, parameter: inspect.Parameter,
        value: (builtins.object, builtins.type),
        function: (types.MethodType, types.FunctionType),
        name=None
    ) -> None:
##
        '''
            Collects information about argument.

            Examples:

            >>> def mocup(a: int):
            ...     pass

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
        self.kind = parameter.kind
        self.empty = parameter.empty
        self.default = parameter.default
        self.annotation = parameter.annotation
        self.value = value
        self.name = parameter.name
        if name is not None:
            self.name = name
        self.function = function

## python2.7
##     def __repr__(self):
    def __repr__(self: boostNode.extension.type.Self) -> builtins.str:
##
        '''
            Represents current instance as string.

            Examples:

            >>> def mocup(a: str):
            ...     pass

            >>> Argument(
            ...     inspect.signature(mocup).parameters['a'], 5, mocup
            ... ) # doctest: +ELLIPSIS
            Object of "Argument" (POSITIONAL_OR_KEYWORD) bounded to "mocup"...
        '''
        default_value = 'default value "%s", ' % builtins.str(self.default)
        if self.default is inspect.Signature.empty:
            default_value = ''
        return ('Object of "{name}" ({kind}) bounded to "{function_path}" '
                'with name "{argument_name}", {default_value}annotation '
                '"{annotation}" and value "{value}".').format(
                    name=self.__class__.__name__, kind=builtins.str(self.kind),
                    function_path=self.function.__qualname__,
                    argument_name=self.name,
                    default_value=default_value,
                    annotation=builtins.str(self.annotation),
                    value=builtins.str(self.value))

            # endregion

        # endregion

    # endregion

## python2.7 """
pass


class PointCut(ReturnAspect):
    '''Generic way to handle point cuts.'''

    # region dynamic methods

        # region public methods

            # region special methods

## python2.7
##     def __init__(self, class_object, object, function, arguments, keywords):
    def __init__(
        self: boostNode.extension.type.Self, class_object: builtins.type,
        object: builtins.object,
        function: (types.FunctionType, types.MethodType),
        arguments: collections.Iterable, keywords: builtins.dict
    ) -> None:
##
        self.class_object = class_object
        self.object = object
        self.function = function
        self.arguments = arguments
        self.keywords = keywords
        self.return_value = None

            # endregion

## python2.7
##     def handle_call(self):
    def handle_call(self: boostNode.extension.type.Self) -> builtins.bool:
##
        '''
            Implementation of point cut for the aspect orientated way.
            Filters all functions calls and run given advice on given event.
        '''
## python2.7         def call_handler(advice):
        def call_handler(advice: builtins.dict) -> builtins.bool:
            '''
                Supports classes, simple functions or methods as triggered
                call handler.
            '''
            if 'call' == advice['event']:
                result = advice['callback'](
                    self.class_object, self.object, self.function,
                    self.arguments, self.keywords)
                if not builtins.isinstance(
                    advice['callback'], (types.FunctionType,
                                         types.MethodType)):
                    result = result.aspect()
                return result is not False
            return True
        return self._handle_aspects(handler=call_handler)

## python2.7
##     def handle_return(self, return_value):
    def handle_return(
        self: boostNode.extension.type.Self, return_value: builtins.object
    ) -> builtins.object:
##
        '''
            Implementation of point cut for the aspect orientated way.
            Filters all functions calls and run given advice on given event.
        '''
## python2.7         def return_handler(advice):
        def return_handler(advice: builtins.dict) -> None:
            '''
                Supports classes, simple functions or methods as triggered
                return handler.
            '''
            if 'return' == advice['event']:
                self.return_value = advice['callback'](
                    self.class_object, self.object,
                    self.function, self.arguments, self.keywords,
                    return_value)
                if not builtins.isinstance(
                    advice['callback'], (types.FunctionType,
                                         types.MethodType)):
                    self.return_value = self.return_value.aspect()
        self.return_value = return_value
        self._handle_aspects(handler=return_handler)
        return self.return_value

        # endregion

        # region protected methods

## python2.7
##     def _handle_aspects(self, handler):
    def _handle_aspects(
        self: boostNode.extension.type.Self, handler: types.MethodType
    ) -> builtins.bool:
##
        '''
            Iterates through each aspect matching current function call.
        '''
        result = True
        if not sys.flags.optimize:
            context_path = boostNode.extension.native.Module.get_context_path(
                path=inspect.getfile(self.function))
            if self.class_object:
                context_path += '.' + self.class_object.__name__
            context_path += '.' + self.function.__name__
            for aspect in ASPECTS:
                if(not 'point_cut' in aspect or
                   re.compile(aspect['point_cut']).match(context_path)):
                    for advice in aspect['advice']:
                        if handler(advice) is False:
                            result = False
        return result

        # endregion

    # endregion


class JointPoint(FunctionDecorator):
    '''
        Implementation of joint point for the aspect orientated way.
        Triggers every function call and look for aspects to wrap around.

        Examples:

        >>> @JointPoint
        ... def test(a):
        ...     return a
    '''

    # region dynamic methods

        # region public methods

## python2.7
##     def get_wrapper_function(self):
    def get_wrapper_function(
        self: boostNode.extension.type.Self
    ) -> (types.FunctionType, types.MethodType):
##
        @functools.wraps(self.function)
        def wrapper_function(*arguments, **keywords):
            '''Unpack wrapper methods.'''
            self.__func__ = self.function
            while '__func__' in builtins.dir(self.__func__):
                self.__func__ = self.__func__.__func__
            arguments = self._determine_arguments(arguments)
            point_cut = PointCut(
                self.class_object, self.object, function=self.__func__,
                arguments=arguments, keywords=keywords)
            if point_cut.handle_call():
                self.return_value = point_cut.handle_return(
                    return_value=self.function(*arguments, **keywords))
            return self.return_value
## python2.7         wrapper_function.__wrapped__ = self.function
        pass
        return wrapper_function

        # endregion

    # endregion

# endregion

# region footer

boostNode.extension.dependent.Resolve(
    name=__name__, frame=inspect.currentframe(), default_caller=False)

# endregion
