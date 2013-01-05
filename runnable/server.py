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

import base64
## python3.3
## import builtins
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
import inspect
import logging
import os
import ssl
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
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Defines which path is used as webroot.',
             'dest': 'root',
             'metavar': 'PATH'}},
        {'arguments': ('-p', '--port'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'choices': builtins.range(0, 2 ** 16),
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Defines the port number to access the webserver.',
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
        {'arguments': ('-o', '--close-order'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Saves a cli-command for shutting down the server.',
             'dest': 'close_order',
             'metavar': 'STRING'}},
        {'arguments': ('-w', '--request-whitelist'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Select request type regex patterns which are only '
                     'allowed for being interpreted.',
             'dest': 'request_whitelist',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-b', '--request-blacklist'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': "Select request type regex patterns which aren't "
                     'allowed for being interpreted.',
             'dest': 'request_blacklist',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-s', '--static-mimetype-pattern'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'All mime-type patterns which should recognize a static '
                     'file. Those files will be directly sent to client '
                     'without any preprocessing.',
             'dest': 'static_mimetype_pattern',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-y', '--dynamic-mimetype-pattern'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'All mime-type patterns which should recognize a dynamic '
                     'file. Those files will be interpreted so the result can '
                     'be send back to client.',
             'dest': 'dynamic_mimetype_pattern',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-f', '--default-file-name-pattern'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'All file name patterns which should be run if there is '
                     'one present and no other default filepattern/name is '
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
             'dest': 'default_module_name_pattern',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-a', '--authentication'),
         'keywords': {
             'action': 'store_true',
             'default': {'execute': '__initializer_default_value__'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Enables basic http authentication. You can controle '
                     'this behavior by providing an authentication file in '
                     'directorys you want to save.',
             'dest': 'authentication'}},
        {'arguments': ('-g', '--authentication-file-pattern'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Defines the regex pattern to define how to parse '
                     'authentication files.',
             'dest': 'authentication_file_pattern',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-e', '--authentication-file-name-pattern'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Defines the authentication file name.',
             'dest': 'authentication_file_name',
             'metavar': 'STRING'}})

        # endregion

    # endregion

    # region dynamic properties

        # region protected properties

    '''
        Holds a file object referencing a "<DOMAIN_NAME>.pem" file needed
        for open ssl connections.
    '''
    _public_key_file = None

        # endregion

        # region public properties

    '''Saves server runtime properties.'''
    root = port = thread_buffer = lock = service = None
    '''Saves a default file if no explicit file was requested.'''
    default = ''
    '''Saves a cli-command for shutting down the server.'''
    close_order = ''
    '''
        Saves informations how to define authentications in protected
        directories.
    '''
    authentication = False
    authentication_file_name = ''
    authentication_file_pattern = ''
    authentication_handler = None
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
            'Object of "Web" with root path "...", port "0" and clo..."clo...'
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
            Object of "Web" with root path "...", port "0" and close order ...
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
##         self: boostNode.extension.type.Self, root='.', port=0,
##         default='', public_key_file_path='', close_order='close',
##         request_whitelist=('/.*',), request_blacklist=(),
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
##         authentication=True, authentication_file_name='.htpasswd',
##         authentication_file_pattern='(?P<name>.+):(?P<password>.+)',
##         authentication_handler=None, **keywords: builtins.object
##     ) -> boostNode.extension.type.Self:
    def _initialize(
        self, root='.', port=0, default='', public_key_file_path='',
        close_order='close', request_whitelist=('/.*',),
        request_blacklist=(),
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
        authentication=True, authentication_file_name='.htpasswd',
        authentication_file_pattern='(?P<name>.+):(?P<password>.+)',
        authentication_handler=None, **keywords
    ):
##
        '''
            Sets root path of webserver and all properties. Although the
            server thread will be started.
        '''
        self.__class__.instances.append(self)
        public_key_file = boostNode.extension.file.Handler(
            location=public_key_file_path)
        if public_key_file.is_file():
            self._public_key_file = public_key_file
        self.authentication_handler = authentication_handler

        self.authentication = authentication
        self.authentication_file_name = authentication_file_name
        self.authentication_file_pattern = authentication_file_pattern
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
        self.lock = threading.Lock()
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
            'Webserver is starting %sand listens at port "%d" and webroot '
            '"%s".',
            ('a secure connection with public key "%s" ' %
             self._public_key_file.path) if self._public_key_file else '',
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
        ports = [80, 8080, 8000, 25, 139, 445, 631, 3306]
        if self._public_key_file:
            ports = [443] + ports
        ports += builtins.list(builtins.set(
            builtins.range(0, 2 ** 16 - 1)
        ).difference(ports))
        for port in ports:
            try:
                self._initialize_server_thread(port)
            except socket.error:
                if not port:
## python3.3
##                     raise __exception__(
##                         'No port is avalible to run the web-server with '
##                         'given rights.'
##                     ) from None
                    raise __exception__(
                        'No port is avalible to run the web-server with '
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
        '''
            Starts the server listing on the given port, if it is free.
        '''
        try:
            self._initialize_server_thread(port=self.port)
        except socket.error:
## python3.3
##             raise __exception__(
##                 "Port %d isn't avalible to run the web-server with given "
##                 'rights.', self.port
##             ) from None
            raise __exception__(
                "Port %d isn't avalible to run the web-server with given "
                'rights.', self.port)
##
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
        if self._public_key_file:
## python3.3
##             self.service = http.server.HTTPServer(
##                 (self._public_key_file.basename, port),
##                 CGIHTTPRequestHandler)
            self.service = BaseHTTPServer.HTTPServer(
                (self._public_key_file.basename, port),
                CGIHTTPRequestHandler)
##
            self.service.socket = ssl.wrap_socket(
                self.service.socket, certfile=self._public_key_file.path,
                server_side=True)
        else:
## python3.3
##             self.service = http.server.HTTPServer(
##                 ('', port), CGIHTTPRequestHandler)
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

        # region protected properties

    '''
        Points to location which is authoritative to be reachable from
        requested destination.
    '''
    _authentication_location = None

        # endregion

    # endregion

    # region dynamic methods

        # region public methods

            # region special methods

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
        self.request_uri = ''
        self.parameter = ''
        self.post_dictionary = {}
        self.requested_file_name = ''
        self.requested_file = None
        self.load_module = False
        self.request_arguments = []
        self.respond = False
## python3.3
##         builtins.super(http.server.CGIHTTPRequestHandler, self).__init__(
##             *arguments, **keywords)
        CGIHTTPServer.CGIHTTPRequestHandler.__init__(
            self, *arguments, **keywords)
##

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
## python3.3             return urllib.parse.urlparse(url), get
            return urlparse.urlparse(url), get
        return None, {}

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
        try:
            self.requested_file = boostNode.extension.file.Handler(
                location=self.server.web.root.path + self.path,
                must_exist=False)
            self._authentication_location = self.server.web.root
            if self.requested_file:
                self._authentication_location = self.requested_file
                if self.requested_file.is_file():
                    self._authentication_location =\
                        boostNode.extension.file.Handler(
                            location=self.requested_file.directory_path)
            if self._is_authenticated():
                if self._is_valid_request():
                    if self._create_environment_variables():
                        if self._is_valid_reference():
                            return self._set_dynamic_or_static_get(
                                file_name=self.path)
                    elif self._default_get():
                        return self
                return self._send_no_file_error()
            return self._send_no_authentication_error()
## python3.3
##         except (
##             builtins.BrokenPipeError, socket.gaierror, socket.herror,
##             socket.timeout
##         ) as exception:
        except (
            socket.herror, socket.gaierror, socket.timeout
        ) as exception:
##
            __logger__.info(
                'Connection interrupted. %s: %s', exception.__class__.__name__,
                builtins.str(exception))
        return self

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
## python3.3             self.flush_headers()
            self.end_headers()
            self.post_dictionary = self._determine_post_dictionary()
        elif data_type == 'application/x-www-form-urlencoded':
## python3.3
##             self.post_dictionary = urllib.parse.parse_qs(self.rfile.read(
##                 builtins.int(self.headers['content-length'])
##             ).decode('utf-8'))
            self.post_dictionary = cgi.parse_qs(
                self.rfile.read(builtins.int(self.headers.getheader(
                    'content-length'))),
                keep_blank_values=True)
##
            for name, value in self.post_dictionary.items():
                if builtins.isinstance(value, builtins.bytes):
                    self.post_dictionary[name] = {'content': value}
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
        error_message = 'See exception detail.'
        if message_or_error_code == 500:
            response_code_or_message = error_message
        elif response_code_or_message == 500:
            message_or_error_code = error_message
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
##     def _is_authenticated(
##         self: boostNode.extension.type.Self
##     ) -> builtins.bool:
    def _is_authenticated(self):
##
        '''
            Determines wheater current request is authenticated.
        '''
        if self.server.web.authentication:
            while True:
                file_path = self._authentication_location.path +\
                    self.server.web.authentication_file_name
                authentication_file = boostNode.extension.file.Handler(
                    location=file_path, must_exist=False)
                if authentication_file:
##                     return (self.headers.getheader('Authorization') ==
##                             'Basic %s' % self._get_login_data(
##                                 authentication_file))
                    return (self.headers['Authorization'] ==
                            'Basic %s' % self._get_login_data(
                                authentication_file))
##
                if self._authentication_location != self.server.web.root:
                    break
                self._authentication_location =\
                    boostNode.extension.file.Handler(
                        location=self._authentication_location.directory_path)
            return builtins.bool(
                self.server.web.authentication_handler is None or
                self.server.web.authentication_handler(
                    self.headers['Authorization'], self.path))
        return True

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
        patterns = self.server.web.dynamic_mimetype_pattern +\
            self.server.web.static_mimetype_pattern
        if not self.requested_file:
            if(boostNode.extension.native.Module.get_file_path(
               context_path=self.path)):
                self.load_module = True
                return True
        elif((not self.requested_file.is_file() or
              self.requested_file.name !=
              self.server.web.authentication_file_name) and
             self._check_pattern(
                 patterns=patterns, subject=self.requested_file.mimetype)):
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
            self.server.web.dynamic_mimetype_pattern,
            boostNode.extension.file.Handler(
                location=self.server.web.root.path + self.requested_file_name
            ).mimetype))

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
            'Use authentication file "%s".', authentication_file.path)
        match = re.compile(
            self.server.web.authentication_file_pattern
        ).match(authentication_file.content.strip())
## python3.3
##         return base64.b64encode(('%s:%s' % (
##             match.group('name'), match.group('password')
##         )).encode('utf-8')).decode()
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
            Determines the post values given by an html form.
            File uploads are includes as bytes.
        '''
## python3.3
##         form = cgi.FieldStorage(
##             fp=self.rfile, headers=self.headers, keep_blank_values=True,
##             strict_parsing=True,
##             environ=self._determine_environement_variables(),
##             encoding='utf-8')
        form = cgi.FieldStorage(
            fp=self.rfile, headers=self.headers, keep_blank_values=True,
            strict_parsing=True,
            environ=self._determine_environement_variables())
##
        post_dictionary = {}
        for name in form:
            post_dictionary[name] = []
            index = 0
            for value in form.getlist(name):
                if builtins.isinstance(value, builtins.bytes):
                    # NOTE: This definition handles a cgi module bug.
                    value_reference = form[name]
                    if builtins.isinstance(form[name], builtins.list):
                        value_reference = form[name][index]
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
##     def _determine_environement_variables(
##         self: boostNode.extension.type.Self
##     ) -> os._Environ:
    def _determine_environement_variables(self):
##
        '''
            Determines all needed envirnoment variables needed to determine
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
        if 'content-type' in self.headers:
            variables['CONTENT_TYPE'] = self.headers['content-type']
        if self.headers.get('content-length'):
            variables['CONTENT_LENGTH'] = self.headers.get(
                'content-length')
        if self.headers.get('referer'):
            variables['HTTP_REFERER'] = self.headers.get('referer')
        if self.headers.get('user-agent'):
            variables['HTTP_USER_AGENT'] = self.headers.get('user-agent')
## python3.3
##         cookie_content = ', '.join(builtins.filter(
##             None, self.headers.get_all('cookie', [])))
##         if cookie_content:
##             variables['HTTP_COOKIE'] = cookie_content
        pass
##
        return variables

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _send_positive_header(
##         self: boostNode.extension.type.Self, mimetype: builtins.str
##     ) -> boostNode.extension.type.Self:
    def _send_positive_header(self, mimetype):
##
        '''
            This method is called for each successful answered http-request.
        '''
        self.send_response(200)
        self.send_header('Content-type', mimetype)
        self.end_headers()
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _send_no_authentication_error(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def _send_no_authentication_error(self):
##
        '''
            This method is called if authentication has failt.
        '''
        self.send_response(401)
        message = 'You request a potected location'
## python3.3
##         if self.headers['Authorization']:
        if self.headers.getheader('Authorization'):
##
            message = 'The authentication failed'
        self.send_header('WWW-Authenticate', 'Basic realm=\"%s\"' % message)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
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
        error_message = 'Requested file not found'
        if __logger__.isEnabledFor(logging.DEBUG) or sys.flags.debug:
            error_message = (
                'None of the following default file-pattern "%s" was found' %
                '", "'.join(self.server.web.default_module_name_pattern))
            if self.path:
                error_message = (
                    'No accessible file "%s" found' %
                    boostNode.extension.file.Handler(
                        location=self.server.web.root.path + self.path,
                        must_exist=False
                    ).path)
            if self.requested_file:
                error_message +=\
                    '. Detected mime-type "%s"' % self.requested_file.mimetype
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
##         self: boostNode.extension.type.Self, file_name: builtins.str
##     ) -> boostNode.extension.type.Self:
    def _set_dynamic_or_static_get(self, file_name):
##
        '''
            Makes a dynamic or static respond depending on incoming
            request.
        '''
        self.requested_file_name = file_name
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
                    return self._set_dynamic_or_static_get(file_name=file.name)
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
        elif(boostNode.extension.native.Module.get_file_path(
             context_path=module_name)):
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
        '''
            Handles request with no explicit file or module to run.
        '''
        if(self.server.web.default == '__main__' or
           boostNode.extension.native.Module.get_file_path(
               context_path=self.server.web.default)):
            self.load_module = True
        return self._set_dynamic_or_static_get(
            file_name=self.server.web.default)

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
        try:
            with builtins.open(self.requested_file._path, mode='rb') as file:
                file_content = file.read()
        except socket.error as exception:
            if sys.flags.debug or __logger__.isEnabledFor(logging.DEBUG):
                self.send_error(500, '%s: %s' % (
                    exception.__class__.__name__,
                    re.compile('\n+').sub('\n', builtins.str(exception))))
                raise
            else:
                self._send_no_file_error()
        else:
            self._send_positive_header(mimetype=self.requested_file.mimetype)
            self.wfile.write(file_content)
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
        self.request_arguments = [
            self.requested_file_name, self.request_uri,
            self.__class__.parse_url(self.request_uri)[1],
            self.post_dictionary, self.server]
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
        self.request_arguments[0] = self.server.web.root.path +\
            self.request_arguments[0]
        self.request_arguments = builtins.list(builtins.map(
            lambda element: builtins.str(element), self.request_arguments))
        output, errors = subprocess.Popen(
            self.request_arguments, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        ).communicate()
        errors = errors.decode()
        if self.respond:
            if errors:
                program_description = ''
                if sys.flags.debug or __logger__.isEnabledFor(logging.DEBUG):
                    program_description = ' "%s"' % self.request_arguments[0]
                self.send_error(
                    500, 'Internal server error with cgi program%s: "%s"' %
                    (program_description, re.compile('\n+').sub('\n', errors)))
            else:
                self._send_positive_header(
                    mimetype=self.requested_file.mimetype)
                self.wfile.write(output)
        if errors:
            __logger__.critical(
                'Error in cgi program "%s": %s', self.request_arguments[0],
                errors)
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
        sys.path = [self.server.web.root.path] + sys.path
        requested_module = builtins.__import__(self.request_arguments[0])
        '''Extend requested scope with request dependent globals.'''
        requested_module.__requested_arguments__ = self.request_arguments
        sys.path = sys_path_save
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
            self._handle_module_exception()
        else:
            if self.respond:
                self._send_positive_header(
                    mimetype=self.requested_file.mimetype)
        finally:
            if self.respond:
                if self.server.web.lock.acquire():
                    self.wfile.write(
                        self.server.web.thread_buffer.clear().encode())
                self.server.web.lock.release()
            boostNode.extension.output.Print.default_buffer =\
                print_default_buffer_save
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _handle_module_exception(
##         self: boostNode.extension.types.Self, exception: builtins.Exception
##     ) -> boostNode.extension.type.Self:
    def _handle_module_exception(self, exception):
##
        '''
            This method handles each exception raised by running a module
            which was requested by client.
        '''
        if self.respond:
            if(sys.flags.debug or
                __logger__.isEnabledFor(logging.DEBUG)):
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

boostNode.extension.native.Module.default(
    name=__name__, frame=inspect.currentframe(), default_caller=Web.__name__)

# endregion
