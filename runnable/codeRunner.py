#!/usr/bin/env python3.3
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

## python2.7
## import __builtin__ as builtins
import builtins
import collections
##
import copy
import inspect
import logging
import os
import sys

'''Make boostNode packages and modules importable via relative paths.'''
for number in (3, 4):
    sys.path.append(os.path.abspath(sys.path[0] + number * ('..' + os.sep)))

from boostNode.extension.file import Handler as FileHandler
from boostNode.extension.native import Module
from boostNode.extension.output import Logger, Print
from boostNode.extension.system import CommandLine, Platform, Runnable
## python2.7 pass
from boostNode.extension.type import Self
from boostNode.paradigm.aspectOrientation import JointPoint
from boostNode.paradigm.objectOrientation import Class
from boostNode.runnable.template import Parser as TemplateParser

# endregion


# region classes

class Run(Class, Runnable):
    '''
        This class provides a large number of supported programming languages
        support for compiling, running and cleaning after running.
    '''

    # region properties

    '''Holds all command line interface argument informations.'''
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
                'run': '"<%code_file.path%>" <%arguments%>'
            },
            'extensions': ('bash',)
        },
        'shell': {
            'commands': {
                'run': '"<%code_file.path%>" <%arguments%>'
            },
            'extensions': ('sh', 'shell')
        },
        'python': {
            'commands': {
                'run': '"<%code_file.path%>" <%arguments%>'
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
                    Platform.UNIX_OPEN_APPLICATIONS)
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
                'run': 'java "<%code_file.basename%>" <%arguments%>'
            },
            'extensions': ('java',),
            'delete_patterns': ('.*\.class$',)
        }
    }

    # endregion

    # region dynamic methods

        # region public

            # region special

    @JointPoint
## python2.7     def __repr__(self):
    def __repr__(self: Self) -> builtins.str:
        '''
            Invokes if this object should describe itself by a string.

            Examples:

            >>> file = FileHandler(
            ...     __test_folder_path__ + '__repr__.py', must_exist=False)
            >>> file.content = '#!/usr/bin/env python'
            >>> repr(Run(code_file_path=file)) # doctest: +ELLIPSIS
            'Object of "Run" with detected path "...__repr__.py".'
        '''
        return 'Object of "{class_name}" with detected path '\
               '"{path}".'.format(
                   class_name=self.__class__.__name__,
                   path=self._code_file.path)

            # endregion

        # endregion

        # region protected

            # region runnable implementation

    @JointPoint
## python2.7     def _run(self):
    def _run(self: Self) -> Self:
        '''
            Entry point for command line call of this program.
            Determines a meaningful file for running. Set the right code
            dependent commands and finally executes them.

            Examples:

            >>> sys_argv_backup = sys.argv

            >>> sys.argv[1:] = ['--runner-meta-help', '--log-level', 'info']
            >>> run = Run.run() # doctest: +ELLIPSIS
            usage:...

            >>> empty_folder = FileHandler(
            ...     __test_folder_path__ + '_run', make_directory=True)
            >>> sys.argv[1:] = ['-f', empty_folder.path, '--log-level', 'info']
            >>> run = Run.run() # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            CodeRunnerError: No supported file path found for running.

            >>> sys.argv = sys_argv_backup
        '''
        command_line_arguments = CommandLine.argument_parser(
            meta=True, arguments=self.COMMAND_LINE_ARGUMENTS,
            module_name=__name__, scope={'self': self})
        if command_line_arguments.meta_help:
            CommandLine.current_argument_parser.print_help()
            return self
        return self._initialize(**self._command_line_arguments_to_dictionary(
            namespace=command_line_arguments))

    @JointPoint
## python2.7
##     def _initialize(
##         self, code_file_path=None,
##         default_command_sequence=('compile', 'run', 'clean'), **keywords
##     ):
    def _initialize(
        self: Self, code_file_path=None,
        default_command_sequence=('compile', 'run', 'clean'), **keywords
    ) -> Self:
##
        '''
            Determines a code file to run and runs them in its own thread by
            piping all outputs through the command line interface.
        '''

                # region properties

        '''
            Holds the current code file and there potentially presented code
            manager as file handler.
        '''
        self.code_manager_file = None
        '''
            Saves every properties for current code taken from
            "SUPPORTED_CODES".
        '''
        self._current_code = {}
        '''Saves currently needed commands taken from "_current_code".'''
        self._current_commands = ()
        '''
            Saves given arguments which should be piped through the run command
            to determined code file.
        '''
        self._command_line_arguments = ()
        '''Saves a default order of steps to deal with a code file.'''
        self._default_command_sequence = default_command_sequence
        '''Saves currently determined runnable code file object.'''
        self._code_file = self._determine_code_file(code_file_path)

                # endregion

        if not self._code_file:
            raise __exception__(
                'No supported file found for running with given hint "%s".',
                code_file_path)
        return self._run_code_file()

            # endregion

    @JointPoint
## python2.7     def _tidy_up(self):
    def _tidy_up(self: Self) -> Self:
        '''
            Tidies up the current working directory after running the given
            file.

            Examples:

            >>> garbage = FileHandler(
            ...     __test_folder_path__ + 'temp_tidy_up', make_directory=True)
            >>> file = FileHandler(
            ...     __test_folder_path__ + '_tidy_up_runnable.py',
            ...     must_exist=False)
            >>> file.content = '#!/usr/bin/env python'
            >>> run = Run(file)
            >>> run # doctest: +ELLIPSIS
            Object of "Run" with detected path "..._tidy_up_runnable.py".

            >>> run._tidy_up() # doctest: +ELLIPSIS
            Object of "Run" with detected path "..._tidy_up_runnable.py".
            >>> garbage.is_element()
            False

            >>> del run._current_code['properties']['delete_patterns']
            >>> run._tidy_up() # doctest: +ELLIPSIS
            Object of "Run" with detected path "..._tidy_up_runnable.py".
        '''
        if 'delete_patterns' in self._current_code['properties']:
            __logger__.info(
                'Delete files which matches one of "%s" pattern.',
                '", "'.join(
                    self._current_code['properties']['delete_patterns']))
            FileHandler(
                location=self._code_file.directory_path
            ).delete_file_patterns(
                *self._current_code['properties']['delete_patterns'])
        return self

    @JointPoint
## python2.7     def _run_commands(self):
    def _run_commands(self: Self) -> Self:
        '''
            Run currently needed commands.

            Examples:

            >>> __test_buffer__.clear() # doctest: +ELLIPSIS
            '...'
            >>> FileHandler(__test_folder_path__).clear_directory()
            True

            >>> file = FileHandler(
            ...     __test_folder_path__ + '_run_commands.py',
            ...     must_exist=False)
            >>> file.content = '#!/usr/bin/env python'
            >>> file.change_right(700) # doctest: +ELLIPSIS
            Object of "Handler" with path "..._run_commands.py" and initiall...
            >>> Run(
            ...     code_file_path=file
            ... )._run_commands() # doctest: +ELLIPSIS
            Object of "Run" with detected path "..._run_commands.py...".

            >>> __test_buffer__.content # doctest: +ELLIPSIS
            '...Detected "python"...No "compile" necessary...'
        '''
        for command_name in self._default_command_sequence:
            if command_name in self._current_commands:
                self._run_command(
                    command_name, command=self._current_commands[command_name])
            else:
                __logger__.info('No "%s" necessary.', command_name)
        return self

    @JointPoint
## python2.7     def _check_code_manager(self):
    def _check_code_manager(self: Self) -> Self:
        '''
            Checks if a code manager file exists for the current detected code
            file. For example it can find a makefile for a detected c++ source
            code.

            Examples:

            >>> file = FileHandler(
            ...     __test_folder_path__ + '_check_code_manager.py',
            ...     must_exist=False)
            >>> file.content = '#!/usr/bin/env python'
            >>> FileHandler(
            ...     __test_folder_path__ + '__init__.py', must_exist=False
            ... ).content = '#!/usr/bin/env python'
            >>> run = Run(code_file_path=file)
            >>> __test_buffer__.clear() # doctest: +ELLIPSIS
            '...'

            >>> run._check_code_manager() # doctest: +ELLIPSIS
            Object of "Run" with detected path "..._check_code_manager.py".
            >>> __test_buffer__.content # doctest: +ELLIPSIS
            '...Detected code manager "...__init__.py".\\n'

            >>> del run._current_code['properties']['code_manager']
            >>> run._check_code_manager() # doctest: +ELLIPSIS
            Object of "Run" ...
        '''
        if 'code_manager' in self._current_code['properties']:
            file_path = self\
                ._current_code['properties']['code_manager']['file_path']
            self.code_manager_file = FileHandler(
                location=self._code_file.directory_path + file_path,
                must_exist=False)
            if self.code_manager_file:
                self._current_commands.update(
                    self._current_code['properties']['code_manager'][
                        'commands'])
                __logger__.info(
                    'Detected code manager "%s".', self.code_manager_file.path)
        return self

    @JointPoint
## python2.7
##     def _determine_code_file(self, path):
    def _determine_code_file(
        self: Self, path: (builtins.str, builtins.type(None), FileHandler)
    ) -> (FileHandler, builtins.bool):
##
        '''
            Determines a code file which could make sense to run.
            It could depend on inputs which where made to this class.
            Searches in the current working directory.

            Examples:

            >>> run = Run()

            >>> run._determine_code_file(path='') # doctest: +ELLIPSIS
            Object of "Handler" with path "..." (type: file).

            >>> run._command_line_arguments = ['--help']
            >>> run._determine_code_file('not_existing')
            False

            >>> run._command_line_arguments = ['--help']
            >>> run._determine_code_file('') # doctest: +ELLIPSIS
            Object of "Handler" with path "..." and initially given path "...
        '''
        if path:
            if not self._command_line_arguments:
                self._command_line_arguments = sys.argv[2:]
            code_file = FileHandler(location=path, must_exist=False)
            if not (code_file.is_file() and
                    self._find_informations_by_extension(
                        extension=code_file.extension, code_file=code_file)):
                return self._search_supported_file_by_path(
                    path=code_file.path)
            return code_file
        if not self._command_line_arguments:
            self._command_line_arguments = sys.argv[1:]
        return self._search_supported_file_in_current_working_directory()

    @JointPoint
## python2.7
##     def _find_informations_by_extension(self, extension, code_file):
    def _find_informations_by_extension(
        self: Self, extension: builtins.str, code_file: FileHandler
    ) -> (builtins.dict, builtins.bool):
##
        '''
            Tries to find the necessary informations for running code with
            given extension.

            Examples:

            >>> code_file = FileHandler(
            ...     __test_folder_path__ +
            ...     '_find_informations_by_extension.py',
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

    @JointPoint
## python2.7
##     def _search_supported_file_by_path(self, path):
    def _search_supported_file_by_path(
        self: Self, path: builtins.str
    ) -> (FileHandler, builtins.bool):
##
        '''
            Tries to find a useful file in current working directory by trying
            to match one file with given path name and supported extension.

            Examples:

            >>> file = FileHandler(
            ...     __test_folder_path__ + '_search_supported_file_by_path.py',
            ...     must_exist=False)
            >>> file.content = '#!/usr/bin/env python'
            >>> Run()._search_supported_file_by_path(
            ...     path=file.directory_path + file.basename
            ... ) # doctest: +ELLIPSIS
            Object of "Handler" with pat..._search_supported_file_by_path.py...

            >>> Run()._search_supported_file_by_path(
            ...     path='') # doctest: +ELLIPSIS
            Object of "Handler" with path "..." (type: file).

            >>> Run()._search_supported_file_by_path('not_exists')
            False
        '''
        self_file = FileHandler(
            location=inspect.currentframe().f_code.co_filename,
            respect_root_path=False)
        location = FileHandler(location=path, must_exist=False)
        for name, properties in self.SUPPORTED_CODES.items():
            for extension in properties['extensions']:
                for code_file in (FileHandler(
                        location=location.path + '.' + extension,
                        must_exist=False),
                    FileHandler(
                        location=location.path + extension, must_exist=False)):
## python2.7
##                     if code_file.is_file() and not (code_file == self_file):
                    if code_file.is_file() and code_file != self_file:
##
                        return code_file
                file = self._search_supported_file_by_directory(
                    location, extension)
                if file:
                    return file
        return False

    @JointPoint
## python2.7
##     def _search_supported_file_by_directory(self, location, extension):
    def _search_supported_file_by_directory(
        self: Self, location: FileHandler, extension: builtins.str,
    ) -> (FileHandler, builtins.bool):
##
        '''
            Searches in a directory for a suitable code file to run.

            Examples:

            >>> FileHandler(
            ...     __test_folder_path__ +
            ...     '_search_supported_file_by_directoryMain.py',
            ...     must_exist=False
            ... ).content = ' '
            >>> Run()._search_supported_file_by_directory(
            ...     FileHandler(__test_folder_path__), 'py'
            ... ) # doctest: +ELLIPSIS
            Object of "Handler" with path "..." and initially given path "...
        '''
        if location.is_directory():
            found_file = False
            for file in location:
                if file.is_file() and file.extension == extension:
                    if file.basename.lower().endswith('main'):
                        return file
                    found_file = file
            if found_file:
                return found_file
        return False

    @JointPoint
## python2.7
##     def _search_supported_file_in_current_working_directory(self):
    def _search_supported_file_in_current_working_directory(
        self: Self
    ) -> (FileHandler, builtins.bool):
##
        '''
            Tries to find a useful file in current working directory
            with a supported extension.

            Examples:

            >>> run = Run()
            >>> supported_codes_backup = copy.copy(run.SUPPORTED_CODES)

            >>> run._search_supported_file_in_current_working_directory(
            ...     ) # doctest: +ELLIPSIS
            Object of "Handler" with path "..." (type: file).

            >>> run.SUPPORTED_CODES = {}
            >>> run._search_supported_file_in_current_working_directory()
            False

            >>> run.SUPPORTED_CODES = supported_codes_backup
        '''
        for name, properties in self.SUPPORTED_CODES.items():
            for extension in properties['extensions']:
                file = self._search_supported_file_by_directory(
                    location=FileHandler(), extension=extension)
                '''NOTE: We should return positive results only.'''
                if file:
                    return file
        return False

    @JointPoint
## python2.7
##     def _run_command(self, command_name, command):
    def _run_command(
        self: Self, command_name: builtins.str, command: builtins.str
    ) -> Self:
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
            result=Platform.run(
                command=command.strip(), shell=True, error=False))
        if return_code != 0 and not __test_mode__:
            sys.exit(return_code)
        return self

    @JointPoint
## python2.7
##     def _log_command_run(self, command_name, command, result):
    def _log_command_run(
        self: Self, command_name: builtins.str, command: builtins.str,
        result: builtins.dict
    ) -> builtins.int:
##
        '''
            Generates logging output for wrapping around generated output by
            running code file.

            Examples:

            >>> log_level_backup = Logger.default_level
            >>> Logger.change_all(level=('error',))
            <class 'boostNode.extension.output.Logger'>

            >>> Run()._log_command_run(
            ...     'test', 'test', {
            ...         'error_output': '', 'standard_output': '',
            ...         'return_code': 0})
            0

            >>> Logger.change_all(level=log_level_backup)
            <class 'boostNode.extension.output.Logger'>
        '''
        terminator_save = Logger.terminator
        Logger.change_all(terminator=('',))
## python2.7
##         if __logger__.isEnabledFor(logging.INFO):
##             Print(
##                 '%s with "%s".\nstandard output:\n[' %
##                 (command_name.capitalize(), command.strip()),
##                 end='', flush=True)
        __logger__.info(
            '%s with "%s".\nstandard output:\n[',
            command_name.capitalize(), command.strip())
        Logger.flush()
##
        Print(result['standard_output'], end='', flush=True)
## python2.7
##         if __logger__.isEnabledFor(logging.INFO):
##             Print(']\nerror output:\n[', end='', flush=True)
        __logger__.info(']\nerror output:\n[')
        Logger.flush()
##
        Logger.change_all(terminator=terminator_save)
        Print(result['error_output'], end='')
        if __logger__.isEnabledFor(logging.INFO):
            Print(']', flush=True)
        __logger__.info('Return code: "%d".', result['return_code'])
        return result['return_code']

    @JointPoint
## python2.7     def _run_code_file(self):
    def _run_code_file(self: Self) -> Self:
        '''Runs all commands needed to run the current type of code.'''
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

    @JointPoint
## python2.7
##     def _render_properties(self, properties, code_file):
    def _render_properties(
        self: Self, properties: builtins.dict, code_file: FileHandler
    ) -> builtins.dict:
##
        '''
            If a given code property is marked as executable respectively
            dynamic it's value will be determined.

            Examples:

            >>> code_file = FileHandler(
            ...     location=__test_folder_path__ + '_render_properties.cpp',
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
                rendered_properties[key] = TemplateParser(
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
__logger__ = __exception__ = __module_name__ = __file_path__ = \
    __test_mode__ = None
'''
    Extends this module with some magic environment variables to provide better
    introspection support. A generic command line interface for some code
    preprocessing tools is provided by default.
'''
Module.default(name=__name__, frame=inspect.currentframe())

# endregion
