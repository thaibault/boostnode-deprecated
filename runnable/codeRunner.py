#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# region vim modline

# vim: set tabstop=4 shiftwidth=4 expandtab:
# vim: foldmethod=marker foldmarker=region,endregion:

# endregion

# region header

'''
    This module provides an easy way to compile, run and clean up a various
    number of scripts.
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

## python3.3
## import builtins
## import collections
import __builtin__ as builtins
##
import copy
import inspect
import logging
import os
import sys

for number in (3, 4):
    sys.path.append(os.path.abspath(sys.path[0] + number * ('..' + os.sep)))

import boostNode.extension.file
import boostNode.extension.native
import boostNode.extension.output
import boostNode.extension.type
import boostNode.paradigm.aspectOrientation
import boostNode.paradigm.objectOrientation
import boostNode.runnable.template

# endregion


# region classes

class Run(
    boostNode.paradigm.objectOrientation.Class,
    boostNode.extension.system.Runnable
):
    '''
        This class provides a large number of supported programming languages
        support for compiling, running and cleaning after running.
    '''

    # region constant properties

        # region public

    '''
        Holds all command line interface argument informations.
    '''
    COMMAND_LINE_ARGUMENTS = (
        {'arguments': ('-f', '--code-file'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Select a file for running.',
             'dest': 'code_file_path',
             'metavar': 'FILE_PATH'}},
        {'arguments': ('-d', '--default-command-sequence'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Select a default sequence of things to do with code '
                     'files.',
             'dest': 'default_command_sequence',
             'metavar': 'COMMAND'}},
        {'arguments': ('-n', '--runner-meta-help'),
         'keywords': {
             'action': 'store_true',
             'default': False,
             'help': 'Shows this help message.',
             'dest': 'meta_help'}})
    '''Holds all supported code types and there methods to do common stuff.'''
    SUPPORTED_CODES = {
        'template': {
            'commands': {
                'compile': "bash --login -c '"
                           'template "<%code_file.path%>" 1>'
                           '"<%code_file.directory_path%>'
                           '<%code_file.basename%>.html"\'',
                'run': 'bash --login -c \'webbrowser '
                       '"<%code_file.directory_path%>'
                       '<%code_file.basename%>.html"\''
            },
            'extensions': ('tpl',)
        },
        'c': {
            'commands': {
                'compile': 'g++ "<%code_file.path%>" -o '
                           '"<%code_file.directory_path%>'
                           '<%code_file.basename%>"',
                'run': '"<%code_file.directory_path%><%code_file.basename%>" '
                       '<%arguments%>',
            },
            'code_manager': {
                'file_path': 'Makefile',
                'commands': {
                    'compile': 'make compile',
                    'test': 'make test',
                    'clean': 'make clean',
                    'all': 'make all'
                }
            },
            'extensions': ('cpp', 'c', 'cc'),
            'delete_patterns': ('.*\.o$', '.*Main$', '.*Test$')
        },
        'bash': {
            'commands': {
                'run': '"<%code_file.path%>" <%arguments%>',
            },
            'extensions': ('bash',)
        },
        'shell': {
            'commands': {
                'run': '"<%code_file.path%>" <%arguments%>',
            },
            'extensions': ('sh', 'shell')
        },
        'python': {
            'commands': {
                'run': '"<%code_file.path%>" <%arguments%>',
            },
            'code_manager': {
                'file_path': '__init__.<%code_file.extension%>',
                'commands': {
                    'clean': '__init__.<%code_file.extension%> clear',
                    'test': '__init__.<%code_file.extension%> test',
                    'all': '__init__.<%code_file.extension%> all'
                }
            },
            'extensions': ('py', 'pyc', 'pyw'),
            'delete_patterns': (
                '.*\.py[cod]$', '^__pycache__$', '^temp_\.*')
        },
        'laTeX': {
            'commands': {
                'compile': 'pdflatex "<%code_file.path%>" && '
                           'bibtex "<%code_file.directory_path%>'
                           '<%code_file.basename%>.aux"; '
                           'pdflatex "<%code_file.path%>" && '
                           'pdflatex "<%code_file.path%>"',
                'run': ' || '.join(builtins.map(
                    lambda name: name + ' "<%code_file.basename%>.pdf"',
                    boostNode.extension.system.Platform.UNIX_OPEN_APPLICATIONS)
                )
            },
            'code_manager': {
                'file_path': 'Makefile',
                'commands': {
                    'compile': 'make compile',
                    'run': 'make preview',
                    'clean': 'make clean',
                    'all': 'make all'
                }
            },
            'extensions': ('tex',),
            'delete_patterns': (
                '^.+\.aux$', '^.+\.log$', '^.+\.toc$', '^.+\.out$',
                '^.+\.blg$', '^.+\.bbl$', '^.+\.lol$')
        },
        'java': {
            'commands': {
                'compile': 'javac "<%code_file.path%>"',
                'run': 'java "<%code_file.basename%>" <%arguments%>',
            },
            'extensions': ('java',),
            'delete_patterns': ('.*\.class$',)
        }
    }

        # endregion

    # endregion

    # region dynamic properties

        # region public

    '''
        Holds the current code file and there potentially presented code
        manager as file handler.
    '''
    code_manager_file = None

        # endregion

        # region protected

    '''
        Saves every properties for current code taken from
        "SUPPORTED_CODES".
    '''
    _current_code = {}
    '''Saves currently needed commands taken from "_current_code".'''
    _current_commands = ()
    '''
        Saves given arguments which should be piped through the run command to
        determined code file.
    '''
    _command_line_arguments = ()
    '''Saves a default order of steps to deal with a code file.'''
    _default_command_sequence = ()
    '''Saves currently determined runnable code file object.'''
    _code_file = None

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

            >>> boostNode.extension.file.Handler(
            ...     __test_folder__ + '__repr__.py', must_exist=False
            ... ).content = '#!/usr/bin/env python'
            >>> repr(Run(
            ...     code_file_path=__test_folder__ + '__repr__.py')
            ... ) # doctest: +ELLIPSIS
            'Object of "Run" with detected path "...__repr__.py".'
        '''
        if self._code_file:
            return 'Object of "{class_name}" with detected path '\
                   '"{path}".'.format(
                       class_name=self.__class__.__name__,
                       path=self._code_file.path)
        return 'Object of "{class_name}" with no detected path.'.format(
            class_name=self.__class__.__name__)

            # endregion

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
            Entry point for command line call of this progam.
            Determines a meaningful file for running. Set the right code
            dependent commands and finnally executes them.

            Examples:

            >>> boostNode.extension.file.Handler(
            ...     location=__test_folder__ + '_run', make_directory=True
            ... ) # doctest: +ELLIPSIS
            Object of "Handler" with path "..._run..." (directory).
            >>> Run(
            ...     code_file_path=__test_folder__ + '_run/'
            ... ) # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            CodeRunnerError: No supported file path found for running.
        '''
        command_line_arguments = boostNode.extension.system.CommandLine\
            .argument_parser(
                meta=True, arguments=self.COMMAND_LINE_ARGUMENTS,
                module_name=__name__, scope={'self': self})
        if command_line_arguments.meta_help:
            boostNode.extension.system.CommandLine\
                .current_argument_parser.print_help()
            return self
        return self._initialize(**self._command_line_arguments_to_dictionary(
            namespace=command_line_arguments))

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _initialize(
##         self: boostNode.extension.type.Self, code_file_path='',
##         default_command_sequence=('compile', 'run', 'clean'), **keywords
##     ) -> boostNode.extension.type.Self:
    def _initialize(
        self, code_file_path='',
        default_command_sequence=('compile', 'run', 'clean'), **keywords
    ):
##
        '''
            Determines a code file to run and runs them in its own thread by
            piping all outputs through the command line interface.
        '''
        self._default_command_sequence = default_command_sequence
        self._code_file = self._determine_code_file(code_file_path)
        return self._run_code_file()

            # endregion

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _tidy_up(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def _tidy_up(self):
##
        '''
            Tidies up the current working directory after running the given
            file.

            Examples:

            >>> garbage = boostNode.extension.file.Handler(
            ...     __test_folder__ + 'temp_tidy_up', make_directory=True)
            >>> boostNode.extension.file.Handler(
            ...     __test_folder__ + '_tidy_up_runnable.py',
            ...     must_exist=False
            ... ).content = '#!/usr/bin/env python'
            >>> runner = Run(__test_folder__ + '_tidy_up_runnable.py')
            >>> runner # doctest: +ELLIPSIS
            Object of "Run" with detected path "..._tidy_up_runnable.py".
            >>> runner._tidy_up() # doctest: +ELLIPSIS
            Object of "Run" with detected path "..._tidy_up_runnable.py".
            >>> garbage.is_element()
            False
        '''
        if 'delete_patterns' in self._current_code['properties']:
            __logger__.info(
                'Delete files which matches one of "%s" pattern.',
                '", "'.join(
                    self._current_code['properties']['delete_patterns']))
            boostNode.extension.file.Handler(
                location=self._code_file.directory_path
            ).delete_file_patterns(
                *self._current_code['properties']['delete_patterns'])
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _run_commands(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def _run_commands(self):
##
        '''
            Run currently needed commands.

            Examples:

            >>> __test_buffer__.clear() # doctest: +ELLIPSIS
            '...'
            >>> boostNode.extension.file.Handler(
            ...     __test_folder__ + '_run_commands.py', must_exist=False
            ... ).content = '#!/usr/bin/env python'
            >>> Run(
            ...     code_file_path=__test_folder__ + '_run_commands.py'
            ... )._run_commands() # doctest: +ELLIPSIS
            Object of "Run" with detected path "..._run_commands.py...".
            >>> __test_buffer__.content # doctest: +ELLIPSIS
            '...Detected "python"...No "compile" necessary...'
        '''
        for command_name in self._default_command_sequence:
            if command_name in self._current_commands:
                if(builtins.isinstance(
                   self._current_commands[command_name], builtins.tuple)):
                    for sub_command in self._current_commands[command_name]:
                        self._run_command(command_name, command=sub_command)
                else:
                    self._run_command(
                        command_name,
                        command=self._current_commands[command_name])
            else:
                __logger__.info('No "%s" necessary.', command_name)
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _check_code_manager(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def _check_code_manager(self):
##
        '''
            Checks if a code manager file exists for the current detected code
            file. For example it can find a makefile for a detected c++ source
            code.

            Examples:

            >>> boostNode.extension.file.Handler(
            ...     __test_folder__ + '_check_code_manager.py',
            ...     must_exist=False
            ... ).content = '#!/usr/bin/env python'
            >>> boostNode.extension.file.Handler(
            ...     __test_folder__ + '__init__.py', must_exist=False
            ... ).content = '#!/usr/bin/env python'

            >>> runner = Run(
            ...     code_file_path=__test_folder__ + '_check_code_manager.py')
            >>> __test_buffer__.clear() # doctest: +ELLIPSIS
            '...'
            >>> runner._check_code_manager() # doctest: +ELLIPSIS
            Object of "Run" with detected path "..._check_code_manager.py".
            >>> __test_buffer__.content # doctest: +ELLIPSIS
            '...Detected code manager "...__init__.py".\\n'
        '''
        if 'code_manager' in self._current_code['properties']:
            file_path = self\
                ._current_code['properties']['code_manager']['file_path']
            self.code_manager_file = boostNode.extension.file.Handler(
                location=self._code_file.directory_path + file_path,
                must_exist=False)
            if self.code_manager_file:
                self._current_commands.update(
                    self._current_code['properties']['code_manager'][
                        'commands'])
                __logger__.info(
                    'Detected code manager "%s".', self.code_manager_file.path)
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _determine_code_file(
##         self: boostNode.extension.type.Self, path: builtins.str
##     ) -> (boostNode.extension.file.Handler, builtins.bool):
    def _determine_code_file(self, path):
##
        '''
            Determines a code file which could make sense to run.
            It could depend on inputs which where made to this class.
            Searches in the current working directory.

            Examples:

            >>> Run()._determine_code_file(path='') # doctest: +ELLIPSIS
            Object of "Handler" with path "..." (file).
        '''
        if path:
            if not self._command_line_arguments:
                self._command_line_arguments = sys.argv[2:]
            code_file = boostNode.extension.file.Handler(
                location=path, must_exist=False)
            if not (code_file.is_file() and
                    self._find_informations_by_extension(
                        extension=code_file.extension, code_file=code_file)):
                return self._search_supported_file_by_path(
                    path=code_file.path)
            return code_file
        if not self._command_line_arguments:
            self._command_line_arguments = sys.argv[1:]
        return self._search_supported_file_in_current_working_directory()

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _find_informations_by_extension(
##         self: boostNode.extension.type.Self, extension: builtins.str,
##         code_file: boostNode.extension.file.Handler
##     ) -> (builtins.dict, builtins.bool):
    def _find_informations_by_extension(self, extension, code_file):
##
        '''
            Tries to find the necessary informations for running code with
            given extension.

            Examples:

            >>> code_file = boostNode.extension.file.Handler(
            ...     __test_folder__ + '_find_informations_by_extension.py',
            ...     must_exist=False)
            >>> Run()._find_informations_by_extension(
            ...     extension='py', code_file=code_file
            ... ) # doctest: +ELLIPSIS
            {...'type': 'python'...}

            >>> Run()._find_informations_by_extension(
            ...     'not_existing', code_file)
            False
        '''
        for name, properties in self.SUPPORTED_CODES.items():
            if extension in properties['extensions']:
                return {
                    'type': name, 'properties': self._render_properties(
                        properties, code_file)}
        return False

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _search_supported_file_by_path(
##         self: boostNode.extension.type.Self, path: builtins.str
##     ) -> (boostNode.extension.file.Handler, builtins.bool):
    def _search_supported_file_by_path(self, path):
##
        '''
            Tries to find a useful file in current working directory by trying
            to match one file with given path name and supported extension.

            Examples:

            >>> file = boostNode.extension.file.Handler(
            ...     __test_folder__ + '_search_supported_file_by_path.py',
            ...     must_exist=False)
            >>> file.content = '#!/usr/bin/env python'
            >>> Run()._search_supported_file_by_path(
            ...     path=file.directory_path + file.basename
            ... ) # doctest: +ELLIPSIS
            Object of "Handler" with pat..._search_supported_file_by_path.py...

            >>> Run()._search_supported_file_by_path(
            ...     path='') # doctest: +ELLIPSIS
            Object of "Handler" with path "..." (file).

            >>> Run()._search_supported_file_by_path('not_exists')
            False
        '''
        self_file = boostNode.extension.file.Handler(
            location=inspect.currentframe().f_code.co_filename,
            respect_root_path=False)
        location = boostNode.extension.file.Handler(
            location=path, must_exist=False)
        for name, properties in self.SUPPORTED_CODES.items():
            for extension in properties['extensions']:
                for code_file in (boostNode.extension.file.Handler(
                        location=location.path + '.' + extension,
                        must_exist=False),
                    boostNode.extension.file.Handler(
                        location=location.path + extension, must_exist=False)):
## python3.3
##                     if code_file.is_file() and code_file != self_file:
                    if code_file.is_file() and not (code_file == self_file):
##
                        return code_file
                file = self._search_supported_file_by_directory(
                    location, extension)
                if file:
                    return file
        return False

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _search_supported_file_by_directory(
##         self: boostNode.extension.type.Self,
##         location: boostNode.extension.file.Handler, extension: builtins.str,
##     ) -> (boostNode.extension.file.Handler, builtins.bool):
    def _search_supported_file_by_directory(self, location, extension):
##
        '''
            Searches in a directory for a suitable code file to run.
        '''
        if location.is_directory():
            found_file = False
            for file in location:
                if file.is_file() and file.extension == extension:
                    if file.basename.endswith('Main'):
                        return file
                    found_file = file
            if found_file:
                return found_file
        return False

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _search_supported_file_in_current_working_directory(
##         self: boostNode.extension.type.Self
##     ) -> (boostNode.extension.file.Handler, builtins.bool):
    def _search_supported_file_in_current_working_directory(self):
##
        '''
            Tries to find a useful file in current working directory
            with a supported extension.

            Examples:

            >>> Run()._search_supported_file_in_current_working_directory(
            ...     ) # doctest: +ELLIPSIS
            Object of "Handler" with path "..." (file).
        '''
        for name, properties in self.SUPPORTED_CODES.items():
            for extension in properties['extensions']:
                file = self._search_supported_file_by_directory(
                    location=boostNode.extension.file.Handler(),
                    extension=extension)
                if file:
                    return file
        return False

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _run_command(
##         self: boostNode.extension.type.Self, command_name: builtins.str,
##         command: builtins.str
##     ) -> boostNode.extension.type.Self:
    def _run_command(self, command_name, command):
##
        '''
            Runs the given command by printing out what is running by
            presenting there results.

            Examples:

            >>> __test_buffer__.clear() # doctest: +ELLIPSIS
            '...'
            >>> Run()._run_command('list', 'ls') # doctest: +SKIP
            Object of "Run" with detected path "...".
            >>> __test_buffer__.content # doctest: +SKIP
            'List with "ls". output [...codeRunner...]'
        '''
        return_code = self._log_command_run(
            command_name, command,
            result=boostNode.extension.system.Platform.run(
                command=command.strip(), shell=True, error=False))
        if return_code != 0 and not __test_mode__:
            sys.exit(return_code)
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _log_command_run(
##         self: boostNode.extension.type.Self, command_name: builtins.str,
##         command: builtins.str, result: builtins.dict
##     ) -> builtins.int:
    def _log_command_run(self, command_name, command, result):
##
        '''
            Generates logging output for wrapping around generated output by
            running code file.
        '''
        terminator_save = boostNode.extension.output.Logger.terminator
        boostNode.extension.output.Logger.change_all(terminator=('',))
## python3.3
##         __logger__.info(
##             '%s with "%s".\nstandard output:\n[',
##             command_name.capitalize(), command.strip())
##         boostNode.extension.output.Logger.flush()
        if __logger__.isEnabledFor(logging.INFO):
            boostNode.extension.output.Print(
                '%s with "%s".\nstandard output:\n[' %
                (command_name.capitalize(), command.strip()),
                end='', flush=True)
##
        boostNode.extension.output.Print(
            result['standard_output'], end='', flush=True)
## python3.3
##         __logger__.info(']\nerror output:\n[')
##         boostNode.extension.output.Logger.flush()
        if __logger__.isEnabledFor(logging.INFO):
            boostNode.extension.output.Print(
                ']\nerror output:\n[', end='', flush=True)
##
        boostNode.extension.output.Logger.change_all(
            terminator=terminator_save)
        boostNode.extension.output.Print(result['error_output'], end='')
        if __logger__.isEnabledFor(logging.INFO):
            boostNode.extension.output.Print(']', flush=True)
        __logger__.info('Return code: "%d".', result['return_code'])
        return result['return_code']

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _run_code_file(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def _run_code_file(self):
##
        '''
            Runs all commands needed to run the current type of code.
        '''
        self._validate_code_file()
        self._current_code = self._find_informations_by_extension(
            extension=self._code_file.extension, code_file=self._code_file)
        self._current_commands = \
            self._current_code['properties']['commands']
        __logger__.info('Detected "%s".', self._current_code['type'])
        self._check_code_manager()
        if not __test_mode__:
            try:
                self._run_commands()
            finally:
                self._tidy_up()
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _validate_code_file(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def _validate_code_file(self):
##
        '''
            Checks weather current code file is supported for running.
        '''
        if not self._code_file:
            raise __exception__(
                'No supported file path found for running.')
        if not self._code_file.is_file():
            raise __exception__(
                'No supported file like "%s" found for running.',
                self._code_file.path)
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _render_properties(
##         self: boostNode.extension.type.Self, properties: builtins.dict,
##         code_file: boostNode.extension.file.Handler
##     ) -> builtins.dict:
    def _render_properties(self, properties, code_file):
##
        '''
            If a given code property is marked as executable respectively
            dynamic it's value will be determined.

            Examples:

            >>> code_file = boostNode.extension.file.Handler(
            ...     location=__test_folder__ + '_render_properties.cpp',
            ...     must_exist=False)

            >>> Run()._render_properties({
            ...     'commands': {
            ...         'compile': 'g++ "<%code_file.path%>"',
            ...         'run': '<%code_file.basename%>',
            ...     },
            ...     'code_manager': {
            ...         'file_path': 'Makefile',
            ...         'commands': {'compile': 'make build'}
            ...     },
            ...     'extensions': ('cpp', 'c')
            ... }, code_file) # doctest: +ELLIPSIS +SKIP
            {'commands': {'compile': 'g++ "...runner.cpp"', 'run': '...}

            >>> Run()._render_properties({'hans': 'peter'}, code_file)
            {'hans': 'peter'}
        '''
        rendered_properties = copy.copy(properties)
        for key, value in rendered_properties.items():
            if builtins.isinstance(value, builtins.dict):
                rendered_properties[key] = self._render_properties(
                    properties=value, code_file=code_file)
            elif builtins.isinstance(value, builtins.str):
                rendered_properties[key] = boostNode.runnable.template.Parser(
                    template=value, string=True
                ).render(
                    code_file=code_file,
                    arguments=' '.join(self._command_line_arguments),
                    path_separator=os.sep
                ).output
        return rendered_properties

        # endregion

    # endregion

# endregion

 # region footer

'''
    Preset some variables given by introspection letting the linter know what
    globale variables are available.
'''
__logger__ = __test_mode__ = __exception__ = __module_name__ = None
'''
    Extends this module with some magic environment variables to provide better
    introspection support. A generic command line interface for some code
    preprocessing tools is provided by default.
'''
boostNode.extension.native.Module.default(
    name=__name__, frame=inspect.currentframe())

# endregion
