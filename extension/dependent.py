#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-

# region header

'''
    This module provides features to handle problems with phantom problems.
    E.g. It handles cyclic import dependencies.
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

## python2.7 import copy
import builtins
import inspect
import os
import sys
## python2.7 pass
import types

## python2.7 builtins = sys.modules['__main__'].__builtins__
pass

sys.path.append(os.path.abspath(sys.path[0] + 3 * ('..' + os.sep)))
sys.path.append(os.path.abspath(sys.path[0] + 4 * ('..' + os.sep)))

# endregion


# region classes

## python2.7 class Resolve(builtins.object):
class Resolve:
    '''
        Handles dependencies with modules.
    '''

    # region dynamic properties

        # region protected properties

    '''
        Saves a list of needed dependencies to call a defined opst event
        handler function.
    '''
    _load_stack = []

        # endregion

    # endregion

    # region dynamic methods

        # region public methods

            # region special methods

## python2.7
##     def __init__(
##         self, name, frame, default_caller=None, function=False,
##         dependencies=('boostNode.extension.system.CommandLine',
##                       'boostNode.extension.native.Module')
##     ):
    def __init__(
        self, name: builtins.str, frame: types.FrameType,
        default_caller=None, function=False,
        dependencies=('boostNode.extension.system.CommandLine',
                      'boostNode.extension.native.Module')
    ) -> None:
##
        '''
            Initializes a new instance of dependency definition for a given
            module. It saves the given dependency with a function to call if
            needed dependencies are ready. Dependencies are stored in a static
            class list.

            Examples:

            >>> def test():
            ...     print('hans')

            >>> r = Resolve(
            ...     __name__, inspect.currentframe(), function=test,
            ...     dependencies=())
            hans
            >>> Resolve._load_stack
            []

            >>> Resolve(
            ...     __name__, inspect.currentframe(), dependencies=())
            Object of "Resolve".
            >>> Resolve._load_stack
            []

            >>> Resolve(
            ...     __name__, inspect.currentframe(), function=test,
            ...     dependencies=('A',))
            Object of "Resolve".
            >>> Resolve._load_stack # doctest: +ELLIPSIS
            [{...('A',)...}]
        '''
        self.__class__._load_stack.append({
            'name': name,
            'frame': frame,
            'default_caller': default_caller,
            'function': function,
            'dependencies': dependencies})
        self._load()

            # endregion

        # endregion

    # endregion

    # region static methods

        # region public methods

            # region special methods

    @builtins.classmethod
## python2.7     def __repr__(cls):
    def __repr__(cls: builtins.type) -> builtins.str:
        '''
            Invokes if this object should describe itself by a string.

            Examples:

            >>> repr(Resolve(name='types', frame=inspect.currentframe()))
            'Object of "Resolve".'
        '''
        return 'Object of "%s".' % cls.__name__

            # endregion

    @builtins.classmethod
## python2.7
##     def get_all(cls, path=sys.path[0]):
    def get_all(cls: builtins.type, path=sys.path[0]) -> builtins.list:
##
        '''
            This method provides a generic way to determine all modules in
            current package or folder. It is useful for "__init__.py" files.

            Examples:

            >>> Resolve.get_all() # doctest: +ELLIPSIS
            [...'dependent'...]

            >>> import boostNode.extension.file
            >>> location = boostNode.extension.file.Handler(
            ...     __test_folder__ + 'get_all', make_directory=True)
            >>> a = boostNode.extension.file.Handler(
            ...     location.path + 'a.py', must_exist=False)
            >>> a.content = ' '
            >>> boostNode.extension.file.Handler(
            ...     location.path + 'b.pyc', make_directory=True
            ... ) # doctest: +ELLIPSIS
            Object of "Handler" with path "...get_all...b.pyc..." (dire...

            >>> Resolve.get_all(__test_folder__ + 'get_all')
            ['a']

            >>> a.remove_file()
            True
            >>> Resolve.get_all(__test_folder__ + 'get_all')
            []
        '''
        return builtins.list(builtins.set(builtins.map(
            lambda name: name[:name.rfind('.')],
            builtins.filter(
                lambda name: ((name.endswith('.py') or
                               name.endswith('.pyc')) and
                              not name.startswith('__init__.') and
                              os.path.isfile(path + os.sep + name)),
                os.listdir(
                    path[:- 1 -builtins.len(os.path.basename(path))] if
                    os.path.isfile(path) else path)))))

        # endregion

        # region protected methods

    @builtins.classmethod
## python2.7     def _load(cls):
    def _load(cls: builtins.type) -> builtins.bool:
        '''
            Checks if all needed dependencies are available for given module
            and runs a given function if provided or a default module
            extension method otherwise.
        '''
## python2.7
##         for key, load in builtins.enumerate(copy.copy(cls._load_stack)):
        for key, load in builtins.enumerate(cls._load_stack.copy()):
##
            if cls._is_loaded(load):
                cls._call_post_event_function(key, load)
                return True
        return False

    @builtins.classmethod
## python2.7
##     def _is_loaded(cls, load):
    def _is_loaded(
        cls: builtins.type, load: builtins.dict
    ) -> builtins.bool:
##
        '''
            Checks if all elements in the given dependency paths are already
            imported and available.

            Examples:

            >>> Resolve._is_loaded({'dependencies': 'A', 'name': '__main__'})
            False
        '''
        loaded = True
        for module_dependence in load['dependencies']:
            for dependence in module_dependence.split('.'):
                if not 'object' in builtins.locals():
                    if dependence in builtins.dir(sys.modules[load['name']]):
                        object = builtins.getattr(
                            sys.modules[load['name']], dependence)
                    else:
                        loaded = False
                        break
                elif dependence in builtins.dir(object):
                    object = builtins.getattr(object, dependence)
                else:
                    loaded = False
                    break
            if 'object' in builtins.locals():
                del object
        return loaded

    @builtins.classmethod
## python2.7
##     def _call_post_event_function(cls, key, load):
    def _call_post_event_function(
        cls: builtins.type, key: builtins.int, load: builtins.dict
    ) -> builtins.bool:
##
        '''
            Runs given post event handler after all needed dependencies loaded.
            If no event handler was given a default function will be called.
            This default method provides a generic command line interface for
            the modules.
        '''
        del cls._load_stack[key]
        if load['function']:
            if load['function'].__name__ in builtins.dir(
                    sys.modules[load['name']]):
                builtins.getattr(sys.modules[load['name']],
                                 load['function'].__name__)
            else:
                load['function']()
        else:
            cls._default_displaced_load(
                name=load['name'], frame=load['frame'],
                default_caller=load['default_caller'])
        return cls._load()

    @builtins.classmethod
## python2.7
##     def _default_displaced_load(cls, name, frame, default_caller):
    def _default_displaced_load(
        cls: builtins.type, name: builtins.str, frame: types.FrameType,
        default_caller: (builtins.str, builtins.type(None))
    ) -> builtins.bool:
##
        '''
            Provides a typical used method for running in any module's
            context.
            This method extends a given module's scope with often used globals
            and a meta command line interface for testing or running objects
            in extended module.

            Returns "True" if default load could be proceed and "False"
            otherwise.
        '''
        if 'boostNode' in builtins.dir(sys.modules[name]):
            displaced_module =\
                sys.modules[name].boostNode.extension.native.Module
            sys.modules[name].boostNode.extension.system.CommandLine\
                .generic_module_interface(
                    module=displaced_module.extend(name, frame),
                    default_caller=default_caller)
            return True
        return False

        # endregion

    # endregion

# endregion

# region footer

if __name__ == '__main__':
    from boostNode.extension.native import Module
    Module.default(
        name=__name__, frame=inspect.currentframe(), default_caller=False)

# endregion
