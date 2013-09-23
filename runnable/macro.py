#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# region vim modline

# vim: set tabstop=4 shiftwidth=4 expandtab:
# vim: foldmethod=marker foldmarker=region,endregion:

# endregion

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
import codecs
##
import inspect
import os
import re
import sys

'''Make boostNode packages and modules importable via relative paths.'''
for number in (3, 4):
    sys.path.append(os.path.abspath(sys.path[0] + number * ('..' + os.sep)))

from boostNode.extension.file import Handler as FileHandler
from boostNode.extension.native import Module, PropertyInitializer
from boostNode.extension.system import CommandLine, Runnable
## python3.3 from boostNode.extension.type import Self
pass
from boostNode.paradigm.aspectOrientation import JointPoint
from boostNode.paradigm.objectOrientation import Class

# endregion


# region classes

class Replace(Class, Runnable):
    '''
        Parse source code and replace version depended code snippets with the
        correct given version code snippets.
    '''

    # region properties

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
             'dest': '_new_version',
             'metavar': 'VERSION'}},
        {'arguments': ('-s', '--skip-self-file'),
         'keywords': {
             'action': 'store_true',
             'default': {'execute': '__initializer_default_value__'},
             'help': 'Determines if this file should be ignored for running '
                     'any macros.',
             'dest': 'skip_self_file'}},
        {'arguments': ('-y', '--dry'),
         'keywords': {
             'action': 'store_true',
             'default': {'execute': '__initializer_default_value__'},
             'help': 'Define if there really should be done something.',
             'dest': 'dry'}},
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
             'dest': '_exclude_locations',
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
             'metavar': 'REGEX'}},
        {'arguments': ('-g', '--encoding'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Define which encoding should be used.',
             'dest': 'encoding',
             'metavar': 'ENCODING'}})

    # endregion

    # region dynamic methods

        # region public

            # region special

    @JointPoint
## python3.3     def __repr__(self: Self) -> builtins.str:
    def __repr__(self):
        '''
            Invokes if this object should describe itself by a string.

            Examples:

            >>> repr(Replace(
            ...     location=__file_path__, _new_version='python3.3'
            ... )) # doctest: +ELLIPSIS
            '...Replace...file "...macro.py" to ...to "python3.3".'
        '''
        return(
            'Object of "{class_name}" with {type} "{path}" to convert to '
            '"{new_version}".'.format(
                class_name=self.__class__.__name__,
                type=self.location.type, path=self.location.path,
                new_version=self._new_version))

            # endregion

            # region setter

    @JointPoint
## python3.3
##     def set_new_version(self: Self, version: builtins.str) -> builtins.str:
    def set_new_version(self, version):
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

            >>> FileHandler(
            ...     location=__test_folder_path__ + 'set_new_version',
            ...     must_exist=False
            ... ).content = ('#!/usr/bin/env version\\n\\n## '
            ...              'alternate_version hans\\npeter\\n')
            >>> replace = Replace(
            ...     location=__test_folder_path__ + 'set_new_version'
            ... )._convert_path()
            >>> replace.new_version = '__determine_useful__'
            >>> replace._new_version
            'version'
        '''
        self._new_version = version
        if version == '__determine_useful__':
            self._new_version = self._determine_useful_version_in_location(
                location=self.location)
            if not self._new_version:
                __logger__.warning('No new version found to convert to.')
        return self._new_version

    @JointPoint
## python3.3
##     def set_exclude_locations(
##         self: Self, paths: collections.Iterable
##     ) -> builtins.list:
    def set_exclude_locations(self, paths):
##
        '''
            Converts all paths setted to "_exclude_locations" via string to
            high level file objects.

            Examples:

            >>> replace = Replace(location=__file_path__)

            >>> replace.exclude_locations = [__file_path__]
            >>> replace._exclude_locations # doctest: +ELLIPSIS
            [Object of "Handler" with path "...macro.py" (type: file).]
        '''
        self._exclude_locations = []
        for path in paths:
            file = FileHandler(location=path, must_exist=False)
            if file:
                self._exclude_locations.append(file)
        return self._exclude_locations

            # endregion

        # endregion

        # region protected

            # region runnable implementation

    @JointPoint
## python3.3     def _run(self: Self) -> Self:
    def _run(self):
        '''
            Entry point for command line call of this program. Validates the
            given input. Gives usage info or raises exception if the given
            inputs don't make sense.
        '''
        command_line_arguments = CommandLine.argument_parser(
            arguments=self.COMMAND_LINE_ARGUMENTS,
            module_name=__name__,
            scope={'os': os, 'module_name': __module_name__, 'self': self})
        return self._initialize(**self._command_line_arguments_to_dictionary(
            namespace=command_line_arguments))

    @JointPoint(PropertyInitializer)
## python3.3
##     def _initialize(
##         self: Self, location=None, skip_self_file=False, extension='',
##         first_line_regex_pattern='(?P<constant_version_pattern>^#!.*?'
##                                  '(?P<current_version>[a-zA-Z0-9\.]+))\n',
##         one_line_regex_pattern='\n(?P<prefix>##) '
##                                '(?P<alternate_version>[^\n ]+) ?'
##                                '(?P<alternate_text>.*)\n'
##                                '(?P<current_text>.*)(?:\n|\Z)',
##         more_line_regex_pattern='(?s)\n(?P<prefix>##) '
##                                 '(?P<alternate_version>[^ ]+)\n'
##                                 '(?P<alternate_text>'
##                                 '(?:(?:## .*?\n)|(?:##\n))+'  # in brackets
##                                 ')(?P<current_text>.*?\n)##(?:\n|\Z)',
##         encoding='utf_8', dry=False, _exclude_locations=(),
##         _new_version='__determine_useful__', **keywords: builtins.object
##     ) -> Self:
    def _initialize(
        self, location=None, skip_self_file=False, extension='',
        first_line_regex_pattern='(?P<constant_version_pattern>^#!.*?'
                                 '(?P<current_version>[a-zA-Z0-9\.]+))\n',
        one_line_regex_pattern='\n(?P<prefix>##) '
                               '(?P<alternate_version>[^\n ]+) ?'
                               '(?P<alternate_text>.*)\n'
                               '(?P<current_text>.*)\n',
        more_line_regex_pattern='(?s)\n(?P<prefix>##) '
                                '(?P<alternate_version>[^ ]+)\n'
                                '(?P<alternate_text>'
                                '(?:(?:## .*?\n)|(?:##\n))+'  # in brackets.
                                ')(?P<current_text>.*?\n)##(?:\n|\Z)',
        encoding='utf_8', dry=False, _exclude_locations=(),
        _new_version='__determine_useful__', **keywords
    ):
##
        '''
            Triggers the conversion process with given arguments.
            NOTE: "(?s...)" is equivalent to regular expression flag
            "re.DOTALL".
            NOTE: That alternate version in one line regular expression
            pattern could be empty.

            Examples:

            >>> Replace(
            ...     location='non_existing_file'
            ... ) # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            boostNode.extension.native.FileError: Invalid path "...non_exist...
        '''

                # region properties

        '''Current location for deep code parsing.'''
        self.location = FileHandler(self.location, encoding=self.encoding)
        '''NOTE: This additional declaration is needed to trigger setter.'''
        self.exclude_locations = self._exclude_locations
        '''
            New version to convert given files to. NOTE: This property can only
            determined after all properties are set. This additional
            declaration is needed to trigger setter.
        '''
        self.new_version = self._new_version
        '''Version of the giving source files.'''
        self._current_version = ''

                # endregion

        return self._convert()

            # endregion

            # region boolean

    @JointPoint
## python3.3
##     def _in_exclude_locations(
##         self: Self, location: FileHandler
##     ) -> builtins.bool:
    def _in_exclude_locations(self, location):
##
        '''
            Returns "True" if given location is in one of initially defined
            exclude locations.
        '''
        for file in self._exclude_locations:
            if location == file or (file.is_directory() and location in file):
                __logger__.info(
                    'Ignore exclude location "%s".', location.path)
                return True
        return False

            # endregion

            # region core concern

    @JointPoint
## python3.3
##     def _determine_useful_version_in_location(
##         self: Self, location: FileHandler
##     ) -> builtins.str:
    def _determine_useful_version_in_location(self, location):
##
        '''
            Determines a useful version for replacing if nothing explicit was
            given.

            Examples:

            >>> file = FileHandler(
            ...     location=__test_folder_path__ +
            ...     '_determine_useful_version_in_location/sub',
            ...     must_exist=False)
            >>> file.make_directorys()
            True
            >>> FileHandler(
            ...     location=file.path + 'file', must_exist=False
            ... ).content = 'hans\\n## new_version peter\\nklaus\\n'

            >>> Replace(
            ...     location=__file_path__
            ... )._determine_useful_version_in_location(location=file)
            'new_version'
        '''
        if not self._in_exclude_locations(location):
            version = self._determine_useful_version_in_location_helper(
                location)
            if version:
                return version
        if location == self.location:
            __logger__.info('No macros found.')
        return ''

    @JointPoint
## python3.3
##     def _determine_useful_version_in_file(
##         self: Self, file: FileHandler
##     ) -> builtins.str:
    def _determine_useful_version_in_file(self, file):
##
        '''
            Searches for first version replacement in macro language as good
            guess for new version if no new version was defined explicitly.

            Examples:

            >>> file = FileHandler(
            ...     __test_folder_path__ + '_determine_useful_version_in_file',
            ...     must_exist=False)
            >>> file.content = 'hans\\n## new_version peter\\nklaus\\n'

            >>> Replace(
            ...     location=__file_path__
            ... )._determine_useful_version_in_file(file)
            'new_version'
        '''
        try:
            file.content
        except builtins.UnicodeDecodeError:
            return ''
        match = re.compile(self.one_line_regex_pattern).search(file.content)
        if match is None:
            match = re.compile(
                self.more_line_regex_pattern
            ).search(file.content)
        if match:
            __logger__.info(
                'Detected "%s" as new version.',
                match.group('alternate_version'))
            return match.group('alternate_version')
        return ''

    @JointPoint
## python3.3     def _convert_path(self: Self) -> Self:
    def _convert_path(self):
        '''Converts the given path to the specified format.'''
        if not self._in_exclude_locations(location=self.location):
            if(self.location.is_file() and
                (not self.extension or
                 self.location.extension == self.extension)
               ):
                self._convert_file(file=self.location)
            elif self.location.is_directory():
                self._convert_directory(directory=self.location)
            else:
                raise __exception__(
                    'Given Path "%s" doesn\'t exists.\n', self.location)
        return self

    @JointPoint
## python3.3
##     def _convert_directory(self: Self, directory: FileHandler) -> Self:
    def _convert_directory(self, directory):
##
        '''
            Walks through a whole directory and its substructure to convert its
            text based files between different versions of marked
            code-snippets.

            "directory" the directory location with text-files which should
                        be converted.
        '''
        for file in directory:
            __logger__.debug('Check "%s".', file.path)
            if not self._in_exclude_locations(location=file):
                if file.is_file() and (not self.extension or
                                       file.extension == self.extension):
                    self._convert_file(file)
                elif file.is_directory():
                    self._convert_directory(directory=file)
        return self

    @JointPoint
## python3.3     def _convert_file(self: Self, file: FileHandler) -> Self:
    def _convert_file(self, file):
        '''
            Opens a given file and parses its content and convert it through
            different versions of code snippets.

            "file" - the file to be converted.

            >>> FileHandler(
            ...     location=__test_folder_path__ + '_convert_file',
            ...     must_exist=False
            ... ).content = 'hans'
            >>> Replace(
            ...     location=__test_folder_path__ + '_convert_file',
            ...     _new_version='python3.3'
            ... )._convert_path(
            ... ) # doctest: +ELLIPSIS
            Object of "Replace" with file "..._convert_file" to convert to ...

            >>> file = FileHandler(
            ...     location=__test_folder_path__ + '_convert_file',
            ...     must_exist=False)
            >>> file.content = ('#!/usr/bin/python3.3\\n'
            ...                 '\\n'
            ...                 '## python2.7 hans\\n'
            ...                'AB\\n')
            >>> interpreter = Replace(
            ...     location=__test_folder_path__ + '_convert_file',
            ...     _new_version='python2.7'
            ... )._convert_path()
            >>> file.content
            '#!/usr/bin/python2.7\\n\\n## python3.3 AB\\nhans\\n'

            >>> file = FileHandler(
            ...     location=__test_folder_path__ + '_convert_file',
            ...     must_exist=False)
            >>> file.content = ('#!/bin/python3.3\\n'
            ...                 '\\n'
            ...                 '## python2.7\\n'
            ...                 '## A\\n'
            ...                 '## B\\n'
            ...                 'C\\n'
            ...                 'D\\n'
            ...                 '##\\n')
            >>> interpreter = Replace(
            ...     location=__test_folder_path__ + '_convert_file',
            ...     _new_version='python2.7'
            ... )._convert_path()
            >>> file.content
            '#!/bin/python2.7\\n\\n## python3.3\\n## C\\n## D\\nA\\nB\\n##\\n'

            >>> file = FileHandler(
            ...     location=__test_folder_path__ + '_convert_file',
            ...     must_exist=False)
            >>> file.content = ('#!/bin/python2.7\\n'
            ...                 '\\n'
            ...                 '## python3.3\\n'
            ...                 '## A\\n'
            ...                 'B\\n'
            ...                 '#\\n'
            ...                 '##\\n')
            >>> interpreter = Replace(
            ...     location=__test_folder_path__ + '_convert_file',
            ...     _new_version='python3.3'
            ... )._convert_path()
            >>> file.content
            '#!/bin/python3.3\\n\\n## python2.7\\n## B\\n## #\\nA\\n##\\n'

            >>> file = FileHandler(
            ...     location=__test_folder_path__ + '_convert_file',
            ...     must_exist=False)
            >>> file.content = ('#!/bin/python3.3\\n'
            ...                 '\\n'
            ...                 '## python2.7\\n'
            ...                 '## A\\n'
            ...                 '##\\n'
            ...                 '## B\\n'
            ...                 'B\\n'
            ...                 '##\\n')
            >>> interpreter = Replace(
            ...     location=__test_folder_path__ + '_convert_file',
            ...     _new_version='python3.3'
            ... )._convert_path()
            >>> file.content
            '#!/bin/python3.3\\n\\n## python2.7\\n## A\\n##\\n## B\\nB\\n##\\n'

            >>> file = FileHandler(
            ...     location=__test_folder_path__ + '_convert_file',
            ...     must_exist=False)
            >>> file.content = ('#!/bin/python2.7\\n'
            ...                 '\\n'
            ...                 '## python3.3\\n'
            ...                 '## A\\n'
            ...                 'B\\n'
            ...                 '\\n'
            ...                 'C\\n'
            ...                 '##\\n')
            >>> interpreter = Replace(
            ...     location=__test_folder_path__ + '_convert_file',
            ...     _new_version='python3.3'
            ... )._convert_path()
            >>> file.content
            '#!/bin/python3.3\\n\\n## python2.7\\n## B\\n##\\n## C\\nA\\n##\\n'

            >>> file = FileHandler(
            ...     location=__test_folder_path__ + '_convert_file',
            ...     must_exist=False)
            >>> file.content = ('#!/bin/python2.7\\n'
            ...                 '\\n'
            ...                 '## python3.3\\n'
            ...                 'A\\n')
            >>> interpreter = Replace(
            ...     location=__test_folder_path__ + '_convert_file',
            ...     _new_version='python3.3'
            ... )._convert_path()
            >>> file.content
            '#!/bin/python3.3\\n\\n## python2.7 A\\n\\n'
        '''
        self_file = FileHandler(
            location=inspect.currentframe().f_code.co_filename,
            respect_root_path=False)
        if self.skip_self_file and self_file == file:
            __logger__.info('Skip self file "%s".', self_file)
        else:
            self._convert_file_code(file)
        return self

    @JointPoint
## python3.3     def _convert_file_code(self: Self, file: FileHandler) -> Self:
    def _convert_file_code(self, file):
        '''Converts source code of given file to new version.'''
        old_file_content = file.content
## python3.3         with builtins.open(
        with codecs.open(
            file.path, mode='r', encoding=self.encoding
        ) as file_handler:
            try:
## python3.3
##                 first_line = file_handler.readline()
                first_line = file_handler.readline().encode(self.encoding)
##
            except builtins.UnicodeDecodeError:
                __logger__.warning(
                    'Can\'t decode file "%s" with given encoding "%s".',
                    file.path, self.encoding)
                return self
            match = re.compile(self.first_line_regex_pattern).match(
                first_line)
            if match is None:
                __logger__.warning(
                    '"%s" hasn\'t path to version in first line.', file.path)
                return self
            self._current_version = match.group('current_version')
            new_interpreter = match.group('constant_version_pattern').replace(
                self._current_version, self._new_version)
            first_line = match.group().replace(
                match.group('constant_version_pattern'), new_interpreter)
            try:
                '''
                    NOTE: Calling "read()" twice is necessary to work around a
                    python bug. First call only reads a part of corresponding
                    file.
                '''
## python3.3
##                 file_content = file_handler.read() + file_handler.read()
                file_content = (
                    file_handler.read() + file_handler.read()
                ).encode(self.encoding)
##
            except builtins.UnicodeDecodeError:
                __logger__.warning(
                    'Can\'t decode file "%s" with given encoding "%s".',
                    file.path, self.encoding)
                return self
        __logger__.info(
            'Convert "{path}" from "{current_version}" to '
            '"{new_version}".'.format(
                path=file.path, current_version=self._current_version,
                new_version=self._new_version))
        file_content = first_line + re.compile(
            self.more_line_regex_pattern
        ).sub(
            self._replace_alternate_lines, file_content)
        if not self.dry:
            try:
                file.content = re.compile(self.one_line_regex_pattern).sub(
                    self._replace_alternate_line, file_content)
            except builtins.UnicodeEncodeError as exception:
                __logger__.warning(
                    'Can\'t encode to file "%s" with given encoding "%s". '
                    '%s: %s', file.path, self.encoding,
                    exception.__class__.__name__, builtins.str(exception))
                file.content = old_file_content
        return self

    @JointPoint
## python3.3
##     def _replace_alternate_lines(
##         self: Self, match: type(re.compile('').match(''))
##     ) -> builtins.str:
    def _replace_alternate_lines(self, match):
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
            try:
                return (
                    '\n{prefix} {current_version}\n{prefix} {current_text}\n'
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
                            '\n%s\n' % match.group('prefix')
                        ).rstrip(), alternate_text=match.group(
                            'alternate_text'
                        ).replace(
                            '\n%s ' % match.group('prefix'), '\n'
                        )[builtins.len(match.group('prefix')) + 1:].replace(
                            '\n%s' % match.group('prefix'), '\n')))
            except:
                raise IOError(match.groups())
        return match.group()

    @JointPoint
## python3.3
##     def _replace_alternate_line(
##         self: Self, match: type(re.compile('').match(''))
##     ) -> builtins.str:
    def _replace_alternate_line(self, match):
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

    @JointPoint
## python3.3
##     def _determine_useful_version_in_location_helper(
##         self: Self, location: FileHandler
##     ) -> builtins.str:
    def _determine_useful_version_in_location_helper(self, location):
##
        '''
            Searches in files in given locations the first occurrences of a
            useful conversion format.
        '''
        if location.is_file():
            if not self.extension or location.extension == self.extension:
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

    @JointPoint
## python3.3     def _convert(self: Self) -> Self:
    def _convert(self):
        '''Triggers the conversion process.'''
        if not __test_mode__ and self._new_version:
            self._convert_path()
        return self

            # endregion

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
