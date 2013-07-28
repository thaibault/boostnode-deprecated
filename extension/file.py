#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-

# region vim modline

# vim: set tabstop=4 shiftwidth=4 expandtab:
# vim: foldmethod=marker foldmarker=region,endregion:

# endregion

# region header

'''
    This module is a high level interface for interaction with
    file systems. This class provides a full object oriented way to handle
    file system objects. Besides a number of new supported interactions with
    the file systems it offers all core file-system methods by the pythons
    native "shutil" and "os" module as wrapper methods.
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

## python2.7 import __builtin__ as builtins
import builtins
import ctypes
## python2.7 import codecs
pass
import collections
import copy
import inspect
import mimetypes
import os
import re
import shutil
import sre_constants
import stat
import sys
## python2.7 pass
import types

for number in (3, 4):
    sys.path.append(os.path.abspath(sys.path[0] + number * ('..' + os.sep)))

import boostNode.extension.dependent
import boostNode.extension.native
import boostNode.extension.system
import boostNode.extension.type
import boostNode.paradigm.aspectOrientation
import boostNode.paradigm.objectOrientation

# endregion


# region classes

class Handler(boostNode.paradigm.objectOrientation.Class):
    '''
        The main class for initializing new file system objects to handle them
        in an object oriented way.
    '''

    # region constant properties

        # region public properties

    '''
        Pattern for supported formats to handle size of file system elements.
    '''
    REGEX_FORMAT = '^([0-9]+\.?[0-9]{{0,2}})\s*({units})$'
    '''Supported formats to handle the size of file.'''
    FORMATS = {'Byte': {'notations': ('byte', 'b'),
                        'decimal_factor': 1,
                        'binary_factor': 1,
                        'useful_range': (0, 1024)},
               'Kilobyte': {'notations': ('kb', 'kib',
                                          'kilobyte', 'kibibyte',
                                          'kbyte', 'kibyte',
                                          'kilob', 'kibib'),
                            'decimal_factor': 10 ** 3,
                            'binary_factor': 2 ** 10,
                            'useful_range': (1024 + 1, 1024 ** 2)},
               'Megabyte': {'notations': ('mb', 'mib',
                                          'megabyte', 'mebibyte',
                                          'mbyte', 'mibyte',
                                          'megab', 'mebib'),
                            'decimal_factor': 10 ** 6,
                            'binary_factor': 2 ** 20,
                            'useful_range': ((1024 ** 2) + 1, 1024 ** 3)},
               'Gigabyte': {'notations': ('gb', 'gib',
                                          'gigabyte', 'gibibyte',
                                          'gbyte', 'gibyte',
                                          'gigab', 'gibib'),
                            'decimal_factor': 10 ** 9,
                            'binary_factor': 2 ** 30,
                            'useful_range': ((1024 ** 3) + 1, 1024 ** 4)},
               'Terabyte': {'notations': ('tb', 'tib',
                                          'terabyte', 'tebibyte',
                                          'tbyte', 'tibyte',
                                          'terab', 'tebib'),
                            'decimal_factor': 10 ** 12,
                            'binary_factor': 2 ** 40,
                            'useful_range': ((1024 ** 4) + 1, 1024 ** 5)},
               'Petabyte': {'notations': ('pb', 'pib',
                                          'petabyte', 'pebibyte',
                                          'pbyte', 'pibyte',
                                          'petab', 'pebib'),
                            'decimal_factor': 10 ** 15,
                            'binary_factor': 2 ** 50,
                            'useful_range': ((1024 ** 5) + 1, 1024 ** 6)},
               'Exabyte': {'notations': ('eb', 'eib',
                                         'exabyte', 'exbibyte',
                                         'ebyte', 'eibyte',
                                         'exab', 'exib'),
                           'decimal_factor': 10 ** 18,
                           'binary_factor': 2 ** 60,
                           'useful_range': ((1024 ** 6) + 1, 1024 ** 7)},
               'Zettabyte': {'notations': ('zb', 'zib',
                                           'zettabyte', 'zebibyte',
                                           'zbyte', 'zibyte',
                                           'zettab', 'zebib'),
                             'decimal_factor': 10 ** 21,
                             'binary_factor': 2 ** 70,
                             'useful_range': ((1024 ** 7) + 1, 1024 ** 8)},
               'Yottabyte': {'notations': ('yb', 'yib',
                                           'yottabyte', 'yobibyte',
                                           'ybyte', 'yibyte',
                                           'yottab', 'yobib'),
                             'decimal_factor': 10 ** 24,
                             'binary_factor': 2 ** 80,
                             'useful_range': ((1024 ** 8) + 1, None)}}
    '''Defines the size of an empty folder, a symbolic link or empty file.'''
    BLOCK_SIZE_IN_BYTE = 4096
    '''
        Defines the maximum number of chars containing in a file
        (or directory) name.
    '''
    MAX_FILE_NAME_LENGTH = 255
    '''
        Defines the default format of current os for calculating with file
        sizes.
    '''
    DECIMAL = False
    '''Defines char set for handling text-based files internally.'''
    DEFAULT_ENCODING = 'utf_8'
    '''Defines the maximum number of signs in a file path.'''
    MAX_PATH_LENGTH = 32767
    '''Defines the maximum number of digits for the biggest file-size.'''
    MAX_SIZE_NUMBER_LENGTH = 24  # 10^21 byte = 1 Yottabyte (-1 byte)
    '''Defines all mimetypes describing a media file.'''
    MEDIA_MIMETYPE_PATTERN = '^audio/.+', '^video/.+'
    '''
        This file pattern is used for all files which should easily open the
        referenced file with a useful program.
        You shouldn't use placeholder more than once.
        Because portable-file-checks could be fail. For bash functionality you
        can declare a bash variable and use how often you need.
        Internal bash variable pattern: "$bash_variable".
    '''
    PORTABLE_DEFAULT_LINK_PATTERN = (
        "#!/bin/bash\n\n# {label} portable link file\n\nsize={size}\ntarget='"
        "{path}'\n\n'{executable_path}' --open \"$target\"")
    PORTABLE_WINDOWS_DEFAULT_LINK_PATTERN = (
        "{label} portable link file\n\n$size={size}\ntarget='"
        "{path}'\n\n'{executable_path}' --open \"$target\"")

    '''
        This file pattern is used for all media files which should easily open
        the referenced media with a useful program on the one hand and behave
        like a real media file on the other hand (e.g. in drag and drop them
        into a media player's gui).
        Like in "PORTABLE_DEFAULT_LINK_PATTERN" you shouldn't use
        placeholders twice.
    '''
    PORTABLE_MEDIA_LINK_PATTERN = (
        '[playlist]\n\nFile1=$path\nTitle1=$name\nLength1=$size\n\n$label '
        'portable link file')

        # endregion

    # endregion

    # region dynamic properties

        # region protected properties

    '''
        Defines a virtual root path for all methods. Through these class
        objects aren't locations except in "_root_path" available.
    '''
    _root_path = '/'
    _root_path_initialized = False
    '''Defines the encoding for writing and reading text-based files.'''
    _encoding = ''
    '''
        This properties are generated at runtime on base of the two
        class constants "PORTABLE_DEFAULT_LINK_PATTERN" and
        "PORTABLE_MEDIA_LINK_PATTERN".
    '''
    _portable_link_pattern = ''
    _portable_link_content = ''
    _portable_regex_link_pattern = ''
    '''Saves the initially given path without any transformations.'''
    _initialized_path = ''
    '''Indicates if current file object has an file extension.'''
    _has_extension = True
    '''Properties depending on the given file system object-/s.'''
    _path = ''
    _name = ''
    _basename = ''
    _extension = ''
    _extension_suffix = ''
    _directory_path = ''
    _relative_path = ''
    _content = ''
    _size = 0
    _dummy_size = 0
    _human_readable_size = 0
    _free_space = 0
    _disk_used_space = 0
    _timestamp = 0
    _lines = 0
    _mimetype = _type = None
    _respect_root_path = True
    _output_with_root_prefix = False
    '''
        Properties to realize an iteration over all elements in a given
        directory.
    '''
    _current_element_index = 0
    _next_element_index = 0

        # endregion

    # endregion

    # region dynamic methods

        # region public methods

            # region special methods

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def __init__(
##         self, location=None, make_directory=False, must_exist=True,
##         encoding='', respect_root_path=True, output_with_root_prefix=False,
##         has_extension=True, *arguments, **keywords
##     ):
    def __init__(
        self: boostNode.extension.type.Self, location=None,
        make_directory=False, must_exist=True, encoding='',
        respect_root_path=True, output_with_root_prefix=False,
        has_extension=True, *arguments: builtins.object,
        **keywords: builtins.object
    ) -> None:
##
        '''
            Initialize a new instance of a given file system object by path.

            "location" is path or "Handler" referencing to file object.
            "make_directory" Make directory of path object if given location
                             doesn't exists.
            "right" Define rights for all created object with an "Handler"
                    object.
            "must_exist" Throws an exception if the given path doesn't exists
                         if this argument is "True".
            "encoding" Define encoding for reading and writing files.
            "respect_root_path" Defines if a previous statically defined
                                virtual root path should be considered.
            "output_with_root_prefix" Defines if "get_path()" returns a path
                                      with or without root path prefixed.

            Examples:

            >>> Handler(
            ...     location=__test_folder__ + 'init_not_existing'
            ... ) # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            boostNode.extension.native.FileError: Invalid path...not_existin...

            >>> handler = Handler(
            ...     location=__test_folder__ + 'init_not_existing',
            ...     make_directory=True)
            >>> handler # doctest: +ELLIPSIS
            Object of "Handler" with path "...init_not_existing..."...
            >>> os.path.isdir(handler.path)
            True

            >>> Handler(
            ...     location=__test_folder__ + 'init_not_existing2',
            ...     must_exist=False) # doctest: +ELLIPSIS
            Object of "Handler" with path "...init_not_existing2...(undefined).

            >>> Handler(location=__file_path__).basename
            'file'

            >>> Handler(location='/not//real',
            ...         must_exist=False).path # doctest: +ELLIPSIS
            '...not...real'

            >>> Handler(location=Handler()).path # doctest: +ELLIPSIS
            '...boostNode...extension...'

            >>> root_path_backup = Handler._root_path
            >>> Handler._root_path = Handler(
            ...     __test_folder__ + 'init_root_directory',
            ...     make_directory=True
            ... )._path

            >>> location = Handler('/init_A', must_exist=False)
            >>> location.path # doctest: +ELLIPSIS
            '...init_A...'
            >>> location._path # doctest: +ELLIPSIS
            '...init_root_directory...init_A...'

            >>> location = Handler(
            ...     __test_folder__  + 'init_root_directory/' + 'init_A',
            ...     must_exist=False, respect_root_path=False)
            >>> location.path # doctest: +ELLIPSIS
            '...init_A...'
            >>> location._path # doctest: +ELLIPSIS
            '...init_root_directory...init_A...'

            >>> Handler(
            ...     __test_folder__ + 'init_A', respect_root_path=False
            ... ) # doctest: +ELLIPSIS +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            boostNode.extension.native.FileError: Invalid path "...init_A" ...

            >>> try:
            ...     Handler(
            ...         __test_folder__ + 'init_A', make_directory=True)
            ... except:
            ...     True
            True

            >>> Handler._root_path = root_path_backup
        '''
        if not encoding:
            encoding = self.DEFAULT_ENCODING
        self._encoding = encoding
        self._respect_root_path = respect_root_path
        self._output_with_root_prefix = output_with_root_prefix
        self._initialized_path = self._initialize_location(location)
        self._initialize_path()
        self._prepend_root_path()
        self._handle_path_existence(
            location, make_directory, must_exist, arguments, keywords
        )._initialize_platform_dependencies()
        if(builtins.len(self.name) and not '.' in self.name[1:] or
           self.is_directory()):
            self._has_extension = False
        else:
            self._has_extension = has_extension

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def __iter__(self):
    def __iter__(
        self: boostNode.extension.type.Self
    ) -> types.GeneratorType:
##
        '''
            Invokes if the current object is tried to iterate.

            Examples:

            >>> for file in Handler(location='.'):
            ...     print('"' + str(file) + '"') # doctest: +ELLIPSIS
            "...file.py..."
        '''
        return (element for element in self.list())

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def __nonzero__(self):
    def __bool__(self: boostNode.extension.type.Self) -> builtins.bool:
##
        '''
            Invokes when the object is tried to convert in a boolean value.

            Examples:

            >>> bool(Handler())
            True

            >>> bool(Handler(
            ...     location=__test_folder__ + 'nonzero_not_existing_file',
            ...     must_exist=False))
            False

            >>> bool(Handler(location=__file_path__))
            True

            >>> bool(Handler(location=__test_folder__))
            True
        '''
        return self.is_element()

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def __eq__(self, other):
    def __eq__(
        self: boostNode.extension.type.Self, other: builtins.object
    ) -> builtins.bool:
##
        '''
            Invokes if a comparison of two "Handler" objects is done.

            Examples:

            >>> Handler(
            ...     location=__test_folder__ + 'eq_a/b', must_exist=False
            ... ) == Handler(
            ...     location=__test_folder__ + 'eq_a//b/', must_exist=False)
            True

            >>> Handler(
            ...     location=__test_folder__ + 'eq_a/b', must_exist=False
            ... ) == Handler(
            ...     location=__test_folder__ + 'eq_a/b/c', must_exist=False)
            False

            >>> __test_folder__ + 'eq_a/b' == Handler(
            ...     location=__test_folder__ + 'eq_a/b', must_exist=False)
            False
        '''
        if builtins.isinstance(other, self.__class__):
            return self._path == other._path
        return False

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def __hash__(self):
    def __hash__(self: boostNode.extension.type.Self) -> builtins.int:
##
        '''
            Returns a hash value for current path as string.

            Examples:

            >>> isinstance(hash(Handler()), int)
            True
        '''
        return builtins.hash(self._path)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def __getitem__(self, key):
    def __getitem__(
        self: boostNode.extension.type.Self, key: builtins.int
    ) -> boostNode.extension.type.SelfClassObject:
##
        '''
            Triggers if an element is tried to get with the "[]" operator.

            Examples:

            >>> Handler()[0] # doctest: +ELLIPSIS
            Object of "Handler" with path "..." (...).
        '''
        return builtins.tuple(self.list())[key]

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def __delitem__(self, key):
    def __delitem__(
        self: boostNode.extension.type.Self, key: builtins.int
    ) -> builtins.bool:
##
        '''
            Deletes the specified item from the file system.

            Examples:

            >>> directory = Handler(
            ...     __test_folder__ + 'delitem', make_directory=True)
            >>> file = Handler(directory.path + 'file', must_exist=False)
            >>> file.content = ' '
            >>> file.is_file()
            True
            >>> del directory[0]
        '''
        return self[key].remove_deep()

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def __contains__(self, item):
    def __contains__(
        self: boostNode.extension.type.Self,
        item: (boostNode.extension.type.SelfClassObject,
               builtins.str)
    ) -> builtins.bool:
##
        '''
            Is triggered if you want to determine if an object is in a
            "Handler" object.

            Examples:

            >>> Handler(location=__file_path__) in Handler(location=Handler(
            ...     location=__file_path__
            ... ).directory_path)
            True

            >>> Handler(
            ...     location=__test_folder__ + 'contains_not_existing.py',
            ...     must_exist=False) in Handler()
            False

            >>> 'not_existing_file' in Handler()
            False

            >>> __file_path__ in Handler()
            True
        '''
        if builtins.isinstance(item, self.__class__):
            return item in self.list()
        else:
            for element in self:
                if item in (element._path, element.relative_path):
                    return True
        return False

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def __len__(self):
    def __len__(self: boostNode.extension.type.Self) -> builtins.int:
##
        '''
            Is triggered if you use the pythons native "builtins.len()"
            function on a "Handler" object.

            Examples:

            >>> len(Handler(
            ...     location=__test_folder__ + 'len_not_existing_location',
            ...     must_exist=False))
            0

            >>> len(Handler(location=__file_path__))
            1

            >>> len(Handler(Handler().directory_path)) > 1
            True
        '''
        if self.is_directory():
            return builtins.len(builtins.list(self.list()))
        elif self.is_file():
            return 1
        return 0

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def __str__(self):
    def __str__(self: boostNode.extension.type.Self) -> builtins.str:
##
        '''
            Is triggered if this object should be converted to string.

            Examples:

            >>> str(Handler(location=__file_path__)) # doctest: +ELLIPSIS
            '...file.py'
        '''
        return self.path

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def __repr__(self):
    def __repr__(self: boostNode.extension.type.Self) -> builtins.str:
##
        '''
            Invokes if this object should describe itself by a string.

            Examples:

            >>> repr(Handler(location=__file_path__)) # doctest: +ELLIPSIS
            'Object of "Handler" with path "...file.py" ... (file).'

            >>> link = Handler(__test_folder__ + 'repr_link', must_exist=False)
            >>> if boostNode.extension.system.Platform(
            ...     ).operating_system == 'windows':
            ...     repr(link)
            ... else:
            ...     created = Handler(
            ...         location=__file_path__
            ...     ).make_symbolic_link(link)
            ...     repr(link) # doctest: +ELLIPSIS
            'Object of "Handler" with path ...'
        '''
        type = self.type
        if self.is_symbolic_link():
            type = 'link to "{path}"'.format(path=self.read_symbolic_link())
        return 'Object of "{class_name}" with path "{path}" and initially '\
            'given path "{given_path}" ({type}).'.format(
                class_name=self.__class__.__name__, path=self.path,
                given_path=self._initialized_path, type=type)

            # endregion

        # endregion

    # endregion

    # region static methods

        # region public methods

            # region getter methods

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python2.7
##     def get_root(cls):
    def get_root(
        cls: boostNode.extension.type.SelfClass
    ) -> boostNode.extension.type.SelfClassObject:
##
        '''
            Returns a file object referencing to the virtual root path.
        '''
        return cls(
            location=cls._root_path, respect_root_path=False,
            output_with_root_prefix=True)

            # endregion

            # region setter methods

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python2.7
##     def set_root(cls, location):
    def set_root(
        cls: boostNode.extension.type.SelfClass,
        location: (boostNode.extension.type.SelfClassObject, builtins.str)
    ) -> boostNode.extension.type.SelfClass:
##
        '''
            Normalizes root path.

            Examples:

            >>> root_path_backup = Handler._root_path

            >>> handler = Handler(
            ...     __test_folder__ + 'set_root', make_directory=True)
            >>> Handler.set_root(location=handler) # doctest: +ELLIPSIS
            <class '...Handler'>
            >>> Handler.get_root().path # doctest: +ELLIPSIS
            '...'

            >>> Handler._root_path = root_path_backup
        '''
        cls._root_path = cls(
            location, respect_root_path=False, output_with_root_prefix=True
        ).path
        return cls

            # endregion

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python2.7
##     def convert_size_format(
##         cls, size, format='byte', decimal=None, formats=None
##     ):
    def convert_size_format(
        cls: boostNode.extension.type.SelfClass,
        size: (builtins.int, builtins.float), format='byte',
        decimal=None, formats=None
    ) -> builtins.float:
##
        '''
            Converts between file size formats.

            "format" determines the returning file size unit.
            "decimal" determines if the decimal or binary interpretation
                      should be used.

            Examples:

            >>> Handler.convert_size_format(size=100, decimal=True)
            100.0

            >>> Handler.convert_size_format(
            ...     size=1024, format='kb', decimal=True)
            1.024

            >>> Handler.convert_size_format(
            ...     size=2 * 1024 ** 2, format='MB', decimal=False)
            2.0

            >>> Handler.convert_size_format(size=0)
            0.0

            >>> Handler.convert_size_format(size=5.2, formats={})
            5.2
        '''
        size = builtins.float(size)
        if decimal is None:
            decimal = cls.DECIMAL
        if formats is None:
            formats = cls.FORMATS
        factor_type = 'decimal_factor' if decimal else 'binary_factor'
        for name, properties in formats.items():
            for notation in properties['notations']:
                if format.lower() == notation:
                    return size / properties[factor_type]
        return size

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python2.7
##     def determine_size_from_string(
##         cls, size_and_unit, format='byte', decimal=None
##     ):
    def determine_size_from_string(
        cls: boostNode.extension.type.SelfClass,
        size_and_unit: builtins.str, format='byte', decimal=None
    ) -> (builtins.float, builtins.bool):
##
        '''
            Becomes a size with unit as string. And gives it as float or
            "False" (if given string hasn't match any number with a useful
            measure) back.

            Examples:

            >>> Handler.determine_size_from_string(size_and_unit='10 MB')
            10485760.0

            >>> Handler.determine_size_from_string(
            ...     size_and_unit='2KB', format='MB')
            0.001953125

            >>> Handler.determine_size_from_string(size_and_unit='2 byte')
            2.0

            >>> Handler.determine_size_from_string(
            ...     size_and_unit='2 bte', decimal=True)
            False
        '''
        if decimal is None:
            decimal = cls.DECIMAL
        match = re.compile(cls.REGEX_FORMAT.format(
            units=cls.determine_regex_units(formats=cls.FORMATS)
        )).match(size_and_unit.lower())
        if match:
            return cls.convert_size_format(
                size=cls.determine_byte_from_other(
                    size=builtins.float(match.group(1)),
                    formats=cls.FORMATS,
                    given_format=match.group(2),
                    decimal=decimal),
                format=format, decimal=decimal, formats=cls.FORMATS)
        return False

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python2.7
##     def determine_byte_from_other(
##         cls, size, formats, given_format='byte', decimal=None
##     ):
    def determine_byte_from_other(
        cls: boostNode.extension.type.SelfClass, size: builtins.float,
        formats: builtins.dict, given_format='byte', decimal=None
    ) -> builtins.float:
##
        '''
            Converts a given size format to byte format.

            Examples:

            >>> Handler.determine_byte_from_other(
            ...     size=10.0, formats=Handler.FORMATS, given_format='MB')
            10485760.0

            >>> Handler.determine_byte_from_other(
            ...     size=10.0, formats={})
            10.0
        '''
        if decimal is None:
            decimal = cls.DECIMAL
        factor_type = 'decimal_factor' if decimal else 'binary_factor'
        for name, properties in formats.items():
            for notation in properties['notations']:
                if given_format.lower() == notation:
                    return size * properties[factor_type]
        return size

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python2.7
##     def determine_regex_units(cls, formats=None):
    def determine_regex_units(
        cls: boostNode.extension.type.SelfClass, formats=None
    ) -> builtins.str:
##
        '''
            Returns a regular expression for validation if a given size format
            is valid. The pattern is created depending on the given size
            formats as dictionary.

            Examples:

            >>> Handler.determine_regex_units(
            ...     Handler.FORMATS
            ... ) # doctest: +ELLIPSIS
            '...tb...

            >>> Handler.determine_regex_units() # doctest: +ELLIPSIS
            '...tb...
        '''
        if formats is None:
            formats = cls.FORMATS
        units = ''
        for name, properties in formats.items():
            if units:
                units += '|'
            units += '|'.join(properties['notations'])
        return units

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python2.7
##     def determine_special_path_values(cls, operating_system=''):
    def determine_special_path_values(
        cls: boostNode.extension.type.SelfClass, operating_system=''
    ) -> builtins.tuple:
##
        '''
            Gives all platform dependent symbols for special file system
            locations.

            Examples:

            >>> Handler.determine_special_path_values(operating_system='unix')
            ('~',)

            >>> Handler.determine_special_path_values() # doctest: +ELLIPSIS
            (...)

            >>> Handler.determine_special_path_values('windows')
            ()
        '''
        if not operating_system:
            operating_system = boostNode.extension.system.Platform()\
                .operating_system
        if operating_system == 'windows':
            return ()
        return ('~',)

        # endregion

        # region protected methods

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python2.7
##     def _sort_by_file_types(cls, files, recursive_in_link):
    def _sort_by_file_types(
        cls: boostNode.extension.type.SelfClass, files: collections.Iterable,
        recursive_in_link: builtins.bool
    ) -> builtins.list:
##
        '''
            Sorts the given list of files. Files come first and folders later.

            Examples:

            >>> current_location = Handler()
            >>> temporary_file = Handler(
            ...     __test_folder__ + '_sort_by_file_types', must_exist=False)
            >>> temporary_file.content = 'A'
            >>> [temporary_file,
            ...  current_location] == Handler._sort_by_file_types([
            ...     current_location, temporary_file],
            ...     False)
            True

            >>> Handler._sort_by_file_types([], True)
            []
        '''
        sorted_files = []
        for file in files:
            if file.is_directory(allow_link=recursive_in_link):
                sorted_files.append(file)
            else:
                sorted_files.reverse()
                sorted_files.append(file)
                sorted_files.reverse()
        return sorted_files

        # endregion

    # endregion

    # region dynamic methods

        # region public methods

            # region getter methods

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def get_encoding(self):
    def get_encoding(self: boostNode.extension.type.Self) -> builtins.str:
##
        '''
            Returns encoding for current file handler. If no encoding was set
            "Handler.DEFAULT_ENCODING" is default.

            Examples:

            >>> Handler().encoding
            'utf_8'

            >>> Handler().get_encoding()
            'utf_8'

            >>> handler = Handler(__test_folder__ + 'test', must_exist=False)
            >>> handler.set_content(
            ...     'test', encoding='ascii'
            ... ) # doctest: +ELLIPSIS
            Object of "Handler" ...
            >>> handler.encoding
            'ascii'
        '''
        return self._encoding

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def get_extension(self):
    def get_extension(self: boostNode.extension.type.Self) -> builtins.str:
##
        '''
            Returns the current file extension or an empty string if current
            file hasn't an extension separated by a dot, current handler
            points to a none existing file object or a directory.

            Examples:

            >>> Handler().extension
            ''

            >>> Handler().get_extension()
            ''

            >>> Handler(location=__file_path__).extension
            'py'
        '''
        if self._has_extension:
            return self.name[builtins.len(self.basename) + 1:]
        return ''

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def get_timestamp(self):
    def get_timestamp(
        self: boostNode.extension.type.Self
    ) -> builtins.float:
##
        '''
            Getter method for time of last modification of the
            file system object referenced by "Handler".

            Examples:

            >>> isinstance(Handler(location=__file_path__).timestamp, float)
            True
        '''
        return os.stat(self._path).st_mtime

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def get_lines(self):
    def get_lines(self: boostNode.extension.type.Self) -> builtins.int:
##
        '''
            Returns the number of lines in the file content referenced by the
            "Handler" object.

            Examples:

            >>> test = Handler(
            ...     __test_folder__ + 'get_lines_test1', must_exist=False)
            >>> test.content = 'a\\nb\\nc\\n'
            >>> test.lines
            3

            >>> test = Handler(
            ...     __test_folder__ + 'get_lines_test2', must_exist=False)
            >>> test.content = ' '
            >>> test.lines
            1

            >>> test.content = ''
            >>> test.lines
            1

            >>> test = Handler(
            ...     __test_folder__ + 'get_lines_test3', must_exist=False)
            >>> test.content = 'a\\nb\\nca\\nb\\nc'
            >>> test.get_lines()
            5
        '''
        with builtins.open(self._path, mode='r') as file:
            for line in file:
                self._lines += 1
        return self._lines

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def get_size(self, limit=0, follow_link=True, *arguments, **keywords):
    def get_size(
        self: boostNode.extension.type.Self, limit=0, follow_link=True,
        *arguments: builtins.object, **keywords: builtins.object
    ) -> builtins.float:
##
        '''
            Calculates the used space for this object by the first request of
            the property "size".
            If the current handler points to none existing file on file system
            zero will be returned.
            This method has the additionally all parameters as
            "self.convert_size_format()".

            "limit" Break and return current calculated size if limit is
                    reached or doesn't if limit is 0. Limit is interpreted in
                    bytes.

            Examples:

            >>> test_size = Handler(
            ...     __test_folder__ + 'test_size', must_exist=False)
            >>> test_size.content = ' '
            >>> test_size.size
            1.0

            >>> test_size.content = ''
            >>> test_size.size
            0.0

            >>> test_size.get_size()
            0.0

            >>> test_size.get_size(limit=1000, follow_link=False)
            0.0

            >>> size = Handler(location='.').get_size(100)
            >>> size > 100
            True
            >>> isinstance(size, float)
            True

            >>> size = Handler(location='.').get_size(0)
            >>> size > 0
            True
            >>> isinstance(size, float)
            True

            >>> size = Handler(location='.').get_size(limit=200)
            >>> size > 200
            True
            >>> isinstance(size, float)
            True

            >>> size = Handler(location='.').size
            >>> size > 0
            True
            >>> isinstance(size, float)
            True

            >>> size = Handler('/').get_size(0)
            >>> size > 0
            True

            >>> size = Handler('/').get_size(limit=1)
            >>> size > 0
            True

            >>> link = Handler(
            ...     __test_folder__ + 'get_size_link', must_exist=False)
            >>> if boostNode.extension.system.Platform(
            ...     ).operating_system == 'windows':
            ...     True
            ... else:
            ...     created = Handler().make_symbolic_link(link)
            ...     size = link.get_size(1, follow_link=False)
            ...     size > 0
            True
        '''
        size = 0
        if os.path.ismount(self._path):
            size = self.disk_used_space
        elif self.is_directory(allow_link=follow_link):
            size = self.BLOCK_SIZE_IN_BYTE
            for file in self:
                if not limit or size < limit:
                    recursive_keywords = copy.deepcopy(keywords)
                    recursive_keywords['format'] = 'byte'
                    '''
                        Take this method type by another instance of this class
                        via introspection.
                    '''
                    size += builtins.getattr(
                        file, inspect.stack()[0][3]
                    )(
                        limit, follow_link=False, *arguments,
                        **recursive_keywords
                    ) + self.BLOCK_SIZE_IN_BYTE
        elif self.is_symbolic_link():
            size = self.BLOCK_SIZE_IN_BYTE
        else:
            size = os.path.getsize(self._path)
        return builtins.float(self.convert_size_format(
            size, *arguments, **keywords))

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def get_dummy_size(self, label=''):
    def get_dummy_size(
        self: boostNode.extension.type.Self, label=''
    ) -> builtins.int:
##
        '''
            Calculates the potential dummy size for a portable link pointing
            to this object.

            "label" is the actual used label for marking the text based
                    portable link files.

            Examples:

            >>> isinstance(
            ...     Handler(location=__file_path__).get_dummy_size(
            ...         label='LinkFile'),
            ...     int)
            True

            >>> isinstance(
            ...     Handler(location=__file_path__).dummy_size,
            ...     int)
            True

            >>> isinstance(Handler().dummy_size, int)
            True
        '''
        if self.is_file():
            self._dummy_size = builtins.len(
                self.portable_link_content % label)
        return self._dummy_size

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def get_human_readable_size(self, size=None):
    def get_human_readable_size(
        self: boostNode.extension.type.Self, size=None
    ) -> builtins.str:
##
        '''
            Represents a given file size in byte as human readable string.

            Examples:

            >>> Handler.DECIMAL = False
            >>> a = Handler(
            ...     __test_folder__ + 'get_human_readable_size_A',
            ...     make_directory=True)
            >>> b = Handler(__test_folder__ + 'get_human_readable_size_A')
            >>> a.human_readable_size == str(b.get_size(format='kb')) + ' kb'
            True

            >>> Handler().get_human_readable_size(size=100)
            '100.0 byte'

            >>> Handler().get_human_readable_size(size=(1024 ** 1) + 1)
            '1.0 kb'

            >>> Handler().get_human_readable_size(size=(1024 ** 2) + 1)
            '1.0 mb'

            >>> Handler().get_human_readable_size(size=(1024 ** 3) + 1)
            '1.0 gb'

            >>> Handler().get_human_readable_size(size=5 * (1024 ** 3) + 1)
            '5.0 gb'

            >>> Handler().get_human_readable_size(size=(1024 ** 4) + 1)
            '1.0 tb'

            >>> Handler().get_human_readable_size(size=(1024 ** 5) + 1)
            '1.0 pb'

            >>> Handler().get_human_readable_size(size=(1024 ** 6) + 1)
            '1.0 eb'

            >>> Handler().get_human_readable_size(size=(1024 ** 7) + 1)
            '1.0 zb'

            >>> Handler().get_human_readable_size(size=(1024 ** 8) + 1)
            '1.0 yb'

            >>> Handler().get_human_readable_size(size=3 * (1024 ** 8) + 1)
            '3.0 yb'

            >>> import copy
            >>> handler = Handler()
            >>> formats_backup = copy.copy(handler.FORMATS)
            >>> handler.FORMATS = {}
            >>> handler.get_human_readable_size(size=3) # doctest: +ELLIPSIS
            '3... byte'
            >>> handler.FORMATS = formats_backup
        '''
        if size is None:
            size = self.size
        for name, properties in self.FORMATS.items():
            if(size >= properties['useful_range'][0] and
               (properties['useful_range'][1] is None or
                size <= properties['useful_range'][1])
               ):
                return builtins.str(builtins.round(
                    self.__class__.convert_size_format(
                        size, format=properties['notations'][0]
                    ), 2)
                ) + ' ' + properties['notations'][0]
        return builtins.str(builtins.round(size, 2)) + ' byte'

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def get_type(self):
    def get_type(self: boostNode.extension.type.Self) -> builtins.str:
##
        '''
            Determines the type of the current object.

            Examples:

            >>> Handler(location=__file_path__).type
            'file'

            >>> Handler().type
            'directory'

            >>> test_type = Handler(
            ...     __test_folder__ + 'get_type', must_exist=False)
            >>> test_type.type
            'undefined'

            >>> test_type.content = 'hans'
            >>> test_type.type
            'file'

            >>> test_type.content = 'hans'
            >>> test_type.get_type()
            'file'

            >>> if boostNode.extension.system.Platform(
            ...     ).operating_system == 'windows':
            ...     True
            ... else:
            ...     created = test_type.make_symbolic_link(
            ...         __test_folder__ + 'get_type_link')
            ...     Handler(
            ...         __test_folder__ + 'get_type_link'
            ...     ).type == 'symbolicLink'
            True

            >>> target = Handler(
            ...     __test_folder__ + 'get_type_link', must_exist=False)
            >>> test_type.make_portable_link(
            ...     __test_folder__ + 'get_type_link', force=True)
            True
            >>> target.type
            'portableLink'
        '''
        self._type = 'undefined'
        if self.is_portable_link():
            self._type = 'portableLink'
        elif self.is_symbolic_link():
            self._type = 'symbolicLink'
        elif self.is_directory():
            self._type = 'directory'
        elif self.is_file():
            self._type = 'file'
        return self._type

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def get_mimetype(self, default_type='text'):
    def get_mimetype(
        self: boostNode.extension.type.Self, default_type='text'
    ) -> builtins.str:
##
        '''
            Determines the mime-type of the current object.

            Returns the current object mime-type. The format is
            "type/subtype".

            Examples:

            >>> Handler(location=__file_path__).mimetype # doctest: +ELLIPSIS
            'text/...python'

            >>> Handler(
            ...     location=__file_path__
            ... ).get_mimetype() # doctest: +ELLIPSIS
            'text/...python'

            >>> Handler().mimetype
            ''

            >>> handler = Handler(
            ...     location=__test_folder__ + 'get_mimetype.unknownType',
            ...     must_exist=False)
            >>> handler.content = 'hans'
            >>> handler.mimetype # doctest: +ELLIPSIS
            'text/x-unknownType'
        '''
        self._mimetype = mimetypes.guess_type(self._path)[0]
        if not builtins.isinstance(self._mimetype, builtins.str):
            if self.is_file():
                subtype = 'plain'
                if self.extension:
                    subtype = 'x-' + self.extension
                self._mimetype = default_type + '/' + subtype
            else:
                self._mimetype = ''
        return self._mimetype

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def get_path(
##         self, location=None, respect_root_path=None,
##         output_with_root_prefix=None
##     ):
    def get_path(
        self: boostNode.extension.type.Self, location=None,
        respect_root_path=None, output_with_root_prefix=None
    ) -> builtins.str:
##
        '''
            Determines path of current "Handler" object
            or returns the path of a given "Handler" instance.

            Examples:

            >>> Handler(location=__file_path__).path # doctest: +ELLIPSIS
            '...file.py'

            >>> Handler(location=__file_path__).get_path(
            ...     location=__test_folder__ + 'get_path/path/'
            ... ) # doctest: +ELLIPSIS
            '...get_path...path...'
        '''
        taken_output_with_root_prefix = output_with_root_prefix
        if output_with_root_prefix is None:
            taken_output_with_root_prefix = self._output_with_root_prefix
        if location is None:
            if not self._path.endswith(os.sep) and self.is_directory():
                self._path += os.sep
            '''
                NOTE: If the given file isn't present the "_path" could be
                smaller than the root path. So simply return the internal
                path in this case.
            '''
            if(taken_output_with_root_prefix or
               not (self and self._path.startswith(self._root_path))):
                return self._path
            return self._path[builtins.len(
                self._root_path) - builtins.len(os.sep):]
        return self._get_path(
            location, respect_root_path,
            output_with_root_prefix=taken_output_with_root_prefix)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def get_relative_path(self, context=None, *arguments, **keywords):
    def get_relative_path(
        self: boostNode.extension.type.Self, *arguments: builtins.object,
        context=None, **keywords: builtins.object
    ) -> builtins.str:
##
        '''
            Returns the relative path of current "Handler" object depending on
            the current location.

            Examples:

            >>> Handler(
            ...     location=__file_path__
            ... ).relative_path # doctest: +ELLIPSIS
            '...file.py'

            >>> Handler().relative_path
            '.'

            >>> Handler().relative_path
            '.'

            >>> Handler().get_relative_path()
            '.'

            >>> Handler(
            ...     location='../../'
            ... ).relative_path == '..' + os.sep + '..'
            True

            >>> Handler(
            ...     location='../../'
            ... ).get_relative_path(context='../')
            '..'
        '''
        if context is None:
            return os.path.relpath(self._path, *arguments, **keywords)
        return os.path.relpath(
            self._path, *arguments, start=self.__class__(
                location=context, must_exist=False)._path,
            **keywords)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def get_directory_path(self, output_with_root_prefix=None):
    def get_directory_path(
        self: boostNode.extension.type.Self, output_with_root_prefix=None,
    ) -> builtins.str:
##
        '''
            Determines the current path of the Directory object without file.

            Examples:

            >>> Handler(
            ...     location=__file_path__
            ... ).directory_path # doctest: +ELLIPSIS
            '...boostNode...extension...'

            >>> Handler(
            ...     location=__file_path__
            ... ).get_directory_path() # doctest: +ELLIPSIS
            '...boostNode...extension...'

            >>> same = True
            >>> for handler in Handler():
            ...     if handler.directory_path != Handler()[0].directory_path:
            ...         same = False
            ...         break
            >>> same
            True

            >>> root_path_backup = Handler._root_path
            >>> Handler.set_root(Handler(
            ...     __file_path__
            ... ).directory_path) # doctest: +ELLIPSIS
            <class '...Handler'>
            >>> Handler().directory_path == root_path_backup
            True
            >>> Handler._root_path = root_path_backup
        '''
        self._directory_path = self.get_path(
            output_with_root_prefix=output_with_root_prefix)
        subtrahend = builtins.len(self.get_name(
            output_with_root_prefix=output_with_root_prefix))
        if(self.is_directory() and
           (builtins.len(self._directory_path) - builtins.len(os.sep)) > 0):
            subtrahend += builtins.len(os.sep)
        if subtrahend:
            self._directory_path = self._directory_path[:-subtrahend]
        return self._directory_path

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def get_name(self, *arguments, **keywords):
    def get_name(
        self: boostNode.extension.type.Self, *arguments: builtins.object,
        output_with_root_prefix=None, force_windows_behavior=False,
        **keywords: builtins.object
    ) -> builtins.str:
##
        '''
            Determines the current file name without directory path.
            Same possible parameters as native python method
            "os.path.name()".

            Examples:

            >>> Handler(location=__file_path__).name
            'file.py'

            >>> Handler().name
            'extension'

            >>> Handler().get_name()
            'extension'

            >>> handler = Handler('C:', must_exist=False)
            >>> handler._path = 'C:'
            >>> handler.get_name(
            ...     force_windows_behavior=True)
            'C:'
        '''
## python2.7
##         keywords_dictionary = boostNode.extension.native.Dictionary(
##             content=keywords)
##         output_with_root_prefix, keywords = keywords_dictionary.pop(
##             name='output_with_root_prefix')
##         force_windows_behavior, keywords = keywords_dictionary.pop(
##             name='force_windows_behavior', default_value=False)
        pass
##
        path = self.get_path(output_with_root_prefix=output_with_root_prefix)
        if builtins.len(path) and path.endswith(os.sep):
            path = path[:-builtins.len(os.sep)]
        if((boostNode.extension.system.Platform().operating_system ==
            'windows' or force_windows_behavior) and
           re.compile('^[A-Za-z]:$').match(path)):
            return path
        return os.path.basename(path, *arguments, **keywords)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def get_basename(self, *arguments, **keywords):
    def get_basename(
        self: boostNode.extension.type.Self, *arguments: builtins.object,
        output_with_root_prefix=None, **keywords: builtins.object
    ) -> builtins.str:
##
        '''
            Determines the current file name without directory path and file
            extension. Same possible parameters as native python method
            "os.path.name()".

            Examples:

            >>> Handler(location=__file_path__).basename
            'file'

            >>> Handler().basename
            'extension'

            >>> Handler().get_basename()
            'extension'
        '''
## python2.7
##         output_with_root_prefix, keywords = \
##             boostNode.extension.native.Dictionary(
##                 content=keywords
##             ).pop(name='output_with_root_prefix')
        pass
##
        if self._has_extension:
            return os.path.splitext(os.path.basename(
                self.get_path(
                    output_with_root_prefix=output_with_root_prefix),
                *arguments, **keywords)
            )[0]
        return self.name

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def get_free_space(self):
    def get_free_space(self: boostNode.extension.type.Self) -> builtins.int:
##
        '''
            Return free space of folder or drive (in bytes).

            Examples:

            >>> file_area_space = round(Handler(
            ...     location=__file_path__
            ... ).free_space, 2)
            >>> directory_space = round(Handler().free_space, 2)
            >>> file_area_space == directory_space
            True

            >>> isinstance(
            ...     Handler(location='../').free_space,
            ...     (long, int) if 'long' in dir(builtins) else int)
            True

            >>> isinstance(
            ...     Handler(location='../').get_free_space(),
            ...     (long, int) if 'long' in dir(builtins) else int)
            True
        '''
        return self._get_platform_dependent_free_and_total_space()[0]

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def get_disk_used_space(self):
    def get_disk_used_space(
        self: boostNode.extension.type.Self
    ) -> builtins.int:
##
        '''
            Determiens used space of current path containing disk.
        '''
        disk_status = self._get_platform_dependent_free_and_total_space()
        return disk_status[1] - disk_status[0]

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def get_content(self, mode='r', strict=False, *arguments, **keywords):
    def get_content(
        self: boostNode.extension.type.Self, mode='r', strict=False,
        *arguments: builtins.object, **keywords: builtins.object
    ) -> (builtins.str, builtins.bytes, types.GeneratorType):
##
        '''
            Returns the file content of a text-file. Accepts all arguments
            python's native "builtins.open()" or "codecs.open()" accepts.
            If current file doesn't exists an empty string will be returned.
            Note that this method shouldn't be used for binary files.
            If current handler points to an directory containing files will be
            returned as list.

            Examples:

            >>> Handler(location=__file_path__).content # doctest: +ELLIPSIS
            '#!/...python...'

            >>> handler = Handler(location=__file_path__)
            >>> handler.get_content(
            ...     mode='r', encoding='utf_8') # doctest: +ELLIPSIS
            '#!/...python...'

            >>> handler._encoding
            'utf_8'

            >>> Handler(location=__file_path__, encoding='utf_8').get_content(
            ...     mode='r'
            ... ) # doctest: +ELLIPSIS
            '#!/...python...'

            >>> Handler(
            ...     location=__test_folder__ + 'get_content_not_existing',
            ...     must_exist=False
            ... ).get_content(strict=True) # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            boostNode.extension.native.FileError: ...

            >>> Handler().content # doctest: +ELLIPSIS
            <generator object list at 0x...>

            >>> Handler().get_content(mode='r') # doctest: +ELLIPSIS
            <generator object list at 0x...>

            >>> handler = Handler(
            ...     __test_folder__ + 'get_content', must_exist=False)

            >>> handler.content = ' '
            >>> handler.get_content(mode='r+b') # doctest: +ELLIPSIS
            ...' '

            >>> handler.content = ' äüöß hans'

            >>> handler.get_content(
            ...     encoding='ascii', strict=True
            ... ) # doctest: +ELLIPSIS
            Traceback (most recent call last):
            ...
            UnicodeDecodeError: 'ascii' codec can't decode byte ...

            >>> handler.content
            '  hans'
        '''
        self._content = ''
        if self.is_file():
            if 'b' in mode:
                with builtins.open(
                    self._path, mode, *arguments, **keywords
                ) as file:
                    self._content = file.read()
            else:
                if 'encoding' in keywords:
                    self._encoding = keywords['encoding']
                else:
                    keywords['encoding'] = self._encoding
                errors = 'strict' if strict else 'ignore'
## python2.7
##                 with codecs.open(
##                     self._path, mode, *arguments, errors=errors, **keywords
##                 ) as file:
##                     '''
##                         NOTE: Double call of "read()" is a
##                         workaround for python bug when finishing
##                         reading file without end reached.
##                     '''
##                     self._content = builtins.str(
##                         (file.read() + file.read()).encode(
##                             encoding=self._encoding))
                with builtins.open(
                    self._path, mode, *arguments, errors=errors, **keywords
                ) as file:
                    '''
                        NOTE: Double call of "read()" is a
                        workaround for python bug when finishing
                        reading file without end reached.
                    '''
                    self._content = file.read() + file.read()
##
            return self._content
        elif self.is_directory():
            return self.list()
        if strict:
            raise __exception__(
                'Could only get content of file or directory (not "%s").',
                self.path)
        return self._content

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def get_portable_link_pattern(self, force_windows_behavior=False):
    def get_portable_link_pattern(
        self: boostNode.extension.type.Self, force_windows_behavior=False
    ) -> builtins.str:
##
        '''
            Determines the portable link file content pattern. With the
            file-independent placeholder "executable_path" replaced.

            Examples:

            >>> Handler().portable_link_pattern # doctest: +ELLIPSIS
            '...portable ...'

            >>> Handler().get_portable_link_pattern(
            ...     force_windows_behavior=True
            ... ) # doctest: +ELLIPSIS
            '...portable ...'

            >>> handler = Handler(location=__file_path__)
            >>> handler.portable_link_pattern # doctest: +ELLIPSIS
            '...portable ...'

            >>> Handler(
            ...     location=__test_folder__ +
            ...         'get_portable_link_pattern_media.mp3',
            ...     must_exist=False
            ... ).portable_link_pattern # doctest: +ELLIPSIS
            '[playlist]\\n\\nFile1=...'
        '''
        pattern = self.PORTABLE_DEFAULT_LINK_PATTERN
        if(boostNode.extension.system.Platform().operating_system ==
           'windows' or force_windows_behavior):
            pattern = self.PORTABLE_WINDOWS_DEFAULT_LINK_PATTERN
        if self.is_media():
            pattern = self.PORTABLE_MEDIA_LINK_PATTERN
        self._portable_link_pattern = pattern.format(
            executable_path=os.path.abspath(sys.argv[0]),
            label='{label}', size='{size}', path='{path}')
        return self._portable_link_pattern

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def get_portable_regex_link_pattern(self):
    def get_portable_regex_link_pattern(
        self: boostNode.extension.type.Self
    ) -> builtins.str:
##
        '''
            Determines the portable regular expression link file content
            pattern. All placeholder will be replaced with a useful regular
            expression pattern to check given file contents against the
            portable link pattern.

            Examples:

            >>> Handler().portable_regex_link_pattern # doctest: +ELLIPSIS
            '...portable...'

            >>> Handler().get_portable_regex_link_pattern(
            ...     ) # doctest: +ELLIPSIS
            '...portable...'
        '''
        self._portable_regex_link_pattern = boostNode.extension.native.String(
            self.portable_link_pattern
        ).validate_regex(exclude_symbols=('{', '}', '-')).content.format(
            size='(?P<size>[0-9]+)', label='(?P<label>.*?)',
            path='(?P<path>.*?)')
        return self._portable_regex_link_pattern

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def get_portable_link_content(
##         self, label='%s', relative=None, target_path=''
##     ):
    def get_portable_link_content(
        self: boostNode.extension.type.Self, label='%s', relative=None,
        target_path=''
    ) -> builtins.str:
##
        '''
            Returns the final portable link content depending on the current
            file referenced by "self.path".

            "label" Label for better distinction with other text-based
                    files.
            "relative" triggers if target should be referenced via relative
                       path. If "True" relative path will be determined from
                       current working directory, if a path or Handler object
                       is provided this location will be used as context to
                       determine relative path, if
                       "boostNode.extension.type.Self" is provided target
                       location will be used as context and if "False"
                       (default) path will be referenced absolute.
            "target_path" this method is only needed if relative is setted to
                          "boostNode.extension.type.Self".

            Examples:

            >>> Handler().portable_link_content # doctest: +ELLIPSIS
            '...portable...'

            >>> Handler().get_portable_link_content(
            ...     label='test-label (%s)') # doctest: +ELLIPSIS
            '...test-label (%s)...'
        '''
        self._portable_link_content = self.portable_link_pattern.format(
            label=label, size=builtins.int(self.size),
            path=self._determine_relative_path(
                relative, target_path
            ).replace('%', '%%'),
            name=self.name.replace('%', '%%'))
        return self._portable_link_content

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def get_extension_suffix(self):
    def get_extension_suffix(
        self: boostNode.extension.type.Self
    ) -> builtins.str:
##
        '''
            Returns the extension of a file or directory (empty string).
            The difference to "self.get_extension()" is that the delimiter
            point is added if neccessary.

            Examples:

            >>> Handler().extension_suffix
            ''

            >>> Handler().get_extension_suffix()
            ''

            >>> handler = Handler(
            ...     __test_folder__ + 'test.ext', must_exist=False)
            >>> handler.content = 'test'
            >>> handler.get_extension_suffix()
            '.ext'

            >>> Handler(
            ...     __test_folder__ + 'test.ext', must_exist=False
            ... ).extension_suffix
            '.ext'

            >>> Handler(
            ...     __test_folder__ + 'test', must_exist=False
            ... ).extension_suffix
            ''
        '''
        return (os.extsep + self.extension) if self._has_extension else ''

            # endregion

            # region setter methods

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def set_encoding(self, encoding, *arguments, **keywords):
    def set_encoding(
        self: boostNode.extension.type.Self, encoding: builtins.str,
        *arguments: builtins.object, **keywords: builtins.object
    ) -> boostNode.extension.type.Self:
##
        '''
            Set encoding for a text-base file if current instance refers to
            one.
            This method serves as wrapper method for "set_content()".

            Examples:

            >>> test_file = Handler(
            ...     __test_folder__ + 'set_encoding_test_encoding',
            ...     must_exist=False)
            >>> test_file.content = 'hans and peter'

            >>> test_file.encoding = 'utf_8'

            >>> test_file.set_encoding('utf_8') # doctest: +ELLIPSIS
            Object of "Handler" with path "..." ...
        '''
        return self.set_content(
            content=self.content, encoding=encoding, *arguments, **keywords)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def set_content(self, content, mode=None, *arguments, **keywords):
    def set_content(
        self: boostNode.extension.type.Self,
        content: (builtins.str, builtins.bytes), mode=None,
        *arguments: builtins.object, **keywords: builtins.object
    ) -> boostNode.extension.type.Self:
##
        '''
            Returns the file content of a text-file. Accepts all arguments
            python's native "builtins.open()" or "codecs.open()" accepts.
            If current file doesn't exists an empty string will be returned.
            Note that this method shouldn't be used for binary files.
            If current handler points to an directory containing files will be
            returned as list.

            Examples:

            >>> handler = Handler(
            ...     __test_folder__ + 'set_content_file', must_exist=False)
            >>> handler.content = 'hans'
            >>> handler.content
            'hans'

            >>> with open(handler.path, mode='r') as file:
            ...     file.read()
            'hans'

            >>> handler.content = 'A'
            >>> with open(handler.path, mode='r') as file:
            ...     file.read()
            'A'

            >>> handler.content += 'A'
            >>> with open(handler.path, mode='r') as file:
            ...     file.read()
            'AA'

            >>> handler.content
            'AA'

            >>> handler.set_content('AA') # doctest: +ELLIPSIS
            Object of "Handler" with path "..." ...

            >>> handler.set_content('hans', mode='w') # doctest: +ELLIPSIS
            Object of "Handler" with path "..." ...

            >>> handler.set_content('hans', mode='w+b') # doctest: +ELLIPSIS
            Object of "Handler" with path "..." ...

            >>> handler.set_content(unicode('hans')) # doctest: +ELLIPSIS
            Object of "Handler" with path "..." ...

            >>> Handler().set_content('AA') # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            boostNode.extension.native.FileError: Set content is only ...

            >>> handler.set_content(bytes(chr(1))) # doctest: +ELLIPSIS
            Object of "Handler" with path "..." ...
        '''
        mode = self._prepare_content_status(mode, content)
        if self._path.endswith(os.sep):
            self._path = self._path[:-builtins.len(os.sep)]
        self._path
        if 'b' in mode:
            with builtins.open(
                self._path, mode, *arguments, **keywords
            ) as file_handler:
                file_handler.write(content)
        else:
            if not 'encoding' in keywords:
                keywords['encoding'] = self._encoding
            else:
                self._encoding = keywords['encoding']
## python2.7
##             with codecs.open(
##                 self._path, mode, *arguments, **keywords
##             ) as file_handler:
##                 if not builtins.isinstance(content, builtins.unicode):
##                     content = builtins.unicode(
##                         content,
##                         boostNode.extension.native.String(
##                             content
##                         ).determine_encoding())
##                 file_handler.write(content)
            with builtins.open(
                self._path, mode, *arguments, **keywords
            ) as file_handler:
                file_handler.write(content)
##
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def set_directory_path(self, location, *arguments, **keywords):
    def set_directory_path(
        self: boostNode.extension.type.Self,
        location: (boostNode.extension.type.SelfClassObject,
                   builtins.str),
        *arguments: builtins.object, respect_root_path=None,
        **keywords: builtins.object
    ) -> builtins.bool:
##
        '''
            This function could be understand as wrapper method for "move()".

            Examples:

            >>> handler = Handler(
            ...     location=__test_folder__ + 'set_directory_path',
            ...     make_directory=True)

            >>> handler.directory_path = (
            ...     __test_folder__ + 'set_directory_path_edited')
            >>> handler.is_directory()
            True
            >>> handler.name
            'set_directory_path'
            >>> handler.directory_path # doctest: +ELLIPSIS
            '...set_directory_path_edited...'

            >>> new_location = Handler(
            ...     location=__test_folder__ + 'set_directory_path2',
            ...     must_exist=False)
            >>> handler.directory_path = new_location
            >>> handler.is_directory()
            True
            >>> handler.name
            'set_directory_path'
            >>> handler.directory_path # doctest: +ELLIPSIS
            '...set_directory_path2...'
            >>> new_location.is_directory()
            True

            >>> new_location = Handler(
            ...     location=__test_folder__ + 'set_directory_path3',
            ...     must_exist=False)
            >>> handler.set_directory_path(new_location)
            True
            >>> handler.name
            'set_directory_path'
            >>> handler.directory_path # doctest: +ELLIPSIS
            '...set_directory_path3...'
            >>> new_location.is_directory()
            True
        '''
## python2.7
##         respect_root_path, keywords = boostNode.extension.native.Dictionary(
##             content=keywords
##         ).pop(name='respect_root_path')
        pass
##
        return self.move(
            target=self.get_path(
                location, respect_root_path
            ) + os.sep + self.name, *arguments, **keywords)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def set_name(self, name, *arguments, **keywords):
    def set_name(
        self: boostNode.extension.type.Self, name: builtins.str,
        *arguments: builtins.object, **keywords: builtins.object
    ) -> builtins.bool:
##
        '''
            This function could be understand as wrapper method for "move()".

            Examples:

            >>> handler = Handler(
            ...     __test_folder__ + 'set_name', make_directory=True)
            >>> handler.name = 'set_name_edited'
            >>> handler.is_directory()
            True
            >>> handler.name
            'set_name_edited'

            >>> handler.set_name('set_name_edited2')
            True
            >>> handler.is_directory()
            True
            >>> handler.name
            'set_name_edited2'

            >>> handler = Handler(
            ...     __test_folder__ + 'set_name.e', must_exist=False)
            >>> handler.content = 'A'
            >>> handler.name = 'set_name.ext'
            >>> handler.is_file()
            True
            >>> handler.name
            'set_name.ext'
            >>> handler.basename
            'set_name'
        '''
        return self.move(
            target=self.directory_path + name, *arguments, **keywords)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def set_basename(self, basename, *arguments, **keywords):
    def set_basename(
        self: boostNode.extension.type.Self, basename: builtins.str,
        *arguments: builtins.object, **keywords: builtins.object
    ) -> builtins.bool:
##
        '''
            This function could be understand as wrapper method for
            "set_name()".

            Examples:

            >>> handler = Handler(
            ...     __test_folder__ + 'set_basename3', make_directory=True)
            >>> handler.basename = 'set_basename_edited3'
            >>> handler.name
            'set_basename_edited3'

            >>> handler = Handler(
            ...     __test_folder__ + 'set_basename4', make_directory=True)
            >>> handler.set_basename('set_basename_edited4')
            True
            >>> handler.basename
            'set_basename_edited4'

            >>> handler = Handler(
            ...     __test_folder__ + 'set_basename5.e', must_exist=False)
            >>> handler.content = 'A'
            >>> handler.basename = 'set_basename_edited5'
            >>> handler.name
            'set_basename_edited5.e'
            >>> handler.basename
            'set_basename_edited5'
        '''
        return self.set_name(
            name=basename + self.extension_suffix, *arguments, **keywords)

## python2.7
##     def set_extension(self, extension, *arguments, **keywords):
    def set_extension(
        self: boostNode.extension.type.Self, extension: builtins.str,
        *arguments: builtins.object, **keywords: builtins.object
    ) -> builtins.bool:
##
        '''
            This function could be understand as wrapper method for
            "set_name()".

            Examples:

            >>> handler = Handler(
            ...     __test_folder__ + 'set_extension.ext', must_exist=False)
            >>> handler.content = 'A'
            >>> handler.extension
            'ext'
            >>> handler.extension = 'mp3'
            >>> handler.is_file()
            True
            >>> handler.name
            'set_extension.mp3'
            >>> handler.extension
            'mp3'

            >>> handler.set_extension('wav')
            True
            >>> handler.extension
            'wav'

            >>> handler.set_extension('')
            True
        '''
        if extension:
            self._has_extension = True
            return self.set_name(
                name=self.basename + os.extsep + extension, *arguments,
                **keywords)
        return self.is_element()

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def set_path(self, *arguments, **keywords):
    def set_path(
        self: boostNode.extension.type.Self,
        *arguments: builtins.object, **keywords: builtins.object
    ) -> builtins.bool:
##
        '''
            Serves as wrapper function for the "move" method.

            Examples:

            >>> handler = Handler(
            ...     location=__test_folder__ + 'set_path', make_directory=True)
            >>> handler.path = __test_folder__ + 'set_path_moved'
            >>> Handler(
            ...     location=__test_folder__ + 'set_path_moved').is_directory()
            True

            >>> handler = Handler(
            ...     location=__test_folder__ + 'set_path2',
            ...     make_directory=True)
            >>> handler.set_path(target=__test_folder__ + 'set_path_moved2')
            True
            >>> Handler(
            ...     location=__test_folder__ + 'set_path_moved2'
            ... ).is_directory()
            True
        '''
        return self.move(*arguments, **keywords)

            # endregion

            # region boolean methods

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def is_same_file(self, other_location):
    def is_same_file(
        self: boostNode.extension.type.Self,
        other_location: boostNode.extension.type.SelfClassObject
    ) -> builtins.bool:
##
        '''
            A simple replacement of the os.path.samefile() function not
            existing on the Windows platform.

            Examples:

            >>> Handler().is_same_file(Handler())
            True

            >>> same_file_backup = os.path.samefile
            >>> del os.path.samefile
            >>> Handler().is_same_file(Handler())
            True
            >>> os.path.samefile = same_file_backup
        '''
        other_location = self.__class__(location=other_location)
## python2.7
##         try:
##             return os.path.samefile(self._path, other_location._path)
##         except builtins.AttributeError:
##             return self == other_location
        return os.path.samefile(self._path, other_location._path)
##

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def is_directory(self, allow_link=True, *arguments, **keywords):
    def is_directory(
        self: boostNode.extension.type.Self, allow_link=True,
        *arguments: builtins.object, **keywords: builtins.object
    ) -> builtins.bool:
##
        '''
            Implements the pythons native "os.path.isdir()" method in an
            object oriented way and adds the "link" parameter.

            "link" triggers if symbolic links to directories also evaluates to
            "True".

            Returns "True" if path is an existing directory.

            Examples:

            >>> Handler().is_directory()
            True

            >>> Handler(location=__file_path__).is_directory()
            False
        '''
        if allow_link:
            return os.path.isdir(self._path, *arguments, **keywords)
        return not self.is_symbolic_link() and\
            self.is_directory(allow_link=True, *arguments, **keywords)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def is_file(self, allow_link=True, *arguments, **keywords):
    def is_file(
        self: boostNode.extension.type.Self, allow_link=True,
        *arguments: builtins.object, **keywords: builtins.object
    ) -> builtins.bool:
##
        '''
            Implements the pythons native "os.path.isfile()" method in an
            object oriented way. And adds the "link" parameter.

            "link" triggers if symbolic links also evaluates to "True".

            Returns "True" if path is an existing regular file.

            Examples:

            >>> Handler(location=__file_path__).is_file()
            True

            >>> Handler().is_file()
            False

            >>> Handler().is_file(allow_link=False)
            False
        '''
        if allow_link:
            return os.path.isfile(self._path, *arguments, **keywords) or\
                os.path.islink(self._path, *arguments, **keywords)
        return(not self.is_symbolic_link() and
               self.is_file(allow_link=True, *arguments, **keywords))

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def is_symbolic_link(
##         self, allow_portable_link=True, *arguments, **keywords
##     ):
    def is_symbolic_link(
        self: boostNode.extension.type.Self, allow_portable_link=True,
        *arguments: builtins.object, **keywords: builtins.object
    ) -> builtins.bool:
##
        '''
            Implements the pythons native "os.path.islink()" method in an
            object oriented way and adds the "portable_link" parameter.

            "portable_link" triggers if portable links also evaluates to
            "True".

            Returns "True" if path refers to a directory entry that is a link
            file. Always "False" for symbolic links if they are not supported.

            Examples:

            >>> target = Handler(
            ...     __test_folder__ + 'is_symbolic_link', must_exist=False)
            >>> if boostNode.extension.system.Platform(
            ...     ).operating_system == 'windows':
            ...     True
            ... else:
            ...     created = Handler(
            ...         location=__file_path__
            ...     ).make_symbolic_link(target, force=True)
            ...     target.is_symbolic_link()
            True

            >>> file = Handler(
            ...     __test_folder__ + 'is_symbolic_link_not', must_exist=False)
            >>> file.content = ' '
            >>> file.is_symbolic_link()
            False

            >>> file = Handler(
            ...     __test_folder__ + 'is_symbolic_link_not2',
            ...     make_directory=True)
            >>> file.is_symbolic_link()
            False

            >>> file = Handler(
            ...     location=__test_folder__ + 'is_symbolic_link_not3',
            ...     must_exist=False)
            >>> Handler(location=__file_path__).make_portable_link(
            ...     target=file, force=True)
            True

            >>> file.is_symbolic_link(allow_portable_link=False)
            False

            >>> file.is_symbolic_link()
            True
        '''
        path = self._path
        if self._path.endswith(os.sep):
            path = self._path[:-builtins.len(os.sep)]
        if allow_portable_link:
            return self.is_symbolic_link(allow_portable_link=False) or\
                self.is_portable_link()
        return os.path.islink(path, *arguments, **keywords)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def is_referenced_via_absolute_path(self, location=None):
    def is_referenced_via_absolute_path(
        self: boostNode.extension.type.Self, location=None
    ) -> builtins.bool:
##
        '''
            Determines if the given path is an absolute one.

            "location" is path or "Handler" object pointing to target
                       destination.

            Returns "False" if the given path is a relative one or "True"
            otherwise.

            Examples:

            >>> Handler().is_referenced_via_absolute_path(
            ...     location=__file_path__)
            True

            >>> Handler().is_referenced_via_absolute_path(location='.')
            False

            >>> Handler(
            ...     location=__file_path__).is_referenced_via_absolute_path()
            True

            >>> Handler().is_referenced_via_absolute_path(location='/')
            True

            >>> Handler().is_referenced_via_absolute_path(location=Handler())
            False
        '''
        if location is None:
            location = self._initialized_path
        elif builtins.isinstance(location, self.__class__):
            return location.is_referenced_via_absolute_path()
        return os.path.isabs(location)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def is_media(self):
    def is_media(self: boostNode.extension.type.Self) -> builtins.bool:
##
        '''
            Determines if the current location referenced to a media file.

            Returns "True" if the current location points to a media file or
            "False" otherwise.

            Examples:

            >>> Handler(location=__file_path__).is_media()
            False

            >>> Handler().is_media()
            False

            >>> Handler(
            ...     location=__test_folder__ + 'is_media_audio.mp3'
            ... ).is_media() # doctest: +SKIP
            True
        '''
        for pattern in self.MEDIA_MIMETYPE_PATTERN:
            if re.search(pattern, self.mimetype):
                return True
        return False

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def is_portable_link(self):
    def is_portable_link(
        self: boostNode.extension.type.Self
    ) -> builtins.bool:
##
        '''
            Checks if the current location points to a portable link.

            Returns "True" id the current location is a portable link or
            "False" otherwise.

            Examples:

            >>> Handler(location=__file_path__).is_portable_link()
            False

            >>> handler = Handler(
            ...     __test_folder__ + 'is_portable_link', must_exist=False)
            >>> if boostNode.extension.system.Platform(
            ...     ).operating_system == 'windows':
            ...     False
            ... else:
            ...     created = Handler(
            ...         location=__file_path__
            ...     ).make_symbolic_link(handler)
            ...     handler.is_portable_link()
            False

            >>> Handler().is_portable_link()
            False

            >>> Handler(
            ...     __test_folder__ + 'is_portable_link_not_existing',
            ...     must_exist=False
            ... ).is_portable_link()
            False

            >>> Handler(location=__file_path__).make_portable_link(
            ...     target=handler, force=True)
            True
            >>> handler.is_portable_link()
            True

            >>> handler.set_content(
            ...     10 * 'ä', encoding='latin1'
            ... ) # doctest: +ELLIPSIS
            Object of "Handler" with path "...
            >>> handler.is_portable_link()
            False
        '''
        if os.path.isfile(self._path):
            maximum_length = (
                builtins.len(self.portable_link_pattern) +
                self.MAX_PATH_LENGTH + self.MAX_SIZE_NUMBER_LENGTH +
                # Maximum label line length + Maximum name length.
                120 + self.MAX_FILE_NAME_LENGTH)
            try:
## python2.7
##                 with codecs.open(
##                     self._path, mode='r', encoding=self.DEFAULT_ENCODING,
##                     errors='strict'
##                 ) as file:
                with builtins.open(
                    self._path, mode='r', encoding=self.DEFAULT_ENCODING,
                    errors='strict'
                ) as file:
##
                    file_content = file.read(maximum_length + 1).strip()
            except(builtins.IOError, builtins.TypeError,
                   builtins.UnicodeDecodeError):
                pass
            else:
                return(
                    builtins.len(file_content) <= maximum_length and
                    builtins.bool(re.compile(
                        self.portable_regex_link_pattern
                    ).match(file_content)))
        return False

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def is_element(self):
    def is_element(self: boostNode.extension.type.Self) -> builtins.bool:
##
        '''
            Determines if the current object path is a valid resource on the
            file system.

            Returns "True" if the current location is a valid file system
            object or "False" otherwise.

            Examples:

            >>> Handler().is_element()
            True

            >>> Handler(location=__file_path__).is_element()
            True

            >>> handler = Handler(
            ...     location=__test_folder__ + 'is_element',
            ...     make_directory=True)
            >>> handler.is_element()
            True

            >>> handler.remove_deep()
            True

            >>> handler.is_element()
            False

            >>> Handler(
            ...     __test_folder__ + 'is_element_not_existing',
            ...     must_exist=False
            ... ).is_element()
            False
        '''
        return os.path.exists(self._path) or self.is_symbolic_link()

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def is_device_file(self):
    def is_device_file(
        self: boostNode.extension.type.Self
    ) -> builtins.bool:
##
        '''
            Determines if the current object path is a device file like a
            socket or pipe.

            Returns "True" if the current location is a device file or "False"
            otherwise.

            Examples:

            >>> Handler().is_device_file()
            False

            >>> Handler(location=__file_path__).is_device_file()
            False

            >>> Handler(
            ...     location=__test_folder__ + 'is_device_file',
            ...     make_directory=True
            ... ).is_device_file()
            False

            >>> Handler(
            ...     __test_folder__ + 'is_device_file_not_existing',
            ...     must_exist=False
            ... ).is_device_file()
            False
        '''
        return self.is_element() and not (
            self.is_file() or self.is_directory())

            # endregion

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def backup(
##         self,
##         name_wrapper='<%file.basename%>_backup<%file.extension_suffix%>',
##         backup_if_exists=True, compare_content=True
##     ):
    def backup(
        self: boostNode.extension.type.Self,
        name_wrapper=(
            '<%file.basename%>_backup<%file.extension_suffix%>'),
        backup_if_exists=True, compare_content=True
    ) -> boostNode.extension.type.Self:
##
        '''
            Creates a backup of current file object in same location.

            "name_wrapper" a template formating the backup file name.
            "backup_if_exists" indicates if a backup should be make even if
                               there is already a file object with given backup
                               name and content (if "compare_content" is set).

            Examples:

            >>> handler = Handler(__test_folder__ + 'backup', must_exist=False)
            >>> handler.content = ' '
            >>> template = '<%file.basename%>_b<%file.extension_suffix%>'

            >>> handler.backup(template) # doctest: +ELLIPSIS
            Object of "Handler" with path "...
            >>> Handler(__test_folder__ + 'backup_b') # doctest: +ELLIPSIS
            Object of "Handler" with path "...

            >>> handler.backup(template) # doctest: +ELLIPSIS
            Object of "Handler" with path "...
            >>> Handler(__test_folder__ + 'backup_b_b').is_file()
            True

            >>> handler.backup(
            ...     template, backup_if_exists=False
            ... ) # doctest: +ELLIPSIS
            Object of "Handler" with path "...
            >>> Handler(
            ...     __test_folder__ + 'backup_b_b_b', must_exist=False
            ... ).is_file()
            False

            >>> handler.content = 'A'
            >>> handler.backup(
            ...     template, backup_if_exists=False
            ... ) # doctest: +ELLIPSIS
            Object of "Handler" with path "...
            >>> Handler(__test_folder__ + 'backup_b_b_b').is_file()
            True

            >>> handler.content = 'B'
            >>> handler.backup(
            ...     template, backup_if_exists=False, compare_content=False
            ... ) # doctest: +ELLIPSIS
            Object of "Handler" with path "...
            >>> Handler(
            ...     __test_folder__ + 'backup_b_b_b_b', must_exist=False
            ... ).is_file()
            False
        '''
        from boostNode.runnable.template import Parser as TemplateParser

        backup = self
        while True:
            earlier_backup = backup
            backup = self.__class__(
                location=self.directory_path + TemplateParser(
                    template=name_wrapper, string=True
                ).render(file=backup).output,
                must_exist=False)
            '''
                Iterate till we have wrapped file name which doesn't exist yet.
            '''
            if not backup:
                '''Check if a new created backup would be redundant.'''
## python2.7
##                 if(not (earlier_backup == self) and not backup_if_exists and
##                    (not compare_content or self.is_equivalent(
##                        other=earlier_backup))):
                if(earlier_backup != self and not backup_if_exists and
                   (not compare_content or self.is_equivalent(
                       other=earlier_backup))):
##
                    return self
                self.copy(target=backup)
                break
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def is_equivalent(self, other):
    def is_equivalent(
        self: boostNode.extension.type.Self,
        other: (boostNode.extension.type.SelfClassObject, builtins.str)
    ) -> builtins.bool:
##
        '''
            Returns "True" if given file object contains likewise content as
            current file object.

            Examples:

            >>> handler = Handler(
            ...     __test_folder__ + 'is_equivalent', make_directory=True)
            >>> handler.is_equivalent(handler)
            True

            >>> Handler(__test_folder__).is_equivalent(
            ...     __test_folder__ + 'test')
            False

            >>> Handler(__test_folder__).is_equivalent(
            ...     Handler(__test_folder__ + 'test', make_directory=True))
            False

            >>> a = Handler(__test_folder__ + 'a', make_directory=True)
            >>> b = Handler(__test_folder__ + 'b', make_directory=True)
            >>> a_file = Handler(__test_folder__ + 'a/test', must_exist=False)
            >>> a_file.content = 'hans'
            >>> b_file = Handler(__test_folder__ + 'b/test', must_exist=False)
            >>> b_file.content = 'hans'

            >>> a.is_equivalent(b)
            True

            >>> a_file.is_equivalent(b_file)
            True

            >>> b_file.content = 'peter'
            >>> a_file.is_equivalent(b_file)
            False

            >>> a_file.is_equivalent(a)
            False
        '''
        other = self.__class__(location=other)
        if self.is_file() and other.is_file():
            return self.content == other.content
        elif(self.is_directory() and other.is_directory() and
             self._is_equivalent_folder(other)):
            return True
        return False

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def change_working_directory(self):
    def change_working_directory(
        self: boostNode.extension.type.Self
    ) -> boostNode.extension.type.Self:
##
        '''
            Changes the current working directory to the instance saved
            location.

            Examples:

            >>> current_working_directory = os.getcwd()
            >>> current_working_directory # doctest: +ELLIPSIS
            '...boostNode...extension'

            >>> test_folder = Handler(
            ...     __test_folder__ + 'change', make_directory=True)
            >>> test_folder.change_working_directory() # doctest: +ELLIPSIS
            Object of "Handler" with path "...change..." (d...
            >>> os.getcwd() # doctest: +ELLIPSIS
            '...change...'
            >>> test_folder.path[:-len(os.sep)] == os.getcwd()
            True
            >>> test_folder.directory_path[:-len(os.sep)] != os.getcwd()
            True

            >>> Handler(
            ...     current_working_directory
            ... ).change_working_directory() # doctest: +ELLIPSIS
            Object of "Handler" with path "..." (directory).

            >>> undefined_object = Handler(
            ...     __test_folder__ + 'change/a', must_exist=False)
            >>> undefined_object.change_working_directory(
            ...     ) # doctest: +ELLIPSIS
            Object of "Handler" with path "...change..." (u...
            >>> os.getcwd() # doctest: +ELLIPSIS
            '...change...'
            >>> undefined_object.directory_path[:-len(os.sep)] == os.getcwd()
            True
            >>> undefined_object.path[:-len(os.sep)] != os.getcwd()
            True

            >>> Handler(
            ...     current_working_directory
            ... ).change_working_directory() # doctest: +ELLIPSIS
            Object of "Handler" with path "..." (directory).

            >>> file = Handler(__test_folder__ + 'change/a', must_exist=False)
            >>> file.content = ' '
            >>> file.change_working_directory() # doctest: +ELLIPSIS
            Object of "Handler" with path "...change..." (f...
            >>> os.getcwd() # doctest: +ELLIPSIS
            '...change...'
            >>> file.directory_path[:-len(os.sep)] == os.getcwd()
            True
            >>> file.path[:-len(os.sep)] != os.getcwd()
            True

            >>> Handler(
            ...     current_working_directory
            ... ).change_working_directory() # doctest: +ELLIPSIS
            Object of "Handler" with path "..." (directory).
        '''
        if self.is_directory():
            os.chdir(self._path)
        else:
            self.directory_path
            os.chdir(self._directory_path)
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def touch(self, *arguments, **keywords):
    def touch(
        self: boostNode.extension.type.Self, *arguments: builtins.object,
        **keywords: builtins.object
    ) -> builtins.bool:
##
        '''
            Sets the modification time of current file object to current time.
            If it was permitted and successful "True" will be returned and
            "False" otherwise.

            Examples:

            >>> import time
            >>> directory = Handler(
            ...     __test_folder__ + 'touch', make_directory=True)
            >>> old_timestamp = directory.timestamp
            >>> time.sleep(0.01)

            >>> directory.touch()
            True
            >>> old_timestamp != directory.timestamp # doctest: +SKIP
            True

            >>> directory.touch((1330, 1332))
            True

            >>> directory.touch(False)
            False
        '''
        if not arguments:
            arguments = (None,)
        try:
            os.utime(self._path, *arguments, **keywords)
        except:
            return False
        return True

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def list(self, *arguments, **keywords):
    def list(
        self: boostNode.extension.type.Self, *arguments: builtins.object,
        **keywords: builtins.object
    ) -> types.GeneratorType:
##
        '''
            Implements the pythons native "os.listdir()" method in an object
            oriented way.

            Return a list containing "Handler" objects of entries in the
            directory given by the object path. The list is in arbitrary order.
            It does not include the special entries '.' and '..' even if they
            are present in the directory.

            Examples:

            >>> Handler().list() # doctest: +ELLIPSIS
            <generator object list at ...>

            >>> for handler in Handler(): # doctest: +ELLIPSIS
            ...     print('"' + str(handler) + '"')
            "...file.py..."

            >>> not_existing_file = Handler(
            ...     __test_folder__ + 'list_not_existing', must_exist=False)
            >>> not_existing_file.list() # doctest: +ELLIPSIS
            <generator object list at ...>
            >>> len(not_existing_file)
            0
            >>> list(not_existing_file.list())
            []

            >>> not_accessible_file = Handler(
            ...     __test_folder__ + 'list_not_accessible',
            ...     make_directory=True)
            >>> not_accessible_file.change_right(000) # doctest: +ELLIPSIS
            Object of "Handler" with path "...
            >>> list(Handler(__test_folder__)) # doctest: +ELLIPSIS
            [...]
            >>> not_accessible_file.remove_directory()
            True

            >>> not_accessible_file.content = ' '
            >>> not_accessible_file.change_right(000) # doctest: +ELLIPSIS
            Object of "Handler" with path "...
            >>> list(Handler(__test_folder__)) # doctest: +ELLIPSIS
            [...]
            >>> not_accessible_file.remove_file()
            True
        '''
        if self:
            if(self._path == '\\' and
               boostNode.extension.system.Platform().operating_system ==
               'windows'):
                for letter_number in builtins.range(
                        builtins.ord('A'), builtins.ord('Z') + 1):
                    path = builtins.chr(letter_number) + ':\\\\'
                    if os.path.exists(path):
                        yield self.__class__(location=path, must_exist=False)
            else:
                try:
                    for file_name in os.listdir(
                        self._path, *arguments, **keywords
                    ):
                        try:
                            yield self.__class__(
                                location=self.path + file_name,
                                must_exist=False)
                        except (builtins.IOError, builtins.OSError):
                            pass
                except builtins.OSError:
                    pass

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def remove_directory(self, *arguments, **keywords):
    def remove_directory(
        self: boostNode.extension.type.Self, *arguments: builtins.object,
        **keywords: builtins.object
    ) -> builtins.bool:
##
        '''
            Implements the pythons native "os.rmdir()" method in an object
            oriented way.

            Remove (delete) the directory path. Works only if the directory
            is empty, otherwise, "OSError" is raised. To remove whole
            directory trees, "remove_deep" or "shutil.rmtree" can be used.

            Returns "True" if deleting was successful or no file exists and
            "False"otherwise.

            Examples:

            >>> handler = Handler(
            ...     __test_folder__ + 'remove_directory', make_directory=True)

            >>> handler.remove_directory()
            True

            >>> handler.remove_directory()
            False

            >>> handler.content = ' '
            >>> handler.remove_directory()
            False
            >>> handler.remove_file()
            True

            >>> handler.make_directory()
            True
            >>> handler.change_right(000) # doctest: +ELLIPSIS
            Object of "Handler" with path "...
            >>> handler.remove_directory()
            True

            >>> handler.make_directory()
            True
            >>> file = Handler(handler.path + 'file', make_directory=True)
            >>> handler.change_right(100) # doctest: +ELLIPSIS
            Object of "Handler" with path "...
            >>> file.change_right(000) # doctest: +ELLIPSIS
            Object of "Handler" with path "...
            >>> file.remove_directory()
            False
            >>> handler.change_right(700) # doctest: +ELLIPSIS
            Object of "Handler" with path "...
            >>> file.remove_directory()
            True
        '''
        if self.is_directory():
            try:
                os.rmdir(self._path, *arguments, **keywords)
            except:
                return False
            else:
                return True
        return False

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def move(self, target, *arguments, **keywords):
    def move(
        self: boostNode.extension.type.Self,
        target: (
            boostNode.extension.type.SelfClassObject, builtins.str),
        *arguments: builtins.object, respect_root_path=None,
        **keywords: builtins.object
    ) -> builtins.bool:
##
        '''
            Implements the pythons native "shutil.move()" method in an object
            oriented way.

            Recursively move a file or directory to another location.
            If the destination is on the current file system, then simply use
            "rename". Otherwise, copy current path (with pythons native
            "shutil.copy2" method) to the target and then remove current path.

            "target" Path or "Handler" object pointing to target destination.

            Examples:

            >>> handler = Handler(
            ...     location=__test_folder__ + 'move', make_directory=True)
            >>> target = Handler(
            ...     location=__test_folder__ + 'move2', must_exist=False)
            >>> handler.move(target)
            True
            >>> target.is_directory()
            True

            >>> handler = Handler(
            ...     location=__test_folder__ + 'move_file', must_exist=False)
            >>> handler.content = ' '
            >>> target = Handler(
            ...     location=__test_folder__ + 'move_file2', must_exist=False)
            >>> handler.move(target)
            True
            >>> target.is_file()
            True

            >>> Handler(
            ...     location=__test_folder__ + 'move_not_existing',
            ...     must_exist=False
            ... ).move(__test_folder__ + 'move_target_not_existing2')
            False
        '''
## python2.7
##         respect_root_path, keywords = boostNode.extension.native.Dictionary(
##             content=keywords
##         ).pop(name='respect_root_path')
        pass
##
        target = self.get_path(
            location=target, respect_root_path=respect_root_path,
            output_with_root_prefix=True)
        if self:
            shutil.move(self._path, dst=target, *arguments, **keywords)
        return self._set_path(path=target)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def remove_deep(self, *arguments, **keywords):
    def remove_deep(
        self: boostNode.extension.type.Self, *arguments: builtins.object,
        **keywords: builtins.object
    ) -> builtins.bool:
##
        '''
            Implements the pythons native "shutil.rmtree()" method in an object
            oriented way.

            Delete an entire directory tree; path must point to a valid
            location (but not a symbolic link). If "ignore_errors" is true,
            errors resulting from failed removals will be ignored; if false or
            omitted, such errors are handled by calling a handler specified by
            "onerror" or, if that is omitted, they raise an exception.
            If "onerror" is provided, it must be a callable that accepts three
            parameters: "function", "path", and "excinfo". The first parameter,
            function, is the function which raised the exception; it will be
            one of pythons native methods: "os.path.islink()", "os.listdir",
            "os.remove" or "os.rmdir". The second parameter "path" will be the
            path name passed to function. The third parameter "excinfo" will
            be the exception information returned by pythons native
            "sys.exc_info()" method.
            Exceptions raised by "onerror" will not be caught.

            Examples:

            >>> root = Handler(
            ...     location=__test_folder__ + 'remove_deep',
            ...     make_directory=True)
            >>> Handler(
            ...     location=__test_folder__ + 'remove_deep/sub_dir',
            ...     make_directory=True) # doctest: +ELLIPSIS
            Object of "Handler" with path "...remove_deep...sub_dir..."...
            >>> root.remove_deep()
            True
            >>> root.is_directory()
            False

            >>> root.remove_deep()
            False

            >>> root.content = ' '
            >>> root.remove_deep()
            True

            >>> root.make_directory()
            True
            >>> file = Handler(root.path + 'file', make_directory=True)
            >>> root.change_right(000) # doctest: +ELLIPSIS
            Object of "Handler" with path "...
            >>> file.remove_deep()
            False
        '''
        if self.is_directory(allow_link=False):
            try:
                shutil.rmtree(self._path, *arguments, **keywords)
            except:
                return False
            else:
                return True
        return self.remove_file()

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def remove_file(self, *arguments, **keywords):
    def remove_file(
        self: boostNode.extension.type.Self, *arguments: builtins.object,
        **keywords: builtins.object
    ) -> builtins.bool:
##
        '''
            Implements the pythons native "os.remove()" method in an object
            oriented way.

            Remove (delete) the file path. This is the same function as
            pythons native "os.remove"; the unlink name is its traditional Unix
            name.

            Returns "True" if file was deleted successfully and "False"
            otherwise.

            Examples:

            >>> Handler(location=__file_path__).copy(
            ...     target=__test_folder__ + 'remove_file')
            True

            >>> handler = Handler(location=__test_folder__ + 'remove_file')
            >>> handler.is_file()
            True

            >>> handler.remove_file()
            True
            >>> handler.is_file()
            False

            >>> handler.remove_file()
            False

            >>> handler.make_directory()
            True
            >>> file = Handler(handler.path + 'file', must_exist=False)
            >>> file.content = ' '
            >>> handler.change_right(100) # doctest: +ELLIPSIS
            Object of "Handler" with path "...
            >>> file.change_right(000) # doctest: +ELLIPSIS
            Object of "Handler" with path "...
            >>> file.remove_file()
            False
            >>> handler.change_right(700) # doctest: +ELLIPSIS
            Object of "Handler" with path "...
            >>> file.remove_file()
            True

            >>> Handler().remove_file()
            False
        '''
        if self.is_file():
            operating_system = \
                boostNode.extension.system.Platform().operating_system
            if(self.is_symbolic_link(allow_portable_link=False) and
               self.is_directory() and operating_system == 'windows'):
                return self.remove_directory()
            try:
                os.remove(self._path, *arguments, **keywords)
            except:
                return False
            else:
                return True
        return False

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def change_right(self, right, octal=True):
    def change_right(
        self: boostNode.extension.type.Self, right, octal=True
    ) -> boostNode.extension.type.Self:
##
        '''
            Implements the pythons native "os.chmod()" method in an object
            oriented way.

            Change the mode of path to the numeric mode. "mode" may take one of
            the following values (as defined in the stat module) or bitwise
            combinations of them:

            stat.S_ISUID
            stat.S_ISGID
            stat.S_ENFMT
            stat.S_ISVTX
            stat.S_IREAD
            stat.S_IWRITE
            stat.S_IEXEC
            stat.S_IRWXU
            stat.S_IRUSR
            stat.S_IWUSR
            stat.S_IXUSR
            stat.S_IRWXG
            stat.S_IRGRP
            stat.S_IWGRP
            stat.S_IXGRP
            stat.S_IRWXO
            stat.S_IROTH
            stat.S_IWOTH
            stat.S_IXOTH

            "right" is the new right for the current object's path location.

            Examples:

            >>> handler = Handler(
            ...     __test_folder__ + 'change_right', must_exist=False)
            >>> Handler(location=__file_path__).copy(target=handler)
            True
            >>> handler.change_right(right=766) # doctest: +ELLIPSIS
            Object of "Handler" with path "...change_right...

            >>> handler.change_right(
            ...     stat.S_IWUSR | stat.S_IXUSR, octal=False
            ... ) # doctest: +ELLIPSIS
            Object of "Handler" with path "...change_right...

            >>> handler = Handler(
            ...     __test_folder__ + 'change_right_folder',
            ...     make_directory=True)
            >>> handler.change_right(right=766) # doctest: +ELLIPSIS
            Object of "Handler" with path "...change_right_folder..." ...

            >>> handler.change_right(
            ...     stat.S_IWRITE | stat.S_IREAD, octal=False
            ... ) # doctest: +ELLIPSIS
            Object of "Handler" with path "...change_right...
        '''
        if octal:
            os.chmod(self._path, builtins.eval('0o%d' % right))
        else:
            os.chmod(self._path, right)
        if self.is_directory():
            '''Take this method name via introspection.'''
            self.iterate_directory(function=inspect.stack()[0][3], right=right)
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def copy(self, target, *arguments, **keywords):
    def copy(
        self: boostNode.extension.type.Self,
        target: (boostNode.extension.type.SelfClassObject,
                 builtins.str),
        *arguments: builtins.object, right=None, octal=True,
        **keywords: builtins.object
    ) -> builtins.bool:
##
        '''
            Implements the pythons native "shutil.copy()" method in an object
            orientated way.

            Copy the current file to the file or directory "target". If current
            location is a directory, a file with the same name is created
            (or overwritten) in the directory specified. Permission bits are
            copied.

            "target" Path or "Handler" object pointing to target destination.

            Returns "True" if the copy process was successful or "False"
            otherwise.

            Examples:

            >>> target = Handler(
            ...     location=__test_folder__ + 'copy_file.py',
            ...     must_exist=False)
            >>> Handler(location=__file_path__).copy(target)
            True
            >>> target.is_file()
            True

            >>> target = Handler(
            ...     location=__test_folder__ + 'copy_directory2',
            ...     must_exist=False)
            >>> Handler(
            ...     __test_folder__ + 'copy_directory', make_directory=True
            ... ).copy(target)
            True
            >>> target.is_directory()
            True

            >>> target.copy(__test_folder__ + 'copy_directory3', right=777)
            True
        '''
## python2.7
##         default_keywords = boostNode.extension.native.Dictionary(
##             content=keywords)
##         right, keywords = default_keywords.pop(name='right')
##         octal, keywords = default_keywords.pop(
##             name='octal', default_value=True)
        pass
##
        target = self.__class__(location=target, must_exist=False)
        if self.is_file():
            shutil.copy2(self._path, target._path, *arguments, **keywords)
        else:
            shutil.copytree(self._path, target._path)
        if right is not None:
            target.change_right(right, octal)
        return target.type == self.type

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def make_new_directory(self, wrapper_pattern='{file_name}_temp'):
    def make_new_directory(
        self: boostNode.extension.type.Self,
        wrapper_pattern='{file_name}_temp'
    ) -> boostNode.extension.type.SelfClassObject:
##
        '''
            Makes a new directory in each case. E.g. if current directory name
            already exists. The given wrapper pattern is used as long resulting
            name is unique. The handler which creates the folder will be
            given back.

            Examples:

            >>> handler = Handler(
            ...     __test_folder__ + 'make_new_directory', must_exist=False)

            >>> handler.make_new_directory().path # doctest: +ELLIPSIS
            '...make_new_directory...'

            >>> handler.make_new_directory().path # doctest: +ELLIPSIS
            '...make_new_directory_temp...'

            >>> handler.make_new_directory().path # doctest: +ELLIPSIS
            '...make_new_directory_temp_temp...'

            >>> handler.make_new_directory(
            ...     wrapper_pattern='{file_name}_t'
            ... ).path # doctest: +ELLIPSIS
            '...make_new_directory_t...'
        '''
        location = self.__class__(self, must_exist=False)
        while location:
            path = location.directory_path + wrapper_pattern.format(
                file_name=location.name)
            location = self.__class__(location=path, must_exist=False)
        location.make_directory()
        return location

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def make_directory(self, *arguments, **keywords):
    def make_directory(
        self: boostNode.extension.type.Self, *arguments: builtins.object,
        right=700, octal=True, **keywords: builtins.object
    ) -> builtins.bool:
##
        '''
            Implements the pythons native "os.mkdir()" method in an object
            oriented way.

            Create a directory named path with numeric mode. The default
            mode is "700" (octal). If the directory already exists, "OSError"
            is raised.

            "right" is new the right for the current object's path location.

            Returns "True" if the creation process was successful or "False"
            otherwise.

            Examples:

            >>> handler = Handler(
            ...     location=__test_folder__ + 'make_directory',
            ...     must_exist=False)

            >>> handler.is_element()
            False
            >>> handler.make_directory()
            True
            >>> handler.is_directory()
            True

            >>> handler.remove_directory()
            True
            >>> handler.make_directory(right=777)
            True
        '''
## python2.7
##         default_keywords = boostNode.extension.native.Dictionary(
##             content=keywords)
##         right, keywords = default_keywords.pop(
##             name='right', default_value=700)
##         octal, keywords = default_keywords.pop(
##             name='octal', default_value=True)
        pass
##
        os.mkdir(self._path, *arguments, **keywords)
        self.change_right(right, octal)
        return self.is_directory()

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def make_symbolic_link(self, *arguments, **keywords):
    def make_symbolic_link(
        self: boostNode.extension.type.Self, *arguments: builtins.object,
        **keywords: builtins.object
    ) -> builtins.bool:
##
        '''
            Implements the pythons native "os.symlink()" method in an object
            oriented way. The optional parameter "force" is added.

            Create a symbolic link pointing to current location named by
            given "target" variable.
            On Windows, symbolic link version takes an additional optional
            parameter, target_is_directory, which defaults to "False".
            On Windows, a symbolic link represents a file or a directory, and
            does not morph to the target dynamically. For this reason, when
            creating a symbolic link on Windows, if the target is not already
            present, the symbolic link will default to being a file symbolic
            link. If "target_is_directory" is set to "True", the symbolic link
            will be created as a directory symbolic link. This parameter is
            ignored if the target exists (and the symbolic link is created
            with the same type as the target).
            Symbolic link support was introduced in Windows 6.0 (Vista).
            The native python "os.symlink()" method will raise a
            "NotImplementedError" on Windows versions earlier than 6.0.

            Note: The "CreateSymbolicLinkPrivilege" is required in order to
            successfully create symbolic links. This privilege is not typically
            granted to regular users but is available to accounts which can
            escalate privileges to the administrator level. Either obtaining
            the privilege or running your application as an administrator are
            ways to successfully create symbolic links.
            OSError is raised when the function is called by an unprivileged
            user.

            "force" triggers if symbolic links with not existing referenced
                    files should be made. If target exists it will be
                    overwritten if set to "True".
            "relative" triggers if target should be referenced via relative
                       path. If "True" relative path will be determined from
                       current working directory, if a path or Handler object
                       is provided this location will be used as context to
                       determine relative path, if
                       "boostNode.extension.type.Self" is provided target
                       location will be used as context and if "False"
                       (default) path will be referenced absolute.

            Examples:

            >>> target = Handler(
            ...     __test_folder__ + 'make_symbolic_link_target',
            ...     must_exist=False)
            >>> if boostNode.extension.system.Platform(
            ...     ).operating_system == 'windows':
            ...     True
            ... else:
            ...     created = Handler(
            ...         location=__test_folder__ +
            ...             'make_symbolic_link_directory_source',
            ...         make_directory=True
            ...     ).make_symbolic_link(target, force=True)
            ...     target.is_symbolic_link()
            True

            >>> target = Handler(
            ...     __test_folder__ + 'make_symbolic_link_target',
            ...     must_exist=False)
            >>> if boostNode.extension.system.Platform(
            ...     ).operating_system == 'windows':
            ...     True
            ... else:
            ...     source = Handler(
            ...         location=__test_folder__ +
            ...             'make_symbolic_link_file_source',
            ...         must_exist=False)
            ...     source.content = ' '
            ...     created = source.make_symbolic_link(target, force=True)
            ...     target.is_symbolic_link()
            True
        '''
        return self._make_link(*arguments, symbolic=True, **keywords)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def make_hardlink(self, *arguments, **keywords):
    def make_hardlink(
        self: boostNode.extension.type.Self, *arguments: builtins.object,
        **keywords: builtins.object
    ) -> builtins.bool:
##
        '''
            Implements the pythons native "os.link()" method in an object
            oriented way. The optional parameter "force" is added.

            "force" triggers if hard links with not existing referenced
                    files should be made. If target exists it will be
                    overwritten if set to "True".

            Examples:

            >>> target = Handler(
            ...     __test_folder__ + 'make_hardlink_target', must_exist=False)
            >>> if boostNode.extension.system.Platform(
            ...     ).operating_system == 'windows':
            ...     True
            ... else:
            ...     source = Handler(
            ...         location=__test_folder__ + 'make_hardlink_source',
            ...         must_exist=False)
            ...     source.content = ' '
            ...     created = source.make_hardlink(target, force=True)
            ...     target.is_file()
            True
        '''
        return self._make_link(*arguments, symbolic=False, **keywords)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def read_symbolic_link(self, as_object=False, *arguments, **keywords):
    def read_symbolic_link(
        self: boostNode.extension.type.Self, as_object=False,
        *arguments: builtins.object, **keywords: builtins.object
    ) -> (builtins.str, boostNode.extension.type.SelfClassObject):
##
        '''
            Implements the pythons native "os.readlink()" method in an object
            oriented way. Additionall support for portable text-based
            link-files is added.

            Return a string representing the path to which the symbolic link
            points. The result may be either an absolute or relative pathname;
            if it is relative, it may be converted to an absolute pathname
            using pythons native "os.path.join" method as
            "os.path.join(os.path.dirname(path), result)".
            If the path is a string object, the result will also be a string
            object, and the call may raise an "UnicodeDecodeError". If the
            path is a bytes object, the result will be a bytes object.
            You can use the optional "as_object" parameter for getting a
            Handler object. This is very useful if you don't know if the
            resulting path is either a relative or an absolute one.

            Returns the path referenced by the link file.

            Examples:

            >>> source = Handler(location=__file_path__)
            >>> target = Handler(
            ...     __test_folder__ + 'read_symbolic_link', must_exist=False)
            >>> if boostNode.extension.system.Platform(
            ...     ).operating_system == 'windows':
            ...     True
            ... else:
            ...     created = source.make_symbolic_link(
            ...         target=target, force=True)
            ...     target.read_symbolic_link() == __file_path__
            True

            >>> if boostNode.extension.system.Platform(
            ...     ).operating_system == 'windows':
            ...     True
            ... else:
            ...     target.read_symbolic_link(as_object=True) == source
            True

            >>> target.remove_file()
            True
            >>> if boostNode.extension.system.Platform(
            ...     ).operating_system == 'windows':
            ...     'Object of "Handler" with path "...'
            ... else:
            ...     os.symlink('../', target._path)
            ...     target.read_symbolic_link(
            ...         as_object=True
            ...     ) # doctest: +ELLIPSIS
            Object of "Handler" with path "...
        '''
        path = self._path
        if self._path.endswith(os.sep):
            path = self._path[:-builtins.len(os.sep)]
        if self.is_symbolic_link(allow_portable_link=False):
            link = os.readlink(path, *arguments, **keywords)
        else:
            link = self.read_portable_link()
        if not link.endswith(os.sep) and os.path.isdir(link):
            link += os.sep
        link = link[builtins.len(self._root_path) - builtins.len(os.sep):]
        if as_object:
            if not self.is_referenced_via_absolute_path(location=link):
                return self.__class__(
                    location=self.directory_path + link,
                    must_exist=False)
            return self.__class__(location=link, must_exist=False)
        return link

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def deep_copy(
##         self, target, symbolic_links=True, *arguments, **keywords
##     ):
    def deep_copy(
        self: boostNode.extension.type.Self,
        target: (boostNode.extension.type.SelfClassObject,
                 builtins.str),
        symbolic_links=True, *arguments: builtins.object,
        respect_root_path=None, **keywords: builtins.object
    ) -> boostNode.extension.type.Self:
##
        '''
            Implements the pythons native "shutil.copytree()" method in an
            object oriented way.

            Recursively copy an entire directory tree rooted at current
            location. The destination directory, named by given parameter
            "target", must not already exist; it will be created as well as
            missing parent directories. Permissions and times of directories
            are copied with pythons native method "shutil.copystat",
            individual files are copied using pythons native "shutil.copy2()"
            method. If given parameter "symbolic_links" is "True",
            symbolic links in the source tree are represented as symbolic
            links in the new tree; if false, the contents of the linked files
            are copied to the new tree. When "symbolic_links" is "False", e.g.
            if the file pointed by the symbolic link doesn't exist, a exception
            will be added in the list of errors raised in a error exception at
            the end of the copy process.
            You can set the optional "ignore_dangling_symlinks" flag to "True"
            if you want to silence this exception. Notice that this option has
            no effect on platforms that don't support pythons native
            "os.symlink" method.
            If ignore is given, it must be a callable that will recieve as its
            arguments the directory being visited by pythons native method
            "shutil.copytree", and a list of its contents, as returned by
            pythons "os.listdir" method. Since "shutil.copytree" is called
            recursively, the ignore callable will be called once for each
            directory that is copied. The callable must return a sequence of
            directory and file names relative to the current directory
            (i.e. a subset of the items in its second argument); these names
            will then be ignored in the copy process. Pythons native method
            "shutil.ignore_patterns()" can be used to create such a callable
            that ignores names based on glob-style patterns.
            If exception(s) occur, an error is raised with a list of reasons.
            If parameter "copy_function" is given, it must be a callable that
            will be used to copy each file. It will be called with the source
            path and the target path as arguments. By default, pythons native
            "shutil.copy2()" is used, but any function that supports the same
            signature (like pythons "shutil.copy()") can be used.

            "target" is path or "Handler" object pointing to target
                     destination.

            Examples:

            >>> handler = Handler(
            ...     location=__test_folder__ + 'deep_copy',
            ...     make_directory=True)
            >>> Handler(
            ...     location=handler.path + 'sub_dir',
            ...     make_directory=True
            ... ) # doctest: +ELLIPSIS
            Object of "Handler" with path "...deep_copy...sub_di..." (d...
            >>> Handler(
            ...     location=handler.path + 'second_sub_dir',
            ...     make_directory=True
            ... ) # doctest: +ELLIPSIS
            Object of "Handler" with path "...deep_copy...second_sub_di...

            >>> target = Handler(
            ...     __test_folder__ + 'deep_copy_dir', must_exist=False)
            >>> handler.deep_copy(target) # doctest: +ELLIPSIS
            Object of "Handler" with path "...deep_copy..." (directory).
            >>> Handler(location=target.path + 'sub_dir').is_directory()
            True
            >>> Handler(target.path + '/second_sub_dir').is_directory()
            True
        '''
## python2.7
##         respect_root_path, keywords = boostNode.extension.native.Dictionary(
##             content=keywords
##         ).pop(name='respect_root_path')
        pass
##
        shutil.copytree(
            src=self._path, dst=self.get_path(
                location=target, respect_root_path=respect_root_path,
                output_with_root_prefix=True),
            symlinks=symbolic_links, *arguments, **keywords)
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def make_directorys(self, *arguments, **keywords):
    def make_directorys(
        self: boostNode.extension.type.Self, *arguments: builtins.object,
        **keywords: builtins.object
    ) -> builtins.bool:
##
        '''
            Implements the pythons native "os.makedirs()" method in an object
            oriented way.

            Recursive directory creation function. Like pythons native
            "os.mkdir()" method, but creates all intermediate-level
            directories needed to contain the leaf directory. If the target
            directory with the same mode as specified already exists, raises
            an "OSError" exception if given parameter "exist_ok" is "False",
            otherwise no exception is raised. If the directory cannot be
            created in other cases, raises an "OSError" exception.
            The default mode is "0o770" (octal). On some systems, "mode" is
            ignored. Where it is used, the current "umask" value is first
            masked out.
            Note "make_directorys()" will become confused if the path elements
            to create include parent directory.

            Examples:

            >>> handler = Handler(
            ...     location=__test_folder__ + 'dir/sub_dir/sub_sub_dir',
            ...     must_exist=False)
            >>> handler.make_directorys()
            True
            >>> handler.path # doctest: +ELLIPSIS
            '...dir...sub_dir...sub_sub_dir...'
            >>> handler.is_directory()
            True

            >>> handler = Handler(
            ...     location=__test_folder__ + 'dir', must_exist=False)
            >>> handler.make_directorys()
            True
            >>> handler.path # doctest: +ELLIPSIS
            '...dir...'
            >>> handler.is_directory()
            True
        '''
        if not self:
            os.makedirs(self._path, *arguments, **keywords)
        return self.is_directory()

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def make_portable_link(
##         self, target, force=False, label='', *arguments, **keywords
##     ):
    def make_portable_link(
        self: boostNode.extension.type.Self,
        target: (boostNode.extension.type.SelfClassObject,
                 builtins.str),
        force=False, label='', *arguments: (builtins.object, builtins.type),
        **keywords: (builtins.object, builtins.type)
    ) -> builtins.bool:
##
        '''
            Creates a portable link on the current location referencing on the
            given path ("target").

            "target" is path or "Handler" object pointing to target
                     destination.
            "force" means to trigger if a file on the target location should
                    be overwritten.
            "label" is a useful label to distinguish portable linked files
                    from other text-based files. Default is setted to the
                    current class description.

            Examples:

            >>> target = Handler(
            ...     location=__test_folder__ + 'link.py', must_exist=False)
            >>> Handler(location=__file_path__).make_portable_link(
            ...     target, force=True)
            True
            >>> target.content # doctest: +ELLIPSIS
            '...portable...'

            >>> target = Handler(
            ...     location=__test_folder__ + 'directory_link',
            ...     must_exist=False)
            >>> Handler(
            ...     __test_folder__ + 'directory', make_directory=True
            ... ).make_portable_link(target, force=True)
            True
            >>> target.content # doctest: +ELLIPSIS
            '...portable...'

            >>> target = Handler(
            ...     location=__test_folder__ + 'link', must_exist=False)
            >>> Handler(location=__file_path__).make_portable_link(
            ...     target, force=True, label='hans')
            True
            >>> target.content # doctest: +ELLIPSIS
            '...portable...'
        '''
        target = self.__class__(location=target, must_exist=False)
        if target and force:
            target.remove_deep()
        if not label:
            label = self.__class__.__name__
        target.content = self.get_portable_link_content(
            label, target_path=target._path, *arguments, **keywords)
        return target.is_portable_link()

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def read_portable_link(self):
    def read_portable_link(
        self: boostNode.extension.type.Self
    ) -> builtins.str:
##
        '''
            Reads the referenced path of a given portable link file.

            Examples:

            >>> target = Handler(
            ...     location=__test_folder__ + 'link.py', must_exist=False)
            >>> handler = Handler(location=__file_path__).make_portable_link(
            ...     target, force=True)
            >>> target.read_portable_link() # doctest: +ELLIPSIS
            '...file.py'

            >>> target = Handler(
            ...     location=__test_folder__ + 'link3', must_exist=False)
            >>> handler = Handler(
            ...     __test_folder__ + 'directory', make_directory=True
            ... ).make_portable_link(target, force=True)
            >>> target.read_portable_link() # doctest: +ELLIPSIS
            '...directory...'

            >>> Handler().read_portable_link()
            ''
        '''
        if self.is_portable_link():
            return re.compile(
                self.portable_regex_link_pattern
            ).match(self.content.strip()).group('path')
        return ''

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def clear_directory(self):
    def clear_directory(
        self: boostNode.extension.type.Self
    ) -> builtins.bool:
##
        '''
            Deletes the contents of the current directory location without
            deleting the current location itself.

            Examples:

            >>> handler = Handler(
            ...     location=__test_folder__ + 'dir', make_directory=True)

            >>> sub_handler = Handler(
            ...     location=__test_folder__ + 'dir/sub_dir',
            ...     make_directory=True)
            >>> handler.clear_directory()
            True
            >>> sub_handler.is_element()
            False
            >>> handler.is_directory()
            True

            >>> handler.clear_directory()
            False
        '''
        if builtins.len(self):
            self.iterate_directory(self.remove_deep.__name__)
            return not builtins.len(self)
        return False

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def iterate_directory(
##         self, function, recursive=False, recursive_in_link=True,
##         deep_first=True, *arguments, **keywords
##     ):
    def iterate_directory(
        self: boostNode.extension.type.Self,
        function: (builtins.str, types.FunctionType,
                   types.MethodType),
        recursive=False, recursive_in_link=True,
        deep_first=True, *arguments: builtins.object,
        **keywords: builtins.object
    ) -> builtins.bool:
##
        '''
            Apply a given function or method to the current directory path.
            If the optional parameter "recursive" is set to "True" the given
            function is applied to to all subdirectories of the current path.
            If the given parameter "function" is a string, a new instance of
            "Directory" will be created for each object.
            If "function" represents a local method the current scope will be
            accessible in the given method.

            If "function" is a string, a new instance is created otherwise not.

            Returns "False" if any call of "function" returns "False" or
            current thread was terminated and "True" otherwise.

            If function call returns "False" further iterations in
            current dimension will be stopped. If function's return value is
            "None", current file object is a directory and recursion is
            enabled the iteration will not enter current directory.

            Examples:

            >>> Handler().iterate_directory(function=lambda file: file)
            True

            >>> Handler().iterate_directory(function=lambda file: False)
            False

            >>> elements = []

            >>> Handler().iterate_directory(
            ...     function=lambda file: elements.append(file.name))
            True
            >>> elements # doctest: +ELLIPSIS
            [...'file.py'...]

            >>> Handler().iterate_directory(
            ...     lambda file: elements.append(file.name), deep_first=False)
            True

            >>> boostNode.extension.system.Platform.terminate_thread = True
            >>> Handler().iterate_directory(lambda file: True)
            False
            >>> boostNode.extension.system.Platform.terminate_thread = False

            >>> Handler(
            ...     Handler(__file_path__).directory_path + '../'
            ... ).iterate_directory(
            ...     lambda file: True, deep_first=False,
            ...     recursive=True)
            True

        '''
        files = self.list()
        if not deep_first:
            files = self._sort_by_file_types(files, recursive_in_link)
        for file in files:
            if boostNode.extension.system.Platform.check_thread():
                return False
            if builtins.isinstance(function, builtins.str):
                result = builtins.getattr(file, function)(
                    *arguments, **keywords)
            else:
                result = function(file, *arguments, **keywords)
            if result is False:
                return False
            if(recursive and result is not None and
               file.is_directory(allow_link=recursive_in_link)):
                '''
                    Take this method type by another instance of this class via
                    introspection.
                '''
                builtins.getattr(file, inspect.stack()[0][3])(
                    function, recursive, recursive_in_link, deep_first,
                    *arguments, **keywords)
        return True

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def delete_file_patterns(self, *patterns):
    def delete_file_patterns(
        self: boostNode.extension.type.Self, *patterns: builtins.str
    ) -> boostNode.extension.type.Self:
##
        '''
            Removes files with filenames matching the given patterns.
            This method search recursively for matching file names.

            Examples:

            >>> handler = Handler(
            ...     __test_folder__ + 'delete_file_patterns',
            ...     make_directory=True)
            >>> a_a = Handler(
            ...     __test_folder__ + 'delete_file_patterns/a.a',
            ...     must_exist=False)
            >>> a_a.content = 'A'
            >>> a_b = Handler(
            ...     __test_folder__ + 'delete_file_patterns/a.b',
            ...     must_exist=False)
            >>> a_b.content = 'A'
            >>> b_b = Handler(
            ...     __test_folder__ + 'delete_file_patterns/b.b',
            ...     must_exist=False)
            >>> b_b.content = 'A'
            >>> a_c = Handler(
            ...     __test_folder__ + 'delete_file_patterns/a.c',
            ...     must_exist=False)
            >>> a_c.content = 'A'
            >>> handler.delete_file_patterns(
            ...     '.+\.b', 'a\.c') # doctest: +ELLIPSIS
            Object of "Handler" with path "...delete_file_patterns..."...
            >>> a_a.is_file()
            True
            >>> a_b.is_file()
            False
            >>> b_b.is_file()
            False
            >>> a_c.is_file()
            False
        '''
        for file in self:
            for pattern in patterns:
                if re.compile(pattern).match(file.name):
                    file.remove_deep()
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def open(self):
    def open(self: boostNode.extension.type.Self) -> builtins.dict:
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

            >>> Handler(location=__file_path__).open() # doctest: +SKIP

            >>> Handler().open() # doctest: +SKIP
        '''
        if builtins.hasattr(os, 'startfile'):
            return os.startfile(self._path)
        shell_file = boostNode.extension.native.String(
            self._path
        ).validate_shell()
        if builtins.hasattr(os, 'open'):
            return boostNode.extension.system.Platform.run(
                command='open', command_arguments=(shell_file,))
        return boostNode.extension.system.Platform.run(
            command='xdg-open', command_arguments=(shell_file,))

        # endregion

        # region protected methods

## python2.7
##     def _prepare_content_status(self, mode, content):
    def _prepare_content_status(
        self: boostNode.extension.type.Self, mode: builtins.str,
        content: (builtins.str, builtins.bytes)
    ) -> builtins.str:
##
        '''Initializes a file for changing its content,'''
        if self.is_element() and not self.is_file():
            raise __exception__(
                'Set content is only possible for files and not for "%s" '
                '(%s).', self.path, self.type)
        if mode is None:
            mode = 'w'
            if boostNode.extension.native.Object(object=content).is_binary():
                mode = 'w+b'
        return mode

## python2.7
##     def _get_path(
##         self, location, respect_root_path, output_with_root_prefix
##     ):
    def _get_path(
        self: boostNode.extension.type.Self,
        location: (boostNode.extension.type.SelfClassObject, builtins.str),
        respect_root_path: (builtins.bool, builtins.type(None)),
        output_with_root_prefix: (builtins.bool, builtins.type(None))
    ) -> builtins.str:
##
        '''
            This method is used as helper method for "get_path()".
            It deals the case where an explicit location was given.

            Examples:

            >>> Handler()._get_path(os.sep, True, False) # doctest: +ELLIPSIS
            '...'
        '''
        taken_respect_root_path = respect_root_path
        if respect_root_path is None:
            taken_respect_root_path = self._respect_root_path
        if not builtins.isinstance(location, self.__class__):
            location = self.__class__(
                location, respect_root_path=taken_respect_root_path,
                output_with_root_prefix=output_with_root_prefix,
                must_exist=False)
        return location.get_path(
            respect_root_path=taken_respect_root_path,
            output_with_root_prefix=output_with_root_prefix)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def _make_link(
##         self, target, symbolic, *arguments, **keywords
##     ):
    def _make_link(
        self: boostNode.extension.type.Self,
        target: (boostNode.extension.type.SelfClassObject, builtins.str),
        symbolic: builtins.bool, *arguments: builtins.object, force=False,
        relative=None, **keywords: builtins.object
    ) -> builtins.bool:
##
        '''
            Makes hard or symbolic links and handles the optional force option.

            Examples:

            >>> target = Handler(
            ...     __test_folder__ + '_make_link', make_directory=True)
            >>> Handler()._make_link(target, symbolic=True)
            False
        '''
## python2.7
##         keywords_dictionary = boostNode.extension.native.Dictionary(
##             content=keywords)
##         force, keywords = keywords_dictionary.pop(
##             name='force', default_value=False)
##         relative, keywords = keywords_dictionary.pop(name='relative')
        pass
##
        target = self.__class__(location=target, must_exist=False)
        if force:
            return self._make_forced_link(
                symbolic, target, relative, *arguments, **keywords)
        elif target:
            __logger__.warning(
                'Link from "{path}" to "{target_path}" wasn\'t created '
                'because "{target_path}" already exists.'.format(
                    path=self.path, target_path=target.path))
            return False
        return self._make_platform_dependent_link(
            symbolic, target, relative, *arguments, **keywords)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def _is_equivalent_folder(self, other, second_round=False):
    def _is_equivalent_folder(
        self: boostNode.extension.type.Self,
        other: boostNode.extension.type.SelfClassObject, second_round=False
    ) -> builtins.bool:
##
        '''
            Returns "True" if given folder contains likewise content.
            Serves as helper method.

            Examples:

            >>> target = Handler(
            ...     __test_folder__ + '_is_equivalent_folder',
            ...      must_exist=False)

            >>> Handler().copy(target)
            True
            >>> del target[0]
            >>> target._is_equivalent_folder(Handler())
            False

            >>> target.remove_deep()
            True
            >>> Handler().copy(target)
            True
            >>> target[0].content = ' '
            >>> Handler()._is_equivalent_folder(target)
            False
        '''
        for file in self:
            same_so_far = False
            for other_file in other:
                if(file.name == other_file.name and
                   file.type == other_file.type):
                    if file.is_equivalent(other=other_file):
                        same_so_far = True
                        break
                    else:
                        return False
            if not same_so_far:
                return False
        '''We have to check the other way around.'''
        return second_round or other._is_equivalent_folder(
            self, second_round=True)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def _prepend_root_path(self):
    def _prepend_root_path(
        self: boostNode.extension.type.Self
    ) -> builtins.str:
##
        '''
            Prepends root path prefix to current file path.

            Examples:

            >>> root_save = Handler.get_root()

            >>> Handler.set_root(
            ...     location='/not/existing/'
            ... ) # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            boostNode.extension.native.FileError: Invalid path "..." ...

            >>> Handler.set_root(location=root_save) # doctest: +ELLIPSIS
            <class '...Handler'>

            >>> handler = Handler()
            >>> handler._prepend_root_path() # doctest: +ELLIPSIS
            '...'

            >>> handler._root_path_initialized = False
            >>> handler._path = 'C:\\\\'
            >>> handler._prepend_root_path() # doctest: +ELLIPSIS
            '...'
        '''
        if self._respect_root_path and not self._root_path_initialized:
            self.set_root(location=self._root_path)
            self._root_path_initialized = True
            operating_system = \
                boostNode.extension.system.Platform().operating_system
            '''
                Prepend root path to given path location, if it wasn't
                given as location in root path.
            '''
            if((self._initialized_path.startswith(
                    self._root_path[:-builtins.len(os.sep)]) or
                not self._path.startswith(
                    self._root_path[:-builtins.len(os.sep)])) and not
                ('windows' == operating_system and
                 re.compile('^[a-zA-Z]:\\.*').match(self._path) and
                 self._root_path == os.sep)):
                if self._path.startswith(os.sep):
                    self._path = self._root_path[:-builtins.len(
                        os.sep)] + self._path
                else:
                    self._path = self._root_path + self._path
        return self._path

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def _handle_path_existence(
##         self, location, make_directory, must_exist, arguments, keywords
##     ):
    def _handle_path_existence(
        self: boostNode.extension.type.Self,
        location: (builtins.str, boostNode.extension.type.SelfClassObject,
                   builtins.type(None)),
        make_directory: builtins.bool, must_exist: builtins.bool,
        arguments: builtins.tuple, keywords: builtins.dict
    ) -> boostNode.extension.type.Self:
##
        '''
            Make initial existence like it was specified on initialisation.

            Examples:

            >>> Handler(
            ...     __test_folder__ + '_handle_path_existence_not_existing',
            ...     must_exist=False
            ... )._handle_path_existence(Handler(
            ...     __test_folder__ + '_handle_path_existence_not_existing',
            ...      must_exist=False), False, True, (), {}
            ... ) # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            boostNode.extension.native.FileError: Invalid path...
        '''
        if make_directory and not self:
            self.make_directory(*arguments, **keywords)
        if not self._set_path(path=self._path) and must_exist:
            if builtins.isinstance(location, self.__class__):
                location = location._path
            raise __exception__(
                'Invalid path "{path}" for an object of "{class_name}". Given '
                'path was "{given_path}".'.format(
                    path=self.path, class_name=self.__class__.__name__,
                    given_path=location))
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def _initialize_path(self):
    def _initialize_path(
        self: boostNode.extension.type.Self
    ) -> builtins.str:
##
        '''
            Normalizes reference to file object.

            Examples:

            >>> Handler()._initialize_path() # doctest: +ELLIPSIS
            '...boostNode...extension'

            >>> Handler('~')._initialize_path() # doctest: +ELLIPSIS
            '...'

            >>> Handler(
            ...     'test/~', must_exist=False
            ... )._initialize_path() # doctest: +ELLIPSIS
            '...test...~'

            >>> Handler(
            ...     '///test//hans/~', must_exist=False
            ... )._initialize_path() # doctest: +ELLIPSIS
            '...test...hans...~'
        '''
        self._path = self._initialized_path
        self._path = os.path.normpath(os.path.expanduser(self._path))
        if re.compile('^[a-zA-Z]:$').match(self._initialized_path):
            self._path += '/'
        if not self.is_referenced_via_absolute_path():
            self._path = os.path.abspath(self._path)
        return self._path

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def _initialize_location(self, location):
    def _initialize_location(
        self: boostNode.extension.type.Self,
        location: (boostNode.extension.type.SelfClassObject, builtins.str,
                   builtins.type(None))
    ) -> builtins.str:
##
        '''
            Normalizes a given file object reference to "builtins.str".
            If "None" is given current directory path is returned.

            Examples:

            >>> Handler()._initialize_location(None)
            '.'

            >>> Handler()._initialize_location(Handler()) == Handler()._path
            True
        '''
        if location is None:
            location = os.curdir
        elif builtins.isinstance(location, self.__class__):
            location = location._path
        return location

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def _set_path(self, path):
    def _set_path(
        self: boostNode.extension.type.Self, path: builtins.str
    ) -> builtins.bool:
##
        '''
            Sets path for the currently used "Handler" object in an convinced
            platform independent way.

            Returns "True" if the given path exists on the file system or
            "False" otherwise.

            Examples:

            >>> Handler()._set_path(path=__file_path__)
            True

            >>> Handler()._set_path(
            ...     path=__test_folder__ + 'set_path_not_existing_file')
            False

            >>> handler = Handler()
            >>> handler._set_path(path='.')
            True
            >>> handler.path # doctest: +ELLIPSIS
            '...boostNode...'
        '''
        self._path = os.path.normpath(path)
        if not self.is_referenced_via_absolute_path():
            self._path = os.path.abspath(self._path)
        self.path
        return self.is_element()

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def _make_forced_link(
##         self, symbolic, target, relative, *arguments, **keywords
##     ):
    def _make_forced_link(
        self: boostNode.extension.type.Self,
        symbolic: builtins.bool,
        target: boostNode.extension.type.SelfClassObject,
        relative: (builtins.object, builtins.type),
        *arguments: builtins.object, **keywords: builtins.object
    ) -> builtins.bool:
##
        '''
            Creates a symbolic link weather their exists already a file with
            given link location or link target doesn't exist.

            Examples:

            >>> Handler()._make_forced_link(
            ...     True, Handler(), False
            ... ) # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            boostNode.extension.native.FileError: ...

            >>> Handler(
            ...     __test_folder__ + '_make_forced_link_not_existing',
            ...     must_exist=False
            ... )._make_forced_link(
            ...     True, Handler(
            ...         __test_folder__ + '_make_forced_link_target',
            ...         must_exist=False),
            ...     False)
            True
        '''
        if self == target:
            raise __exception__('It isn\'t possible to link to itself.')
        if target:
            if not target.remove_deep():
                return False
        if not self:
            '''
                Create a necessary dummy path to create symbolic links pointing
                to nothing.
            '''
            path = ''
            for path_part in self._path[builtins.len(os.sep):].split(os.sep):
                path += os.sep + path_part
                path_object = self.__class__(location=path, must_exist=False)
                if not path_object:
                    break
            self.make_directorys()
            successfull = self._make_platform_dependent_link(
                symbolic, target, relative, *arguments, **keywords)
            '''Delete everything we temporary created before.'''
            path_object.remove_deep()
            return successfull
        return self._make_platform_dependent_link(
            symbolic, target, relative, *arguments, **keywords)

            # region handle platform dependencies methods

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def _make_platform_dependent_link(
##         self, symbolic, target, relative, *arguments, **keywords
##     ):
    def _make_platform_dependent_link(
        self: boostNode.extension.type.Self, symbolic: builtins.bool,
        target: boostNode.extension.type.SelfClassObject,
        relative: (builtins.object, builtins.type),
        *arguments: builtins.object, **keywords: builtins.object
    ) -> builtins.bool:
##
        '''
            Handles platform dependent stuff by creating a symbolic link.

            Examples:

            >>> if boostNode.extension.system.Platform(
            ...     ).operating_system == 'windows':
            ...     True
            ... else:
            ...     Handler()._make_platform_dependent_link(
            ...         symbolic=True,
            ...         target=Handler(
            ...             __test_folder__ +
            ...             '_make_platform_dependent_link',
            ...             must_exist=False),
            ...         relative=False
            ...     ) # doctest: +ELLIPSIS
            True
        '''
        target_path = target._path
        if target._path.endswith(os.sep):
            target_path = target._path[:-builtins.len(os.sep)]
        source_path = self._determine_relative_path(relative, target_path)
        if source_path.endswith(os.sep):
            source_path = source_path[:-builtins.len(os.sep)]
        operating_system = \
            boostNode.extension.system.Platform().operating_system
        if symbolic:
            try:
                if operating_system == 'windows':
## python2.7
##                     create_symbolic_link = \
##                         ctypes.windll.kernel32.CreateSymbolicLinkW
##                     create_symbolic_link.argtypes = (
##                         ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32)
##                     create_symbolic_link.restype = ctypes.c_ubyte
##                     if(create_symbolic_link(
##                        target_path, source_path,
##                        (1 if self.is_directory() else 0)) == 0):
##                         raise ctypes.WinError()
                    os.symlink(
                        source_path, target_path,
                        target_is_directory=self.is_directory())
##
                else:
                    os.symlink(source_path, target_path)
            except(builtins.AttributeError, builtins.NotImplementedError):
                return self.make_portable_link(target, *arguments, **keywords)
            else:
                return target.is_symbolic_link()
        os.link(source_path, target_path)
        return target.is_file()

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def _determine_relative_path(self, relative, target_path):
    def _determine_relative_path(
        self: boostNode.extension.type.Self,
        relative: (builtins.object, builtins.type),
        target_path: builtins.str
    ) -> builtins.str:
##
        '''
            Determines relative depending on given requirements defined by
            "relative".
        '''
        if relative:
            if relative is boostNode.extension.type.Self:
                '''
                    NOTE: "target_path" is one level to deep because references
                    are save in parent directory.
                '''
                return self.get_relative_path(
                    context=self.__class__(
                        location=target_path, must_exist=False,
                        respect_root_path=False
                    ).directory_path)
            if builtins.isinstance(relative, (builtins.str, self.__class__)):
                return self.get_relative_path(context=relative)
            return self.relative_path
        return self._path

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def _determine_get_windows_disk_free_space_function(self):
    def _determine_get_windows_disk_free_space_function(
        self: boostNode.extension.type.Self
    ) -> (builtins.bool, builtins.int):
##
        '''
            Determines windows internal method to get disk free space.
        '''
        if(sys.version_info >= (3,) or
           builtins.isinstance(self._path, builtins.unicode)):
            return ctypes.windll.kernel32.GetDiskFreeSpaceExW
        return ctypes.windll.kernel32.GetDiskFreeSpaceExA

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def _get_platform_dependent_free_and_total_space(self):
    def _get_platform_dependent_free_and_total_space(
        self: boostNode.extension.type.Self
    ) -> (builtins.bool, builtins.tuple):
##
        '''
            Handles platform dependent stuff by determining free and total
            space on given file system location.

            Examples:

            >>> isinstance(
            ...     Handler()._get_platform_dependent_free_and_total_space(),
            ...     builtins.tuple)
            True

            >>> Handler(
            ...     'not_existing', must_exist=False
            ... )._get_platform_dependent_free_and_total_space()
            False
        '''
        os_statvfs = self._initialize_platform_dependencies()
        if os.path.isfile(self._path) or os.path.isdir(self._path):
            if not os_statvfs is None:
                return (
                    os_statvfs.f_bavail * self.BLOCK_SIZE_IN_BYTE,
                    os_statvfs.f_blocks * self.BLOCK_SIZE_IN_BYTE)
            if builtins.hasattr(ctypes, 'windll'):
                path = self._path
                if self.is_file():
                    path = self.directory_path
                free_bytes = ctypes.c_ulonglong(0)
                total_bytes = ctypes.c_ulonglong(0)
                self._determine_get_windows_disk_free_space_function()(
                    ctypes.c_wchar_p(path), None, ctypes.pointer(total_bytes),
                    ctypes.pointer(free_bytes))
                return free_bytes.value, total_bytes.value
        return False

    @boostNode.paradigm.aspectOrientation.JointPoint
# NOTE return type only available in unix like systems:
# -> (posix.statvfs_result, builtins.type(None))
## python2.7
##     def _initialize_platform_dependencies(
##         self, force_macintosh_behavior=False
##     ):
    def _initialize_platform_dependencies(
        self: boostNode.extension.type.Self, force_macintosh_behavior=False
    ):
##
        '''
            Handles platform specified stuff like determining inode size.

            Examples:

            >>> len(Handler()._initialize_platform_dependencies()) > 0
            True

            >>> len(Handler()._initialize_platform_dependencies(True)) > 0
            True
        '''
        os_statvfs = None
        if((os.path.isfile(self._path) or os.path.isdir(self._path)) and
           builtins.hasattr(os, 'statvfs')):
            os_statvfs = os.statvfs(self._path)
            self.__class__.BLOCK_SIZE_IN_BYTE = os_statvfs.f_bsize
            self.__class__.MAX_FILE_NAME_LENGTH = os_statvfs.f_namemax
            operating_system = \
                boostNode.extension.system.Platform().operating_system
            if operating_system == 'macintosh' or force_macintosh_behavior:
                self.DECIMAL = True
        return os_statvfs

            # endregion

        # endregion

    # endregion

# endregion

# region footer

'''
    Extends this module with some magic environment variables to provide better
    introspection support. A generic command line interface for some code
    preprocessing tools is provided by default.
'''
boostNode.extension.dependent.Resolve(
    name=__name__, frame=inspect.currentframe(), default_caller=False)

# endregion
