#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# region vim modline

# vim: set tabstop=4 shiftwidth=4 expandtab:
# vim: foldmethod=marker foldmarker=region,endregion:

# endregion

# region header

'''
    is the main element of the "Reflector".
    The Reflector's public methods implements the general features of the
    whole application.
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
import inspect
import os
import sys

'''Make boostNode packages and modules importable via relative paths.'''
for number in (3, 4):
    sys.path.append(os.path.abspath(sys.path[0] + number * ('..' + os.sep)))

from boostNode.extension.file import Handler as FileHandler
from boostNode.extension.native import Module, PropertyInitializer
from boostNode.extension.output import Logger
from boostNode.extension.system import CommandLine, Platform, Runnable
## python3.3 from boostNode.extension.type import Self, SelfClass
pass
from boostNode.paradigm.aspectOrientation import JointPoint
from boostNode.paradigm.objectOrientation import Class

# endregion


# region classes

class Reflector(Class, Runnable):
    '''Main class of the file reflection application.'''

    # region properties

    '''Holds all command line arguments.'''
    COMMAND_LINE_ARGUMENTS = (
        {'arguments': ('source_location',),
         'keywords': {
             'action': 'store',
             'nargs': '?',
             'const': '',
             'type': builtins.str,
             #'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Select which path you want to use as source path.',
             #'dest': 'source_location',
             'metavar': 'FOLDER_PATH'}},
        {'arguments': ('target_location',),
         'keywords': {
             'action': 'store',
             'nargs': '?',
             'const': '',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             #'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Select which path you want to use as target (reflection)'
                     ' path.',
             #'dest': 'target_location',
             'metavar': 'FOLDER_PATH'}},
        {'arguments': ('-a', '--source'),
         'keywords': {'execute': 'arguments[0]["keywords"]'}},
        {'arguments': ('-b', '--target'),
         'keywords': {'execute': 'arguments[1]["keywords"]'}},
        {'arguments': ('-f', '--limit'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Select a limit for your cache size.',
             'dest': 'limit',
             'metavar': 'LIMIT'}},
        {'arguments': ('-p', '--priority-locations'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Select locations which should be handle with higher '
                     'priority this application will try to copy these files '
                     'into the cache.',
             'dest': 'priority_locations',
             'metavar': 'PATHS'}},
        {'arguments': ('-e', '--exclude-locations'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Select locations which should be ignored. '
                     "This application doesn't touch these files in source "
                     'and its corresponding locations in target.',
             'dest': 'exclude_locations',
             'metavar': 'PATHS'}},
        {'arguments': ('-r', '--target-rights'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Select which rights your reflection files should have.',
             'dest': 'target_rights',
             'metavar': 'RIGHT'}},
        {'arguments': ('-s', '--synchronize-back'),
         'keywords': {
             'action': 'store_true',
             'default': {'execute': '__initializer_default_value__'},
             'help': 'Select to synchronize an existing reflection back.',
             'dest': 'synchronize_back'}},
        {'arguments': ('-d', '--create'),
         'keywords': {
             'action': 'store_true',
             'default': {'execute': '__initializer_default_value__'},
             'help': 'Select to create a reflection (optionally after '
                     'a synchronisation).',
             'dest': 'create'}},
        {'arguments': ('-n', '--use-native-symlinks'),
         'keywords': {
             'action': 'store_true',
             'default': {'execute': '__initializer_default_value__'},
             'help': 'Use native system symbolic links instead of portable '
                     'FileReflector links.',
             'dest': 'use_native_symlinks'}},
        {'arguments': ('-u', '--minimum-reflection-size'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'A treshold from where a warning is shown.',
             'dest': 'minimum_reflection_size_in_byte',
             'metavar': 'NUMBER_OF_BYTES'}},
        {'arguments': ('-o', '--open'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': (),
             'type': builtins.str,
             'required': False,
             'help': 'Open given files with a useful program.',
             'dest': 'open',
             'metavar': 'FILE_PATHS'}},)

    # endregion

    # region static methods

        # region public

            # region boolean

    @JointPoint(builtins.classmethod)
## python3.3
##     def is_path_in_paths(
##         cls: SelfClass, search: FileHandler, paths: collections.Iterable
##     ) -> builtins.bool:
    def is_path_in_paths(cls, search, paths):
##
        '''
            Checks if a given path represented in a given list of paths or it's
            substructure.

            Examples:

            >>> file = FileHandler(
            ...     location=__test_folder_path__ + 'source5',
            ...     must_exist=False)
            >>> file.make_directorys()
            True

            >>> Reflector.is_path_in_paths(
            ...     search=file, paths=[__test_folder_path__ + 'source5'])
            True

            >>> Reflector.is_path_in_paths(
            ...     search=file, paths=[__test_folder_path__ + 'target5'])
            False
        '''
        for path in paths:
            if(FileHandler(location=path, must_exist=False).path in
               search.path):
                return True
        return False

            # endregion

        # endregion

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

            >>> FileHandler(
            ...     __test_folder_path__ + 's/A/B', must_exist=False
            ... ).make_directorys()
            True

            >>> repr(Reflector(
            ...     source_location=__test_folder_path__ + 's',
            ...     target_location=__test_folder_path__ + 't',
            ...     priority_locations=(__test_folder_path__ + 's/A',),
            ...     exclude_locations=(__test_folder_path__ + 's/A/B',))
            ... ) # doctest: +ELLIPSIS
            '...s...t...s...A...s...A...B".'

            >>> repr(Reflector(
            ...     source_location=__test_folder_path__ + 's',
            ...     target_location=__test_folder_path__ + 't',
            ...     target_rights=777,
            ...     limit='500 byte',
            ...     use_native_symlinks=True)) # doctest: +ELLIPSIS
            '...s..."...t..."...500.0 byte...'

            >>> repr(Reflector(
            ...     source_location=__test_folder_path__ + 's',
            ...     target_location=__test_folder_path__ + 't',
            ...     priority_locations=(__test_folder_path__ + 's',))
            ... ) # doctest: +ELLIPSIS
            '...s..."...t..."...s" and exclude locations "".'

            >>> repr(Reflector(
            ...     source_location=__test_folder_path__ + 's',
            ...     target_location=__test_folder_path__ + 't')
            ... ) # doctest: +ELLIPSIS
            '...s..."...t..."...ority locations "" and exclude locations "".'
        '''
        limit = FileHandler.determine_size_from_string(
            size_and_unit=self.given_limit)
        return ('Object of "{class_name}" with source path "{source_path}" '
                'and target path "{target_path}". Limit is {limit} byte, '
                'priority locations "{priority_locations}" and exclude '
                'locations "{exclude_locations}".'.format(
                    class_name=self.__class__.__name__,
                    source_path=self.source_location.path,
                    target_path=self.target_location.path,
                    limit=limit,
                    priority_locations='", "'.join(self.priority_locations),
                    exclude_locations='", "'.join(self.exclude_locations)))

            # endregion

            # region getter

    @JointPoint(Class.pseudo_property)
## python3.3     def get_status_in_percent(self: Self) -> builtins.float:
    def get_status_in_percent(self):
        '''
            Calculates the edited part of files in percent.

            Examples:

            >>> source = FileHandler(
            ...     location=__test_folder_path__ + 'source6',
            ...     make_directory=True)
            >>> reflector = Reflector(
            ...     source_location=__test_folder_path__ + 'source6',
            ...     target_location=__test_folder_path__ + 'target6')
            >>> reflector._edited_number_of_files = 5
            >>> reflector._number_of_files = 10
            >>> reflector.status_in_percent
            50.0

            >>> reflector._edited_number_of_files = 3
            >>> reflector._number_of_files = 9
            >>> reflector.status_in_percent
            33.33

            >>> reflector._edited_number_of_files = 1
            >>> reflector._number_of_files = 10
            >>> reflector.status_in_percent
            10.0

            >>> reflector._edited_number_of_files = 10000
            >>> reflector._number_of_files = 10000
            >>> reflector.get_status_in_percent()
            100.0
        '''
        return builtins.round(
            (builtins.float(self._edited_number_of_files) /
             builtins.float(self._number_of_files)) * 100, 2)

            # endregion

    @JointPoint
## python3.3     def open(self: Self, files: collections.Iterable) -> Self:
    def open(self, files):
        '''
            Opens the given files by using the "Platform.open()" method. It can
            handle symbolic and portable links.
        '''
        for file in files:
            file = FileHandler(location=file, must_exist=False)
            if file.is_portable_link():
                referenced_file = FileHandler(
                    location=file.read_portable_link(), must_exist=False)
                if referenced_file:
                    Platform.open(location=referenced_file)
                    return self
                raise __exception__(
                    'The referenced object "%s" of portable symlink "%s" '
                    'isn\'t currently available.', referenced_file, file.path)
            Platform.open(location=file)
        return self

    @JointPoint
## python3.3     def create_cache(self: Self) -> Self:
    def create_cache(self):
        '''
            Creates a new reflection cache of the given source object.

            Examples:

            >>> FileHandler(
            ...     location=__test_folder_path__ + 'source',
            ...     make_directory=True
            ... ) # doctest: +ELLIPSIS
            Object of "Handler" with path "...source..." (type: directory).
            >>> reflector = Reflector(
            ...     source_location=__test_folder_path__ + 'source',
            ...     target_location=__test_folder_path__ + 'target')
            >>> repr(reflector.create_cache()) # doctest: +ELLIPSIS
            '...source..." and target path "...target...". Limit...'

            >>> FileHandler(
            ...     location=__test_folder_path__ + 'source/A/B/C',
            ...     must_exist=False
            ... ).make_directorys()
            True
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'source/B/A/B/C',
            ...     must_exist=False
            ... ).make_directorys()
            True
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'source/B/B/C',
            ...     must_exist=False
            ... ).make_directorys()
            True
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'source/A/a.txt',
            ...     must_exist=False
            ... ).content = 'hans'
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'source/A/b.txt',
            ...     must_exist=False
            ... ).content = 'hans'
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'source/A/B/C/a.txt',
            ...     must_exist=False
            ... ).content = 'hans'
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'source/B/B/C/a.txt',
            ...     must_exist=False
            ... ).content = 'hans'
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'source/B/A/B/c.txt',
            ...     must_exist=False
            ... ).content = 'hans'
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'source/B/A/B/C/big.txt',
            ...     must_exist=False
            ... ).content = 100 * '10bytes - '
            >>> reflector = Reflector(
            ...     source_location=__test_folder_path__ + 'source',
            ...     target_location=__test_folder_path__ + 'target',
            ...     limit='20 byte')
            >>> repr(reflector.create_cache()) # doctest: +ELLIPSIS
            '...Re...source..." and target path "...target...".'
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'target/A/B/C'
            ... ).is_directory(allow_link=False)
            True
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'target/B/A/B/C'
            ... ).is_directory(allow_link=False)
            True
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'target/B/B/C'
            ... ).is_directory(allow_link=False)
            True
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'target/A/a.txt'
            ... ).is_file(allow_link=False)
            True
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'target/A/b.txt'
            ... ).is_file(allow_link=False)
            True
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'target/A/B/C/a.txt'
            ... ).is_file(allow_link=False)
            True
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'target/B/B/C/a.txt'
            ... ).is_file(allow_link=False)
            True
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'target/B/A/B/c.txt'
            ... ).is_file(allow_link=False)
            True
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'target/B/A/B/C/big.txt'
            ... ).is_portable_link()
            True

            >>> reflector = Reflector(
            ...     source_location=__test_folder_path__ + 'source',
            ...     target_location=__test_folder_path__ + 'target',
            ...     limit='1020 byte',
            ...     priority_locations=(
            ...         __test_folder_path__ + 'source/B/A/B/C/',))
            >>> repr(reflector.create_cache()) # doctest: +ELLIPSIS
            '...source...source..." and target path "...target...".'
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'target/A/B/C'
            ... ).is_directory(allow_link=False)
            True
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'target/B/A/B/C'
            ... ).is_directory(allow_link=False)
            True
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'target/B/B/C'
            ... ).is_directory(allow_link=False)
            True
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'target/A/a.txt'
            ... ).is_file(allow_link=False)
            True
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'target/A/b.txt'
            ... ).is_file(allow_link=False)
            True
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'target/A/B/C/a.txt'
            ... ).is_file(allow_link=False)
            True
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'target/B/B/C/a.txt'
            ... ).is_file(allow_link=False)
            True
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'target/B/A/B/c.txt'
            ... ).is_file(allow_link=False)
            True
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'target/B/A/B/C/big.txt'
            ... ).is_file(allow_link=False)
            True

            >>> if Platform().operating_system != 'windows':
            ...     created = FileHandler(
            ...         location='.'
            ...     ).make_symbolic_link(
            ...         target=__test_folder_path__ + 'source/link',
            ...         force=True)
            ...     created = FileHandler(
            ...         location=__test_folder_path__ +
            ...         'source/B/A/B/C/big.txt'
            ...     ).make_symbolic_link(
            ...         target=__test_folder_path__ + 'source/big_link',
            ...         force=True)

            >>> reflector = Reflector(
            ...     source_location=__test_folder_path__ + 'source',
            ...     target_location=__test_folder_path__ + 'target',
            ...     limit='1020 byte',
            ...     priority_locations=(
            ...         __test_folder_path__ + 'source/B/A/B/C/',))
            >>> repr(reflector.create_cache()) # doctest: +ELLIPSIS
            'Object of "Reflector" with source path "...source..."...'

            >>> if Platform().operating_system == 'windows':
            ...     '...runnable...'
            ... else:
            ...     FileHandler(
            ...         location=__test_folder_path__ + 'source/link'
            ...     ).read_symbolic_link() # doctest: +ELLIPSIS
            '...runnable...'
            >>> if Platform().operating_system == 'windows':
            ...     '...target...B...A...B...C...big.txt'
            ... else:
            ...     FileHandler(
            ...         location=__test_folder_path__ + 'target/big_link'
            ...     ).read_symbolic_link() # doctest: +ELLIPSIS
            '...target...B...A...B...C...big.txt'
        '''
        __logger__.info('Clear reflection directory.')
        self.target_location.clear_directory()
        __logger__.info('Create reflection structure.')
        self.source_location.iterate_directory(
            function=self._create_reflection_structure,
            target=self.target_location,
            recursive_in_link=False)
        __logger__.info('Create reflection files.')
        return self._create_reflection_files()

    @JointPoint
## python3.3     def synchronize_back_to_source(self: Self) -> Self:
    def synchronize_back_to_source(self):
        '''
            Syncs the current cache location back to the source.

            Examples:

            >>> FileHandler(
            ...     location=__test_folder_path__ + 'source2',
            ...     make_directory=True
            ... ) # doctest: +ELLIPSIS
            Object of "Handler" with path "...source2..." (type: directory).
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'target2/new_folder',
            ...     must_exist=False
            ... ).make_directorys() # doctest: +ELLIPSIS
            True
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'target2/new_file.txt',
            ...     must_exist=False
            ... ).content = 'hans'
            >>> reflector = Reflector(
            ...     source_location=__test_folder_path__ + 'source2',
            ...     target_location=__test_folder_path__ + 'target2')
            >>> repr(
            ...     reflector.synchronize_back_to_source()
            ... ) # doctest: +ELLIPSIS
            '...path "...source2..." and target path "...target2...'
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'source2/new_folder'
            ... ).is_directory(allow_link=False)
            True
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'source2/new_file.txt'
            ... ).is_file(allow_link=False)
            True

            >>> len(FileHandler(location=__test_folder_path__ + 'source2')) > 0
            True
            >>> reflector = Reflector(
            ...     source_location=__test_folder_path__ + 'source2',
            ...     target_location=__test_folder_path__ + 'target2')
            >>> repr(
            ...     reflector.synchronize_back_to_source()
            ... ) # doctest: +ELLIPSIS
            '...path "...source2..." and target path "...target2...'
            >>> len(FileHandler(location=__test_folder_path__ + 'source2'))
            0

            >>> FileHandler(
            ...     location=__test_folder_path__ + 'source3/A/B/C',
            ...     must_exist=False
            ... ).make_directorys()
            True
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'source3/B/A/B/C',
            ...     must_exist=False
            ... ).make_directorys()
            True
            >>> file = FileHandler(
            ...     location=__test_folder_path__ + 'source3/A/B/C/test.txt',
            ...     must_exist=False)
            >>> file.content = ((int(file.BLOCK_SIZE_IN_BYTE) + 1) * 'A')
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'source3/A/delete_it.txt',
            ...     must_exist=False
            ... ).content = 'hans'
            >>> source_ignore = FileHandler(
            ...     location=__test_folder_path__ + 'source3/ignore',
            ...     make_directory=True)
            >>> reflector = Reflector(
            ...     source_location=__test_folder_path__ + 'source3',
            ...     target_location=__test_folder_path__ + 'target3',
            ...     exclude_locations=(
            ...         __test_folder_path__ + 'source3/ignore',),
            ...     limit='1 byte', use_native_symlinks=False)
            >>> repr(reflector.create_cache()) # doctest: +ELLIPSIS
            '...source3...target...target3...Limit is 1.0 byte...'
            >>> file = FileHandler(
            ...     location=__test_folder_path__ + 'target3/A/B/C/test.txt')
            >>> file.is_portable_link()
            True
            >>> file.path = __test_folder_path__ + 'target3/B/A/B/C/test.txt'
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'target3/A/delete_it.txt'
            ... ).remove_file()
            True
            >>> target_ignore = FileHandler(
            ...     location=__test_folder_path__ + 'target3/ignore',
            ...     must_exist=False)
            >>> target_ignore.is_element()
            False
            >>> target_ignore.make_directory()
            True

            >>> reflector = Reflector(
            ...     source_location=__test_folder_path__ + 'source3',
            ...     target_location=__test_folder_path__ + 'target3',
            ...     exclude_locations=(
            ...         __test_folder_path__ + 'source3/ignore',),
            ...     limit='1 byte', use_native_symlinks=True)
            >>> repr(
            ...     reflector.synchronize_back_to_source()
            ... ) # doctest: +ELLIPSIS
            '...source3...path "...target3...1.0 byte...ignore...".'
            >>> file = FileHandler(
            ...     location=__test_folder_path__ + 'source3/B/A/B/C/test.txt')
            >>> file.content == ((int(file.BLOCK_SIZE_IN_BYTE) + 1) * 'A')
            True
            >>> FileHandler(
            ...     location=__test_folder_path__ + 'source3/A/delete_it.txt',
            ...     must_exist=False
            ... ).is_element()
            False
            >>> target_ignore.is_element()
            False
            >>> source_ignore.is_element()
            True
        '''
        if Platform.check_process_lock(description=__module_name__):
            __logger__.warning(
                'The last synchronisation process was interrupted in an '
                'unstable state. %s will finish last process so you can '
                'repeat your intended job after this.',
                __module_name__.capitalize())
        else:
            __logger__.info('Relocate moved files.')
            self.target_location.iterate_directory(
                function=self._relocate_moved_file,
                recursive=True, recursive_in_link=False)
            __logger__.info('Copy new files in cache to source.')
            self.target_location.iterate_directory(
                function=self._copy_cache_to_source,
                recursive=True, recursive_in_link=False)
            __logger__.info('Delete source files not existing in target.')
            self.source_location.iterate_directory(
                function=self._delete_source_file_not_existing_in_target,
                recursive=True, recursive_in_link=False)
            Platform.set_process_lock(description=__module_name__)
        __logger__.info('Clear cache.')
        self.target_location.clear_directory()
        Platform.clear_process_lock(description=__module_name__)
        return self

        # endregion

        # region protected

            # region runnable implementation

    @JointPoint
## python3.3     def _run(self: Self) -> Self:
    def _run(self):
        '''
            Entry point for command line call of this program.
            Initializes a new instance of the option parser for the
            application interface.
        '''
        '''Saves all given command line arguments.'''
        self._command_line_arguments = CommandLine.argument_parser(
            arguments=self.COMMAND_LINE_ARGUMENTS, module_name=__name__,
            scope={'arguments': self.COMMAND_LINE_ARGUMENTS, 'self': self})
        if self._command_line_arguments.open:
            return self.open(self._command_line_arguments.open)
        return self._initialize(**self._command_line_arguments_to_dictionary(
            namespace=self._command_line_arguments))

    @JointPoint(PropertyInitializer)
## python3.3
##     def _initialize(
##         self: Self, source_location: (FileHandler, builtins.str),
##         target_location=None, limit='100 MB', priority_locations=(),
##         exclude_locations=(), target_rights=777, synchronize_back=False,
##         create=False, use_native_symlinks=False,
##         minimum_reflection_size_in_byte=100 * 10 ** 3,  # 100 Kilobyte
##         **keywords: builtins.object
##     ) -> Self:
    def _initialize(
        self, source_location, target_location=None, limit='100 MB',
        priority_locations=(), exclude_locations=(),
        target_rights=777, synchronize_back=False, create=False,
        use_native_symlinks=False,
        minimum_reflection_size_in_byte=100 * 10 ** 3,  # 100 Kilobyte
        **keywords
    ):
##
        '''
            Initializes a new object of a given synchronisation process.

            Examples:

            >>> Reflector(
            ...     source_location=__test_folder_path__,
            ...     target_location=__test_folder_path__ + 'target'
            ... ) # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            boostNode.extension.native.SynchronisationError: Source path "...

            >>> Reflector(
            ...     source_location='not existing',
            ...     target_location=__test_folder_path__ + 'target'
            ... ) # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            boostNode.extension.native.FileError: Invalid path "...

            >>> FileHandler(
            ...     __test_folder_path__ + 's/A/B', must_exist=False
            ... ).make_directorys()
            True

            >>> Reflector(
            ...     source_location=__test_folder_path__ + 's',
            ...     target_location=__test_folder_path__ + 't',
            ...     limit='10 apples'
            ... ) # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            boostNode.extension.native.SynchronisationError: Invalid cache-l...

            >>> Reflector(
            ...     source_location=__test_folder_path__ + 's',
            ...     target_location=__test_folder_path__ + 't',
            ...     limit='-1 byte'
            ... ) # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            boostNode.extension.native.SynchronisationError: Invalid cache-l...

            >>> Reflector(
            ...     source_location=__test_folder_path__ + 's',
            ...     target_location=__test_folder_path__ + 't',
            ...     target_rights=800
            ... ) # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            SynchronisationError: Reflection-rights "800" aren't written in ...

            >>> Reflector(
            ...     source_location=__test_folder_path__ + 's',
            ...     target_location=__test_folder_path__ + 't',
            ...     priority_locations=(__test_folder_path__ + 't',)
            ... ) # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            SynchronisationError: Priority path ".../t/" have to be inside...

            >>> Reflector(
            ...     source_location=__test_folder_path__ + 's',
            ...     target_location=__test_folder_path__ + 't',
            ...     priority_locations=('not existing',)
            ... ) # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            boostNode.extension.native.FileError: Invalid path "...not existi

            >>> Reflector(
            ...     source_location=__test_folder_path__ + 's',
            ...     target_location=__test_folder_path__ + 't',
            ...     priority_locations=(__test_folder_path__ + '../',),
            ... ) # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            boostNode.extension.native.SynchronisationError: ...have to be in
        '''

                # region properties

        '''Count all real files existing in source.'''
        self._number_of_files = 0
        '''Count all edited files during the creation process.'''
        self._edited_number_of_files = 0
        '''
            Lists which will be created before the reflection starts. It
            provides a list of all files in descending order depending on there
            file-sizes.
        '''
        self._files = []
        self._priority_files = []
        '''Defines source and target objects for there locations.'''
        self.source_location = FileHandler(location=self.source_location)
        self.target_location = FileHandler(
            location=self.target_location, make_directory=True,
            right=self.target_rights)
        self.given_limit = self.limit
        self.limit = FileHandler.determine_size_from_string(
            size_and_unit=self.limit)
        self.priority_locations = builtins.list(builtins.set(
            self.priority_locations))
        self.exclude_locations = builtins.list(builtins.set(
            self.exclude_locations))

                # endregion

        self._validate_inputs()._log_status()
        if not __test_mode__:
            self._create_or_synchronize_back()
        return self

            # endregion

    @JointPoint
## python3.3     def _create_or_synchronize_back(self: Self) -> Self:
    def _create_or_synchronize_back(self):
        '''
            Synchronizes and/or creates a new reflection cache dependent on
            given command line arguments.
        '''
        if self.synchronize_back:
            target_size = self.target_location.get_size(
                limit=self.minimum_reflection_size_in_byte)
            '''
                Check only for minimum reflection size if process was invoked
                via command line.
            '''
            if(self._command_line_arguments and
               target_size < self.minimum_reflection_size_in_byte and
               not CommandLine.boolean_input(
                   question='Reflection has only a size of %s. Do you want to '
                            'continue? {boolean_arguments}: ' %
                            self.target_location.human_readable_size)):
                return self
            self.synchronize_back_to_source()
            if self.create:
                self.create_cache()
        else:
            self.create_cache()
        __logger__.info(
            '{program} {version} {status} finished successful.'.format(
                program=__module_name__, version=__version__,
                status=__status__))
        return self

    @JointPoint
## python3.3     def _validate_inputs(self: Self) -> Self:
    def _validate_inputs(self):
        '''
            Validates the given parameters to the "self.__init__()" method.
            Checks if all paths makes sense and all inputs are in the right
            format.
        '''
        self._validate_paths()
        if self.limit is False or self.limit < 0:
            raise __exception__('Invalid cache-limit.')
        elif(not (builtins.isinstance(
                self.target_rights, builtins.int) and
            builtins.len(builtins.str(self.target_rights)) == 3 and
            self.target_rights >= 0 and self.target_rights <= 777)
        ):
            raise __exception__(
                'Reflection-rights "%s" aren\'t written in a convenient way '
                'like "770".', self.target_rights)
        return self._check_path_lists()

    @JointPoint
## python3.3     def _validate_paths(self: Self) -> Self:
    def _validate_paths(self):
        '''
            Validates source and target (reflection) path.
        '''
        if not self.source_location.path:
            raise __exception__(
                'Invalid source path "%s".', self.source_location.path)
        elif not self.target_location.path:
            raise __exception__(
                'Invalid target path "%s".', self._target.path)
        elif(self.source_location.path in self.target_location.path or
             self.target_location.path in self.source_location.path):
            raise __exception__(
                'Source path "%s" and reflection path "%s" have to be in '
                'different locations.', self.source_location.path,
                self.target_location.path)
        return self

    @JointPoint
## python3.3     def _check_path_lists(self: Self) -> Self:
    def _check_path_lists(self):
        '''
            Checks if all given paths lists are in locations which makes
            sense, to prevent user for failures.
        '''
        return self._check_path_in_source(
            paths=self.priority_locations, path_type='Priority'
        )._check_path_in_source(
            paths=self.exclude_locations, path_type='Exclude')

    @JointPoint
## python3.3
##     def _check_path_in_source(
##         self: Self, paths: collections.Iterable, path_type='Given'
##     ) -> Self:
    def _check_path_in_source(self, paths, path_type='Given'):
##
        '''
            Checks if the given paths are in source location. This method
            uses serves as helper method for "self._check_path_lists()".

            "path_type" is an optional string which describes the meaning of
                        the given paths. They are used for an exact user
                        feedback for whats going on.

            Examples:

            >>> FileHandler(
            ...     location=__test_folder_path__ + 'source4/A/B/C',
            ...     must_exist=False
            ... ).make_directorys()
            True
            >>> reflector = Reflector(
            ...     source_location=__test_folder_path__ + 'source4/A',
            ...     target_location=__test_folder_path__ + 'target4')
            >>> reflector._check_path_in_source(
            ...     paths=[__test_folder_path__ + 'source4/A',
            ...            __test_folder_path__ + 'source4/A/B/C']
            ... ) # doctest: +ELLIPSIS
            Object of "Reflector" with source path "...
            >>> reflector._check_path_in_source(
            ...     paths=[__test_folder_path__ + 'source4/A/B',
            ...            __test_folder_path__ + 'source4/']
            ... ) # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            boostNode.extension.native.SynchronisationError: ...source4...
        '''
        paths = builtins.list(paths)
        for index, path in builtins.enumerate(paths):
            path = FileHandler(location=path).path
            paths[index] = path
            if not self.source_location.path in path:
                raise __exception__(
                    '%s path "%s" have to be inside the source location '
                    '"%s".', path_type.capitalize(), path,
                    self.source_location.path)
        return self

    @JointPoint
## python3.3     def _log_status(self: Self) -> Self:
    def _log_status(self):
        '''
            Logs the initial status of the current Reflector instance.
            Output is written to standard output or output buffer.
        '''
        given_limit = ''
        if ('%s byte' % self.limit) != self.given_limit:
            given_limit = ' ("%s")' % self.given_limit
        native_symbolic_link_option = 'disabled'
        if self.use_native_symlinks:
            native_symbolic_link_option = 'enabled'
        __logger__.info(
            '\n\nInitialize {class_name} with logging level "{log_level}".\n\n'
            'source path: "{source_path}"\n'
            'reflection path: "{target_path}"\n'
            'reflection rights: "0{rights}"\n'
            'limit: {limit} byte{given_limit}\n'
            'priority paths: "{priority_locations}"\n'
            'exclude paths: "{exclude_locations}"\n'
            'native symbolic links: "{native_symbolic_link_option}"\n'.format(
                class_name=self.__class__.__name__,
                log_level=Logger.default_level[0],
                source_path=self.source_location.path,
                target_path=self.target_location.path,
                rights=self.target_rights, limit=self.limit,
                given_limit=given_limit,
                priority_locations='", "'.join(self.priority_locations),
                exclude_locations='", "'.join(self.exclude_locations),
                native_symbolic_link_option=native_symbolic_link_option))
        return self

            # region core concern

    @JointPoint
## python3.3     def _create_reflection_files(self: Self) -> Self:
    def _create_reflection_files(self):
        '''
            Iterates throw all files which should be included in
            the reflection. They will be sorted by its file-size in
            descending order. Small files will be preferred.
            In that way the maximum number of files which fits to
            the cache-limit will be copied in the reflection location.
        '''
        self._priority_files.sort()
        self._files.sort()
        self._number_of_files = builtins.len(self._priority_files) +\
            builtins.len(self._files)
        for size, relative_path in self._priority_files + self._files:
            if Platform.check_thread():
                return self
            source = FileHandler(
                location=self.source_location.path + relative_path)
            self._edited_number_of_files += 1
            if(self.limit >= size or
               size <= source.dummy_size and not self.use_native_symlinks or
               size <= source.BLOCK_SIZE_IN_BYTE and
               self.use_native_symlinks):
                self._copy_reflection_file(
                    source, path=relative_path, size=size)
            else:
                self._create_reflection_link(source, path=relative_path)
        return self

    @JointPoint
## python3.3
##     def _copy_reflection_file(
##         self: Self, source: FileHandler, path: builtins.str,
##         size: builtins.float
##     ) -> Self:
    def _copy_reflection_file(self, source, path, size):
##
        '''
            Serves as helper method for "_create_reflection_files()".
            Copies given files in source to its pendant in the reflection
            area.

            "source" is a directory object with the file in source to copy.
            "path" is the relative path to the new file in the reflection
                   area.
            "size" is the given files size.
        '''
        __logger__.info(
            'Copying file "{source}" to "{target}". '
            '({edited_number_of_files}/{number_of_files} {percent}%)'.format(
                source=source.path, target=self.target_location.path + path,
                edited_number_of_files=self._edited_number_of_files,
                number_of_files=self._number_of_files,
                percent=self.status_in_percent))
        source.copy(
            target=self.target_location.path + path,
            right=self.target_rights)
        self.limit -= size
        return self

    @JointPoint
## python3.3
##     def _create_reflection_link(
##         self: Self, source: FileHandler, path: builtins.str
##     ) -> Self:
    def _create_reflection_link(self, source, path):
##
        '''
            Creates a link to the given source element in target.

            "source" is a handler object with the file in source to link.
            "path" is the relative path to the new link in the reflection
                   area.
        '''
        __logger__.info(
            'Creating link from "{source}" to "{target}". '
            '({edited_number_of_files}/{number_of_files} {percent}%)'.format(
                source=source.path, target=self.target_location.path + path,
                edited_number_of_files=self._edited_number_of_files,
                number_of_files=self._number_of_files,
                percent=self.status_in_percent))
        if self.use_native_symlinks:
            source.make_symbolic_link(target=self.target_location.path + path)
        else:
            source.make_portable_link(target=self.target_location.path + path)
        return self

    @JointPoint
## python3.3
##     def _relocate_moved_file(
##         self: Self, file: FileHandler
##     ) -> builtins.bool:
    def _relocate_moved_file(self, file):
##
        '''
            Determines if the given Handler object ("file") was
            relocated since last cache creation. If "file" was relocated the
            file will also be relocated in source.

            Returns "True" if relocation where successful or "False"
            otherwise.
        '''
        if file.is_symbolic_link():
            linked_path = file.read_symbolic_link(as_object=True)
            if(linked_path.path[:builtins.len(self.source_location.path)] ==
                self.source_location.path
               ):
                relocated = FileHandler(
                    location=self.source_location.path + file.path[
                        builtins.len(self.target_location.path):],
                    must_exist=False)
                if not relocated.is_file():
                    return self._relocate_missing_file(relocated, linked_path)
            return False
        return True

    @JointPoint
## python3.3
##     def _relocate_missing_file(
##         self: Self, relocated: FileHandler, linked_path: FileHandler
##     ) -> builtins.bool:
    def _relocate_missing_file(self, relocated, linked_path):
##
        '''
            Serves as helper method for "_relocate_moved_file()".
            It relocates a file in the source, if it was relocated in the
            reflection area.

            "relocated" is a file which should be relocated.
            "linked_path" The new path for the given relocated file.

            Returns "True" if relocation where successful or "False"
            otherwise.
        '''
        relocated_directory_path = FileHandler(
            location=relocated.directory_path, must_exist=False)
        if not relocated_directory_path.is_directory():
            __logger__.info(
                'Create directory path "%s" for relocation of "%s".',
                relocated_directory_path.path, linked_path.path)
            relocated_directory_path.make_directorys()
        if linked_path:
            __logger__.info(
                'Relocate "%s" to "%s".', linked_path.path, relocated.path)
            return linked_path.move(target=relocated.path)
        __logger__.warning(
            'Inconsistent reflection "%s". Do not manipulate your source or '
            'create links from source to reflection manually!',
            linked_path.path)
        return True

    @JointPoint
## python3.3
##     def _copy_cache_to_source(
##         self: Self, file: FileHandler
##     ) -> builtins.bool:
    def _copy_cache_to_source(self, file):
##
        '''
            Copy a real (not dummy files or symbolic links) cache file to
            source.

            Returns "True" if file-copy where successful or "False"
            otherwise.
        '''
        if not self.is_path_in_paths(
            search=file, paths=self.exclude_locations
        ):
            target_path_len = builtins.len(self.target_location.path)
            source_file = FileHandler(
                location=self.source_location.path + file.path[
                    target_path_len:],
                must_exist=False)
            if file.is_symbolic_link():
                return self._copy_link_in_cache_to_source(
                    source_file, file, target_path_len)
            if file.is_file():
                __logger__.info(
                    'Copying file "%s" to "%s".', file.path, source_file.path)
                return file.copy(
                    target=source_file, right=self.target_rights)
            if file.is_directory() and not source_file.is_directory():
                __logger__.info(
                    'Copying directory "%s" to "%s".', file.path,
                    source_file.path)
                if source_file.is_file():
                    source_file.unlink()
                return source_file.make_directory(
                    right=self.target_rights)
            return True

    @JointPoint
## python3.3
##     def _copy_link_in_cache_to_source(
##         self: Self, source_file: FileHandler, file: FileHandler,
##         target_path_len: builtins.int
##     ) -> builtins.bool:
    def _copy_link_in_cache_to_source(
        self, source_file, file, target_path_len
    ):
##
        '''
            Copies link in the reflection area which wasn't interpreted as
            dummy file for a real file in the source area.

            "source_file" The source location where the given reflection file
                          will be located. It's the analogical location to the
                          given file location.
            "file" The link-file in the reflection area.
            "target_path_len" Number of chars in the path to link file in
                              cache.

            Returns "True" if all file-copies where successful or "False"
            if something goes wrong or a symlink circle was broken.
        '''
        link = file.read_symbolic_link(as_object=True)
        if link.path[:target_path_len] == self.target_location.path:
            new_link = FileHandler(
                location=self.source_location.path + link.path[
                    target_path_len:],
                must_exist=False)
## python3.3
##             if(not source_file.is_symbolic_link() or
##                 source_file.read_symbolic_link(as_object=True) != new_link
##                ):
            if(not source_file.is_symbolic_link() or
                not (source_file.read_symbolic_link(
                     as_object=True) == new_link)
               ):
##
                __logger__.info(
                    'Link "%s" to "%s".', source_file.path, new_link.path)
                return new_link.make_symbolic_link(
                    target=source_file, force=True)
            __logger__.info(
                'Leave "%s" unchanged because it is pointing to corresponding'
                ' file in source as "%s" in target.', source_file.path,
                file.path)
        elif(link.path[:builtins.len(self.source_location.path)] !=
             self.source_location.path):
## python3.3
##             if(not source_file.is_symbolic_link() or
##                source_file.read_symbolic_link(as_object=True) !=
##                file.read_symbolic_link(as_object=True)):
            if not (source_file.read_symbolic_link(as_object=True) ==
                    file.read_symbolic_link(as_object=True)):
##
                __logger__.info('Copy link "%s" as link.', file.path)
                return link.make_symbolic_link(source_file, force=True)
            __logger__.info(
                'Leave "%s" unchanged because "%s" is pointing to same file.',
                source_file.path, file.path)
        return True

    @JointPoint
## python3.3
##     def _delete_source_file_not_existing_in_target(
##         self: Self, file: FileHandler
##     ) -> builtins.bool:
    def _delete_source_file_not_existing_in_target(self, file):
##
        '''
            Delete a given source file if deleted in cache since last cache
            creation.

            Returns "True" if file-deletion where successful or "False"
            otherwise.
        '''
        if(not self.is_path_in_paths(
            search=file, paths=self.exclude_locations)
           ):
            target = FileHandler(
                location=self.target_location.path +
                file.path[builtins.len(self.source_location.path):],
                must_exist=False)
            if(file.is_directory() and not target.is_directory() or
                file.is_file() and not target.is_file()
               ):
                __logger__.info('Remove "%s".', file.path)
                return file.remove_deep()
        return True

    @JointPoint
## python3.3
##     def _create_reflection_structure(
##         self: Self, file: FileHandler, target: FileHandler, priority=False
##     ) -> builtins.bool:
    def _create_reflection_structure(
        self, file, target, priority=False
    ):
##
        '''
            Copies or represent a file in the source in reflection area.

            "file" A file in the source area.
            "target" The analogical location of "file" in the cache area.
            "priority" Determines if the current handling file object is in an
                       higher priority location.

            Returns "True" if file-operation where successful or "False"
            otherwise.
        '''
        if(not self.is_path_in_paths(
            search=file, paths=self.exclude_locations)
           ):
            return self._handle_source_element(
                source_file=file,
                target_file=FileHandler(
                    location=target.path + file.name, must_exist=False),
                priority=(priority or self.is_path_in_paths(
                    search=file, paths=self.priority_locations)))
        __logger__.info('Ignore exclude location: "%s".', file.path)
        return True

    @JointPoint
## python3.3
##     def _handle_source_element(
##         self: Self, source_file: FileHandler, target_file: FileHandler,
##         priority: builtins.bool
##     ) -> builtins.bool:
    def _handle_source_element(
        self, source_file, target_file, priority
    ):
##
        '''
            Serves as helper method for "self._create_reflection_structure()".
            Handles each source element which should be represented in cache.

            "source_file" A file in the source area.
            "target_file" The analogical location of "file" in the cache area.
            "priority" Determines if the current handling file object is in an
                       higher priority location.

            Returns "True" if all file-operations where successful or "False"
            otherwise.
        '''
        if source_file.is_symbolic_link():
            return self._handle_source_link(source_file, target_file)
        elif source_file.is_directory():
            __logger__.info(
                'Generating target folder: "%s".', target_file.path)
            target_file.make_directory(right=self.target_rights)
            return source_file.iterate_directory(
                function=self._create_reflection_structure,
                target=target_file,
                priority=priority,
                recursive_in_link=False)
        __logger__.info('Analyzing file: "%s".', source_file.path)
        if source_file.is_device_file():
            __logger__.warning(
                'Ignoring device file: "%s".', source_file.path)
        else:
            appending_list = self._priority_files if priority else self._files
            appending_list.append(
                (source_file.size, source_file.path[builtins.len(
                    self.source_location.path):]))
        return True

    @JointPoint
## python3.3
##     def _handle_source_link(
##         self: Self, source_file: FileHandler, target_file: FileHandler
##     ) -> builtins.bool:
    def _handle_source_link(self, source_file, target_file):
##
        '''
            Serves as helper method for "self._handle_source_element()".
            Handles each source link element which should be represented in
            cache.

            "source_file" A file in the source area.
            "target_file" The analogical location of "file" in the cache
                              area.

            Returns "True" if file-link-operation where successful or
            "False" otherwise.
        '''
        source_path_len = builtins.len(self.source_location.path)
        link = source_file.read_symbolic_link(as_object=True)
        if link.path[:source_path_len] == self.source_location.path:
            '''
                Link refers to a location in source; it will be bend to its
                corresponding location in target.
            '''
            new_link = FileHandler(
                location=self.target_location.path + link.path[
                    source_path_len:],
                must_exist=False)
            __logger__.info(
                'Link "%s" to "%s".', target_file.path, new_link.path)
            return new_link.make_symbolic_link(
                target=target_file, force=True)
        elif(link.path[:builtins.len(self.target_location.path)] !=
             self.target_location.path):
            '''
                Link doesn't refer to any location in source; it will be
                leaved as same link.
            '''
            __logger__.info('Copy link "%s" as link.', source_file.path)
            return link.make_symbolic_link(target_file, force=True)
        __logger__.warning(
            'Link "%s" refers to reflection location. It will be ignored and '
            'deleted on next synchronisation.', source_file.path)
        return True

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
