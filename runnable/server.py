#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# region vim modline

# vim: set tabstop=4 shiftwidth=4 expandtab:
# vim: foldmethod=marker foldmarker=region,endregion:

# endregion

# region header

'''
    Provides a number of servers.
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

import base64
## python3.3
## import builtins
import __builtin__ as builtins
import BaseHTTPServer
import CGIHTTPServer
##
import cgi
## python3.3
## import collections
## import copy
## import http.server
## import imp
import copy
##
import gzip
import inspect
## python3.3 import io
pass
import logging
import multiprocessing
import os
import posixpath
## python3.3 import socketserver
pass
import ssl
import re
import signal
import socket
import subprocess
import sys
## python3.3
## import io
import SocketServer
import StringIO
##
import threading
import time
## python3.3
## import types
## import urllib.parse
import urllib
import urlparse
##

'''Make boostNode packages and modules importable via relative paths.'''
for number in (3, 4):
    sys.path.append(os.path.abspath(sys.path[0] + number * ('..' + os.sep)))

import boostNode.extension.dependent
import boostNode.extension.file
import boostNode.extension.native
import boostNode.extension.type
import boostNode.paradigm.aspectOrientation
import boostNode.paradigm.objectOrientation
import boostNode.extension.output
import boostNode.extension.system

# endregion


# region classes

## python3.3
## pass
class SocketFileObjectWrapper(socket._fileobject):
    '''
        This class wraps the native implementation of the server
        socket. The main goal is that the first line from given
        socket have to be taken twice. This curious feature is the
        only way to get the requested file as early as needed to decide
        if we are able to spawn a new process for better load
        balancing.
    '''

    # region dynamic properties

        # region public

    '''Indicates and saves the first line read of the socket.'''
    first_read_line = False

        # endregion

    # endregion

    # region dynamic methods

        # region public

            # region special

    @boostNode.paradigm.aspectOrientation.JointPoint
    def __init__(self, *arguments, **keywords):
        '''
            This methods wraps the initializer to make the first read line
            variable instance bounded.
        '''
        self.first_read_line = False
        '''Take this method via introspection.'''
        return builtins.getattr(
            builtins.super(self.__class__, self), inspect.stack()[0][3]
        )(*arguments, **keywords)

            # endregion

    @boostNode.paradigm.aspectOrientation.JointPoint
    def readline(self, *arguments, **keywords):
        '''Wraps the "readline()" method to get the first line twice.'''
        if self.first_read_line is False:
            try:
                '''Take this method via introspection.'''
                self.first_read_line = builtins.getattr(
                    builtins.super(self.__class__, self),
                    inspect.stack()[0][3]
                )(*arguments, **keywords)
                return self.first_read_line
            except (
                socket.herror, socket.gaierror, socket.timeout, socket.error
            ) as exception:
                __logger__.info(
                    'Connection interrupted. %s: %s',
                    exception.__class__.__name__, builtins.str(exception))
                return ''
        elif self.first_read_line is True:
            try:
                '''Take this method via introspection.'''
                return builtins.getattr(
                    builtins.super(self.__class__, self),
                    inspect.stack()[0][3]
                )(*arguments, **keywords)
            except (
                socket.herror, socket.gaierror, socket.timeout, socket.error
            ) as exception:
                __logger__.info(
                    'Connection interrupted. %s: %s',
                    exception.__class__.__name__, builtins.str(exception))
                return ''
        result = self.first_read_line
        self.first_read_line = True
        return result

        # endregion

    # endregion

##


## python3.3
## class MultiProcessingHTTPServer(
##     socketserver.ThreadingMixIn, http.server.HTTPServer
## ):
class MultiProcessingHTTPServer(
    SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer, builtins.object
):
##
    '''The Class implements a partial multiprocessing supported web server.'''

    # region dynamic properties

        # region public

    '''
        This attribute saves the modified read file socket to apply it in the
        request handler.
    '''
    read_file_socket = None

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
            This initializer wrapper makes sure that the special wrapped file
            socket is instance bounded.
        '''
        self.read_file_socket = self.__class__.read_file_socket
        '''Take this method via introspection.'''
        return builtins.getattr(
            builtins.super(self.__class__, self), inspect.stack()[0][3]
        )(*arguments, **keywords)

            # endregion

        # endregion

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def is_same_thread_request(
##         self: boostNode.extension.type.Self, request: socket.socket
##     ) -> builtins.bool:
    def is_same_thread_request(self, request):
##
        '''
            Determines if the given request could be run in its own dedicated
            process.
        '''
        first_request_line = self.read_file_socket.readline(
            Web.MAXIMUM_FIRST_GET_REQUEST_LINE_IN_CHARS
        ).strip()
        for pattern in self.web.same_thread_request_whitelist:
            if re.compile(pattern).match(first_request_line):
                return True
        return False

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def process_request_no_termination_wrapper(
##         self: boostNode.extension.type.Self,
##         parent_function: types.FunctionType, request: socket.socket,
##         arguments: builtins.tuple, keywords: builtins.dict
##     ) -> None:
    def process_request_no_termination_wrapper(
        self, parent_function, request, arguments, keywords
    ):
##
        '''
            Wraps the normal "process_request" method. To manage the process
            forking stuff.
        '''
        try:
            signal_numbers = boostNode.extension.system.Platform.\
                termination_signal_numbers
            for signal_number in signal_numbers:
                signal.signal(signal_number, signal.SIG_IGN)
            parent_function(self, request, *arguments, **keywords)
## python3.3
##         except (
##             builtins.BrokenPipeError, socket.gaierror,
##             socket.herror, socket.timeout, socket.error
##         ) as exception:
        except (
            socket.herror, socket.gaierror, socket.timeout, socket.error
        ) as exception:
##
            __logger__.info(
                'Connection interrupted. %s: %s', exception.__class__.__name__,
                builtins.str(exception))

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def process_request(
##         self: boostNode.extension.type.Self, request_socket: socket.socket,
##         *arguments: builtins.object, **keywords: builtins.object
##     ) -> None:
    def process_request(self, request_socket, *arguments, **keywords):
##
        '''
            This method indicates weather the request is a read only or not.
            Read only requests will be forked if enough free processors are
            available.
        '''
        if self.web.block_new_worker:
            return None
## python3.3
##         self.read_file_socket = request_socket.makefile('rb', -1)
##         read_file_socket = self.read_file_socket
##
##         @boostNode.paradigm.aspectOrientation.JointPoint
##         def readline(
##             *arguments: builtins.object, **keywords: builtins.object
##         ) -> builtins.bytes:
##             '''
##                 Wraps the native file object method version.
##             '''
##             self = read_file_socket
##             if not builtins.hasattr(self, 'first_read_line'):
##                 self.first_read_line = builtins.getattr(
##                     io.BufferedReader, inspect.stack()[0][3]
##                 )(self, *arguments, **keywords)
##                 return self.first_read_line
##             elif self.first_read_line is True:
##                 '''Take this method via introspection.'''
##                 return builtins.getattr(
##                     io.BufferedReader, inspect.stack()[0][3]
##                 )(self, *arguments, **keywords)
##             result = self.first_read_line
##             self.first_read_line = True
##             return result
##         self.read_file_socket.readline = readline
        '''
            This assignment replace the python's native
            "socket.socket.makefile('rb', -1)" behavior.
        '''
        self.read_file_socket = SocketFileObjectWrapper(
            request_socket, 'rb', -1)
##
        '''NOTE: We have to add 1 for the server processes itself.'''
        self.web.number_of_running_processes = \
            builtins.len(multiprocessing.active_children()) + 1
## python3.3
##         parent_function = builtins.getattr(
##             http.server.HTTPServer, inspect.stack()[0][3])
        parent_function = builtins.getattr(
            BaseHTTPServer.HTTPServer, inspect.stack()[0][3])
##
        if(not self.is_same_thread_request(request_socket) and
           self.web.number_of_running_processes <
           self.web.maximum_number_of_processes):
            self.web.number_of_running_processes += 1
            '''Takes this method via introspection from now on.'''
## python3.3
##             multiprocessing.Process(
##                 target=self.process_request_no_termination_wrapper,
##                 daemon=True,
##                 args=(parent_function, request_socket, arguments, keywords)
##             ).start()
            forked_request_process = multiprocessing.Process(
                target=self.process_request_no_termination_wrapper,
                args=(parent_function, request_socket, arguments, keywords))
            forked_request_process.daemon = True
            forked_request_process.start()
##
        else:
            try:
## python3.3
##                 return parent_function(
##                     self, request_socket, *arguments, **keywords)
##             except (
##                 builtins.BrokenPipeError, socket.gaierror, socket.herror,
##                 socket.timeout, socket.error
##             ) as exception:
                return parent_function(
                    self, request_socket, *arguments, **keywords)
            except (
                socket.herror, socket.gaierror, socket.timeout, socket.error
            ) as exception:
##
                __logger__.info(
                    'Connection interrupted. %s: %s',
                    exception.__class__.__name__, builtins.str(exception))

    # endregion


class Web(
    boostNode.paradigm.objectOrientation.Class,
    boostNode.extension.system.Runnable
):
    '''
        Provides a small platform independent web server designed for easily
        serve a client-server structure.
    '''

    # region constant properties

        # region public

    '''
        Holds all command line interface argument informations.
    '''
    COMMAND_LINE_ARGUMENTS = (
        {'arguments': ('-r', '--root'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Defines which path is used as web root.',
             'dest': 'root',
             'metavar': 'PATH'}},
        {'arguments': ('-p', '--port'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'choices': builtins.range(2 ** 16),
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Defines the port number to access the web server.',
             'dest': 'port',
             'metavar': 'NUMBER'}},
        {'arguments': ('-d', '--default'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Defines which file or module should be requested if '
                     'nothing was declared explicitly. It could be understood'
                     ' as welcome page.',
             'dest': 'default',
             'metavar': 'PATH'}},
        {'arguments': ('-u', '--public-key-file-path'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Defines a public key file (*.pem) to enable open ssl '
                     'encryption.',
             'dest': 'public_key_file_path',
             'metavar': 'PATH'}},
        {'arguments': ('-o', '--stop-order'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': {'execute': '"""Saves a cli-command for shutting down '
                                 'the server (default: "%s").""" % '
                                 '__initializer_default_value__'},
             'dest': 'stop_order',
             'metavar': 'STRING'}},
        {'arguments': ('-w', '--request-whitelist'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Select request type regular expression patterns which '
                     'are only allowed for being interpreted.',
             'dest': 'request_whitelist',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-b', '--request-blacklist'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Select request type regular expression patterns which '
                     "aren't allowed for being interpreted.",
             'dest': 'request_blacklist',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-s', '--static-mime-type-pattern'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'All mime-type patterns which should recognize a static '
                     'file. Those files will be directly sent to client '
                     'without any preprocessing.',
             'dest': 'static_mime_type_pattern',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-y', '--dynamic-mime-type-pattern'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'All mime-type patterns which should recognize a dynamic '
                     'file. Those files will be interpreted so the result can '
                     'be send back to client.',
             'dest': 'dynamic_mime_type_pattern',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-C', '--compressible-mime-type-pattern'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'All mime-type patterns which should compressed before '
                     'sending through network socket.',
             'dest': 'compressible_mime_type_pattern',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-f', '--default-file-name-pattern'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'All file name patterns which should be run if there is '
                     'one present and no other default file pattern/name is '
                     'given on initialisation.',
             'dest': 'default_file_name_pattern',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-n', '--default-module-name-pattern'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Same as file name for module name patterns. '
                     'Note that default files have a lower priority as '
                     'default python modules.',
             'dest': 'default_module_names',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-q', '--file-size-stream-threshold-in-byte'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Defines the minimum number of bytes which triggers the '
                     'server to send an octet-stream header to client.',
             'dest': 'file_size_stream_threshold_in_byte',
             'metavar': 'NUMBER'}},
        {'arguments': ('-a', '--authentication'),
         'keywords': {
             'action': 'store_true',
             'default': {'execute': '__initializer_default_value__'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Enables basic http authentication. You can control '
                     'this behavior by providing an authentication file in '
                     'directorys you want to save.',
             'dest': 'authentication'}},
        {'arguments': ('-e', '--enable-module-loading'),
         'keywords': {
             'action': 'store_true',
             'default': False,
             'required': False,
             'help': 'Enables module loading via get query. '
                     'Enabling this feature can slow down your request '
                     'performance extremely. Note that self module loading '
                     'via "__main__" is independently possible.',
             'dest': 'module_loading'}},
        {'arguments': ('-z', '--disable-directory-listing'),
         'keywords': {
             'action': 'store_false',
             'default': True,
             'required': False,
             'help': 'Disables automatic directory listing if a directory is '
                     'requested.',
             'dest': 'directory_listing'}},
        {'arguments': ('-g', '--authentication-file-content-pattern'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Defines the regular expression pattern to define how to '
                     'parse authentication files.',
             'dest': 'authentication_file_content_pattern',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-i', '--authentication-file-name-pattern'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Defines the authentication file name.',
             'dest': 'authentication_file_name',
             'metavar': 'STRING'}},
        {'arguments': ('-j', '--request-parameter-delimiter'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Defines the request delimiter parameter.',
             'dest': 'request_parameter_delimiter',
             'metavar': 'STRING'}},
        {'arguments': ('-k', '--maximum-number-of-processes'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Defines the maximum number of concurrent running '
                     'processes.',
             'dest': 'maximum_number_of_processes',
             'metavar': 'NUMBER'}})
    '''
        Globally accessable socket to ask for currently useful ip determining.
    '''
    DETERMINE_IP_SOCKET = '8.8.8.8', 80
    '''
        This is the maximum number of forked processes if nothing better was
        defined or determined.
    '''
    DEFAULT_NUMBER_OF_PROCESSES = 8
    '''This values describes the longest possible first get request line.'''
    MAXIMUM_FIRST_GET_REQUEST_LINE_IN_CHARS = 65537

        # endregion

    # endregion

    # region dynamic properties

        # region public

    '''Saves server runtime properties.'''
    root = port = thread_buffer = service = None
    '''Saves the host name.'''
    host_name = ''
    '''Saves a default file if no explicit file was requested.'''
    default = ''
    '''Saves a cli-command for shutting down the server.'''
    stop_order = ''
    '''
        Saves informations how to define authentications in protected
        directories.
    '''
    authentication = False
    authentication_file_name = ''
    authentication_file_content_pattern = ''
    authentication_handler = None
    '''
        A list of regular expression pattern which every request have to match.
    '''
    request_whitelist = ()
    '''A list of regular expression pattern which no request should match.'''
    request_blacklist = ()
    '''
        A list of regular expression pattern which indicates requests which
        should guaranteed to be run in the same thread as the server itself.
        This requests usually modifies shared memory.
    '''
    same_thread_request_whitelist = ()
    '''Saves all initializes server instances.'''
    instances = []
    '''
        Saves all mime-type pattern to interpret as files which shouldn't be
        ran.
    '''
    static_mime_type_pattern = ()
    '''
        Saves all mime-type pattern to interpret as files which should be
        ran. There standard output will be given back to request.
    '''
    dynamic_mime_type_pattern = ()
    '''
        Saves all mime-type pattern which should be compressed before sending
        via network.
    '''
    compressible_mime_type_pattern = ()
    '''
        Saves all file name pattern to be taken as fall-back if no explicit
        file or module was requested.
    '''
    default_file_name_pattern = ()
    '''
        Saves all module names to be taken as fall-back if no explicit
        file or module was requested.
    '''
    default_module_names = ()
    '''Indicates if module loading via get query is enabled.'''
    module_loading = None
    '''Saves the number of running threads.'''
    number_of_running_threads = 0
    '''Saves the number of running process forked by this server instance.'''
    number_of_running_processes = 0
    '''
        Number of maximum forked processes. This should be less or equal to
        the number of processors installed in your pc.
        We will try to determine the number of processors. If this fails
        "DEFAULT_NUMBER_OF_PROCESSES" will be applied.
    '''
    maximum_number_of_processes = 0
    '''Indicates if new worker are currently allowed to spawn.'''
    block_new_worker = False
    '''
        This attribute saves a shared data object. It will be given to all
        sub workers which computes request results.
    '''
    shared_data = None
    '''
        This property saves the current request parameter delimiter. It will be
        used to determine where the requested file name ends if get parameter
        are given.
    '''
    request_parameter_delimiter = ''
    '''
        Defines the minimum file size till the server sends an octet-stream
        header.
    '''
    file_size_stream_threshold_in_byte = 0
    '''Indicates if directory listing is allowed.'''
    directory_listing = False

        # endregion

        # region protected

    '''
        Holds a file object referencing a "<DOMAIN_NAME>.pem" file needed for
        open ssl connections.
    '''
    _public_key_file = None

        # endregion

    # endregion

    # region dynamic methods

        # region public

            # region special

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def __repr__(self: boostNode.extension.type.Self) -> builtins.str:
    def __repr__(self):
##
        '''
            Invokes if this object should describe itself by a string.

            Examples:

            >>> repr(Web()) # doctest: +ELLIPSIS
            'Object of "Web" with root path "...", port "0" and sto..."sto...'
        '''
        return ('Object of "{class_name}" with root path "{path}", port '
                '"{port}" and stop order "{stop_order}". Number of running '
                'threads/processes: {number_of_running_threads}/'
                '{number_of_running_processes}.'.format(
                    class_name=self.__class__.__name__, path=self.root,
                    port=self.port, stop_order=self.stop_order,
                    number_of_running_threads=self.number_of_running_threads,
                    number_of_running_processes=
                    self.number_of_running_processes))

            # endregion

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def stop(
##         self: boostNode.extension.type.Self, *arguments: builtins.object,
##         **keywords: builtins.object
##     ) -> boostNode.extension.type.Self:
    def stop(self, *arguments, **keywords):
##
        '''Waits for running workers and shuts the server down.'''
        if self.service:
            self.block_new_worker = True
            number_of_running_workers = self.number_of_running_threads + \
                builtins.len(multiprocessing.active_children())
            shown_number = 0
            while number_of_running_workers > 0:
                if(number_of_running_workers !=
                   self.number_of_running_threads +
                   builtins.len(multiprocessing.active_children())):
                    number_of_running_workers = \
                        self.number_of_running_threads + \
                        builtins.len(multiprocessing.active_children())
                if(shown_number != number_of_running_workers and
                   number_of_running_workers > 0):
                    __logger__.info(
                        'Waiting for %d running workers (%d threads and '
                        '%d processes).', number_of_running_workers,
                        self.number_of_running_threads,
                        builtins.len(multiprocessing.active_children()))
                    shown_number = number_of_running_workers
                time.sleep(2)
            __logger__.info('Shutting down web server.')
            self.__class__.instances.remove(self)
            try:
                self.service.socket.shutdown(socket.SHUT_RDWR)
            except socket.error:
                pass
            self.service.socket.close()
        '''Take this method type by the abstract class via introspection.'''
        return builtins.getattr(
            builtins.super(self.__class__, self), inspect.stack()[0][3]
        )(*arguments, **keywords)

        # endregion

        # region protected

            # region runnable implementation

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _run(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def _run(self):
##
        '''
            Entry point for command line call of this program.
            Starts the server's request handler listing for incoming requests.

            Examples:

            >>> Web(root='.') # doctest: +ELLIPSIS
            Object of "Web" with root path "...", port "0" and stop order ...
        '''
        command_line_arguments = boostNode.extension.system.CommandLine\
            .argument_parser(
                arguments=self.COMMAND_LINE_ARGUMENTS,
                module_name=__name__, scope={'self': self})
        return self._initialize(**self._command_line_arguments_to_dictionary(
            namespace=command_line_arguments))

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _initialize(
##         self: boostNode.extension.type.Self, root='.', host_name='', port=0,
##         default='', public_key_file_path='', stop_order='stop',
##         request_whitelist=('/.*',), request_blacklist=(),
##         same_thread_request_whitelist=(),
##         # NOTE: Tuple for explicit web_server file reference validation.
##         # ('^text/.+', '^image/.+', '^application/(x-)?javascript$')
##         static_mime_type_pattern=('^.+/.+$',),
##         dynamic_mime_type_pattern=(
##             '^text/x-(python|sh|bash|shellscript)$',),
##         compressible_mime_type_pattern=(
##             '^text/.+$', '^application/javascript$'),
##         default_file_name_pattern=(
##             '^((__main__)|(main)|(index)|(initialize))\.?(?!tpl$)'
##             '[a-zA-Z0-9]{0,4}$',),
##         default_module_names=('__main__', 'main', 'index', 'initialize'),
##         authentication=True, authentication_file_name='.htpasswd',
##         authentication_file_content_pattern='(?P<name>.+):(?P<password>.+)',
##         authentication_handler=None, module_loading=None,
##         maximum_number_of_processes=0, shared_data=None,
##         request_parameter_delimiter='\?',
##         file_size_stream_threshold_in_byte=1048576,  # 1 MB
##         directory_listing=True, **keywords: builtins.object
##     ) -> boostNode.extension.type.Self:
    def _initialize(
        self, root='.', host_name='', port=0, default='',
        public_key_file_path='', stop_order='stop',
        request_whitelist=('/.*',), request_blacklist=(),
        same_thread_request_whitelist=(),
        # NOTE: Tuple for explicit web_server file reference validation.
        # ('^text/.+', '^image/.+', '^application/(x-)?javascript$')
        static_mime_type_pattern=('^.+/.+$',),
        dynamic_mime_type_pattern=(
            '^text/x-(python|sh|bash|shellscript)$',),
        compressible_mime_type_pattern=(
            '^text/.+$', '^application/javascript$'),
        default_file_name_pattern=(
            '^((__main__)|(main)|(index)|(initialize))\.?(?!tpl$)'
            '[a-zA-Z0-9]{0,4}$',),
        default_module_names=('__main__', 'main', 'index', 'initialize'),
        authentication=True, authentication_file_name='.htpasswd',
        authentication_file_content_pattern='(?P<name>.+):(?P<password>.+)',
        authentication_handler=None, module_loading=None,
        maximum_number_of_processes=0, shared_data=None,
        request_parameter_delimiter='\?',
        file_size_stream_threshold_in_byte=1048576,  # 1 MB
        directory_listing=True, **keywords
    ):
##
        '''
            Sets root path of web server and all properties. Although the
            server thread will be started.
        '''
        self.__class__.instances.append(self)

        if public_key_file_path:
            public_key_file = boostNode.extension.file.Handler(
                location=public_key_file_path)
            if public_key_file.is_file():
                self._public_key_file = public_key_file

        self.authentication_handler = authentication_handler
        self.authentication = authentication
        self.authentication_file_name = authentication_file_name
        self.authentication_file_content_pattern = \
            authentication_file_content_pattern
        self.stop_order = stop_order
        self.root = boostNode.extension.file.Handler(location=root)
        self.host_name = host_name
        self.port = port
        self.default = default
        self.request_whitelist = request_whitelist
        self.request_blacklist = request_blacklist
        self.same_thread_request_whitelist = same_thread_request_whitelist
        self.static_mime_type_pattern = static_mime_type_pattern
        self.dynamic_mime_type_pattern = dynamic_mime_type_pattern
        self.compressible_mime_type_pattern = compressible_mime_type_pattern
        self.default_file_name_pattern = default_file_name_pattern
        self.default_module_names = default_module_names
        self.thread_buffer = boostNode.extension.output.Buffer(
            queue=True)
        self.module_loading = module_loading
        self.maximum_number_of_processes = maximum_number_of_processes
        self.request_parameter_delimiter = request_parameter_delimiter
        self.file_size_stream_threshold_in_byte = \
            file_size_stream_threshold_in_byte
        self.directory_listing = directory_listing
        if boostNode.extension.system.Platform.operating_system == 'windows':
            self.maximum_number_of_processes = 1
        elif not self.maximum_number_of_processes:
            try:
                self.maximum_number_of_processes = \
                    2 * multiprocessing.cpu_count()
            except builtins.NotImplementedError:
                self.maximum_number_of_processes = \
                    self.DEFAULT_NUMBER_OF_PROCESSES
        self.shared_data = shared_data
        '''NOTE: Make this properties instance bounded.'''
        self.number_of_running_threads = \
            self.__class__.number_of_running_threads
        self.number_of_running_processes = \
            self.__class__.number_of_running_processes
        return self._start_server_thread()

            # endregion

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _start_server_thread(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def _start_server_thread(self):
##
        '''
            Starts the server's request handler instance and listens for
            shutting-down-command.
        '''
        if not __test_mode__:
            if self.port:
                self._start_with_static_port()
            else:
                self._start_with_dynamic_port()
        self._log_server_status()
        if not __test_mode__ and self.stop_order:
            self.wait_for_order()
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _log_server_status(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def _log_server_status(self):
##
        '''Prints some information about the way the server was started.'''
        determineIPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            determineIPSocket.connect(self.DETERMINE_IP_SOCKET)
## python3.3
##         except (
##             builtins.BrokenPipeError, socket.gaierror, socket.herror,
##             socket.timeout, socket.error
##         ) as exception:
        except (
            socket.herror, socket.gaierror, socket.timeout, socket.error
        ):
##
            ip = socket.gethostbyname(socket.gethostname())
        else:
            ip = determineIPSocket.getsockname()[0]
        finally:
            try:
                determineIPSocket.shutdown(socket.SHUT_RDWR)
            except socket.error:
                pass
            determineIPSocket.close()
        __logger__.info(
            'Web server is starting %sand listens at port "%d" and webroot '
            '"%s". Currently reachable ip is "%s". Maximum parallel process '
            'is limited to %d.', (
                'a secure connection with public key "%s" ' %
                self._public_key_file._path
            ) if self._public_key_file else '',
            self.port, self.root._path, ip, self.maximum_number_of_processes)
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _start_with_dynamic_port(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def _start_with_dynamic_port(self):
##
        '''Searches for the highest free port for listing.'''
        ports = [
            80, 8080, 8008, 8090, 8280, 8887, 9080, 16080, 3128, 4567,
            5000, 4711, 443, 5001, 5104, 5800, 8243, 8888]
        if self._public_key_file:
            ports = [443] + ports
        ports += builtins.list(builtins.set(
            builtins.range(2 ** 16 - 1)
        ).difference(ports))
        for port in ports:
            try:
                self._initialize_server_thread(port)
            except socket.error:
                if not port:
## python3.3
##                     raise __exception__(
##                         'No port is available to run the web-server with '
##                         'given rights.'
##                     ) from None
                    raise __exception__(
                        'No port is available to run the web-server with '
                        'given rights.')
##
            else:
                self.port = port
                return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _start_with_static_port(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def _start_with_static_port(self):
##
        '''Starts the server listing on the given port, if it is free.'''
        try:
            self._initialize_server_thread(port=self.port)
        except socket.error:
## python3.3
##             raise __exception__(
##                 "Port %d isn't available to run the web-server with given "
##                 'rights.', self.port
##             ) from None
            raise __exception__(
                "Port %d isn't available to run the web-server with given "
                'rights.', self.port)
##
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _serve_service_forever_exception_catcher(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def _serve_service_forever_exception_catcher(self):
##
        '''
            This method wraps the python's native server "serve_forever()"
            method to handle incoming exceptions in a separat thread.
        '''
        try:
            return self.service.serve_forever()
## python3.3         except builtins.ValueError as exception:
        except socket.error as exception:
            __logger__.info(
                '%s: %s', exception.__class__.__name__,
                builtins.str(exception))
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _initialize_server_thread(
##         self: boostNode.extension.type.Self, port: builtins.int
##     ) -> boostNode.extension.type.Self:
    def _initialize_server_thread(self, port):
##
        '''Initializes a new request-handler and starts its own thread.'''
        if self._public_key_file:
            self.service = MultiProcessingHTTPServer(
                (self.host_name, port), CGIHTTPRequestHandler)
            self.service.socket = ssl.wrap_socket(
                self.service.socket, certfile=self._public_key_file._path,
                server_side=True)
        else:
            self.service = MultiProcessingHTTPServer(
                (self.host_name, port), CGIHTTPRequestHandler)
        self.service.web = self
## python3.3
##         threading.Thread(
##             target=self._serve_service_forever_exception_catcher,
##             daemon=True
##         ).start()
        server_thread = threading.Thread(
            target=self._serve_service_forever_exception_catcher)
        server_thread.daemon = True
        server_thread.start()
##
        return self

        # endregion

    # endregion


## python3.3
## class CGIHTTPRequestHandler(http.server.CGIHTTPRequestHandler):
class CGIHTTPRequestHandler(
    CGIHTTPServer.CGIHTTPRequestHandler, builtins.object
):
##
    '''
        A small request-handler dealing with incoming file requests.
        It can directly send static files back to client or run dynamic
        scripts and give the output back to client.
    '''

    # region dynamic properties

        # region public

    '''Properties defined by incoming request.'''
    request_uri = ''
    parameter = ''
    post_dictionary = {}
    '''Saves the last started worker thread instance.'''
    last_running_worker = None
    '''
        Consists the explicit requested file name (like python's native
        "self.file") coming from client.
    '''
    requested_file_name = ''
    '''References the corresponding file handler to requested file name.'''
    requested_file = None
    '''
        Defines weather the handler has decided to run a python module or an
        external script.
    '''
    load_module = False
    '''
        Defines arguments given to a requested file which is running by the
        server.
    '''
    request_arguments = []
    '''Indicates if an answer is expected from the requested file.'''
    respond = False
    '''Indicates if the specified response was sent yet.'''
    response_sent = headers_ended = content_type_sent = content_length_sent = \
        False
    '''
        Saves the self describing server version string. This string is
        included in every response.
    '''
    server_version = '{program} {version} {status}'
    '''Saves gziped encoded output.'''
    _encoded_output = None

        # endregion

        # region protected

    '''
        Points to location which is authoritative to be reachable from
        requested destination.
    '''
    _authentication_location = None

        # endregion

    # endregion

    # region dynamic methods

        # region public

            # region special

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def __init__(
##         self, *arguments: builtins.object, **keywords: builtins.object
##     ) -> None:
##         '''
##             This method calls is parent. It's necessary to make some class
##             properties instance properties.
##         '''
    def __init__(self, *arguments, **keywords):
##
        '''Initializes a http request response.'''
        self.request_uri = ''
        self.parameter = ''
        self.post_dictionary = {}
        self.requested_file_name = ''
        self.requested_file = None
        self.load_module = False
        self.request_arguments = []
        self.respond = False
        self.server_version = self.server_version.format(
            program=boostNode.extension.native.String(
                __module_name__
            ).camel_case_capitalize().content,
            version=__version__,
            status=__status__)
        '''Take this method via introspection.'''
        return builtins.getattr(
            builtins.super(self.__class__, self), inspect.stack()[0][3]
        )(*arguments, **keywords)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def __repr__(self: boostNode.extension.type.Self) -> builtins.str:
    def __repr__(self):
##
        '''
            Invokes if this object should describe itself by a string.

            Examples:

            >>> repr(CGIHTTPRequestHandler()) # doctest: +SKIP
            'Object of "CGIHTTPRequestHandler" with request uri "" and para...'
        '''
        return 'Object of "{class_name}" with request uri "{url}" and '\
               'parameter "{parameter}".'.format(
                   class_name=self.__class__.__name__, url=self.request_uri,
                   parameter=self.parameter)

            # endregion

        # endregion

    # endregion

    # region static methods

        # region public

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def parse_url(
##         self: boostNode.extension.type.Self, url=None
##     ) -> builtins.tuple:
    def parse_url(self, url=None):
##
        '''
            This static method provides an easy way to split a http
            request-string into its components.
        '''
        if url is None and builtins.len(sys.argv) > 1:
            url = sys.argv[1]
        if url:
            url = re.compile(
                self.server.web.request_parameter_delimiter
            ).sub('?', url, 1)
## python3.3             get = urllib.parse.urlparse(url).query
            get = urlparse.urlparse(url).query
            if get:
                try:
## python3.3
##                     get = urllib.parse.parse_qs(
##                         qs=get, keep_blank_values=True, strict_parsing=True,
##                         encoding='utf_8', errors='replace')
                    get = urlparse.parse_qs(
                        qs=get, keep_blank_values=True,
                        strict_parsing=True)
##
                except builtins.ValueError:
                    get = {}
                    __logger__.info('Query "%s" string is not valid.', url)
            if not get:
                get = {}
            for key, value in get.items():
                get[key] = value[0]
## python3.3             return urllib.parse.urlparse(url), get
            return urlparse.urlparse(url), get
        return None, {}

        # endregion

    # endregion

    # region dynamic  methods

        # region public

            # region event

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def do_GET(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def do_GET(self):
##
        '''
            Is triggered if an incoming get-request is detected.
            Decides if request is valid and static or dynamic.
            It also through an exception and sends an http-error
            if request isn't valid.
        '''
        self._create_environment_variables()
        if self._is_authenticated():
            valid_request = self._is_valid_request()
            if valid_request:
                if self.path:
                    if self._is_valid_reference():
                        return self._set_dynamic_or_static_get(
                            file_name=self.path)
                elif self._default_get():
                    return self
            return self._send_no_file_error(valid_request)
        return self._send_no_authentication_error()

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def do_POST(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def do_POST(self):
##
        '''Is triggered if a post-request is coming.'''
## python3.3
##         data_type, post_data = cgi.parse_header(
##             self.headers.get_content_type())
        data_type, post_data = cgi.parse_header(self.headers.getheader(
            'content-type'))
##
        if data_type == 'multipart/form-data':
            self.post_dictionary = self._determine_post_dictionary()
        elif data_type == 'application/x-www-form-urlencoded':
## python3.3
##             self.post_dictionary = urllib.parse.parse_qs(self.rfile.read(
##                 builtins.int(self.headers.get('content-length'))
##             ).decode('utf_8'))
            self.post_dictionary = cgi.parse_qs(
                self.rfile.read(builtins.int(self.headers.getheader(
                    'content-length'))),
                keep_blank_values=True)
##
            for name, value in self.post_dictionary.items():
                if boostNode.extension.native.Object(object=value).is_binary():
                    self.post_dictionary[name] = {'content': value}
        return self.do_GET()

            # endregion

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def send_response(
##         self: boostNode.extension.type.Self, *arguments: builtins.object,
##         **keywords: builtins.object
##     ) -> boostNode.extension.type.Self:
    def send_response(self, *arguments, **keywords):
##
        '''
            Send the given response code to client if no response code was sent
            yet.
        '''
        if not self.response_sent:
            self.response_sent = True
            '''Take this method via introspection.'''
            builtins.getattr(
                builtins.super(self.__class__, self), inspect.stack()[0][3]
            )(*arguments, **keywords)
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def list_directory(
##         self: boostNode.extension.type.Self, *arguments: builtins.object,
##         **keywords: builtins.object
##     ) -> boostNode.extension.type.Self:
    def list_directory(self, *arguments, **keywords):
##
        '''
            Generates a simple html web page listing requested directory
            content.
        '''
        path_backup = self.path
        self.path = self.requested_file.path[builtins.len(
            self.server.web.root.path
        ) - builtins.len(os.sep):]
        '''Take this method via introspection.'''
        file_handler = builtins.getattr(
            builtins.super(self.__class__, self), inspect.stack()[0][3]
        )(self.requested_file._path, *arguments, **keywords)
        self._send_output(output=file_handler)
        self.path = path_backup
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def end_headers(
##         self: boostNode.extension.type.Self, *arguments: builtins.object,
##         **keywords: builtins.object
##     ) -> boostNode.extension.type.Self:
    def end_headers(self, *arguments, **keywords):
##
        '''Finishes all sent headers by a trailing new empty line.'''
        if not self.headers_ended:
            self.headers_ended = True
            '''Take this method via introspection.'''
            builtins.getattr(
                builtins.super(self.__class__, self), inspect.stack()[0][3]
            )(*arguments, **keywords)
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def send_static_file_cache_header(
##         self: boostNode.extension.type.Self, timestamp: builtins.float
##     ) -> boostNode.extension.type.Self:
    def send_static_file_cache_header(self, timestamp):
##
        '''Response a static file-request header.'''
        self.send_header('Cache-Control', 'public, max-age=99999999')
        self.send_header('Last-Modified', self.date_time_string(timestamp))
        self.send_header('Expires', self.date_time_string(
            timestamp + 99999999))
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def send_content_type_header(
##         self: boostNode.extension.type.Self, *arguments: builtins.object,
##         mime_type='text/html', encoding='UTF-8', response_code=200,
##         **keywords: builtins.object
##     ) -> boostNode.extension.type.Self:
    def send_content_type_header(self, *arguments, **keywords):
##
        '''Sends a content type header to client if not sent yet.'''
## python3.3
##         pass
        default_keywords = boostNode.extension.native.Dictionary(
            content=keywords)
        mime_type, keywords = default_keywords.pop(
            name='mime_type', default_value='text/html')
        encoding, keywords = default_keywords.pop(
            name='encoding', default_value='UTF-8')
        response_code, keywords = default_keywords.pop(
            name='response_code', default_value=200)
##
        if not self.content_type_sent:
            self.send_response(response_code).content_type_sent = True
            self.send_header(
                'Content-Type', '%s; charset=%s' % (mime_type, encoding),
                *arguments, **keywords)
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def send_content_length_header(
##         self: boostNode.extension.type.Self, size: builtins.int,
##         *arguments: builtins.object, dynamic_output='', encoding='UTF-8',
##         response_code=200, **keywords: builtins.object
##     ) -> boostNode.extension.type.Self:
    def send_content_length_header(self, size, *arguments, **keywords):
##
        '''Sends the content length header to client if not sent yet.'''
## python3.3
##         pass
        default_keywords = boostNode.extension.native.Dictionary(
            content=keywords)
        encoding, keywords = default_keywords.pop(
            name='encoding', default_value='UTF-8')
        response_code, keywords = default_keywords.pop(
            name='response_code', default_value=200)
        dynamic_output, keywords = default_keywords.pop(
            name='dynamic_output', default_value='')
##
        if not self.content_length_sent:
            self.send_response(response_code).content_length_sent = True
            threshold = self.server.web.file_size_stream_threshold_in_byte
## python3.3
##             if(size < threshold and
##                self.headers.get('Accept-Encoding') and
##                gzip.__name__ in self.headers.get('Accept-Encoding').split(
##                    ','
##                ) and (dynamic_output or self._check_pattern(
##                    patterns=self.server.web.compressible_mime_type_pattern,
##                    subject=self.requested_file.mime_type))):
            if(size < threshold and
               self.headers.getheader('Accept-Encoding') and
               gzip.__name__ in self.headers.getheader(
                   'Accept-Encoding'
               ).split(',') and
               (dynamic_output or self._check_pattern(
                   patterns=self.server.web.compressible_mime_type_pattern,
                   subject=self.requested_file.mime_type))):
##
                self.send_header('Content-Encoding', gzip.__name__)
                if dynamic_output:
                    self._encoded_output = self._gzip(content=dynamic_output)
                else:
                    self._encoded_output = self._gzip(
                        content=self.requested_file.content)
                self.send_header('Content-Length', builtins.len(
                    self._encoded_output))
            else:
                self.send_header(
                    'Content-Length', size, *arguments, **keywords)
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def log_message(
##         self: boostNode.extension.type.Self, format: builtins.str,
##         message_or_error_code: (builtins.int, builtins.str),
##         response_code_or_message: (builtins.str, builtins.int),
##         message_end=None
##     ) -> boostNode.extension.type.Self:
    def log_message(
        self, format, message_or_error_code, response_code_or_message,
        message_end=None
    ):
##
        '''
            Wrapper method for all logging output coming through the server
            thread.
        '''
        format = (
            '{client_ip}:{client_port} {request_description} -> '
            '{response_code}')
        forwarded_ip = forwarded_host = forwarded_server = None
        if builtins.hasattr(self, 'headers'):
## python3.3
##             forwarded_ip = self.headers.get('X-Forwarded-For')
##             forwarded_host = self.headers.get('X-Forwarded-Host')
##             forwarded_server = self.headers.get('X-Forwarded-Server')
            forwarded_ip = self.headers.getheader('X-Forwarded-For')
            forwarded_host = self.headers.getheader('X-Forwarded-Host')
            forwarded_server = self.headers.getheader('X-Forwarded-Server')
##
            if forwarded_ip:
                format += ' - forwarded for: {forwarded_ip}'
            if forwarded_host:
                format += ' - forwarded host: {forwarded_host}'
            if forwarded_server:
                format += ' - forwarded server: {forwarded_server}'
        if builtins.len(self.server.web.instances) > 1:
            format += ' (server port: {server_port})'
        request_description = message_or_error_code
        response_code = response_code_or_message
        if builtins.isinstance(message_or_error_code, builtins.int):
            request_description = response_code_or_message
            response_code = message_or_error_code
        __logger__.info(format.format(
            client_ip=self.client_address[0],
            client_port=self.client_address[1],
            request_description=request_description,
            response_code=response_code, forwarded_ip=forwarded_ip,
            forwarded_host=forwarded_host, forwarded_server=forwarded_server,
            server_port=self.server.web.port))
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def setup(
##         self: boostNode.extension.type.Self, *arguments: builtins.object,
##         **keywords: builtins.object
##     ) -> None:
    def setup(self, *arguments, **keywords):
##
        '''
            This method wraps the python's native request handler to provide
            our wrapped file socket buffer.
        '''
        '''Take this method via introspection.'''
        result = builtins.getattr(
            builtins.super(self.__class__, self), inspect.stack()[0][3]
        )(*arguments, **keywords)
        self.rfile = self.server.web.service.read_file_socket
        return result

        # endregion

        # region protected

            # region boolean

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _is_authenticated(
##         self: boostNode.extension.type.Self
##     ) -> builtins.bool:
    def _is_authenticated(self):
##
        '''Determines weather current request is authenticated.'''
        if self.server.web.authentication:
            while self.server.web.authentication_file_name:
                file_path = self._authentication_location.path +\
                    self.server.web.authentication_file_name
                authentication_file = boostNode.extension.file.Handler(
                    location=file_path, must_exist=False)
                if authentication_file:
## python3.3
##                     return (self.headers.get('authorization') ==
##                             'Basic %s' % self._get_login_data(
##                                 authentication_file))
                    return (
                        self.headers.getheader('authorization') ==
                        'Basic %s' % self._get_login_data(
                            authentication_file))
##
                if self._authentication_location != self.server.web.root:
                    break
                self._authentication_location = \
                    boostNode.extension.file.Handler(
                        location=self._authentication_location.directory_path)
## python3.3
##             return builtins.bool(
##                 self.server.web.authentication_handler is None or
##                 self.server.web.authentication_handler(
##                     self.headers.get('authorization'), self.request_uri))
            return builtins.bool(
                self.server.web.authentication_handler is None or
                self.server.web.authentication_handler(
                    self.headers.getheader('authorization'),
                    self.request_uri))
##
        return True

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _is_valid_reference(
##         self: boostNode.extension.type.Self
##     ) -> builtins.bool:
    def _is_valid_reference(self):
##
        '''
            Checks weather the requested is one of a python module-, static- or
            dynamic file request. Returns "True" if so and "False" otherwise.
        '''
        if self.requested_file:
            patterns = self.server.web.dynamic_mime_type_pattern + \
                self.server.web.static_mime_type_pattern
            if self.server.web.directory_listing:
                patterns += '^$',
            if(self.requested_file and self.requested_file.name !=
               self.server.web.authentication_file_name and
               self._check_pattern(
                   patterns=patterns, subject=self.requested_file.mime_type
               ) is not False):
                return True
        elif((self.server.web.module_loading is True or
              self.server.web.module_loading == self.path) and
             boostNode.extension.native.Module.get_file_path(
                 context_path=self.path)):
            self.load_module = True
            return True
        return False

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _is_dynamic(self: boostNode.extension.type.Self) -> builtins.bool:
    def _is_dynamic(self):
##
        '''
            Determines if the current request points to a dynamic executable
            file or is a static type which should be send back unmodified.
        '''
        return builtins.bool(self.load_module or self._check_pattern(
            self.server.web.dynamic_mime_type_pattern,
            boostNode.extension.file.Handler(
                location=self.server.web.root.path + self.requested_file_name
            ).mime_type))

            # endregion

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _get_login_data(
##         self: boostNode.extension.type.Self,
##         authentication_file: boostNode.extension.file.Handler
##     ) -> builtins.str:
    def _get_login_data(self, authentication_file):
##
        __logger__.info(
            'Use authentication file "%s".', authentication_file._path)
        match = re.compile(
            self.server.web.authentication_file_content_pattern
        ).match(authentication_file.content.strip())
## python3.3
##         return base64.b64encode(('%s:%s' % (
##             match.group('name'), match.group('password')
##         )).encode('utf_8')).decode()
        return base64.b64encode(
            '%s:%s' % (match.group('name'), match.group('password')))
##

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _determine_post_dictionary(
##         self: boostNode.extension.type.Self
##     ) -> builtins.dict:
    def _determine_post_dictionary(self):
##
        '''
            Determines the post values given by an html form. File uploads are
            includes as bytes.
        '''
## python3.3
##         form = cgi.FieldStorage(
##             fp=self.rfile, headers=self.headers, keep_blank_values=True,
##             strict_parsing=True,
##             environ=self._determine_environment_variables(),
##             encoding='utf_8')
        form = cgi.FieldStorage(
            fp=self.rfile, headers=self.headers, keep_blank_values=True,
            strict_parsing=True,
            environ=self._determine_environment_variables())
##
        post_dictionary = {}
        for name in form:
            post_dictionary[name] = []
            index = 0
            for value in form.getlist(name):
                # NOTE: This definition handles a cgi module bug.
                value_reference = form[name]
                if builtins.isinstance(form[name], builtins.list):
                    value_reference = form[name][index]
                if(builtins.isinstance(value_reference.file, builtins.file) or
                   value_reference.filename):
## python3.3
##                     post_dictionary[name].append({
##                         'content': value,
##                         'name': value_reference.filename,
##                         'disposition': value_reference.disposition,
##                         'encoding': value_reference.encoding})
                    post_dictionary[name].append({
                        'content': value,
                        'name': value_reference.filename,
                        'disposition': value_reference.disposition})
##
                else:
                    post_dictionary[name].append(value)
                index += 1
        return post_dictionary

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _determine_environment_variables(
##         self: boostNode.extension.type.Self
##     ) -> os._Environ:
    def _determine_environment_variables(self):
##
        '''
            Determines all needed environment variables needed to determine
            given post data with cgi module.
        '''
        accept = []
        for line in self.headers.getallmatchingheaders('accept'):
            if line[:1] in "\t\n\r ":
                accept.append(line.strip())
            else:
                accept = accept + line[7:].split(',')
        variables = copy.deepcopy(os.environ)
## python3.3         content_type = self.headers.get_content_type()
        content_type = self.headers.getheader('content-type')
        variables.update({
            'HTTP_ACCEPT': ','.join(accept),
            'REQUEST_METHOD': self.command,
            'CONTENT_TYPE': content_type,
            'QUERY_STRING': '',
            'REMOTE_HOST': '',
            'CONTENT_LENGTH': '',
            'HTTP_USER_AGENT': '',
            'HTTP_COOKIE': '',
            'HTTP_REFERER': ''})
        for variable_name in variables:
## python3.3
##             if self.headers.get(variable_name.replace('_', '-').lower()):
##                 variables[variable_name] = self.headers.get(
##                     variable_name.replace('_', '-').lower())
##         cookie_content = ', '.join(builtins.filter(
##             None, self.headers.get_all('cookie', [])))
##         if cookie_content:
##             variables['HTTP_COOKIE'] = cookie_content
            if self.headers.getheader(
                variable_name.replace('_', '-').lower()
            ):
                variables[variable_name] = self.headers.getheader(
                    variable_name.replace('_', '-').lower())
##
        return variables

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _send_no_authentication_error(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def _send_no_authentication_error(self):
##
        '''This method is called if authentication failed.'''
        self.send_response(401)
        message = 'You request a protected location'
## python3.3
##         if self.headers.get('authorization'):
        if self.headers.getheader('authorization'):
##
            message = 'The authentication failed'
        self.send_header('WWW-Authenticate', 'Basic realm=\"%s\"' % message)
        self.send_header('Content-Type', 'text/html; charset=UTF-8')
        self.end_headers()
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _send_no_file_error(
##         self: boostNode.extension.type.Self, valid_request=True
##     ) -> boostNode.extension.type.Self:
    def _send_no_file_error(self, valid_request=True):
##
        '''
            Generates a http-404-error if no useful file was found for
            responding.
        '''
        error_message = 'Requested file not found'
        if __logger__.isEnabledFor(logging.DEBUG) or sys.flags.debug:
            error_message = (
                'Eather none of the following default module names "%s" nor '
                'none of the following default file name pattern "%s" found' %
                ('", "'.join(self.server.web.default_module_names),
                 '", "'.join(self.server.web.default_file_name_pattern)))
            if builtins.isinstance(
                self.server.web.module_loading, builtins.str
            ):
                error_message = (
                    'Eather default module name "%s" nor '
                    'none of the following default file name pattern "%s" '
                    'found' % (self.server.web.module_loading, '", "'.join(
                        self.server.web.default_file_name_pattern)))
            elif not self.server.web.module_loading:
                error_message = (
                    'None of the following default file name pattern "%s" '
                    'found' % '", "'.join(
                        self.server.web.default_file_name_pattern))
            if self.path:
                error_message = (
                    'No accessible file "%s" found' %
                    boostNode.extension.file.Handler(
                        location=self.server.web.root.path + self.path,
                        must_exist=False
                    )._path)
            if not valid_request:
                error_message = (
                    "Given request isn't valid. Check your white- and "
                    'blacklists')
            if self.requested_file.is_file():
                error_message += \
                    '. Detected mime-type "%s"' % self.requested_file.mime_type
        self.send_error(404, re.compile('\n+').sub('\n', error_message))
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _check_pattern(
##         self: boostNode.extension.type.Self,
##         patterns: collections.Iterable, subject: builtins.str
##     ) -> (builtins.str, builtins.bool):
    def _check_pattern(self, patterns, subject):
##
        '''
            Checks if one of a list of given regular expression patterns
            matches the given subject.
        '''
        for pattern in patterns:
            if re.compile(pattern).match(subject):
                return subject
        return False

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _is_valid_request(
##         self: boostNode.extension.type.Self
##     ) -> builtins.bool:
    def _is_valid_request(self):
##
        '''Checks if given request fulfill all restrictions.'''
        return self._request_in_pattern_list(
            self.server.web.request_whitelist) and\
            not self._request_in_pattern_list(
                self.server.web.request_blacklist)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _request_in_pattern_list(
##         self: boostNode.extension.type.Self,
##         pattern_list: collections.Iterable
##     ) -> builtins.bool:
    def _request_in_pattern_list(self, pattern_list):
##
        '''Checks if current request matches on of the given pattern.'''
        for pattern in pattern_list:
            if re.compile(pattern).match(self.request_uri):
                return True
        return False

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _create_environment_variables(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def _create_environment_variables(self):
##
        '''Creates all request specified environment-variables.'''
        self.request_uri = self.path
        match = re.compile(
            '[^/{delimiter}]*/+(?P<file_name>[^{delimiter}]*){delimiter}?'
            '(?P<parameter>.*)'.format(
                delimiter=self.server.web.request_parameter_delimiter)
        ).match(self.request_uri)
        self.path = ''
        if match:
## python3.3
##             self.path = posixpath.normpath(urllib.parse.unquote(match.group(
##                 'file_name')))
            self.path = posixpath.normpath(urllib.unquote(match.group(
                'file_name')))
##
            if self.path == '.':
                self.path = ''
            self.parameter = match.group('parameter')
        self.requested_file = boostNode.extension.file.Handler(
            location=self.server.web.root.path + self.path, must_exist=False)
        self._authentication_location = self.server.web.root
        if self.requested_file:
            self._authentication_location = self.requested_file
            if self.requested_file.is_file():
                self._authentication_location = \
                    boostNode.extension.file.Handler(
                        location=self.requested_file.directory_path)
        return self.path

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _set_dynamic_or_static_get(
##         self: boostNode.extension.type.Self, file_name: builtins.str
##     ) -> boostNode.extension.type.Self:
    def _set_dynamic_or_static_get(self, file_name):
##
        '''
            Makes a dynamic or static respond depending on incoming request.
        '''
        self.requested_file_name = file_name
        if self._is_dynamic():
            return self._dynamic_get()
        return self._static_get()

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _default_get(
##         self: boostNode.extension.type.Self
##     ) -> builtins.bool:
    def _default_get(self):
##
        '''
            Handles every request which doesn't takes a file or python module
            with.
        '''
        if self.server.web.default:
            self._handle_given_default_get()
            return True
        if self.server.web.module_loading and self._default_get_module():
            return True
        for file_name_pattern in self.server.web.default_file_name_pattern:
            for file in self.server.web.root:
                if self._check_pattern((file_name_pattern,), file.name):
                    self.requested_file = file
                    self._set_dynamic_or_static_get(file_name=file.name)
                    return True
        if self.server.web.directory_listing:
            self._static_get()
            return True
        return False

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _default_get_module(
##         self: boostNode.extension.type.Self
##     ) -> builtins.bool:
    def _default_get_module(self):
##
        '''Handle if possible a default module request.'''
        for module_name in self.server.web.default_module_names:
            if((self.server.web.module_loading is True or
                module_name == self.server.web.module_loading) and
               self._handle_default_modules_get(module_name)):
                return True
        return False

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _handle_default_modules_get(
##         self: boostNode.extension.type.Self, module_name: builtins.str
##     ) -> (boostNode.extension.type.Self, builtins.bool):
    def _handle_default_modules_get(self, module_name):
##
        '''
            Handles requests which wants the current defaults modules
            (initially called module) run for a server thread.
        '''
        if module_name == '__main__':
            if __name__ != '__main__':
                self.load_module = True
                return self._set_dynamic_or_static_get(file_name=module_name)
        elif boostNode.extension.native.Module.get_file_path(
            context_path=module_name
        ):
            self.load_module = True
            return self._set_dynamic_or_static_get(file_name=module_name)
        return False

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _handle_given_default_get(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def _handle_given_default_get(self):
##
        '''Handles request with no explicit file or module to run.'''
        if((self.server.web.dynamic_module_loading is True or
            self.server.web.dynamic_module_loading ==
            self.server.web.default) and
           boostNode.extension.native.Module.get_file_path(
               context_path=self.server.web.default)):
            self.load_module = True
            __logger__.info(
                'Determine "%s" as default module.', self.server.web.default)
        self.requested_file = boostNode.extension.file.Handler(
            location=self.server.web.root.path + self.server.web.default,
            must_exist=False)
        if self.requested_file:
            __logger__.info(
                'Determine "%s" as default file.', self.server.web.default)
        return self._set_dynamic_or_static_get(
            file_name=self.server.web.default)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _static_get(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def _static_get(self):
##
        '''Handles a static file-request.'''
        if self.requested_file.is_directory():
            return self.list_directory()
        try:
            file_handler = builtins.open(self.requested_file._path, mode='rb')
        except builtins.IOError:
            self._send_no_file_error()
            return self
## python3.3
##         if(self.headers.get('If-Modified-Since') ==
##            self.date_time_string(
##                builtins.int(self.requested_file.timestamp))):
        if(self.headers.getheader('If-Modified-Since') ==
           self.date_time_string(
               builtins.int(self.requested_file.timestamp))):
##
            return self._send_not_modified_header()
        return self._send_static_file(output=file_handler)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _send_static_file(
##         self: boostNode.extension.type.Self, output: (builtins.str,)
##     ) -> boostNode.extension.type.Self:
    def _send_static_file(self, output):
##
        '''Sends given output to client.'''
        threshold = self.server.web.file_size_stream_threshold_in_byte
        if threshold < self.requested_file.size:
            self.send_content_type_header(mime_type='application/octet-stream')
            self.send_header('Content-Transfer-Encoding', 'binary')
        else:
            self.send_content_type_header(
                mime_type=self.requested_file.mime_type)
        self.send_static_file_cache_header(
            timestamp=self.requested_file.timestamp)
        self.send_content_length_header(
            size=builtins.int(self.requested_file.size))
        self.end_headers()
        return self._send_output(output)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _send_not_modified_header(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def _send_not_modified_header(self):
##
        '''Sends a header to client indicating cached file hasn't changed.'''
        self.send_content_type_header(
            mime_type=self.requested_file.mime_type, response_code=304
        ).send_static_file_cache_header(
            timestamp=self.requested_file.timestamp
        ).send_content_length_header(
            size=builtins.int(self.requested_file.size))
        self.end_headers()
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _send_output(
##         self: boostNode.extension.type.Self, output: (builtins.str,)
##     ) -> boostNode.extension.type.Self:
    def _send_output(self, output):
##
        '''Sends the final given output to client.'''
        if self._encoded_output:
            self.wfile.write(self._encoded_output)
        elif builtins.isinstance(output, builtins.str):
            self.wfile.write(output)
        else:
            self.copyfile(output, self.wfile)
            output.close()
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _gzip(
##         self: boostNode.extension.type.Self, content: builtins.str
##     ) -> builtins.str:
    def _gzip(self, content):
##
        '''Compresses the given content and returns the encoded result.'''
## python3.3         output = io.BytesIO()
        output = StringIO.StringIO()
        gzip_file_handler = gzip.GzipFile(
            fileobj=output, mode='w', compresslevel=5)
## python3.3
##         if builtins.isinstance(content, builtins.bytes):
##             gzip_file_handler.write(content)
##         else:
##             # TODO utf_8 shouldn't be hardcoded at this point.
##             gzip_file_handler.write(content.encode(encoding='utf_8'))
        gzip_file_handler.write(content)
##
        gzip_file_handler.close()
        return output.getvalue()

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _dynamic_get(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def _dynamic_get(self):
##
        '''
            Handles a dynamic file or python module request.
            It initializes the given script-file or python module environment
            weather to decide running it in its own thread or not.
            If no respond is expected from client it could be run without its
            own thread environment.
        '''
        self.request_arguments = [
            self.requested_file_name, self.request_uri,
            self.parse_url(self.request_uri)[1],
            self.post_dictionary, self.server.web.shared_data, self]
        if '__no_respond__' not in self.post_dictionary:
            self.respond = True
            return self._run_request()
        self.__class__.last_running_worker = threading.Thread(
            target=self._run_request)
        self.__class__.last_running_worker.start()
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _run_request(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def _run_request(self):
##
        '''
            Decides to run the given script as python-module or standalone
            script-file.
        '''
        if self.load_module:
            return self._run_requested_module()
        return self._run_requested_file()

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _run_requested_file(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def _run_requested_file(self):
##
        '''
            Runs a given external process in a subprocess. Output and errors
            are piped to requested client.
        '''
        self.request_arguments[0] = self.server.web.root.path + \
            self.request_arguments[0]
        self.request_arguments = builtins.list(builtins.map(
            lambda element: builtins.str(element), self.request_arguments))
        __logger__.debug('Execute file "%s".', self.request_arguments[0])
        self.server.web.number_of_running_threads += 1
        try:
            output, errors = subprocess.Popen(
                self.request_arguments, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            ).communicate()
        except builtins.OSError as exception:
            output = ''
            errors = '%s: %s' % (
                exception.__class__.__name__, builtins.str(exception))
        self.server.web.number_of_running_threads -= 1
        size = builtins.len(output)
        errors = errors.decode(
            encoding=boostNode.extension.native.String(errors).encoding,
            errors='strict')
        if self.respond:
            if errors:
                program_description = ''
                if sys.flags.debug or __logger__.isEnabledFor(logging.DEBUG):
                    program_description = ' "%s"' % self.request_arguments[0]
                self.send_error(
                    500, 'Internal server error with cgi program%s: "%s"' %
                    (program_description, re.compile('\n+').sub('\n', errors)))
            else:
                '''Check if given output contains a header.'''
                header_match = re.compile(
                    '^[A-Z0-9]+/([0-9]+\.)+[0-9]+ [0-9]{3} [a-zA-Z ]+\n'
                    '([^:]+: .+\n)+\n.+'
                ).match(output.decode(
                    encoding=boostNode.extension.native.String(output).encoding
                ))
                if not header_match:
                    self.send_content_type_header().send_content_length_header(
                        size, dynamic_output=output
                    ).end_headers()
                self._send_output(output)
        if errors:
            __logger__.critical(
                'Error in common getaway interface program "%s": %s',
                self.request_arguments[0], errors)
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _run_requested_module(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def _run_requested_module(self):
##
        '''
            Imports and runs a given python module. Errors and output are
            piped to requested client.
        '''
        '''Redirect output buffer.'''
        print_default_buffer_backup = \
            boostNode.extension.output.Print.default_buffer
        boostNode.extension.output.Print.default_buffer = \
            self.server.web.thread_buffer
## python3.3         sys_path_backup = sys.path.copy()
        sys_path_backup = copy.copy(sys.path)
        sys.path = [self.server.web.root.path] + sys.path
        self.server.web.number_of_running_threads += 1
        requested_module = builtins.__import__(self.request_arguments[0])
        '''Extend requested scope with request dependent globals.'''
        requested_module.__requested_arguments__ = self.request_arguments
        sys.path = sys_path_backup
        __logger__.debug('Run module "%s".', requested_module)
        return self._handle_module_running(
            requested_module, print_default_buffer_backup, sys_path_backup)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _handle_module_running(
##         self: boostNode.extension.type.Self,
##         requested_module: types.ModuleType,
##         print_default_buffer_backup: builtins.object,
##         sys_path_backup: collections.Iterable
##     ) -> boostNode.extension.type.Self:
    def _handle_module_running(
        self, requested_module, print_default_buffer_backup, sys_path_backup
    ):
##
        '''Handles exceptions raising in requested modules.'''
        get_defined_callables = boostNode.extension.native.Module\
            .get_defined_callables
        try:
            builtins.getattr(
                requested_module,
                boostNode.extension.native.Module.determine_caller(
                    callable_objects=get_defined_callables(
                        scope=requested_module)))()
        except builtins.Exception as exception:
            self._handle_module_exception(requested_module, exception)
        else:
            if self.respond:
                self.send_content_type_header().send_content_length_header(
                    size=builtins.len(self.server.web.thread_buffer.content),
                    dynamic_output=self.server.web.thread_buffer.content
                ).end_headers()
        finally:
            self.server.web.number_of_running_threads -= 1
            if self.respond:
                self._send_output(
                    output=self.server.web.thread_buffer.clear())
            boostNode.extension.output.Print.default_buffer = \
                print_default_buffer_backup
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _handle_module_exception(
##         self: boostNode.extension.type.Self,
##         requested_module: types.ModuleType, exception: builtins.Exception
##     ) -> boostNode.extension.type.Self:
    def _handle_module_exception(self, requested_module, exception):
##
        '''
            This method handles each exception raised by running a module
            which was requested by client.
        '''
        if self.respond:
            if(sys.flags.debug or __logger__.isEnabledFor(logging.DEBUG)):
                self.send_error(
                    500, '%s: %s' %
                    (exception.__class__.__name__,
                     re.compile('\n+').sub('\n', builtins.str(exception))))
            else:
                self.send_error(500, 'Internal server error')
        if sys.flags.debug or __logger__.isEnabledFor(logging.DEBUG):
            raise
        else:
            __logger__.critical(
                'Error in module "%s" %s: %s',
                requested_module.__name__,
                exception.__class__.__name__, builtins.str(exception))
        return self

        # endregion

    # endregion

# endregion

# region footer

'''
    Preset some variables given by introspection letting the linter know what
    globale variables are available.
'''
__logger__ = __test_mode__ = __exception__ = __module_name__ = \
    __file_path__ = None
'''
    Extends this module with some magic environment variables to provide better
    introspection support. A generic command line interface for some code
    preprocessing tools is provided by default.
'''
boostNode.extension.native.Module.default(
    name=__name__, frame=inspect.currentframe(), default_caller=Web.__name__)

# endregion
