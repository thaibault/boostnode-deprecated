#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

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
__credits__ = ('Torben Sickert',)
__license__ = 'see boostNode/__init__.py'
__maintainer__ = 'Torben Sickert'
__maintainer_email__ = 't.sickert@gmail.com'
__status__ = 'stable'
__version__ = '1.0'

## python3.3
## import builtins
import BaseHTTPServer
import CGIHTTPServer
##
import cgi
## python3.3
## import collections
## import http.server
## import imp
import copy
##
import inspect
import logging
import os
import re
import socket
import subprocess
import sys
import threading
## python3.3
## import types
## import urllib.parse
import urlparse
##

## python3.3 pass
builtins = sys.modules['__main__'].__builtins__

sys.path.append(os.path.abspath(sys.path[0] + 3 * ('..' + os.sep)))
sys.path.append(os.path.abspath(sys.path[0] + 4 * ('..' + os.sep)))

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

class Web(
    boostNode.paradigm.objectOrientation.Class,
    boostNode.extension.system.Runnable
):
    '''
        Provides a small platform independent webserver designed for easily
        serve a client-server structure.
    '''

    # region constant properties

        # region public properties

    '''
        Holds all command line interface argument informations.
    '''
    COMMAND_LINE_ARGUMENTS = (
        {'arguments': ('-r', '--root'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': False,
             'help': 'Defines which path is used as webroot.',
             'dest': 'root',
             'metavar': 'PATH'}},
        {'arguments': ('-p', '--port'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'choices': builtins.range(0, 2 ** 16),
             'required': False,
             'help': 'Defines the port number to access the webserver.',
             'dest': 'port',
             'metavar': 'NUMBER'}},
        {'arguments': ('-d', '--default'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': False,
             'help': 'Defines which file or module should be requested if '
                     'nothing was declared explicitly. It could be understood'
                     ' as welcome page.',
             'dest': 'default',
             'metavar': 'PATH'}},
        {'arguments': ('-o', '--close-order'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': False,
             'help': 'Saves a cli-command for shutting down the server.',
             'dest': 'close_order',
             'metavar': 'STRING'}},
        {'arguments': ('-w', '--request-whitelist'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': False,
             'help': 'Select request type regex patterns which are only '
                     'allowed for being interpreted.',
             'dest': 'request_whitelist',
             'metavar': 'REQUEST_REGEX_PATTERN'}},
        {'arguments': ('-b', '--request-blacklist'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': False,
             'help': "Select request type regex patterns which aren't "
                     'allowed for being interpreted.',
             'dest': 'request_blacklist',
             'metavar': 'REQUEST_REGEX_PATTERN'}},
        {'arguments': ('-s', '--static-mimetype-pattern'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': False,
             'help': 'All mime-type patterns which should recognize a static '
                     'file. Those files will be directly sent to client '
                     'without any preprocessing.',
             'dest': 'static_mimetype_pattern',
             'metavar': 'MIMETYPE_REGEX_PATTERN'}},
        {'arguments': ('-y', '--dynamic-mimetype-pattern'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': False,
             'help': 'All mime-type patterns which should recognize a dynamic '
                     'file. Those files will be interpreted so the result can '
                     'be send back to client.',
             'dest': 'dynamic_mimetype_pattern',
             'metavar': 'MIMETYPE_REGEX_PATTERN'}},
        {'arguments': ('-f', '--default-file-name-pattern'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': False,
             'help': 'All file name patterns which should be run if there is '
                     'one present and no other default filepattern/name is '
                     'given on initialisation.',
             'dest': 'default_file_name_pattern',
             'metavar': 'FILE_NAME_REGEX_PATTERN'}},
        {'arguments': ('-a', '--default-module-name-pattern'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': False,
             'help': 'Same as file name for module name patterns. '
                     'Note that default files have a lower priority as '
                     'default python modules.',
             'dest': 'default_module_name_pattern',
             'metavar': 'MODULE_NAME_REGEX_PATTERN'}})

        # endregion

    # endregion

    # region dynamic properties

        # region public properties

    '''Saves server runtime properties.'''
    root = port = thread_buffer = service = None
    '''Saves a default file if no explicit file was requested.'''
    default = ''
    '''Saves a cli-command for shutting down the server.'''
    close_order = ''
    '''A list of regex pattern which every request have to match.'''
    request_whitelist = ()
    '''A list of regex pattern which no request should match.'''
    request_blacklist = ()
    '''Saves all initializes server instances.'''
    instances = []
    '''
        Saves all mimetype pattern to interpret as files which shouldn't be
        ran.
    '''
    static_mimetype_pattern = ()
    '''
        Saves all mimetype pattern to interpret as files which should be
        ran. There standart output will be given back to request.
    '''
    dynamic_mimetype_pattern = ()
    '''
        Saves all file name pattern to be taken as fallback if no explicit file
        or module was requested.
    '''
    default_file_name_pattern = ()
    '''
        Saves all mpodule name pattern to be taken as fallback if no explicit
        file or module was requested.
    '''
    default_module_name_pattern = ()

        # endregion

    # endregion

    # region dynamic methods

        # region public methods

            # region special methods

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def __repr__(self: boostNode.extension.type.Self) -> builtins.str:
    def __repr__(self):
##
        '''
            Invokes if this object should describe itself by a string.

            Examples:

            >>> repr(Web()) # doctest: +ELLIPSIS
            'Object of "Web" with root path "...", port "80" and clo..."clo...'
        '''
        return 'Object of "{class_name}" with root path "{path}", port '\
               '"{port}" and close order "{close_order}".'.format(
                   class_name=self.__class__.__name__, path=self.root,
                   port=self.port, close_order=self.close_order)

            # endregion

        # endregion

        # region protected methods.

            # region runnable implementation

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _run(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def _run(self):
##
        '''
            Entry point for command line call of this progam.
            Starts the server's request handler listing for incoming requests.

            Examples:

            >>> Web(root='.') # doctest: +ELLIPSIS
            Object of "Web" with root path "...", port "80" and close order ...
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
##         self: boostNode.extension.type.Self, root='.', port=80,
##         default='', close_order='close', request_whitelist=('/.*',),
##         request_blacklist=(),
##         # NOTE: Tuple for explicit webserver file reference validation.
##         # ('^text/.+', '^image/.+', '^application/(x-)?javascript$')
##         static_mimetype_pattern=('^.+/.+$',),
##         dynamic_mimetype_pattern=(
##             '^text/x-python$', 'text/x-sh', '^text/x-shellscript$'),
##         default_file_name_pattern=(
##             '^__main__.[a-zA-Z0-9]{2,4}$', '^main.[a-zA-Z0-9]{2,4}$',
##             '^index.[a-zA-Z0-9]{2,4}$', '^initialize.[a-zA-Z0-9]{2,4}$'),
##         default_module_name_pattern=(
##             '__main__', 'main', 'index', 'initialize'),
##         **keywords: builtins.object
##     ) -> boostNode.extension.type.Self:
    def _initialize(
        self, root='.', port=80, default='', close_order='close',
        request_whitelist=('/.*',), request_blacklist=(),
        # NOTE: Tuple for explicit webserver file reference validation.
        # ('^text/.+', '^image/.+', '^application/(x-)?javascript$')
        static_mimetype_pattern=('^.+/.+$',),
        dynamic_mimetype_pattern=(
            '^text/x-python$', 'text/x-sh', '^text/x-shellscript$'),
        default_file_name_pattern=(
            '^__main__.[a-zA-Z0-9]{2,4}$', '^main.[a-zA-Z0-9]{2,4}$',
            '^index.[a-zA-Z0-9]{2,4}$', '^initialize.[a-zA-Z0-9]{2,4}$'),
        default_module_name_pattern=(
            '__main__', 'main', 'index', 'initialize'),
        **keywords
    ):
##
        '''
            Sets root path of webserver and all properties. Although the
            server thread will be started.
        '''
        self.__class__.instances.append(self)
        self.close_order = close_order
        self.root = boostNode.extension.file.Handler(location=root)
        self.port = port
        self.default = default
        self.request_whitelist = request_whitelist
        self.request_blacklist = request_blacklist
        self.static_mimetype_pattern = static_mimetype_pattern
        self.dynamic_mimetype_pattern = dynamic_mimetype_pattern
        self.default_file_name_pattern = default_file_name_pattern
        self.default_module_name_pattern = default_module_name_pattern
        self.thread_buffer = boostNode.extension.output.Buffer(
            queue=True)
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
        if __name__ == '__main__' and not __test_mode__:
            def wait_for_close_order():
                '''
                    Handler for waiting till a server close order comes through
                    the command line interface.
                '''
                try:
                    wait_for_close = ''
                    while wait_for_close != self.close_order:
## python3.3                         wait_for_close = builtins.input(
                        wait_for_close = builtins.raw_input(
                            'Write "%s" for shutting down server:\n' %
                            self.close_order)
                except builtins.KeyboardInterrupt:
                    wait_for_close_order()
            wait_for_close_order()
            __logger__.info('Shutting down webserver.')
            self.service.socket.close()
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _log_server_status(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def _log_server_status(self):
##
        '''
            Prints some information about the way the server was started.
        '''
        __logger__.info(
            'Webserver is starting and listens at port "%d". Webroot is "%s".',
            self.port, self.root.path)
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _start_with_dynamic_port(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def _start_with_dynamic_port(self):
##
        '''
            Searches for the highest free port for listing.
        '''
        range = builtins.list(builtins.range(1, 2 ** 16 - 1))
        for port in [8080, 80, 25, 139, 445, 631, 3306] + range + [0]:
            try:
                self._initialize_server_thread(port)
            except socket.error:
                if not port:
                    raise __exception__(
                        'No port is avalible to run the web-server with given'
                        'rights.')
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
        '''
            Starts the server listing on the given port, if it is free.
        '''
        try:
            self._initialize_server_thread(port=self.port)
        except socket.error:
            raise __exception__(
                "Port %d isn't avalible to run the web-server with given "
                'rights.', self.port)
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _initialize_server_thread(
##         self: boostNode.extension.type.Self, port: builtins.int
##     ) -> boostNode.extension.type.Self:
    def _initialize_server_thread(self, port):
##
        '''
            Initializes a new request-handler and starts its own thread.
        '''
## python3.3
##         self.service = http.server.HTTPServer(
##             ('', port), CGIHTTPRequestHandler)
        self.service = BaseHTTPServer.HTTPServer(
            ('', port), CGIHTTPRequestHandler)
##
        self.service.web = self
        threading.Thread(target=self.service.serve_forever).start()
        return self

        # endregion

    # endregion


## python3.3
## class CGIHTTPRequestHandler(http.server.CGIHTTPRequestHandler):
class CGIHTTPRequestHandler(CGIHTTPServer.CGIHTTPRequestHandler):
##
    '''
        A small request-handler dealing with incoming file requests.
        It can directly send static files back to client or run dynamic
        scripts and give the output back to client.
    '''

    # region dynamic properties

        # region public properties

    '''Properties defined by incoming request.'''
    request_uri = ''
    parameter = ''
    post_dictonary = {}
    '''Saves the last started worker thread instance.'''
    last_running_worker = None
    '''Consists the explicit requested file-handler coming from client.'''
    request_file = None
    '''
        Defines wether the handler has decided to run a python module or an
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

        # endregion

    # endregion

    # region dynamic methods

        # region public methods

            # region special methods

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

        # region public methods

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def parse_url(
##         cls: boostNode.extension.type.SelfClass, url=None
##     ) -> builtins.tuple:
    def parse_url(cls, url=None):
##
        '''
            This static method provides an easy way to split a http
            request-string into its components.
        '''
        if url is None and builtins.len(sys.argv) > 1:
            url = sys.argv[1]
        if url:
## python3.3             get = urllib.parse.urlparse(url).query
            get = urlparse.urlparse(url).query
            if get:
                try:
## python3.3
##                     get = urllib.parse.parse_qs(
##                         qs=urllib.parse.urlparse(url).query,
##                         keep_blank_values=True,
##                         strict_parsing=True,
##                         encoding='utf-8',
##                         errors='replace')
                    get = urlparse.parse_qs(
                        qs=urlparse.urlparse(url).query,
                        keep_blank_values=True,
                        strict_parsing=True)
##
                except builtins.ValueError:
                    get = {}
                    __logger__.info('Query "%s" string is not valid.', url)
            if not get:
                get = {}
            for key, value in get.items():
                get[key] = value[0]
## python3.3             return (urllib.parse.urlparse(url), get)
            return (urlparse.urlparse(url), get)
        return (None, {})

        # endregion

    # endregion

    # region dynamic methods

        # region public methods

            # region event methods

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
        if self._is_valid_request():
            if self._create_environment_variables():
                if self._is_valid_reference():
                    return self._set_dynamic_or_static_get(file=self.path)
            elif self._default_get():
                return self
        return self._send_no_file_error()

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def do_POST(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def do_POST(self):
##
        '''
            Is triggered if a post-request is coming.
        '''
## python3.3
##         data_type, post_data = cgi.parse_header(
##             self.headers.get_content_type())
        data_type, post_data = cgi.parse_header(self.headers.getheader(
            'content-type'))
##
        if data_type == 'multipart/form-data':
            self.post_dictonary = cgi.parse_multipart(self.rfile, post_data)
        elif data_type == 'application/x-www-form-urlencoded':
## python3.3
##             self.post_dictonary = urllib.parse.parse_qs(self.rfile.read(
##                 builtins.int(self.headers['content-length'])
##             ).decode('utf-8'))
            self.post_dictonary = cgi.parse_qs(
                self.rfile.read(builtins.int(self.headers.getheader(
                    'content-length'))),
                keep_blank_values=1)
##
        return self.do_GET()

            # endregion

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
        if builtins.len(self.server.web.instances) > 1:
            format += '(port: %d)' % self.server.web.port
        if message_end is None:
            __logger__.info(
                format, message_or_error_code, response_code_or_message)
        else:
            __logger__.info(
                format, message_or_error_code, response_code_or_message, '')
        return self

        # endregion

        # region protected methods

            # region boolean methods

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
            self.server.web.dynamic_mimetype_pattern,
            boostNode.extension.file.Handler(
                location=self.server.web.root.path + self.request_file
            ).mimetype))

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _is_valid_reference(
##         self: boostNode.extension.type.Self
##     ) -> builtins.bool:
    def _is_valid_reference(self):
##
        '''
            Checks wether the incoming is one of a python module-, static- or
            dynamic file request.
        '''
        requested_file = boostNode.extension.file.Handler(
            location=self.server.web.root.path + self.path, must_exist=False)
        if not requested_file:
            if(boostNode.extension.native.Module.get_file_path(
               context_path=self.path)):
                self.load_module = True
                return True
        elif(self._check_pattern(
             patterns=(
                 self.server.web.dynamic_mimetype_pattern +
                 self.server.web.static_mimetype_pattern),
             subject=requested_file.mimetype)):
            return True
        return False

            # endregion

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _send_positive_header(
##         self: boostNode.extension.type.Self, mimetype: builtins.str
##     ) -> boostNode.extension.type.Self:
    def _send_positive_header(self, mimetype):
##
        '''
            Is called for each successful answered http-request.
        '''
        try:
            self.send_response(200)
            self.send_header('Content-type', mimetype)
            self.end_headers()
        except socket.error:
            __logger__.info('Connection interrupted.')
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _send_no_file_error(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def _send_no_file_error(self):
##
        '''
            Generates a http-404-error if no useful file was found for
            responding.
        '''
        error_message = 'Requested file not found.'
        if __logger__.isEnabledFor(logging.DEBUG) or sys.flags.debug:
            error_message = (
                'None of the following default file-pattern "%s" was found' %
                '", "'.join(self.server.web.default_module_name_pattern))
            if self.path:
                error_message = 'No file "%s" found.' %\
                                self.server.web.root.path + self.path
            if self.request_file:
                error_message += ' Detected mime-type "%s".' %\
                                 self.request_file.mimetype
        self.send_error(404, error_message)
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
            Checks if one of a list of given regular expression
            patterns matches the given subject.
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
        '''
            Checks if given request fulfill all restrictions.
        '''
        return self._request_is_in_pattern_list(
            self.server.web.request_whitelist) and\
            not self._request_is_in_pattern_list(
                self.server.web.request_blacklist)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _request_is_in_pattern_list(
##         self: boostNode.extension.type.Self,
##         pattern_list: collections.Iterable
##     ) -> builtins.bool:
    def _request_is_in_pattern_list(self, pattern_list):
##
        '''
            Checks if current request matches on of the given pattern.
        '''
        for pattern in pattern_list:
            if re.compile(pattern).match(self.path):
                return True
        return False

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _create_environment_variables(
##         self: boostNode.extension.type.Self
##     ) -> builtins.bool:
    def _create_environment_variables(self):
##
        '''
            Creates all request specified environment-variables.
        '''
        self.request_uri = self.path
        match = re.compile('[^/\?]*/+([^?]*)\??(.*)').match(self.request_uri)
        if match:
            self.path = match.group(1)
            self.parameter = match.group(2)
        return builtins.bool(self.path)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _set_dynamic_or_static_get(
##         self: boostNode.extension.type.Self, file: builtins.str
##     ) -> boostNode.extension.type.Self:
    def _set_dynamic_or_static_get(self, file):
##
        '''
            Makes a dynamic or static respond depending on incoming
            request.
        '''
        self.request_file = file
        if self._is_dynamic():
            return self._dynamic_get()
        return self._static_get()

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _default_get(
##         self: boostNode.extension.type.Self
##     ) -> (boostNode.extension.type.Self, builtins.bool):
    def _default_get(self):
##
        '''
            Handles every request which doesn't takes a file or python module
            with.
        '''
        if self.server.web.default:
            return self._handle_given_default_get()
        for module_name in self.server.web.default_module_name_pattern:
            if self._handle_default_modules_get(module_name):
                return self
        for file_name_pattern in self.server.web.default_file_name_pattern:
            for file in self.server.web.root:
                if self._check_pattern((file_name_pattern,), file.name):
                    return self._set_dynamic_or_static_get(file=file.name)
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
                return self._set_dynamic_or_static_get(file=module_name)
        elif(boostNode.extension.native.Module.get_file_path(
             context_path=module_name)):
            self.load_module = True
            return self._set_dynamic_or_static_get(file=module_name)
        return False

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _handle_given_default_get(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def _handle_given_default_get(self):
##
        '''
            Handles request with no explicit file or module to run.
        '''
        if(self.server.web.default == '__main__' or
           boostNode.extension.native.Module.get_file_path(
               context_path=self.server.web.default)):
            self.load_module = True
        return self._set_dynamic_or_static_get(file=self.server.web.default)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _static_get(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def _static_get(self):
##
        '''
            Handles a static file-request.
        '''
        requested_file = boostNode.extension.file.Handler(
            location=self.server.web.root.path + self.request_file)
        self._send_positive_header(mimetype=requested_file.mimetype)
        with builtins.open(requested_file._path, mode='rb') as file:
            try:
                self.wfile.write(file.read())
            except socket.error:
                __logger__.info('Connection interrupted.')
        return self

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
        self._send_positive_header(mimetype='text/html')
        self.request_arguments = [
            self.request_file, self.request_uri,
            self.__class__.parse_url(self.request_uri)[1],
            self.post_dictonary, self.server]
        if 'no_respond' not in self.post_dictonary:
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
        self.request_arguments[0] = self.server.web.root.path +\
            self.request_arguments[0]
        self.request_arguments = builtins.list(builtins.map(
            lambda element: builtins.str(element), self.request_arguments))
        output, errors = subprocess.Popen(
            self.request_arguments, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        ).communicate()
        if self.respond:
            if((__logger__.isEnabledFor(logging.DEBUG) or sys.flags.debug) and
               errors):
                output = b'<pre>' + errors + b'</pre>' + output
            try:
                self.wfile.write(output)
            except socket.error:
                __logger__.info('Connection interrupted.')
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
        print_default_buffer_save =\
            boostNode.extension.output.Print.default_buffer
        boostNode.extension.output.Print.default_buffer =\
            self.server.web.thread_buffer
## python3.3         sys_path_save = sys.path.copy()
        sys_path_save = copy.copy(sys.path)
        sys.path = [self.server.web.root.path]
        requested_module = builtins.__import__(self.request_arguments[0])
        '''Extend requested scope with request dependent globals.'''
        requested_module.__requested_arguments__ = self.request_arguments
        return self._handle_module_running(
            requested_module, print_default_buffer_save, sys_path_save)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _handle_module_running(
##         self: boostNode.extension.type.Self,
##         requested_module: types.ModuleType,
##         print_default_buffer_save: builtins.object,
##         sys_path_save: collections.Iterable
##     ) -> boostNode.extension.type.Self:
    def _handle_module_running(
        self, requested_module, print_default_buffer_save,
        sys_path_save
    ):
##
        '''
            Handles exceptions raising in requested modules.
        '''
        filter_none_callable_and_builtins = boostNode.extension.native.Module\
            .filter_none_callable_and_builtins
        try:
            builtins.getattr(
                requested_module,
                boostNode.extension.native.Module.determine_caller(
                    callable_objects=filter_none_callable_and_builtins(
                        scope=requested_module)))()
        except builtins.Exception as exception:
            if self.respond:
                if __logger__.isEnabledFor(logging.DEBUG) or sys.flags.debug:
                    self.send_error(500, builtins.str(exception))
                else:
                    self.send_error(500, 'Internal server error.')
            raise exception
        finally:
            sys.path = sys_path_save
            boostNode.extension.output.Print.default_buffer =\
                print_default_buffer_save
        if self.respond:
            try:
                self.wfile.write(
                    self.server.web.thread_buffer.content.encode())
            except socket.error:
                __logger__.info('Connection interrupted.')
            self.server.web.thread_buffer.clear()
        return self

        # endregion

    # endregion

# endregion

# region footer

boostNode.extension.native.Module.default(
    name=__name__, frame=inspect.currentframe(), default_caller=Web.__name__)

# endregion
