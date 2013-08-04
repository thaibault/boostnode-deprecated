#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# region vim modline

# vim: set tabstop=4 shiftwidth=4 expandtab:
# vim: foldmethod=marker foldmarker=region,endregion:

# endregion

# region header

'''
    This module provides classes for handling issues with the operating
    system or command line.
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

import argparse
import atexit
## python3.3
## import builtins
## import collections
import __builtin__ as builtins
##
import doctest
try:
    import fcntl
except ImportError:
    fcntl = None
import inspect
import logging
import multiprocessing
import os
import signal
import socket
import struct
import subprocess
import sys
import tempfile
import time
## python3.3 import types
pass

for number in (3, 4):
    sys.path.append(os.path.abspath(sys.path[0] + number * ('..' + os.sep)))

import boostNode.extension.file
import boostNode.extension.native
import boostNode.extension.output
import boostNode.extension.type
import boostNode.paradigm.aspectOrientation

# endregion


# region abstract classes

## python3.3 class Runnable:
class Runnable(builtins.object):
    '''
        Abstract class (interface) for implementing reusable classes which acts
        directly as an command line interface to provide their features
        platform independent.
    '''

    # region static properties

        # region private

    '''
        This lock is acquired at startup und will be released as soon the
        runnable receives a termination signal.
    '''
    __termination_lock = multiprocessing.Lock()

        # endregion

    # endregion'

    # region dynamic properties

        # region public

    '''Saves a cli-command for shutting down the runnable implementation.'''
    stop_order = 'stop'
    '''Saves a cli-command for restarting the runnable implementation.'''
    restart_order = 'restart'

        # endregion

        # region protected

    '''
        Currently given inputs via command line during "wait_for_order()"
        is running.
    '''
    _given_order = ''
    '''
        This properties saves the initial given arguments to handle a
        reinitialisation by given restart order.
    '''
    _childrens_module = None
    _initial_arguments = ()
    _initial_keywords = {}

        # endregion

        # region private

    '''This lock prevents form triggering the stop method twice.'''
    __stop_lock = None

        # endregion

    # endregion

    # region static methods

        # region public

            # region special

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def __repr__(cls: boostNode.extension.type.SelfClass) -> builtins.str:
    def __repr__(cls):
##
        '''
            Generic representation method.

            Examples:

            >>> class A(Runnable):
            ...     def _initialize(self):
            ...         pass

            >>> repr(A()) # doctest: +ELLIPSIS
            'Object of "A" implementing a command line runnable interfaceto...'
        '''
        return 'Object of "%s" implementing a command line runnable interface'\
               'to be usable outside this python environment.' % cls.__name__

            # endregion

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def run(
##         cls: boostNode.extension.type.SelfClass,
##         *arguments: builtins.object, **keywords: builtins.object
##     ) -> boostNode.extension.type.SelfClassObject:
    def run(cls, *arguments, **keywords):
##
        '''
            Method for an explicit run of a class implementing this abstract
            class (interface).

            Examples:

            >>> __test_buffer__.clear() # doctest: +ELLIPSIS
            '...'

            >>> class A(Runnable):
            ...     @boostNode.paradigm.aspectOrientation.JointPoint
            ...     def _run(self, a):
            ...         boostNode.extension.output.Print(a)
            >>> a = A.run('A')
            >>> __test_buffer__.content
            'A\\n'

            >>> class B(Runnable):
            ...     def _run(self, a):
            ...         boostNode.extension.output.Print(a)
            >>> b = B.run('B')
            >>> __test_buffer__.content
            'A\\nB\\n'
        '''
        arguments += (cls._get_potential_wrapped_method(cls._run.__name__),)
        return cls(*arguments, **keywords)

        # endregion

        # region protected

            # region has to be implemented

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _run(
##         cls: boostNode.extension.type.SelfClass
##     ) -> boostNode.extension.type.SelfClass:
    def _run(cls):
##
        '''
            Abstract method to force runnable classes to implement their entry
            point if running through command line interface.
        '''
        raise boostNode.extension.native.Object\
            .determine_abstract_method_exception(
                abstract_class_name=Runnable.__name__, class_name=cls.__name__)
        return cls

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _initialize(
##         cls: boostNode.extension.type.SelfClass
##     ) -> boostNode.extension.type.SelfClass:
    def _initialize(cls):
##
        '''
            Abstract methods to force runnable classes to implement their entry
            point if running through this python environment.
        '''
        raise boostNode.extension.native.Object\
            .determine_abstract_method_exception(
                abstract_class_name=Runnable.__name__, class_name=cls.__name__)
        return cls

            # endregion

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _get_potential_wrapped_method(
##         cls: boostNode.extension.type.SelfClass, method_name: builtins.str
##     ) -> (types.MethodType, types.FunctionType):
    def _get_potential_wrapped_method(cls, method_name):
##
        '''
            Unpacks a wrapped method if necessary.

            Examples:

            >>> (Runnable._run.__wrapped__ ==
            ...     Runnable._get_potential_wrapped_method('_run'))
            True

            >>> (Runnable._run.__wrapped__ ==
            ...     Runnable._get_potential_wrapped_method(
            ...         Runnable._run.__name__))
            True
        '''
        method = builtins.getattr(cls, method_name)
        while builtins.hasattr(method, '__wrapped__'):
            method = method.__wrapped__
        return method

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _command_line_arguments_to_dictionary(
##         cls: boostNode.extension.type.SelfClass,
##         namespace: argparse.Namespace
##     ) -> builtins.dict:
    def _command_line_arguments_to_dictionary(self, namespace):
##
        '''
            This method converts command line arguments generated by python's
            native "argparse" to "builtins.dict".
        '''
        result = {}
        for name in builtins.dir(namespace):
            if not name.startswith('_'):
                value = builtins.getattr(namespace, name)
                if builtins.isinstance(value, builtins.list):
                    value = builtins.tuple(value)
                result[name] = value
        return result

        # endregion

    # endregion

    # region dynamic methods

        # region public

            # region special

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def __init__(
##         self: boostNode.extension.type.Self, *arguments: builtins.object,
##         **keywords: builtins.object
##     ) -> None:
    def __init__(self, *arguments, **keywords):
##
        '''
            A generic initializer for Runnable class implementations.
        '''
        '''Make this properties instance attributes explicitly.'''
        self.stop_order = self.__class__.stop_order
        self.restart_order = self.__class__.restart_order
        self._given_order = self.__class__._given_order
        self._childrens_module = self.__class__._childrens_module
        self.__stop_lock = self.__class__.__stop_lock

        '''Attach this properties to child class.'''
        self.__class__._given_order = self._given_order
        self.__class__._childrens_module = self._childrens_module
        self.__class__.__stop_lock = self.__stop_lock

        run = False
        if(builtins.len(arguments) and arguments[-1] ==
           self._get_potential_wrapped_method(self._run.__name__)):
            arguments = arguments[:-1]
            run = True
        self.__stop_lock = multiprocessing.Lock()
        self._childrens_module = inspect.getmodule(self.__class__)
        caller_module = inspect.getmodule(inspect.stack()[2][0])
        this_module = inspect.getmodule(inspect.stack()[0][0])
        if(caller_module is this_module and
           self._childrens_module.__name__ == '__main__' and
           not self._childrens_module.__test_mode__) or run:
            self._initial_arguments = arguments
            self._initial_keywords = keywords

            self._handle_module_running(arguments, keywords, run)
        else:
            self._initialize(*arguments, **keywords)

            # endregion

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def wait_for_order(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def wait_for_order(self):
##
        '''
            Handler for waiting till a server stop order comes through
            the command line interface.
        '''
        self._given_order = ''
        try:
            while self._given_order not in (
                self.stop_order, self.restart_order
            ):
                given_input_explanation = ''
                if self._given_order:
                    given_input_explanation = ' (not "%s")' % self._given_order
## python3.3
##                 self._given_order = builtins.input(
##                     'Write "%s" or "%s"%s for shutting or restarting '
##                     '"%s":\n' %
##                     (self.stop_order, self.restart_order,
##                      given_input_explanation, self.__class__.__name__))
                self._given_order = builtins.raw_input(
                    'Write "%s" or "%s"%s for shutting or restarting '
                    '"%s":\n' %
                    (self.stop_order, self.restart_order,
                     given_input_explanation, self.__class__.__name__))
##
        except (builtins.IOError, builtins.EOFError):
            __logger__.info(
                "We have lost standard input. stop order couldn't be "
                'received. Use a termination signal instead.')
            try:
                self.__class__.__termination_lock.acquire()
            except builtins.OSError:
                pass
        except (builtins.KeyboardInterrupt):
            __logger__.debug('Standard input stream was interrupted.')
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def stop(
##         self: boostNode.extension.type.Self, signal_number=None,
##         stack_frame=None, reason=''
##     ) -> boostNode.extension.type.Self:
    def stop(self, signal_number=None, stack_frame=None, reason=''):
##
        '''
            This method should usually be overwritten to handle cleanup jobs.
        '''
        if not reason:
            reason = 'program trigger or normal termination'
            if signal_number:
                reason = 'signal number %d' % signal_number
        __logger__.debug(
            'Closing "%s" caused by %s.', self.__class__.__name__, reason)
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint(atexit.register)
## python3.3
##     def trigger_stop(
##         self=None, *arguments: builtins.object, exit=True,
##         **keywords: builtins.object
##     ) -> boostNode.extension.type.Self:
    def trigger_stop(self=None, *arguments, **keywords):
##
        '''Method for cleaning up running workers.'''
        if(not (('__test_mode__' in builtins.globals() and __test_mode__) or
                self is None) and self.__stop_lock.acquire(False)):
## python3.3
##             pass
            exit, keywords = boostNode.extension.native.Dictionary(
                content=keywords
            ).pop(name='exit', default_value=True)
##
            reason = ''
            if self._given_order and self._given_order in (
                self.stop_order, self.restart_order
            ):
                reason = 'given order "%s"' % self._given_order
            self.stop(*arguments, reason=reason, **keywords)
            if self._given_order == self.restart_order:
                __logger__.debug(
                    'Restart "%s" with arguments "%s" and keywords "%s".',
                    self.__class__.__name__,
                    '", "'.join(self._initial_arguments),
                    builtins.str(self._initial_keywords))
                self.__class__.run(
                    *self._initial_arguments, **self._initial_keywords)
            else:
                self._terminate(arguments, exit)
        return self

        # endregion

        # region protected

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _terminate(
##         cls: boostNode.extension.type.SelfClass, arguments: builtins.tuple,
##         exit: builtins.bool
##     ) -> boostNode.extension.type.SelfClass:
    def _terminate(cls, arguments, exit):
##
        '''Termines current runnable and all child threads.'''
        cls.__termination_lock.release()
        if builtins.len(arguments) and arguments[0] == signal.SIGINT:
            sys.exit(130)
        elif exit:
            '''
                NOTE: "sys.exit()" has to be called to terminate all
                child threads.
            '''
            sys.exit()
        return cls

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _handle_module_running(
##         self: boostNode.extension.type.Self,
##         arguments: builtins.tuple, keywords: builtins.dict,
##         run: builtins.bool
##     ) -> boostNode.extension.type.Self:
    def _handle_module_running(self, arguments, keywords, run):
##
        '''Handle the running interface for current module.'''
        if not (self._childrens_module.__test_mode__ or run):
            self.__class__.__termination_lock.acquire()
            signal_numbers = \
                boostNode.extension.system.Platform.termination_signal_numbers
            for signal_number in signal_numbers:
                signal.signal(signal_number, self.trigger_stop)
        try:
            self._run(*arguments, **keywords)
        except builtins.Exception as exception:
            if(self._childrens_module.__test_mode__ or
               self._childrens_module.__logger__.isEnabledFor(logging.DEBUG) or
               sys.flags.debug):
                raise
            else:
                __logger__.critical(
                    '{exception_name}: {exception_message}\nType "'
                    '{program_file_path} --help" for additional '
                    'informations.'.format(
                        exception_name=exception.__class__.__name__,
                        exception_message=builtins.str(exception),
                        program_file_path=sys.argv[0]))
                sys.exit(1)
        finally:
            '''
                NOTE: we have to let the exception stop all contexts to make
                sure that the whole traceback could be printed before
                termination.
            '''
            self.trigger_stop(exit=False)
        return self

        # endregion

    # endregion

# endregion


# region classes

## python3.3 class Platform:
class Platform(builtins.object):
    '''
        Handles issues dealing with the underlying operating system.
    '''

    # region constant properties

        # region public

    '''
        Saves a list of process signal codes which should bring the application
        down.
    '''
    TERMINATION_SIGNALS = 'SIGTERM', 'SIGINT', 'SIGHUP'
    '''Saves a list of known unix commands to open a specified file.'''
    UNIX_OPEN_APPLICATIONS = (
        'gnome-open', 'kde-open', 'xdg-open', 'gedit', 'mousepad', 'gvim',
        'vim', 'emacs', 'nano', 'vi', 'less', 'cat')

        # endregion

    # endregion

    # region dynamic properties

        # region public

    '''Saves the current operating system type.'''
    operating_system = 'unknown'
    '''
        Saves an indicating value weather a currently running thread should be
        terminated on next possibility.
    '''
    terminate_thread = False
    '''
        Saves an indicating value weather a currently running thread should be
        paused on next possibility. By setting this value back to "True"
        paused threads will continue their work.
    '''
    pause_thread = False
    '''Holds all process termination signal numbers.'''
    termination_signal_numbers = []

        # endregion

    # endregion

    # region static methods

        # region public

            # region special

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3     def __init__(cls: boostNode.extension.type.SelfClass) -> None:
    def __init__(cls):
        '''
            Determines the operating system.

            Examples:

            >>> os = Platform().operating_system
            >>> os == Platform.operating_system
            True
            >>> os # doctest: +SKIP
            'posix'
        '''
        for termination_signal_number in cls.TERMINATION_SIGNALS:
            if builtins.hasattr(signal, termination_signal_number):
                cls.termination_signal_numbers.append(builtins.getattr(
                    signal, termination_signal_number))
        if 'nt' == os.name:
            cls.operating_system = 'windows'
        elif 'darvin' == sys.platform:
            cls.operating_system = 'macintosh'
        elif sys.platform.startswith('linux'):
            cls.operating_system = 'linux'
        elif 'posix' == os.name:
            cls.operating_system = 'posix'

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def __repr__(cls: boostNode.extension.type.SelfClass) -> builtins.str:
    def __repr__(cls):
##
        '''
            Invokes if this object should describe itself by a string.

            Examples:

            >>> repr(Platform()) # doctest: +ELLIPSIS
            'Object of "Platform" on operating system "...".'
        '''
        return 'Object of "{class_name}" on operating system '\
               '"{operating_system}".'.format(
                   class_name=cls.__name__,
                   operating_system=cls.operating_system)

            # endregion

            # region change computer status

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def make_computer_ready(
##         cls: boostNode.extension.type.SelfClass,
##         *arguments: builtins.object, **keywords: builtins.object
##     ) -> builtins.tuple:
    def make_computer_ready(cls, *arguments, **keywords):
##
        '''
            Wakes a remote computer and ensure that it is ready by pinging till
            it answers.
        '''
        return cls.change_computer_status(
            *arguments, handler=cls.wake_computer, **keywords)

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def change_computer_status(
##         cls: boostNode.extension.type.SelfClass, host: builtins.str,
##         mac_address: builtins.str, broadcast: builtins.str,
##         handler: (types.MethodType, types.FunctionType), down=False,
##         number_of_tries=10
##     ) -> builtins.tuple:
    def change_computer_status(
        cls, host, mac_address, broadcast, handler, down=False,
        number_of_tries=10
    ):
##
        '''
            Shuts down or boot a computer and ensure that is is available after
            boot or not available if it should be shut down.

            Returns a tuple: first value indicats weather it was successfull
            and second is "True" if computer status was needed
            to be changed and "False" otherwise.
        '''
        __logger__.info('Try to reach "%s". Please wait.', host)
        counter = 1
        timeout_in_seconds = 3
        maximum_timeout_in_seconds = 60
        while counter <= number_of_tries and not (
            down or cls.check_computer_reachability(
                timeout_in_seconds, host
            )) or (down and cls.check_computer_reachability(
                timeout_in_seconds, host)):
            counter += 1
            handler(mac_address, broadcast)
            __logger__.info(
                '%d. try to reach "%s" with timeout of %d seconds.',
                counter, host, timeout_in_seconds)
            time.sleep(timeout_in_seconds)
            timeout_in_seconds = builtins.min(
                timeout_in_seconds + 1, maximum_timeout_in_seconds)
        return counter <= number_of_tries, counter > 1

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def wake_computer(
##         cls: boostNode.extension.type.SelfClass, mac_address: builtins.str,
##         broadcast: builtins.str
##     ) -> builtins.bool:
    def wake_computer(cls, mac_address, broadcast):
##
        '''
            Wakes up a remote computer using a magic package
            (wake-on-lan-package).

            Examples:

            >>> Platform.wake_computer(
            ...     'f0:de:f1:a2:55:9f', '192.168.178.255'
            ... ) # doctest: +SKIP
        '''
        '''Check mac-address format and try to compensate if necessary.'''
        if builtins.len(mac_address) == 12 + 5:
            sep = mac_address[2]
            mac_address = mac_address.replace(sep, '')
        elif builtins.len(mac_address) != 12:
            raise __exception__('Incorrect MAC-address format given.')
        '''Pad the synchronization stream.'''
        data = b'FFFFFFFFFFFF' + (mac_address * 20).encode()
        send_data = b''
        '''Split up the hex values and pack.'''
        for counter in builtins.range(builtins.len(data), 2):
            send_data += struct.pack(
                'B', builtins.int(data[counter:counter + 2], 16))
        '''Broadcast it to the network.'''
        try:
            wake_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            wake_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            wake_socket.sendto(send_data, (broadcast, 7))
        except socket.error:
            return False
        finally:
            wake_socket.close()
        return True

            # endregion

        # region thread handling

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def check_thread(cls, waiting_delay_in_seconds=2) -> builtins.bool:
    def check_thread(cls, waiting_delay_in_seconds=2):
##
        '''
            Checks weather the current thread should be paused or terminated.
            If thread should be terminated "True" will be given back.
            In case of pausing the current thread stay in the current function
            call still a continue event is triggered.

            Examples:

            >>> Platform.check_thread()
            False

            >>> Platform.terminate_thread = True
            >>> Platform.check_thread()
            True

            >>> Platform.terminate_thread = False
            >>> Platform.check_thread()
            False

            >>> Platform.pause_thread = True
            >>> Platform.terminate_thread = True
            >>> Platform.check_thread()
            True

            >>> Platform.pause_thread = True
            >>> Platform.terminate_thread = False
            >>> Platform.check_thread() # doctest: +SKIP
            will wait until "pause_thread" is setted to "False" or
            "terminate_thread" to "True".
        '''
        while cls.pause_thread or cls.terminate_thread:
            if cls.terminate_thread:
                return True
            time.sleep(waiting_delay_in_seconds)
        return False

        # endregion

        # region process handling

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def set_process_lock(
##         cls: boostNode.extension.type.SelfClass, description=''
##     ) -> boostNode.extension.type.SelfClass:
    def set_process_lock(cls, description=''):
##
        '''
            Sets a global lock. Creates a file with given name prefix of
            "description".

            Examples:

            >>> Platform.set_process_lock('temp') # doctest: +ELLIPSIS
            <class ...Platform...>
            >>> bool(boostNode.extension.file.Handler('temp_lock'))
            True
            >>> Platform.set_process_lock() # doctest: +ELLIPSIS
            <class ...Platform...>
            >>> bool(boostNode.extension.file.Handler('_lock'))
            True
            >>> Platform.clear_process_lock() # doctest: +ELLIPSIS
            <class ...Platform...>
        '''
        boostNode.extension.file.Handler(
            location=boostNode.extension.native.Module.get_package_name(
                frame=inspect.currentframe(),
                path=True
            ) + description + '_lock',
            must_exist=False
        ).content = ' '
        return cls

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def clear_process_lock(
##         cls: boostNode.extension.type.SelfClass, description=''
##     ) -> boostNode.extension.type.SelfClass:
    def clear_process_lock(cls, description=''):
##
        '''
            Removes a prior setted lock file.

            Examples:

            >>> file = boostNode.extension.file.Handler(
            ...     'temp_file_lock', must_exist=False)
            >>> file.content = ' '
            >>> Platform.clear_process_lock('temp_file') # doctest: +ELLIPSIS
            <class ...Platform...>
            >>> bool(file)
            False

            >>> Platform.set_process_lock('temp_test') # doctest: +ELLIPSIS
            <class ...Platform...>
            >>> Platform.clear_process_lock('temp_test') # doctest: +ELLIPSIS
            <class ...Platform...>
            >>> Platform.check_process_lock('temp_test')
            False
        '''
        boostNode.extension.file.Handler(
            location=boostNode.extension.native.Module.get_package_name(
                frame=inspect.currentframe(),
                path=True
            ) + description + '_lock',
            must_exist=False
        ).remove_file()
        return cls

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def check_process_lock(
##         cls: boostNode.extension.type.SelfClass, description=''
##     ) -> builtins.bool:
    def check_process_lock(cls, description=''):
##
        '''
            Checks if a lock file with given description exists.
            NOTE: Calling this function doesn't give you savety during race
            conditions.

            Examples:

            >>> Platform.set_process_lock('temp') # doctest: +ELLIPSIS
            <class ...Platform...>
            >>> Platform.check_process_lock('temp')
            True
        '''
        return builtins.bool(
            boostNode.extension.file.Handler(
                location=boostNode.extension.native.Module.get_package_name(
                    frame=inspect.currentframe(),
                    path=True
                ) + description + '_lock',
                must_exist=False))

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def run(
##         cls: boostNode.extension.type.SelfClass,
##         command: collections.Iterable,
##         command_arguments=None, secure=False, error=True, shell=None,
##         log=False, no_blocking=False, *arguments: builtins.object,
##         **keywords: builtins.object
##     ) -> builtins.dict:
    def run(
        cls, command, command_arguments=None, secure=False, error=True,
        shell=None, log=False, no_blocking=False, *arguments, **keywords
    ):
##
        '''
            Runs a command natively on the current operating system using the
            command line. Result will be given back as tuple. First element is
            standard and second error output.

            "command" A command line interface command optionally with
                      arguments.
            "command_arguments" A list of arguments passing through the command
                                line interface.
            "secure" Disable output piping by python and run command in systems
                     native process.
            "error" If "False" exceptions by running command are kept back.
            "shell" Simulate a shell if "True". If explicit command arguments
                    are given shell's default value is "True" and "False"
                    otherwise.
            "log" If "True" standard output will be logged with level "info"
                  and error output with level "warning".
            "no_blocking" If "True" resulting output won't be a string. You
                          will get an python "IOBuffer" like object.
                          NOTE: If Buffer is empty and you try to read from
                          Buffer an exception will occur.

            All following arguments are given through python's native
            "subprocess.Popen()" class initialisation.

            Examples:

            >>> Platform.run(command='ls') # doctest: +SKIP
            {...'standard_output': ...}

            >>> Platform.run(
            ...     command=('ls', 'chmod +x test.py'), shell=True
            ... ) # doctest: +SKIP
            {...'standard_output': ...}

            >>> Platform.run(
            ...     command='not', command_arguments=('existing',), error=False
            ... ) # doctest: +ELLIPSIS
            {...'standard_output': ...}

            >>> Platform.run(
            ...     command='not', command_arguments=('existing',)
            ... ) # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            boostNode.extension.native.SystemError: Command "not existing" ...
        '''
        if command_arguments is None:
            command_arguments = []
            shell = False if shell is None else shell
        elif shell is None:
            shell = True
        if builtins.isinstance(command, builtins.str):
            result = cls._run_one_command(
                command, command_arguments, secure, error, shell, no_blocking,
                *arguments, **keywords)
        else:
            result = cls._run_multiple_commands(
                commands=command, command_arguments=command_arguments,
                secure=secure, error=error, shell=shell, *arguments,
                **keywords)
        return cls._log_command_result(result, log, secure, no_blocking)

    @boostNode.paradigm.aspectOrientation.JointPoint
    # NOTE: "location" can't get file handler signature type. It isn't loaded
    # yet.
## python3.3
##     def open(
##         cls: boostNode.extension.type.SelfClass, location
##     ) -> builtins.dict:
    def open(cls, location):
##
        '''
            Opens the current file with its default user preference
            application.

            On Unix, the return value is the exit state of the process encoded
            in the format specified for wait(). Note that "POSIX" does not
            specify the meaning of the return value of the C system() function,
            so the return value of the Python function is system-dependent.
            On Windows, the return value is that returned by the system shell
            after running command. The shell is given by the Windows
            environment variable "COMSPEC": it is usually "cmd.exe",
            which returns the exit status of the command run; on systems
            using a non-native shell, consult your shell documentation.

            Examples:

            >>> Platform.open('/path/to/file') # doctest: +SKIP

            >>> Platform.open(boostNode.extension.file.Handler(
            ...     '/path/to/file'
            ... )) # doctest: +SKIP
        '''
        file = boostNode.extension.file.Handler(location)
        if builtins.hasattr(os, 'startfile'):
            return os.startfile(file)
        shell_file = boostNode.extension.native.String(
            file._path
        ).validate_shell()
        for unix_application_name in cls.UNIX_OPEN_APPLICATIONS:
            result = boostNode.extension.system.Platform.run(
                command=unix_application_name, command_arguments=(shell_file,))
            if result['return_code'] == 0:
                break
        return result

            # endregion

        # endregion

        # region protected

            # region change computer status

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def check_computer_reachability(
##         cls: boostNode.extension.type.SelfClass,
##         timeout_in_seconds: builtins.int, host: builtins.str
##     ) -> builtins.bool:
    def check_computer_reachability(cls, timeout_in_seconds, host):
##
        '''
            Checks if a remote computer is available by pinging it.
        '''
        check_computer_reachability_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        check_computer_reachability_socket.settimeout(timeout_in_seconds)
        try:
            check_computer_reachability_socket.connect((host, 22))
        except socket.error:
            return False
        finally:
            check_computer_reachability_socket.close()
        return True

            # endregion

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _log_command_result(
##         cls: boostNode.extension.type.SelfClass, result: builtins.dict,
##         log: builtins.bool, secure: builtins.bool,
##         no_blocking: builtins.bool
##     ) -> builtins.dict:
    def _log_command_result(cls, result, log, secure, no_blocking):
##
        '''
            Logs the result of an invoked and given subprocess output.
        '''
        if builtins.isinstance(result['standard_output'], builtins.list):
            for index, standard_output in builtins.enumerate(
                result['standard_output']
            ):
                cls._log_command_result({
                    'standard_output': standard_output,
                    'error_output': result['error_output'][index]},
                    log, secure, no_blocking)
        elif log and not (secure or no_blocking):
            if result['standard_output']:
                __logger__.info(result['standard_output'])
            if result['error_output']:
                __logger__.warning(result['error_output'])
        return result

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _run_one_command(
##         cls: boostNode.extension.type.SelfClass,
##         command: collections.Iterable,
##         command_arguments: collections.Iterable, secure: builtins.bool,
##         error: builtins.bool, shell: builtins.bool,
##         no_blocking: builtins.bool, *arguments: builtins.object,
##         **keywords: builtins.object
##     ) -> builtins.dict:
    def _run_one_command(
        cls, command, command_arguments, secure, error, shell, no_blocking,
        *arguments, **keywords
    ):
##
        '''
            Runs a command line command in its own process.
        '''
        result = {'standard_output': '', 'error_output': '', 'return_code': 1}
        command = ' '.join([command] + builtins.list(command_arguments))
        if secure:
            result['return_code'] = os.system(command)
            if error and result['return_code'] != 0:
                sys.exit(result['return_code'])
        else:
## python3.3
##             with subprocess.Popen(
##                 command, *arguments, shell=shell,
##                 stdin=subprocess.PIPE, stdout=subprocess.PIPE,
##                 stderr=subprocess.PIPE, **keywords
##             ) as process_handler:
##                 result = cls._communicate_to_process_handler(
##                     process_handler, no_blocking)
            process_handler = subprocess.Popen(
                command, *arguments, shell=shell,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, **keywords)
            result = cls._communicate_to_process_handler(
                process_handler, no_blocking)
##
            if error and result['return_code'] != 0:
                raise __exception__(
                    'Command "%s" returns a none zero return code (%d).',
                    command, result['return_code'])
        return result

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _communicate_to_process_handler(
##         cls: boostNode.extension.type.SelfClass,
##         process_handler: subprocess.Popen,
##         no_blocking: builtins.bool
##     ) -> builtins.dict:
    def _communicate_to_process_handler(cls, process_handler, no_blocking):
##
        '''
            Handle communication with a given process. It returns all api
            informations about the given process.
        '''
        if fcntl and no_blocking:
            fcntl.fcntl(
                process_handler.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
            fcntl.fcntl(
                process_handler.stderr.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
            result = {
                'standard_output': process_handler.stdout,
                'error_output': process_handler.stderr}
        else:
            result = process_handler.communicate()
## python3.3
##             result = {
##                 'standard_output': result[0].decode(),
##                 'error_output': result[1].decode()}
            result = {
                'standard_output': result[0],
                'error_output': result[1]}
##
            result['return_code'] = process_handler.returncode
        return result

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _run_multiple_commands(
##         cls: boostNode.extension.type.SelfClass,
##         commands: collections.Iterable,
##         command_arguments: collections.Iterable, secure: builtins.bool,
##         error: builtins.bool, shell: builtins.bool,
##         *arguments: builtins.object, **keywords: builtins.object
##     ) -> builtins.dict:
    def _run_multiple_commands(
        cls, commands, command_arguments, secure, error, shell,
        *arguments, **keywords
    ):
##
        '''
            Runs a list of command line commands as its own process.
        '''
        result = {'standard_output': [], 'error_output': [], 'return_code': []}
        for sub_command in commands:
            sub_result = cls.run(
                command=sub_command, command_arguments=command_arguments,
                secure=secure, error=error, shell=shell, *arguments,
                **keywords)
            if builtins.isinstance(sub_result, builtins.dict):
                result['standard_output'].append(sub_result['standard_output'])
                result['error_output'].append(sub_result['error_output'])
                result['return_code'].append(sub_result['return_code'])
        return result

        # endregion

    # endregion


## python3.3 class CommandLine:
class CommandLine(builtins.object):
    '''
        Defines which possibilities are supported for boolean interactive
        command line user inputs.
    '''

    # region constant properties

        # region public

    POSITIVE_INPUTS = 'y', 'yes', 'positive'
    NEGATIVE_INPUTS = 'n', 'no', 'not', 'none', 'negative'

    '''Output on every information request for applications.'''
    EPILOG = 'powered by thaibault'
    '''Small overview about the right using of this program.'''
    USAGE = ('\n  %(prog)s [positional arguments] [optional arguments]\n\n'
             '  Type "%(prog)s --help" for more informations.')
    '''Set the global default value for arguments.'''
    ARGUMENT_DEFAULT = None
    '''The set of characters that prefix optional arguments.'''
    PREFIX_CHARS = '-'
    '''
        The set of characters that prefix files from which additional
        arguments should be read.
    '''
    FROMFILE_PREFIX_CHARS = '@'
    '''
        Usually unnecessary, defines strategy to resolve conflicting
        optionals.
    '''
    CONFLICT_HANDLER = 'resolve'
    '''Defines standard arguments for every command line interface program.'''
    DEFAULT_ARGUMENTS = (
        {'arguments': ('-x', '--version'),
         'keywords': {
             'action': 'version',
             'version': {'execute': '__version_string__'},
             'help': 'Show current program version.',
             'dest': 'version'}},
        {'arguments': ('-l', '--log-level'),
         'keywords': {
             'action': 'store',
             'default': 'critical',
             'type': builtins.str,
             'choices': ('debug', 'info', 'warning', 'error',
                         'critical'),
             'help': {'execute':
                      '"Defines log level of current program '
                      'instance. (Level: \\"%s\\")" % '
                      '"\\", \\"".join(__default_arguments__[1]["keywords"]'
                      '["choices"])'},
             'dest': 'log_level',
             'metavar': 'LOG_LEVEL'}})
    DEFAULT_CALLER_ARGUMENTS = (
        {'arguments': ('-c', '--module-object',),
         'keywords': {
             'action': 'store',
             'default': {'execute': 'default_caller'},
             'type': builtins.str,
             'choices': {'execute': 'objects'},
             'help': {'execute':
                      '"Select a callable module object to run. '
                      '(Objects: \\"%s\\")" % "\\", \\"".join(objects)'},
             'dest': 'module_object',
             'metavar': 'CALLABLE_MODULE_OBJECT'}},
        {'arguments': ('-t', '--test'),
         'keywords': {
             'action': 'store_true',
             'default': False,
             'help': 'Test current library.',
             'dest': 'test'}},
        {'arguments': ('-v', '--verbose-test'),
         'keywords': {
             'action': 'store_true',
             'default': False,
             'help': 'Test current library verbosely.',
             'dest': 'verbose_test'}},
        {'arguments': ('-m', '--meta-help'),
         'keywords': {
             'action': 'store_true',
             'default': False,
             'help': 'Shows this help message.',
             'dest': 'meta_help'}})
    '''Defines arguments for performing actions on python packages.'''
    PACKAGE_INTERFACE_ARGUMENTS = (
        {'arguments': ('commands',),
         'keywords': {
             'action': 'store',
             'default': '',
             'type': builtins.str,
             'choices': ('all', 'test', 'clear', 'document', 'lint'),
             #'required': True,
             'help': {'execute':
                      '"Select commands for performing action with this '
                      'package. (Command: \\"%s\\")" % '
                      '"\\", \\"".join(choices)'},
             'metavar': 'COMMAND'}},)

        # endregion

    # endregion

    # region dynamic properties

        # region public

    current_argument_parser = None

        # endregion

    # endregion

    # region static methods

        # region public

            # region special

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def __repr__(cls: boostNode.extension.type.SelfClass) -> builtins.str:
    def __repr__(cls):
##
        '''
            Invokes if this object should describe itself by a string.

            Examples:

            >>> repr(CommandLine()) # doctest: +ELLIPSIS
            'Object of "CommandLine" with parser "None".'
        '''
        return 'Object of "{class_name}" with parser "{parser}".'.format(
            class_name=cls.__name__,
            parser=builtins.repr(cls.current_argument_parser))

            # endregion

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def argument_parser(
##         cls: boostNode.extension.type.SelfClass, arguments=(),
##         module_name=__name__, scope={}, meta=False, description='',
##         version='', default=True,
##         *additional_arguments: builtins.object,
##         **keywords: builtins.object
##     ) -> argparse.Namespace:
    def argument_parser(
        cls, arguments=(), module_name=__name__, scope={}, meta=False,
        description='', version='', default=True, *additional_arguments,
        **keywords
    ):
##
        '''
            Represents a basic argument parsing for command line interface
            inputs. It's used as default pattern for many interface concepts.

            Examples:

            >>> import copy
            >>> log_level = boostNode.extension.output.Logger.default_level
            >>> sys_argv_save = copy.copy(sys.argv)
            >>> del sys.argv[1:]

            >>> sys.argv += '--long', 'hans'
            >>> CommandLine.argument_parser((
            ...     {'arguments': ('-s', '--long'),
            ...      'keywords': {'action': 'store', 'type': str}},))
            Namespace(log_level='critical', long='hans')

            >>> sys.argv = sys_argv_save
            >>> boostNode.extension.output.Logger.change_all(
            ...     level=log_level) # doctest: +ELLIPSIS
            <class ...boostNode.extension.output.Logger...>
        '''
        version = cls._get_version(version, module_name)
        description = cls._get_description(description, module_name, version)
        scope.update({
            '__version_string__': version,
            '__default_arguments__': cls.DEFAULT_ARGUMENTS,
            'type': builtins.type})
        cls.current_argument_parser = argparse.ArgumentParser(
            *additional_arguments, **cls._determine_argument_parser_keywords(
                keywords, meta, description))
        default_arguments = [] if not default else cls.DEFAULT_ARGUMENTS
        cls._add_command_line_arguments(arguments, default_arguments, scope)
        if meta:
            arguments_split = cls.current_argument_parser.parse_known_args()
            arguments = arguments_split[0]
            sys.argv = [sys.argv[0]] + arguments_split[1]
        else:
            arguments = cls.current_argument_parser.parse_args()
        cls.handle_log_level(arguments)
        if sys.modules[module_name].__doc__ is None:
            __logger__.warning(
                'There is no module level docstring available (It should be '
                'used as description for this module if running with "help" '
                'flag).')
        return arguments

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def handle_log_level(
##         cls: boostNode.extension.type.SelfClass,
##         arguments: argparse.Namespace
##     ) -> boostNode.extension.type.SelfClass:
    def handle_log_level(cls, arguments):
##
        '''
            Handles log level in a generic way. If given command line arguments
            contains a log level all logger levels will be setted to this
            level.
        '''
        if(builtins.hasattr(arguments, 'log_level') and
           arguments.log_level is not None):
            boostNode.extension.output.Logger.change_all(
                level=(arguments.log_level,))
        return cls

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def boolean_input(
##         cls: boostNode.extension.type.SelfClass, question: builtins.str
##     ) -> builtins.bool:
    def boolean_input(cls, question):
##
        '''
            This methods implements a handy way to get "yes" or "no" answers
            from the user via command line.

            Examples:

            >>> CommandLine.boolean_input(
            ...     question='All right? {boolean_arguments}: '
            ... ) # doctest: +SKIP
            All right? (Choose one of: y, n...)
        '''
## python3.3         input_string = builtins.input(question.format(
        input_string = builtins.raw_input(question.format(
            boolean_arguments='(Choose one of: {choices})'.format(
                choices=', '.join(cls.POSITIVE_INPUTS + cls.NEGATIVE_INPUTS)))
        ).lower()
        if input_string in cls.POSITIVE_INPUTS:
            return True
        if input_string in cls.NEGATIVE_INPUTS:
            return False
        return cls.boolean_input(question)

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def determine_wrapped_objects(
##         cls: boostNode.extension.type.SelfClass, module: types.ModuleType
##     ) -> builtins.dict:
    def determine_wrapped_objects(cls, module):
##
        '''
            Returns all aspect orientated wrapped methods in given module.

            Examples:

            >>> CommandLine.determine_wrapped_objects(
            ...     boostNode.extension.system
            ... ) # doctest: +ELLIPSIS
            {...'determine_wrapped_objects': <function ...>...}
        '''
        objects = {}
        for name, object in module.__dict__.items():
            '''Exclude included objects.'''
            if inspect.getmodule(object) is module:
                '''Iterate classes and functions.'''
                if(builtins.isinstance(
                   object, boostNode.paradigm.aspectOrientation.JointPoint)):
                    objects[name] = builtins.getattr(module, name).__func__
                if builtins.hasattr(object, '__dict__'):
                    for sub_name, sub_object in object.__dict__.items():
                        '''Iterate inner functions.'''
                        if(builtins.isinstance(
                           sub_object,
                           boostNode.paradigm.aspectOrientation.JointPoint)):
                            objects[sub_name] = sub_object.__func__
        return objects

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def generic_package_interface(
##         cls: boostNode.extension.type.SelfClass, name=__name__,
##         frame=inspect.currentframe(), command_line_arguments=(),
##         linter='pep8 --repeat --ignore=E225,E701',
##         documenter='pydoc3.3', documenter_arguments=('-w',),
##         documentation_path='documentation', clear_old_documentation=True,
##         documentation_file_extension='html', temp_file_patterns=(
##             '^temp_.+$', '^__pycache__$', '^.+\.pyc$', '^.+~$'),
##         exclude_packages=()
##     ) -> (builtins.tuple, builtins.bool):
    def generic_package_interface(
        cls, name=__name__, frame=inspect.currentframe(),
        command_line_arguments=(), linter='pep8 --repeat --ignore=E225',
        documenter='pydoc2', documenter_arguments=('-w',),
        documentation_path='documentation', clear_old_documentation=True,
        documentation_file_extension='html', temp_file_patterns=(
            '^temp_.+$', '^__pycache__$', '^.+\.pyc$', '^.+~$'),
        exclude_packages=()
    ):
##
        '''
            Provides a command-line interface like a makefile.
            Supported features are linting, generate documentation, testing and
            removing temporay files.

            Examples:

            >>> CommandLine.generic_package_interface(
            ...     name=__name__, frame=inspect.currentframe()
            ... ) # doctest: +SKIP
            Namespace(log_level='info'...)
        '''
        if name == '__main__':
            all, arguments, current_working_directory_save = \
                cls._package_start_helper(name, frame, command_line_arguments)
            try:
                module_names = cls._handle_packages_in_package(
                    current_working_directory_save, frame,
                    command_line_arguments, exclude_packages
                )._get_modules(name)
                cls._test_lint_document_modules(
                    all, arguments, module_names, temp_file_patterns, linter,
                    documentation_path, clear_old_documentation, documenter,
                    documenter_arguments, documentation_file_extension, frame,
                    current_working_directory_save)
            finally:
                '''Tidy up.'''
                cls._restore_current_directory(
                    clear=all or 'clear' in arguments.commands,
                    current_directory=current_working_directory_save,
                    temp_file_patterns=temp_file_patterns)
            return all, arguments, current_working_directory_save
        return False

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def generic_module_interface(
##         cls: boostNode.extension.type.SelfClass, module: builtins.dict,
##         test=False, default_caller=None, caller_arguments=(),
##         caller_keywords={}
##     ) -> boostNode.extension.type.SelfClass:
    def generic_module_interface(
        cls, module, test=False, default_caller=None,
        caller_arguments=(), caller_keywords={}
    ):
##
        '''
            Provides a generic command line interface for modules.
            Things like unit testing or calling objects in module are provided.

            Examples:

            >>> CommandLine.module(
            ...     module={'name': __name__, 'scope': sys.modules[__name__]},
            ...     default_caller='main', test=False) # doctest: +SKIP
        '''
        if module['name'] == '__main__' or test:
            callable_objects, default_caller = cls._determine_callable_objects(
                module, default_caller, test)
            given_arguments = cls.argument_parser(
                arguments=cls.DEFAULT_CALLER_ARGUMENTS,
                scope={'objects': callable_objects,
                       'default_caller': default_caller},
                meta=True, default=False)
            if given_arguments.meta_help:
                cls.current_argument_parser.print_help()
            elif given_arguments.verbose_test or given_arguments.test or test:
                cls.test_module(module, verbose=given_arguments.verbose_test)
            elif given_arguments.module_object is not False:
                cls._call_module_object(
                    module, callable_objects,
                    object=given_arguments.module_object,
                    caller_arguments=caller_arguments,
                    caller_keywords=caller_keywords)
        return cls

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def test_module(
##         cls: boostNode.extension.type.SelfClass, module: builtins.dict,
##         verbose=False
##     ) -> boostNode.extension.type.SelfClass:
    def test_module(cls, module, verbose):
##
        '''
            Test a given's module doctests.
        '''
        test_folder = boostNode.extension.file.Handler(
            location=tempfile.mkdtemp(suffix=module['scope'].__name__))
        module['scope'].__test_folder__ = test_folder.path
        module['scope'].__test__ = cls.determine_wrapped_objects(
            module=module['scope'])
        module['scope'].__name__ = '__main__'
        module['scope'].__test_mode__ = True
        module['scope'].__test_buffer__ = \
            boostNode.extension.output.Buffer()
        default_print_buffer_save = \
            boostNode.extension.output.Print.default_buffer
        log_level_save = boostNode.extension.output.Logger.default_level
        logger_buffer_save = boostNode.extension.output.Logger.buffer
        '''
            Modules get log level "info" as default for their test
            cases.
        '''
        boostNode.extension.output.Print.default_buffer = \
            module['scope'].__test_buffer__
        boostNode.extension.output.Logger.change_all(
            level=('info',), buffer=(module['scope'].__test_buffer__,))
## python3.4
##         doctest.testmod(
##             module['scope'], verbose=verbose,
##             optionflags=doctest.DONT_ACCEPT_TRUE_FOR_1 |
##             doctest.REPORT_ONLY_FIRST_FAILURE | doctest.FAIL_FAST)
        doctest.testmod(
            module['scope'], verbose=verbose,
            optionflags=doctest.DONT_ACCEPT_TRUE_FOR_1 |
            doctest.REPORT_ONLY_FIRST_FAILURE)
##
        '''Recover old output buffer.'''
        boostNode.extension.output.Logger.change_all(
            level=log_level_save, buffer=logger_buffer_save)
        boostNode.extension.output.Print.default_buffer = \
            default_print_buffer_save
        if not sys.flags.debug:
            test_folder.remove_deep()
        return cls

        # endregion

        # region protected

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _determine_argument_parser_keywords(
##         cls: boostNode.extension.type.SelfClass, keywords: builtins.dict,
##         meta: builtins.bool, description: builtins.str
##     ) -> builtins.dict:
    def _determine_argument_parser_keywords(
        cls, keywords, meta, description
    ):
##
        '''
            Determines keyword arguments given to python's native command line
            argument parser.
        '''
        determined_keywords = {
            'description': description,
            'epilog': cls.EPILOG,
            'add_help': not meta,
            'argument_default': cls.ARGUMENT_DEFAULT,
            'prefix_chars': cls.PREFIX_CHARS,
            'fromfile_prefix_chars': cls.FROMFILE_PREFIX_CHARS,
            'conflict_handler': cls.CONFLICT_HANDLER,
            'usage': cls.USAGE}
        determined_keywords.update(keywords)
        return determined_keywords

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _validate_command_line_argument(
##         cls: boostNode.extension.type.SelfClass, argument: builtins.dict,
##         arguments: collections.Iterable
##     ) -> boostNode.extension.type.SelfClass:
    def _validate_command_line_argument(cls, argument, arguments):
##
        '''
            Checks command line arguments for rendundant option names.
        '''
        for other_argument in builtins.list(
                cls.DEFAULT_CALLER_ARGUMENTS) +\
                builtins.list(cls.DEFAULT_ARGUMENTS) +\
                builtins.list(arguments):
            if(other_argument['arguments'][0] ==
               argument['arguments'][0] and
               (builtins.len(argument['arguments']) != builtins.len(
                   other_argument['arguments']) or
                builtins.len(argument['arguments']) > 1 and
                other_argument['arguments'][1] !=
                argument['arguments'][1])
               ):
                raise __exception__(
                    'Argument "%s" shadows argument "%s" with shortcut '
                    '"%s".', argument['keywords']['dest'],
                    other_argument['keywords']['dest'],
                    argument['arguments'][0])
        return cls._validate_command_line_argument_again_help_argument(
            argument)

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _validate_command_line_argument_again_help_argument(
##         cls: boostNode.extension.type.SelfClass, argument: builtins.dict
##     ) -> boostNode.extension.type.SelfClass:
    def _validate_command_line_argument_again_help_argument(cls, argument):
##
        '''
            Checks if given command line argument specification collides with
            default help command line argument.
        '''
        if(argument['arguments'][0] == '-h' or
           builtins.len(argument['arguments']) > 1 and
           argument['arguments'][1] == '--help'):
            raise __exception__(
                'Argument "%s" shadows default argument "help".',
                argument['keywords']['dest'])
        return cls

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _handle_initializer_default_values(
##         cls: boostNode.extension.type.SelfClass, scope: builtins.dict
##     ) -> builtins.dict:
    def _handle_initializer_default_values(cls, scope):
##
        '''
            Determines the default value from the runnable module's
            "_initialize" method forced to be defined by the "Runnable"
            implementation.
        '''
        scope['__initializer_default_value__'] = None
        if 'self' in scope:
            '''Unpack initializer method.'''
            initializer = scope['self']._initialize
            while builtins.hasattr(initializer, '__wrapped__'):
                initializer = initializer.__wrapped__
## python3.3
##             parameters = inspect.signature(initializer).parameters
##             if scope['__name__'] in parameters:
##                 if(parameters[scope['__name__']].default is
##                    inspect.Parameter.empty):
##                     if builtins.type(
##                         parameters[scope['__name__']].annotation
##                     ) is builtins.type:
##                         '''
##                             Set default value to default value of sepecified
##                             parameter type.
##                         '''
##                         scope['__initializer_default_value__'] = \
##                             parameters[scope['__name__']].annotation()
##                 else:
##                     scope['__initializer_default_value__'] = \
##                         parameters[scope['__name__']].default
            if inspect.getargspec(initializer).defaults:
                parameters = builtins.dict(builtins.zip(
                    inspect.getargspec(
                        initializer
                    ).args[builtins.len(
                        inspect.getargspec(initializer).args
                    ) - builtins.len(inspect.getargspec(
                        initializer
                    ).defaults):],
                    inspect.getargspec(initializer).defaults))
                if scope['__name__'] in parameters:
                    scope['__initializer_default_value__'] = \
                        parameters[scope['__name__']]
##
        return scope

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _add_command_line_arguments(
##         cls: boostNode.extension.type.SelfClass,
##         arguments: collections.Iterable,
##         default_arguments: collections.Iterable, scope: builtins.dict
##     ) -> boostNode.extension.type.SelfClass:
    def _add_command_line_arguments(
        cls, arguments, default_arguments, scope
    ):
##
        '''
            Add's command line arguments to python's native command line
            argument parser.
        '''
        for argument in builtins.list(arguments) + builtins.list(
                default_arguments):
            cls._validate_command_line_argument(argument, arguments)
            scope['__name__'] = argument['arguments'][0]
            if 'dest' in argument['keywords']:
                scope['__name__'] = argument['keywords']['dest']
            scope = cls._handle_initializer_default_values(scope)
            argument['keywords'] = cls._render_command_line_argument(
                argument=argument['keywords'], scope=scope)
            for keyword, value in argument['keywords'].items():
                try:
                    argument['keywords'][keyword] = cls\
                        ._render_command_line_argument(
                            argument=value, scope=scope)
                except builtins.Exception as exception:
                    raise __exception__(
                        'During rendering argument "%s". Error "%s" occurs '
                        'for "%s".', builtins.str(argument['keywords']),
                        builtins.str(exception), keyword)
            cls.current_argument_parser.add_argument(
                *argument['arguments'], **argument['keywords'])
        return cls

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _call_module_object(
##         cls: boostNode.extension.type.SelfClass, module: builtins.dict,
##         callable_objects: collections.Iterable, object: builtins.str,
##         caller_arguments: collections.Iterable,
##         caller_keywords: builtins.dict
##     ) -> boostNode.extension.type.SelfClass:
    def _call_module_object(
        cls, module, callable_objects, object, caller_arguments,
        caller_keywords
    ):
##
        '''
            Calls a suitable module object to provide an entry point for
            modules supporting a command line interface.
        '''
        if builtins.len(sys.argv) > 2 and sys.argv[1] in callable_objects:
            sys.argv = [sys.argv[0]] + sys.argv[2:]
        builtins.getattr(module['scope'], object)(
            *caller_arguments, **caller_keywords)
        return cls

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _determine_callable_objects(
##         cls: boostNode.extension.type.SelfClass, module: builtins.dict,
##         default_caller: (builtins.str, builtins.bool, builtins.type(None)),
##         test: builtins.bool
##     ) -> builtins.tuple:
    def _determine_callable_objects(cls, module, default_caller, test):
##
        '''
            Determines all callable objects and a default caller in given
            module. Both are given back in one tuple.
        '''
        callable_objects = boostNode.extension.native.Module\
            .get_defined_callables(scope=sys.modules[module['name']])
        if callable_objects:
            default_caller = boostNode.extension.native.Module.\
                determine_caller(
                    caller=default_caller, callable_objects=callable_objects)
        else:
            message = 'No callable objects in "{name}" ({module}).'.format(
                name=module['name'], module=module['scope'])
            if test:
                __logger__.info(message)
            else:
                raise __exception__(message)
        return callable_objects, default_caller

        # endregion

        # region protected

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _test_lint_document_modules(
##         cls: boostNode.extension.type.SelfClass,
##         all: builtins.bool, arguments: argparse.Namespace,
##         module_names: collections.Iterable,
##         temp_file_patterns: collections.Iterable, linter: builtins.str,
##         documentation_path: builtins.str,
##         clear_old_documentation: builtins.bool,
##         documenter: builtins.str,
##         documenter_arguments: collections.Iterable,
##         documentation_file_extension: builtins.str, frame: types.FrameType,
##         current_working_directory_save: builtins.str
##     ) -> boostNode.extension.type.SelfClass:
    def _test_lint_document_modules(
        cls, all, arguments, module_names, temp_file_patterns, linter,
        documentation_path, clear_old_documentation, documenter,
        documenter_arguments, documentation_file_extension, frame,
        current_working_directory_save
    ):
##
        '''
            Test, lints and documents given modules if corresponding command
            line flags are set.
        '''
        if all or 'test' in arguments.commands:
            cls._test_modules(module_names, temp_file_patterns)
        if all or 'lint' in arguments.commands:
            cls._lint_modules(linter, module_names)
        if all or 'document' in arguments.commands:
            cls._document_modules(
                documentation_path, clear_old_documentation,
                module_names, documenter, documenter_arguments,
                documentation_file_extension
            )._put_documentations_together(
                documentation_path, frame,
                current_working_directory_save,
                documentation_file_extension)
        return cls

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _get_modules(
##         cls: boostNode.extension.type.SelfClass, name: builtins.str
##     ) -> builtins.list:
    def _get_modules(cls, name):
##
        '''
            Get all module names in given package name.
        '''
        module_names = []
        if(builtins.hasattr(sys.modules[name], '__all__') and
           sys.modules[name].__all__):
            module_names = sys.modules[name].__all__
        else:
            __logger__.info('No modules found.')
        module_names.append('__init__')
        return module_names

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _get_version(
##         cls: boostNode.extension.type.SelfClass, version: builtins.str,
##         module_name: builtins.str
##     ) -> builtins.str:
    def _get_version(cls, version, module_name):
##
        '''
            Generates a version string by for a given module name.
            If "version" is not empty it will be given back untouched.

            Examples:

            >>> CommandLine._get_version('version', '__main__')
            'version'

            >>> CommandLine._get_version('', '__main__') # doctest: +ELLIPSIS
            'System ... stable'
        '''
        if version:
            return version
        return '{program} {version} {status}'.format(
            program=boostNode.extension.native.String(
                sys.modules[module_name].__module_name__
            ).camel_case_capitalize().content,
            version=sys.modules[module_name].__version__,
            status=sys.modules[module_name].__status__)

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _get_description(
##         cls: boostNode.extension.type.SelfClass, description: builtins.str,
##         module_name: builtins.str, version: builtins.str
##     ) -> builtins.str:
    def _get_description(cls, description, module_name, version):
##
        '''
            Generates a description string for given module.
            If description is not empty it will be given back untouched.

            Examples:

            >>> CommandLine._get_description(
            ...     'description', '__main__', 'version')
            'description'

            >>> CommandLine._get_description(
            ...     '', '__main__', 'version'
            ... ) # doctest: +ELLIPSIS
            'version - ...'
        '''
        if description is not None:
            if not description:
                description = '{version}'
                if sys.modules[module_name].__doc__ is not None:
                    description += ' - ' + sys.modules[module_name].__doc__
            return description.format(version=version)
        return ''

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _put_documentations_together(
##         cls: boostNode.extension.type.SelfClass,
##         documentation_path: builtins.str, frame: types.FrameType,
##         current_working_directory_save: builtins.str,
##         documentation_file_extension: builtins.str
##     ) -> boostNode.extension.type.SelfClass:
    def _put_documentations_together(
        cls, documentation_path, frame, current_working_directory_save,
        documentation_file_extension
    ):
##
        '''
            Moves all documentation files in subpackages to root
            package.
        '''
        meta_documentation = boostNode.extension.file.Handler(
            location=documentation_path, make_directory=True)
        '''
            In this way suppackages deletes their documentations
            too bevor they will be copied to root package
            directory.
        '''
        #if clear_old_documentation:
        #    meta_documentation.clear_directory()
        for package, initializer in cls._get_packages(
                current_working_directory_save, frame):
            package_documentation = boostNode.extension.file.Handler(
                location=package.path + documentation_path, must_exist=False)
            if package_documentation:
                for file in package_documentation:
                    if file.extension == documentation_file_extension:
                        '''
                            This two statements have to be in this
                            order to prevent overwriting files.
                        '''
                        file.name = package.basename + '.' + file.name
                        file.directory_path = meta_documentation.path
                package_documentation.remove_directory()
        return cls

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _document_modules(
##         cls: boostNode.extension.type.SelfClass,
##         documentation_path: builtins.str,
##         clear_old_documentation: builtins.bool,
##         module_names: collections.Iterable, documenter: builtins.str,
##         documenter_arguments: collections.Iterable,
##         documentation_file_extension: builtins.str
##     ) -> boostNode.extension.type.SelfClass:
    def _document_modules(
        cls, documentation_path, clear_old_documentation, module_names,
        documenter, documenter_arguments, documentation_file_extension
    ):
##
        '''
            Documents given modules with given documenter in given
            documentation location.
        '''
        documentation = boostNode.extension.file.Handler(
            location=documentation_path, make_directory=True)
        if clear_old_documentation:
            documentation.clear_directory()
        __logger__.info(
            'Document modules "{modules}" with '
            '"{documenter}".'.format(
                modules='", "'.join(module_names),
                documenter=documenter))
        boostNode.extension.native.Module.execute_program_for_modules(
            program_type='documenter', program=documenter,
            modules=module_names, arguments=documenter_arguments, error=False)
        for file in boostNode.extension.file.Handler():
            if file.extension == documentation_file_extension:
                file.directory_path = documentation.path
        return cls

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _lint_modules(
##         cls: boostNode.extension.type.SelfClass, linter: builtins.str,
##         module_names: collections.Iterable
##     ) -> boostNode.extension.type.SelfClass:
    def _lint_modules(cls, linter, module_names):
##
        '''
            Lints given modules with given linter.
        '''
        __logger__.info(
            'Lint modules "{modules}" with "{linter}".'.format(
                modules='", "'.join(module_names), linter=linter))
        result = boostNode.extension.native.Module\
            .execute_program_for_modules(
                program_type='linter', program=linter, modules=module_names,
                log=False, error=False)
        if result is False:
            __logger__.warning('Linter "%s" wasn\'t found.', linter)
        else:
            if result[0].strip():
                __logger__.warning(result[0].strip())
            if result[1].strip():
                __logger__.warning(result[1].strip())
        return cls

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _test_modules(
##         cls: boostNode.extension.type.SelfClass,
##         module_names: collections.Iterable,
##         temp_file_patterns: collections.Iterable
##     ) -> boostNode.extension.type.SelfClass:
    def _test_modules(cls, module_names, temp_file_patterns):
##
        '''
            Handle modules in given package.
        '''
        for module_name in module_names:
            __logger__.info('Test module "%s".', module_name)
            command_line_arguments_save = sys.argv
            main_module_reference_save = sys.modules['__main__']
            module = builtins.__import__(module_name)
            sys.modules['__main__'] = module
            cls.generic_module_interface(
                module={'scope': module, 'name': module_name}, test=True)
            sys.modules['__main__'] = main_module_reference_save
            sys.argv = command_line_arguments_save
            cls._clear_temp_files(temp_file_patterns)
        return cls

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _handle_packages_in_package(
##         cls: boostNode.extension.type.SelfClass,
##         current_working_directory_save: builtins.str,
##         frame: types.FrameType,
##         command_line_arguments: collections.Iterable,
##         exclude_packages: collections.Iterable
##     ) -> boostNode.extension.type.SelfClass:
    def _handle_packages_in_package(
        cls, current_working_directory_save, frame, command_line_arguments,
        exclude_packages
    ):
##
        '''
            Handle packages in current directory or package.
        '''
        new_command_line_arguments = sys.argv[1:]
        for record in command_line_arguments:
            for argument in record['arguments']:
                while argument in new_command_line_arguments:
                    del new_command_line_arguments[
                        new_command_line_arguments.index(argument)]
        for package, initializer in cls._get_packages(
                current_working_directory_save, frame):
            if not package.basename in builtins.map(
                lambda package: package.__name__, exclude_packages
            ):
                __logger__.info(
                    'Run "{package}" with initializer "{code_manager}" and'
                    ' arguments "{arguments}".'.format(
                        package=package.basename,
                        code_manager=initializer.path,
                        arguments='", "'.join(new_command_line_arguments)))
                Platform.run(
                    command=initializer.path, secure=True,
                    command_arguments=new_command_line_arguments)
        return cls

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _package_start_helper(
##         cls: boostNode.extension.type.SelfClass, name: builtins.str,
##         frame: types.FrameType, command_line_arguments: collections.Iterable
##     ) -> builtins.tuple:
    def _package_start_helper(cls, name, frame, command_line_arguments):
##
        '''
            This method does some starting routine for initializing an
            package interface.
        '''
        arguments = cls._package_argument_parser(
            name, frame, command_line_arguments)
        current_working_directory_save = os.getcwd()
        boostNode.extension.file.Handler(
            location=sys.argv[0]
        ).change_working_directory()
        return (
            'all' in arguments.commands, arguments,
            current_working_directory_save)

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _restore_current_directory(
##         cls: boostNode.extension.type.SelfClass, clear: builtins.bool,
##         temp_file_patterns: collections.Iterable,
##         current_directory=None
##     ) -> boostNode.extension.type.SelfClass:
    def _restore_current_directory(
        cls, clear, temp_file_patterns, current_directory=None
    ):
##
        '''
            Restores former directory state. This method deletes e.g.
            temporary binary file and test files.

            Examples:

            >>> test_folder = boostNode.extension.file.Handler(
            ...     'temp_test', make_directory=True)
            >>> boostNode.extension.file.Handler(
            ...     'temp_test/file', must_exist=False
            ... ).content = 'hans'
            >>> __test_buffer__.clear() # doctest: +ELLIPSIS
            '...'
            >>> CommandLine._restore_current_directory(
            ...     clear=True, temp_file_patterns=('temp_.*',)
            ... ) # doctest: +ELLIPSIS
            <class ...CommandLine...>
            >>> __test_buffer__.content # doctest: +ELLIPSIS
            '...Delete temporary files in "..." which matches "temp_.*".\\n'
            >>> test_folder.is_element()
            False
        '''
        if clear:
            cls._clear_temp_files(temp_file_patterns)
        if current_directory is not None:
            boostNode.extension.file.Handler(
                location=current_directory
            ).change_working_directory()
        return cls

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _clear_temp_files(
##         cls: boostNode.extension.type.SelfClass,
##         temp_file_patterns: collections.Iterable
##     ) -> boostNode.extension.type.SelfClass:
    def _clear_temp_files(cls, temp_file_patterns):
##
        '''
            Clears all temporary files in current directory.

            "temp_file_patterns" Defines wich file name machtes a temporary
                                 file.
        '''
        directory = boostNode.extension.file.Handler()
        __logger__.info(
            'Delete temporary files in "{path}" which matches '
            '"{pattern}".'.format(
                path=directory.path, pattern='", "'.join(temp_file_patterns)))
        directory.delete_file_patterns(*temp_file_patterns)
        return cls

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _get_packages(
##         cls: boostNode.extension.type.SelfClass,
##         current_working_directory_save: builtins.str,
##         frame: types.FrameType
##     ) -> builtins.list:
    def _get_packages(cls, current_working_directory_save, frame):
##
        '''
            Returns all sub packages found in the current package.

            Examples:

            >>> CommandLine._get_packages(
            ...     '/home/user/scripts', inspect.currentframe()
            ... ) # doctest: +SKIP
            [...]
        '''
        if(os.getcwd() == current_working_directory_save or
           boostNode.extension.file.Handler(
               location=frame.f_code.co_filename, must_exist=False
           ).is_referenced_via_absolute_path()):
            current_working_directory_save = ''
        else:
            current_working_directory_save += os.sep
        init_file = boostNode.extension.file.Handler(
            location=current_working_directory_save +
            frame.f_code.co_filename, respect_root_path=False)
        packages = []
        for file in boostNode.extension.file.Handler(
                location=init_file.directory_path):
            if boostNode.extension.native.Module.is_package(path=file.path):
                packages.append((file, boostNode.extension.file.Handler(
                    location=file.path + init_file.name, must_exist=False)))
        return packages

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _package_argument_parser(
##         cls: boostNode.extension.type.SelfClass, name: builtins.str,
##         frame: types.FrameType, command_line_arguments: collections.Iterable
##     ) -> argparse.Namespace:
    def _package_argument_parser(cls, name, frame, command_line_arguments):
##
        '''
            Returns a meta parser specialized for package interfaces.

            Examples:

            >>> CommandLine._package_argument_parser(
            ...     name=__name__, frame=inspect.currentframe()
            ... ) # doctest: +SKIP
            Namespace(...)
        '''
        boostNode.extension.output.Logger.change_all(level=('info',))
        package_name = boostNode.extension.native.Module.get_package_name(
            frame)
        choices = cls.PACKAGE_INTERFACE_ARGUMENTS[0]['keywords']['choices']
        return cls.argument_parser(
            version='{package} {version} {status}'.format(
                package=boostNode.extension.native.String(
                    package_name
                ).camel_case_capitalize().content,
                version=sys.modules[name].__version__,
                status=sys.modules[name].__status__),
            module_name=name,
            arguments=cls.PACKAGE_INTERFACE_ARGUMENTS + command_line_arguments,
            scope={'choices': choices})

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _render_command_line_argument(
##         cls: boostNode.extension.type.SelfClass, argument: builtins.object,
##         scope={}
##     ) -> builtins.object:
    def _render_command_line_argument(
        cls, argument, scope={}
    ):
##
        '''
            If a given argument property is marked as executable respectively
            dynamic it's value will be determined.

            Examples:

            >>> CommandLine._render_command_line_argument(
            ...     argument={'execute': 'value'}, scope={'value': 'hans'})
            'hans'

            >>> CommandLine._render_command_line_argument(argument='peter')
            'peter'
        '''
        if(builtins.isinstance(argument, builtins.dict) and
           'execute' in argument):
            return builtins.eval(argument['execute'], scope)
        return argument

        # endregion

    # endregion

# endregion

# region footer

'''Resolve cyclic dependency issues.'''
boostNode.extension.dependent.Resolve(
    name=__name__, frame=inspect.currentframe(), default_caller=False,
    dependencies=('boostNode.extension.native.__loaded__',))

# endregion
