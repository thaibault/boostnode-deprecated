#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-

# region header

'''
    This module provides an interpreter to run a simple macro language written
    in text-files.
    Converts special commented version depending code snippets in given
    location to another given version. This code transformation can always be
    made in both directions.
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

## python2.7
## pass
import builtins
import collections
##
import inspect
import os
import re
import sys

## python2.7 builtins = sys.modules['__main__'].__builtins__
pass

sys.path.append(os.path.abspath(sys.path[0] + 3 * ('..' + os.sep)))
sys.path.append(os.path.abspath(sys.path[0] + 4 * ('..' + os.sep)))

import boostNode.extension.file
import boostNode.extension.native
import boostNode.paradigm.aspectOrientation
import boostNode.paradigm.objectOrientation

# endregion


# region classes

class Replace(
    boostNode.paradigm.objectOrientation.Class,
    boostNode.extension.system.Runnable
):
    '''
        Parse source code and replace version depended code snippets with the
        correct given version code snippets.
    '''

    # region constant properties

        # region public properties

    '''Defines options for manipulating the programs default behavior.'''
    COMMAND_LINE_ARGUMENTS = (
        {'arguments': ('-p', '--path'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Defines files to convert. A directory or file path is '
                     'supported.',
             'dest': 'location',
             'metavar': 'PATH'}},
        {'arguments': ('-n', '--new-version'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Defines new version of converted files.',
             'dest': 'new_version',
             'metavar': 'VERSION'}},
        {'arguments': ('-s', '--skip-self-file'),
         'keywords': {
             'action': 'store_true',
             'default': {'execute': '__initializer_default_value__'},
             'help': 'Determines if this file should be ignored for running '
                     'any macros.',
             'dest': 'skip_self_file'}},
        {'arguments': ('-e', '--extension'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'If setted only files with given extension will be '
                     'parsed.',
             'dest': 'extension',
             'metavar': 'FILE_EXTENSION'}},
        {'arguments': ('-a', '--exclude-locations'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': {
                 'execute': "'Select locations which should be ignored. %s "
                            "doesn\\'t touch these files.' "
                            '% module_name.capitalize()'},
             'dest': 'exclude_locations',
             'metavar': 'PATHS'}},
        {'arguments': ('-f', '--first-line-regex-pattern'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Defines line to determine current version of file to '
                     'parse.',
             'dest': 'first_line_regex_pattern',
             'metavar': 'REGEX'}},
        {'arguments': ('-o', '--one-line-regex-pattern'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Defines line to determine current version of file to '
                     'parse.',
             'dest': 'one_line_regex_pattern',
             'metavar': 'REGEX'}},
        {'arguments': ('-r', '--more-line-regex-pattern'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Defines line to determine current version of file to '
                     'parse.',
             'dest': 'more_line_regex_pattern',
             'metavar': 'REGEX'}})

        # endregion

    # endregion

    # region dynamic properties

        # region protected properties

    '''Current location for deep code parsing.'''
    _location = None
    '''Version of the giving source files.'''
    _current_version = ''
    '''Determines if this file should be ignored for running any macros.'''
    _skip_self_file = False
    '''If not empty only files with given extension will be parsed.'''
    _extension = ''
    '''Holds all file system locations to ignore during parsing.'''
    _exclude_locations = []
    '''New version to convert given files to.'''
    _new_version = ''
    '''Defines regex patterns how to determine macro hints in source text.'''
    _first_line_regex_pattern = ''
    _one_line_regex_pattern = ''
    _more_line_regex_pattern = ''

        # endregion

    # endregion

    # region dynamic methods

        # region public methods

            # region special methods

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def __repr__(self):
    def __repr__(self: boostNode.extension.type.Self) -> builtins.str:
##
        '''
            Invokes if this object should describe itself by a string.

            Examples:

            >>> repr(Replace(
            ...     location=__file_path__, new_version='python3.3'
            ... )) # doctest: +ELLIPSIS
            '...Replace...file "...macro.py" to ...to "python3.3".'
        '''
        return 'Object of "{class_name}" with {type} "{path}" to convert to '\
               '"{new_version}".'.format(
                   class_name=self.__class__.__name__,
                   type=self._location.type, path=self._location.path,
                   new_version=self._new_version)

            # endregion

            # region setter methods

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def set_new_version(self, version):
    def set_new_version(
        self: boostNode.extension.type.Self, version: builtins.str
    ) -> builtins.str:
##
        '''
            Checks if an explicit new version was given or a useful should be
            determined.

            Examples:

            >>> macro = Replace(location=__file_path__)
            >>> macro.set_new_version(version='python3.3')
            'python3.3'

            >>> replace = Replace(location=__file_path__)
            >>> replace.new_version = '__determine_useful__'
            >>> replace._new_version # doctest: +ELLIPSIS
            'python...'

            >>> boostNode.extension.file.Handler(
            ...     location=__test_folder__ + 'macro_file', must_exist=False
            ... ).content = ('#!/usr/bin/env version\\n\\n## '
            ...              'alternate_version hans\\npeter\\n')
            >>> replace = Replace(
            ...     location=__test_folder__ + 'macro_file'
            ... )._convert_path()
            >>> replace.new_version = '__determine_useful__'
            >>> replace._new_version
            'version'
        '''
        self._new_version = version
        if version == '__determine_useful__':
            self._new_version = self._determine_useful_version_in_location(
                location=self._location)
            if not self._new_version:
                __logger__.warning('No new version found to convert to.')
        return self._new_version

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def set_exclude_locations(self, paths):
    def set_exclude_locations(
        self: boostNode.extension.type.Self, paths: collections.Iterable
    ) -> builtins.list:
##
        '''
            Converts all paths setted to "_exclude_locations" via string to
            high level file objects.

            Examples:

            >>> replace = Replace(location=__file_path__)

            >>> replace.exclude_locations = [__file_path__]
            >>> replace._exclude_locations # doctest: +ELLIPSIS
            [Object of "Handler" with path "...macro.py" (file).]

            >>> replace.exclude_locations = [
            ...     'A', 'B'] # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            boostNode.extension.native.FileError: Invalid path "...A" for an...
        '''
        self._exclude_locations = []
        for path in paths:
            self._exclude_locations.append(boostNode.extension.file.Handler(
                location=path))
        return self._exclude_locations

            # endregion

        # endregion

        # region protected methods

            # region runnable implementation

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def _run(self):
    def _run(
        self: boostNode.extension.type.Self
    ) -> boostNode.extension.type.Self:
##
        '''
            Entry point for command line call of this progam.
            Validates the given input. Gives usage info or raises exception if
            the given inputs don't make sense.
        '''
        command_line_arguments =\
            boostNode.extension.system.CommandLine.argument_parser(
                arguments=self.COMMAND_LINE_ARGUMENTS,
                module_name=__name__,
                scope={'os': os, 'module_name': __module_name__, 'self': self})
        return self._initialize(**self._command_line_arguments_to_dictionary(
            namespace=command_line_arguments))

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def _initialize(
##         self, location=None, new_version='__determine_useful__',
##         skip_self_file=False, extension='', exclude_locations=(),
##         first_line_regex_pattern='(?P<constant_version_pattern>^#!.*?'
##                                  '(?P<current_version>[a-zA-Z0-9\.]+))\n',
##         one_line_regex_pattern='\n(?P<prefix>##) '
##                                '(?P<alternate_version>[^\n ]+) '
##                                '?(?P<alternate_text>.*)\n'
##                                '(?P<current_text>.*)\n',
##         more_line_regex_pattern='\n(?P<prefix>##) '
##                                 '(?P<alternate_version>[^ ]+)\n'
##                                 '(?P<alternate_text>((## .*?\n)|(##\n))+)'
##                                 '(?P<current_text>.*?\n)##\n',
##         **keywords
##     ):
    def _initialize(
        self: boostNode.extension.type.Self, location=None,
        new_version='__determine_useful__', skip_self_file=False,
        extension='', exclude_locations=(),
        first_line_regex_pattern='(?P<constant_version_pattern>^#!.*?'
                                 '(?P<current_version>[a-zA-Z0-9\.]+))\n',
        one_line_regex_pattern='\n(?P<prefix>##) '
                               '(?P<alternate_version>[^\n ]+) '
                               '?(?P<alternate_text>.*)\n'
                               '(?P<current_text>.*)\n',
        more_line_regex_pattern='\n(?P<prefix>##) '
                                '(?P<alternate_version>[^ ]+)\n'
                                '(?P<alternate_text>((## .*?\n)|(##\n))+)'
                                '(?P<current_text>.*?\n)##\n',
        **keywords: builtins.object
    ) -> boostNode.extension.type.Self:
##
        '''
            Triggers the conversion process with given arguments.

            Examples:

            >>> Replace(
            ...     location='non_existing_file'
            ... ) # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            boostNode.extension.native.FileError: Invalid path "...non_exist...
        '''
        self._location = boostNode.extension.file.Handler(location)
        self._first_line_regex_pattern = first_line_regex_pattern
        self._one_line_regex_pattern = one_line_regex_pattern
        self._more_line_regex_pattern = more_line_regex_pattern
        self._extension = extension
        self._skip_self_file = skip_self_file

        self.exclude_locations = exclude_locations
        self.new_version = new_version
        return self._convert()

            # endregion

            # region boolean methods

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def _in_exclude_locations(self, location):
    def _in_exclude_locations(
        self: boostNode.extension.type.Self,
        location: boostNode.extension.file.Handler
    ) -> builtins.bool:
##
        '''
            Returns "True" if given location is in one of intially defined
            exclude locations.
        '''
        for file in self._exclude_locations:
            if location == file or (file.is_directory() and location in file):
                __logger__.info(
                    'Ignore exclude location "%s".', location.path)
                return True
        return False

            # endregion

            # region core concern methods

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def _determine_useful_version_in_location(self, location):
    def _determine_useful_version_in_location(
        self: boostNode.extension.type.Self,
        location: boostNode.extension.file.Handler
    ) -> builtins.str:
##
        '''
            Determines a useful version for replacing if nothing explicit was
            given.

            Examples:

            >>> boostNode.extension.file.Handler(
            ...     location=__test_folder__ + 'directory/sub',
            ...     must_exist=False
            ... ).make_directorys()
            True
            >>> boostNode.extension.file.Handler(
            ...     location=__test_folder__ + 'directory/sub/file',
            ...     must_exist=False
            ... ).content = 'hans\\n## new_version peter\\nklaus\\n'
            >>> Replace(
            ...     location=__file_path__
            ... )._determine_useful_version_in_location(
            ...     location=boostNode.extension.file.Handler(
            ...         location=__test_folder__ + 'directory'))
            'new_version'
        '''
        if not self._in_exclude_locations(location):
            version = self._determine_useful_version_in_location_helper(
                location)
            if version:
                return version
        if location == self._location:
            __logger__.info('No macros found.')
        return ''

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def _determine_useful_version_in_file(self, file):
    def _determine_useful_version_in_file(
        self: boostNode.extension.type.Self,
        file: boostNode.extension.file.Handler
    ) -> builtins.str:
##
        '''
            Searches for first version replacement in macro language as good
            guess for new version if no new version was defined explicitly.

            Examples:

            >>> boostNode.extension.file.Handler(
            ...     location=__test_folder__ + 'macro', must_exist=False
            ... ).content = 'hans\\n## new_version peter\\nklaus\\n'
            >>> Replace(
            ...     location=__file_path__
            ... )._determine_useful_version_in_file(
            ...     file=boostNode.extension.file.Handler(
            ...         location=__test_folder__ + 'macro'))
            'new_version'
        '''
        try:
            file.content
        except builtins.UnicodeDecodeError:
            return ''
        match = re.compile(
            self._one_line_regex_pattern
        ).search(file.content)
        if match is None:
            match = re.compile(
                self._more_line_regex_pattern
            ).search(file.content)
        if match:
            __logger__.info(
                'Detected "%s" as new version.',
                match.group('alternate_version'))
            return match.group('alternate_version')
        return ''

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def _convert_path(self):
    def _convert_path(
        self: boostNode.extension.type.Self
    ) -> boostNode.extension.type.Self:
##
        '''
            Converts the given path to the specified format.
        '''
        if not self._in_exclude_locations(location=self._location):
            if(self._location.is_file() and
                (not self._extension or
                 self._location.extension == self._extension)
            ):
                self._convert_file(file=self._location)
            elif self._location.is_directory():
                self._convert_directory(directory=self._location)
            else:
                raise __exception__(
                    'Given Path "%s" doesn\'t exists.\n', self._location)
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def _convert_directory(self, directory):
    def _convert_directory(
        self: boostNode.extension.type.Self,
        directory: boostNode.extension.file.Handler
    ) -> boostNode.extension.type.Self:
##
        '''
            Walks through a whole directory and its substructure to convert
            its text based files between different versions of marked
            code-snippets.

            "directory" the directory location with text-files which should
                        be converted.
        '''
        for file in directory:
            __logger__.debug('Check "%s".', file.path)
            if not self._in_exclude_locations(location=file):
                if file.is_file() and (not self._extension or
                                       file.extension == self._extension):
                    self._convert_file(file)
                elif file.is_directory():
                    self._convert_directory(directory=file)
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def _convert_file(self, file):
    def _convert_file(
        self: boostNode.extension.type.Self,
        file: boostNode.extension.file.Handler
    ) -> boostNode.extension.type.Self:
##
        '''
            Opens a given file and parses its content and convert it through
            different versions of code snippets.

            "file" - the file to be converted.

            >>> boostNode.extension.file.Handler(
            ...     location=__test_folder__ + 'test', must_exist=False
            ... ).content = 'hans'
            >>> Replace(
            ...     location=__test_folder__ + 'test', new_version='python3.3'
            ... )._convert_path(
            ... ) # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            boostNode.extension.native.MacroError:...test"...interpreter...

            >>> file = boostNode.extension.file.Handler(
            ...     location=__test_folder__ + 'test', must_exist=False)
            >>> file.content = ('#!/usr/bin/python3.3\\n'
            ...                 '\\n'
            ...                 '## python2.7 hans\\n'
            ...                'AB\\n')
            >>> interpreter = Replace(
            ...     location=__test_folder__ + 'test', new_version='python2.7'
            ... )._convert_path()
            >>> file.content
            '#!/usr/bin/python2.7\\n\\n## python3.3 AB\\nhans\\n'

            >>> file = boostNode.extension.file.Handler(
            ...     location=__test_folder__ + 'test', must_exist=False)
            >>> file.content = ('#!/bin/python3.3\\n'
            ...                 '\\n'
            ...                 '## python2.7\\n'
            ...                 '## A\\n'
            ...                 '## B\\n'
            ...                 'C\\n'
            ...                 'D\\n'
            ...                 '##\\n')
            >>> interpreter = Replace(
            ...     location=__test_folder__ + 'test', new_version='python2.7'
            ... )._convert_path()
            >>> file.content
            '#!/bin/python2.7\\n\\n## python3.3\\n## C\\n## D\\nA\\nB\\n##\\n'

            >>> file = boostNode.extension.file.Handler(
            ...     location=__test_folder__ + 'test', must_exist=False)
            >>> file.content = ('#!/bin/python2.7\\n'
            ...                 '\\n'
            ...                 '## python3.3\\n'
            ...                 '## A\\n'
            ...                 'B\\n'
            ...                 '#\\n'
            ...                 '##\\n')
            >>> interpreter = Replace(
            ...     location=__test_folder__ + 'test', new_version='python3.3'
            ... )._convert_path()
            >>> file.content
            '#!/bin/python3.3\\n\\n## python2.7\\n## B\\n## #\\nA\\n##\\n'

            >>> file = boostNode.extension.file.Handler(
            ...     location=__test_folder__ + 'test', must_exist=False)
            >>> file.content = ('#!/bin/python3.3\\n'
            ...                 '\\n'
            ...                 '## python2.7\\n'
            ...                 '## A\\n'
            ...                 '##\\n'
            ...                 '## B\\n'
            ...                 'B\\n'
            ...                 '##\\n')
            >>> interpreter = Replace(
            ...     location=__test_folder__ + 'test', new_version='python3.3'
            ... )._convert_path()
            >>> file.content
            '#!/bin/python3.3\\n\\n## python2.7\\n## A\\n##\\n## B\\nB\\n##\\n'

            >>> file = boostNode.extension.file.Handler(
            ...     location=__test_folder__ + 'test', must_exist=False)
            >>> file.content = ('#!/bin/python2.7\\n'
            ...                 '\\n'
            ...                 '## python3.3\\n'
            ...                 '## A\\n'
            ...                 'B\\n'
            ...                 '\\n'
            ...                 'C\\n'
            ...                 '##\\n')
            >>> interpreter = Replace(
            ...     location=__test_folder__ + 'test', new_version='python3.3'
            ... )._convert_path()
            >>> file.content
            '#!/bin/python3.3\\n\\n## python2.7\\n## B\\n##\\n## C\\nA\\n##\\n'

            >>> file = boostNode.extension.file.Handler(
            ...     location=__test_folder__ + 'test', must_exist=False)
            >>> file.content = ('#!/bin/python2.7\\n'
            ...                 '\\n'
            ...                 '## python3.3\\n'
            ...                 'A\\n')
            >>> interpreter = Replace(
            ...     location=__test_folder__ + 'test', new_version='python3.3'
            ... )._convert_path()
            >>> file.content
            '#!/bin/python3.3\\n\\n## python2.7 A\\n\\n'
        '''
        self_file = boostNode.extension.file.Handler(
            location=inspect.currentframe().f_code.co_filename,
            respect_root_path=False)
        if self._skip_self_file and self_file == file:
            __logger__.info('Skip self file "%s".', self_file)
        else:
            self._convert_file_code(file)
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def _convert_file_code(self, file):
    def _convert_file_code(
        self: boostNode.extension.type.Self,
        file: boostNode.extension.file.Handler
    ) -> boostNode.extension.type.Self:
##
        '''
            Converts source code of given file to new version.
        '''
        with builtins.open(file.path, 'r') as file_handler:
            try:
                first_line = file_handler.readline()
            except builtins.UnicodeDecodeError:
                __logger__.warning('Can\'t decode file "%s".', file.path)
                return self
            match = re.compile(self._first_line_regex_pattern).match(
                first_line)
            if match is None:
                raise __exception__(
                    '"%s" hasn\'t path to interpreter in first line.',
                    file.path)
            self._current_version = match.group('current_version')
            new_interpreter = match.group('constant_version_pattern').replace(
                self._current_version, self._new_version)
            first_line = match.group().replace(
                match.group('constant_version_pattern'), new_interpreter)
            file_content = file_handler.read()
        __logger__.info(
            'Convert "{path}" from "{current_version}" to '
            '"{new_version}".'.format(
                path=file.path, current_version=self._current_version,
                new_version=self._new_version))
        file_content = first_line + re.compile(
            self._more_line_regex_pattern, re.DOTALL).sub(
                self._replace_alternate_lines, file_content)
        file.content = re.compile(self._one_line_regex_pattern).sub(
            self._replace_alternate_line, file_content)
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def _replace_alternate_lines(self, match):
    def _replace_alternate_lines(
        self: boostNode.extension.type.Self,
        match: type(re.compile('').match(''))
    ) -> builtins.str:
##
        '''
            Replaces various numbers of code lines with its corresponding code
            line in another version.

            "match" is a regular expression match object with all needed infos
                    about the current code snippet and its corresponding
        '''
        if match.group('alternate_version') == self._new_version:
            '''
                "str.replace()" has to run over "current_text" twice.
                Two consecutive lines with whitespace at the end of line
                aren't matched in first run.
            '''
            return '\n{prefix} {current_version}\n{prefix} {current_text}\n'\
                   '{alternate_text}{prefix}\n'.format(
                       prefix=match.group('prefix'),
                       current_version=self._current_version,
                       current_text=match.group('current_text').replace(
                           '\n', '\n%s ' % match.group('prefix')
                       )[:-(builtins.len(match.group('prefix')) + 2)].replace(
                           '\n%s \n' % match.group('prefix'),
                           '\n%s\n' % match.group('prefix')
                       ).replace(
                           '\n%s \n' % match.group('prefix'),
                           '\n%s\n' % match.group('prefix')),
                       alternate_text=match.group('alternate_text').replace(
                           '\n%s ' % match.group('prefix'),
                           '\n'
                       )[builtins.len(match.group('prefix')) + 1:].replace(
                           '\n%s' % match.group('prefix'), '\n'))
        return match.group()

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def _replace_alternate_line(self, match):
    def _replace_alternate_line(
        self: boostNode.extension.type.Self,
        match: type(re.compile('').match(''))
    ) -> builtins.str:
##
        '''
            Replaces one code line with its corresponding code line in another
            version.

            "match" is a regular expression match object with all needed infos
                    about the current code snippet and its corresponding
                    alternative.
        '''
        if match.group('alternate_version') == self._new_version:
            current_text = match.group('current_text')
            if current_text:
                current_text = ' ' + current_text
            return (
                '\n{prefix} {current_version}{current_text}\n{alternate_text}'
                '\n'.format(
                    prefix=match.group('prefix'),
                    current_version=self._current_version,
                    current_text=current_text,
                    alternate_text=match.group('alternate_text')))
        return match.group()

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def _determine_useful_version_in_location_helper(self, location):
    def _determine_useful_version_in_location_helper(
        self: boostNode.extension.type.Self,
        location: boostNode.extension.file.Handler
    ) -> builtins.str:
##
        '''
            Searches in files in given locations the first occurences of a
            useful conversion format.
        '''
        if location.is_file():
            if not self._extension or location.extension == self._extension:
                version = self._determine_useful_version_in_file(file=location)
                if version:
                    return version
        elif location.is_directory():
            for sub_location in location:
                version = self._determine_useful_version_in_location(
                    location=sub_location)
                if version:
                    return version
        else:
            raise __exception__(
                'Given Path "%s" doesn\'t exists.\n', location.path)
        return ''

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def _convert(self):
    def _convert(
        self: boostNode.extension.type.Self
    ) -> boostNode.extension.type.Self:
##
        '''
            Triggers the conversion process.
        '''
        if not __test_mode__ and self._new_version:
            self._convert_path()
        return self

            # endregion

        # endregion

    # endregion

# endregion

# region footer

boostNode.extension.dependent.Resolve(
    name=__name__, frame=inspect.currentframe())

# endregion
