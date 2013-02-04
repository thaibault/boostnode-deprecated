#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-

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
__credits__ = ('Torben Sickert',)
__license__ = 'see boostNode/__init__.py'
__maintainer__ = 'Torben Sickert'
__maintainer_email__ = 't.sickert@gmail.com'
__status__ = 'stable'
__version__ = '1.0'

## python2.7 pass
import builtins
import ctypes
## python2.7 import codecs
pass
import copy
import inspect
import mimetypes
import os
import re
import shutil
import sre_constants
import string
import sys
## python2.7 pass
import types

## python2.7 builtins = sys.modules['__main__'].__builtins__
pass

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
    '''Defines the maximum number of signs in a file path.'''
    MAX_PATH_LENGTH = 32767
    '''Defines the maximum number of digits for the biggest file-size.'''
    MAX_SIZE_NUMBER_LENGTH = 24  # 10^21 byte = 1 Yottabyte (-1 byte)
    '''Defines char set for handling text-based files internally.'''
    DEFAULT_ENCODING = 'utf-8'
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
        "#!/bin/bash\n\n# $label portable link file\n\nsize=$size\ntarget='"
        "$path'\n\n$executable_path --open \$target")
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

        # region public properties

    '''
        Defines a virtual root path for all methods. Through these class
        objects aren't locations except in "root_path" available.
    '''
    root_path = '/'

        # endregion

        # region protected properties

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
##         self, location=None, make_directory=False, right=770,
##         must_exist=True, encoding='utf-8', respect_root_path=True,
##         has_extension=True
##     ):
    def __init__(
        self: boostNode.extension.type.Self, location=None,
        make_directory=False, right=770, must_exist=True,
        encoding='utf-8', respect_root_path=True, has_extension=True
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

            >>> root_location = Handler(
            ...     __test_folder__ + 'init_root_directory',
            ...     make_directory=True)
            >>> Handler.root_path = root_location.path

            >>> location = Handler('/init_A', must_exist=False)
            >>> location.path # doctest: +ELLIPSIS
            '...init_A...'
            >>> location._path # doctest: +ELLIPSIS
            '...init_root_directory...init_A...'

            >>> location = Handler(
            ...     __test_folder__ + 'init_A', must_exist=False,
            ...     respect_root_path=False)
            >>> location.path # doctest: +ELLIPSIS
            '...init_A...'
            >>> location._path # doctest: +ELLIPSIS
            '...init_A...'

            >>> Handler(
            ...     __test_folder__ + 'init_A', respect_root_path=False
            ... ) # doctest: +ELLIPSIS +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            FileError: Invalid path "...init_A" for an obj...

            >>> try:
            ...     Handler(
            ...         __test_folder__ + 'init_A', make_directory=True)
            ... except builtins.Exception as exception:
            ...     str(exception) # doctest: +ELLIPSIS
            "...Errno..."

            >>> Handler.root_path = '/'
        '''
        self.__class__.root_path = os.path.normpath(
            self.__class__.root_path)
        self._encoding = encoding
        self._respect_root_path = respect_root_path
        self._initialize_root_path()
        self._initialized_path = self._initialize_location(location)
        self._initialize_path()
        self._prepend_root_path()
        if make_directory and not self:
            self.make_directory(right)
        if not self._set_path(path=self._path) and must_exist:
            raise __exception__(
                'Invalid path "{path}" for an object of "{class_name}". Given '
                'path was "{given_path}".'.format(
                    path=self.path, class_name=self.__class__.__name__,
                    given_path=location))
        if not '.' in self.name[1:] or self.is_directory():
            self._has_extension = False
        else:
            self._has_extension = has_extension
        self._initialize_platform_dependencies()

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
            ...     location=__test_folder__ + 'nonzero_not_existsing_file',
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

            >>> dir = Handler(
            ...     __test_folder__ + 'delitem_test', make_directory=True)
            >>> a = Handler(
            ...     __test_folder__ + 'delitem_test/a', must_exist=False)
            >>> a.content = ' '
            >>> a.is_file()
            True
            >>> del dir[0]
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
        '''
        if builtins.isinstance(item, self.__class__):
            return item in self.list()
        elif builtins.isinstance(item, builtins.str):
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

            >>> Handler.convert_size_format(size=1024, format='kb',
            ...                             decimal=True)
            1.024

            >>> Handler.convert_size_format(size=2 * 1024 ** 2, format='MB',
            ...                             decimal=False)
            2.0

            >>> Handler.convert_size_format(size=0)
            0.0
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
        '''
        if decimal is None:
            decimal = cls.DECIMAL
        match = re.compile(cls.REGEX_FORMAT.format(
            units=cls.determine_regex_units(formats=cls.FORMATS))).match(
                size_and_unit.lower())
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
        formats: builtins.dict, given_format='byte', decimal=False
    ) -> builtins.float:
##
        '''
            Converts a given size format to byte format.

            Examples:

            >>> Handler.determine_byte_from_other(
            ...     size=10.0, formats=Handler.FORMATS, given_format='MB')
            10485760.0
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
        '''
        if not operating_system:
            operating_system = boostNode.extension.system.Platform()\
                .operating_system
        if operating_system != 'windows':
            return ('~',)
        return ()

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
            "utf-8" is default.

            Examples:

            >>> Handler().encoding
            'utf-8'

            >>> Handler().get_encoding()
            'utf-8'

            >>> handler = Handler(__test_folder__ + 'test', must_exist=False)
            >>> handler.set_content(
            ...     'test', encoding='US-ASCII'
            ... ) # doctest: +ELLIPSIS
            Object of "Handler" ...
            >>> handler.encoding
            'US-ASCII'
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
        with builtins.open(self._path, 'r') as file:
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
            reached or doesn't if limit is 0.

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
        '''
        size = 0
        if os.path.ismount(self._path):
            size = self.disk_used_space
        elif self.is_directory(allow_link=follow_link):
            size = self.BLOCK_SIZE_IN_BYTE
            for file in self:
                if not limit or self._size < limit:
                    recursive_keywords = copy.deepcopy(keywords)
                    recursive_keywords['format'] = 'byte'
                    '''
                        Take this method type by another instance of
                        this class via introspection.
                    '''
                    size += builtins.getattr(
                        file, inspect.stack()[0][3])(
                            limit, follow_link=False, *arguments,
                            **recursive_keywords
                        ) + self.BLOCK_SIZE_IN_BYTE
        elif self.is_file():
            size = os.path.getsize(self._path)
        elif self.is_link:
            size = self.BLOCK_SIZE_IN_BYTE
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

            >>> test_type.make_symbolic_link(__test_folder__ + 'get_type_link')
            True
            >>> Handler(__test_folder__ + 'get_type_link').type
            'symbolicLink'
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
            ...     location=__file_path__).get_mimetype() # doctest: +ELLIPSIS
            'text/...python'

            >>> Handler().mimetype
            ''
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
##     def get_path(self, location=None):
    def get_path(
        self: boostNode.extension.type.Self, location=None
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
        if location is None:
            if self._path[-1] != os.sep and self.is_directory():
                self._path += os.sep
            if self._respect_root_path:
                return self._path[builtins.len(self.__class__.root_path) - 1:]
            return self._path
        if not builtins.isinstance(location, self.__class__):
            location = self.__class__(
                location, respect_root_path=self._respect_root_path,
                must_exist=False)
        return location.path

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
            ...     location='../../').relative_path == '..' + os.sep + '..'
            True
        '''
        if context is None:
            return os.path.relpath(self._path, *arguments, **keywords)
        return os.path.relpath(
            self._path, *arguments, start=self.__class__(
                location=context, must_exist=False)._path,
            **keywords)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def get_directory_path(self):
    def get_directory_path(
        self: boostNode.extension.type.Self
    ) -> builtins.str:
##
        '''
            Determines the current path of the Directory object without file.

            Examples:

            >>> Handler(
            ...     location=__file_path__
            ... ).directory_path # doctest: +ELLIPSIS
            '...boostNode...extension'

            >>> Handler(
            ...     location=__file_path__
            ... ).get_directory_path() # doctest: +ELLIPSIS
            '...boostNode...extension'

            >>> same = True
            >>> for handler in Handler():
            ...     if handler.directory_path != Handler()[0].directory_path:
            ...         same = False
            ...         break
            >>> same
            True
        '''
        subtrahend = 1
        if self.is_directory():
            subtrahend = 2
        self._directory_path = self._path[:-builtins.len(
            self.name) - subtrahend]
        return self.path[:-builtins.len(self.name) - subtrahend]

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def get_name(self, *arguments, **keywords):
    def get_name(
        self: boostNode.extension.type.Self, *arguments: builtins.object,
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
        '''
        path = self._path[:-1] if self._path[-1] == os.sep else self._path
        if(boostNode.extension.system.Platform().operating_system ==
           'windows' and re.compile('^[A-Z]:$').match(path)):
            return path
        return os.path.basename(path, *arguments, **keywords)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def get_basename(self, *arguments, **keywords):
    def get_basename(
        self: boostNode.extension.type.Self, *arguments: builtins.object,
        **keywords: builtins.object
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
        path = self._path[:-1] if self._path[-1] == os.sep else self._path
        if self._has_extension:
            return os.path.splitext(
                os.path.basename(path, *arguments, **keywords))[0]
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
##     def get_content(self, mode='r', *arguments, **keywords):
    def get_content(
        self: boostNode.extension.type.Self, mode='r',
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
            ...     mode='r', encoding='utf-8') # doctest: +ELLIPSIS
            '#!/...python...'

            >>> handler._encoding
            'utf-8'

            >>> Handler(location=__file_path__, encoding='utf-8').get_content(
            ...     mode='r'
            ... ) # doctest: +ELLIPSIS
            '#!/...python...'

            >>> Handler(
            ...     location=__test_folder__ + 'get_content_not_existing',
            ...     must_exist=False
            ... ).content
            ''

            >>> Handler().content # doctest: +ELLIPSIS
            <generator object list at 0x...>

            >>> Handler().get_content(mode='b') # doctest: +ELLIPSIS
            <generator object list at 0x...>

            >>> test = Handler(
            ...     __test_folder__ + 'get_content_binary',
            ...     must_exist=False)
            >>> test.content = ' '
            >>> test.get_content(mode='U')
            ' '
        '''
        if self:
            if self.is_file():
                if 'b' in mode:
                    with builtins.open(
                        self._path, mode, *arguments, **keywords
                    ) as file:
                        self._content = file.read()
                else:
                    if not 'encoding' in keywords:
                        keywords['encoding'] = self._encoding
                    else:
                        self._encoding = keywords['encoding']
## python2.7
##                     with codecs.open(
##                         self._path, mode, *arguments, **keywords
##                     ) as file:
##                         try:
##                             '''
##                                 NOTE: Double call of "read()" is a
##                                 workaround
##                                 for python bug when finishing reading file
##                                 without end reached.
##                             '''
##                             self._content = builtins.str(
##                                 (file.read() + file.read()).encode(
##                                     self.DEFAULT_ENCODING))
##                         except builtins.UnicodeDecodeError as exception:
##                             __logger__.warning(
##                                 'File "%s" couldn\'t be ridden. %s: %s',
##                                 self.path, exception.__class__.__name__,
##                                 builtins.str(exception))
##                             return ''
                    with builtins.open(
                        self._path, mode, *arguments, **keywords
                    ) as file:
                        try:
                            '''
                                NOTE: Double call of "read()" is a
                                workaround for python bug when finishing
                                reading file without end reached.
                            '''
                            self._content = file.read() + file.read()
                        except builtins.UnicodeDecodeError:
                            __logger__.warning(
                                'File "%s" couldn\'t be ridden. %s: %s',
                                self.path, exception.__class__.__name__,
                                builtins.str(exception))
                            return ''
##
                return self._content
            elif self.is_directory():
                return self.list()
            else:
                raise __exception__(
                    'Could only get content of file or directory.')
        return ''

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def get_portable_link_pattern(self):
    def get_portable_link_pattern(
        self: boostNode.extension.type.Self
    ) -> builtins.str:
##
        '''
            Determines the portable link file content pattern. With the
            file-independent placeholder "executable_path" replaced.

            Examples:

            >>> Handler().portable_link_pattern # doctest: +ELLIPSIS
            "#!/bin/bash\\n\\n# ..."

            >>> handler = Handler(location=__file_path__)
            >>> handler.portable_link_pattern # doctest: +ELLIPSIS
            "#!/bin/bash\\n\\n# ..."

            >>> Handler(
            ...     location=__test_folder__ +
            ...         'get_portable_link_pattern_media.mp3',
            ...     must_exist=False
            ... ).portable_link_pattern # doctest: +ELLIPSIS
            '[playlist]\\n\\nFile1=...'
        '''
        pattern = self.PORTABLE_DEFAULT_LINK_PATTERN
        if self.is_media():
            pattern = self.PORTABLE_MEDIA_LINK_PATTERN
        self._portable_link_pattern = string.Template(
            pattern
        ).safe_substitute(
            executable_path=os.path.abspath(sys.argv[0]))
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
            "#!/bin/bash\\n\\n# (?P<label>.*?) portable link file\\n\\nsiz..."

            >>> Handler().get_portable_regex_link_pattern(
            ...     ) # doctest: +ELLIPSIS
            "#!/bin/bash\\n\\n# (?P<label>.*?) portable link file\\n\\nsiz..."
        '''
        self._portable_regex_link_pattern = re.compile(
            string.Template.delimiter + '{?' + string.Template.idpattern +
            '}?').sub(
                '(.*?)', string.Template(
                    boostNode.extension.native.String(
                        self.portable_link_pattern
                    ).validate_regex(eception=['$', '\\']).content
                ).safe_substitute(
                    size='(?P<size>[0-9]+)',
                    label='(?P<label>.*?)',
                    path='(?P<path>.*?)',
                    name='(?P<name>.*?)'))
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
            "#!/bin/bash\\n\\n# %s...

            >>> Handler().get_portable_link_content(
            ...     label='test-label (%s)') # doctest: +ELLIPSIS
            "#!/bin/bash\\n\\n# test-label (%s)..."
        '''
        self._portable_link_content = re.compile(r'\\(.)').sub(
            '\\1', string.Template(
                self.portable_link_pattern
            ).safe_substitute(
                label=label,
                size=builtins.int(self.size),
                path=self._determine_relative_path(
                    relative, target_path
                ).replace('%', '%%'),
                name=self.name.replace('%', '%%')))
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

            >>> test_file.encoding = 'utf-8'

            >>> test_file.set_encoding('utf-8') # doctest: +ELLIPSIS
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
        '''
        if self.is_element() and not self.is_file():
            raise __exception__(
                'Set content is only possible for files and not for "%s" '
                '(%s).', self.path, self.type)
        if mode is None:
            mode = 'w+b'
## python2.7
##             if builtins.isinstance(
##                 content, (builtins.str, builtins.unicode)
##             ):
            if builtins.isinstance(content, builtins.str):
##
                mode = 'w'
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
## python2.7             with codecs.open(
            with builtins.open(
                self._path, mode, *arguments, **keywords
            ) as file_handler:
                file_handler.write(content)
# TODO check if necessary for python2.7
#            '''
#                Python2.7 workaround for right charset by writing text-based
#                files.
#            '''
#            with codecs.open(
#                self._path, mode='r', encoding='utf-8', errors='strict'
#            ) as file:
#                content_utf_8 = file.read()
#            with codecs.open(
#                self._path, mode='w', encoding=self._encoding,
#                errors='strict'
#            ) as file:
#                file.write(content_utf_8)
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def set_directory_path(self, location, *arguments, **keywords):
    def set_directory_path(
        self: boostNode.extension.type.Self,
        location: (boostNode.extension.type.SelfClassObject,
                   builtins.str),
        *arguments: builtins.object, **keywords: builtins.object
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
            '...set_directory_path3'
            >>> new_location.is_directory()
            True
        '''
        return self.move(
            target=self.get_path(location) + os.sep + self.name, *arguments,
            **keywords)

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
            >>> handler.name = __test_folder__ + 'set_name_edited'
            >>> handler.is_directory()
            True
            >>> handler.name
            'set_name_edited'

            >>> handler.set_name(__test_folder__ + 'set_name_edited2')
            True
            >>> handler.is_directory()
            True
            >>> handler.name
            'set_name_edited2'

            >>> handler = Handler(
            ...     __test_folder__ + 'set_name.e', must_exist=False)
            >>> handler.content = 'A'
            >>> handler.name = __test_folder__ + 'set_name.ext'
            >>> handler.is_file()
            True
            >>> handler.name
            'set_name.ext'
            >>> handler.basename
            'set_name'
        '''
        return self.move(
            target=self.directory_path + os.sep + name, *arguments, **keywords)

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
            >>> handler.basename = __test_folder__ + 'set_basename_edited3'
            >>> handler.name
            'set_basename_edited3'

            >>> handler = Handler(
            ...     __test_folder__ + 'set_basename4', make_directory=True)
            >>> handler.set_basename(__test_folder__ + 'set_basename_edited4')
            True
            >>> handler.basename
            'set_basename_edited4'

            >>> handler = Handler(
            ...     __test_folder__ + 'set_basename5.e', must_exist=False)
            >>> handler.content = 'A'
            >>> handler.basename = __test_folder__ + 'set_basename_edited5'
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
        '''
        other_location = self.__class__(location=other_location)
        try:
            return os.path.samefile(self._path, other_location._path)
        except builtins.AttributeError:
            return self == other_location

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

            >>> Handler(location=__file_path__).make_symbolic_link(
            ...     target=__test_folder__ + 'is_link.py', force=True)
            True
            >>> handler = Handler(location=__test_folder__ + 'is_link.py')

            >>> handler.is_symbolic_link()
            True

            >>> file = Handler(
            ...     __test_folder__ + 'is_link_not', must_exist=False)
            >>> file.content = ' '
            >>> file.is_symbolic_link()
            False

            >>> file = Handler(
            ...     __test_folder__ + 'is_link_not2', make_directory=True)
            >>> file.is_symbolic_link()
            False

            >>> target_handler = Handler(
            ...     location=__test_folder__ + 'is_link_not3',
            ...     must_exist=False)
            >>> Handler(location=__file_path__).make_portable_link(
            ...     target=target_handler, force=True)
            True

            >>> target_handler.is_symbolic_link(allow_portable_link=False)
            False

            >>> handler.is_symbolic_link()
            True
        '''
        path = self._path[:-1] if self._path[-1] == os.sep else self._path
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

            >>> link_target = Handler(
            ...     __test_folder__ + 'is_portable_link', must_exist=False)
            >>> Handler(location=__file_path__).make_symbolic_link(link_target)
            True
            >>> link_target.is_portable_link()
            False

            >>> Handler().is_portable_link()
            False

            >>> Handler(
            ...     __test_folder__ + 'is_portable_link_not_existing',
            ...     must_exist=False
            ... ).is_portable_link()
            False

            >>> handler = Handler(location=__file_path__).make_portable_link(
            ...     target=__test_folder__ + 'is_portable_link.py', force=True)
            >>> Handler(
            ...     __test_folder__ + 'is_portable_link.py').is_portable_link()
            True
        '''
        if os.path.isfile(self._path):
            maximum_length = (
                builtins.len(self.portable_link_pattern) +
                self.MAX_PATH_LENGTH + self.MAX_SIZE_NUMBER_LENGTH +
                # Maximum label line length + Maximum name length.
                120 + self.MAX_FILE_NAME_LENGTH)
            try:
                with builtins.open(self._path, 'r') as file:
                    file_content = file.read(maximum_length + 1).strip()
            except(builtins.IOError, builtins.TypeError,
                   builtins.UnicodeDecodeError):
                pass
            else:
                try:
                    return builtins.len(file_content) <= maximum_length and\
                        builtins.bool(re.compile(
                            self.portable_regex_link_pattern
                        ).match(file_content))
                except sre_constants.error:
                    pass
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
            ...     __test_folder__ + 'is_element_not_existsing',
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
        '''
        from boostNode.runnable.template import Parser as TemplateParser

        backup = self
        while True:
            other_backup = backup
            backup = self.__class__(
                location=self.directory_path + '/' + TemplateParser(
                    template=name_wrapper, string=True).render(
                        file=backup
                    ).output,
                must_exist=False)
            if not backup:
## python2.7
##                 if(not (other_backup == self) and not backup_if_exists and
##                    (not compare_content or self.is_equivalent(
##                        other=other_backup))):
                if(other_backup != self and not backup_if_exists and
                   (not compare_content or self.is_equivalent(
                       other=other_backup))):
##
                    return self
                self.copy(target=backup)
                return self
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

            >>> Handler(__test_folder__).is_equivalent(__test_folder__)
            True

            >>> Handler(__test_folder__).is_equivalent(Handler(
            ... __test_folder__))
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
            >>> test_folder.path[0:-1] == os.getcwd()
            True
            >>> test_folder.directory_path != os.getcwd()
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
            >>> undefined_object.directory_path == os.getcwd()
            True
            >>> undefined_object.path != os.getcwd()
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
            >>> file.directory_path == os.getcwd()
            True
            >>> file.path != os.getcwd()
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
            ...     'temp_not_existing', must_exist=False)
            >>> not_existing_file.list() # doctest: +ELLIPSIS
            <generator object list at ...>
            >>> len(not_existing_file)
            0
            >>> list(not_existing_file.list())
            []
        '''
        if self:
            if(self._path == '\\' and
               boostNode.extension.system.Platform().operating_system ==
               'windows'):
                for letter_number in builtins.range(
                        builtins.ord('A'), builtins.ord('Z') + 1):
                    path = builtins.chr(letter_number) + ':\\\\'
                    if os.path.exists(path):
                        yield self.__class__(location=path)
            else:
                try:
                    for file in os.listdir(self._path, *arguments, **keywords):
                        try:
                            yield self.__class__(
                                location=self.path + file, must_exist=False,
                                encoding=self._encoding,
                                respect_root_path=self._respect_root_path)
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

            >>> Handler(location=__test_folder__ + 'remove_directory',
            ...         make_directory=True) # doctest: +ELLIPSIS
            Object of "Handler" with path "...remove_directory..." (dir...
            >>> Handler(
            ...     location=__test_folder__ + 'remove_directory'
            ... ).remove_directory()
            True

            >>> Handler(
            ...     __test_folder__ + 'remove_directory_not_existing',
            ...     must_exist=False
            ... ).remove_directory()
            True

            >>> file = Handler(__test_folder__ + 'file', must_exist=False)
            >>> file.content = ' '
            >>> file.remove_directory() # doctest: +ELLIPSIS
            False
        '''
        if self:
            try:
                os.rmdir(self._path, *arguments, **keywords)
            except:
                return False
        return True

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def move(self, target, *arguments, **keywords):
    def move(
        self: boostNode.extension.type.Self,
        target: (boostNode.extension.type.SelfClassObject,
                 builtins.str), *arguments: builtins.object,
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
            >>> target.remove_deep()
            True
            >>> handler.move(target)
            True
            >>> target.is_directory()
            True

            >>> handler = Handler(
            ...     location=__test_folder__ + 'move_file', must_exist=False)
            >>> handler.content = ' '
            >>> target = Handler(
            ...     location=__test_folder__ + 'move_file2', must_exist=False)
            >>> target.remove_file()
            True
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
        target = self.get_path(location=target)
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
            >>> root # doctest: +ELLIPSIS
            Object of "Handler" with path "...remove_deep..." (directory).
            >>> Handler(location=__test_folder__ + 'remove_deep/sub_dir',
            ...         make_directory=True) # doctest: +ELLIPSIS
            Object of "Handler" with path "...remove_deep...sub_dir..."...
            >>> root.remove_deep()
            True
            >>> root.is_directory()
            False

            >>> file = Handler(
            ...     location=__test_folder__ + 'remove_deep', must_exist=False)
            >>> file.remove_deep()
            True

            >>> file = Handler(
            ...     location=__test_folder__ + 'remove_deep', must_exist=False)
            >>> file.content = ' '
            >>> file.remove_deep()
            True
        '''
        if self.is_directory(allow_link=False):
            shutil.rmtree(self._path, *arguments, **keywords)
        else:
            self.remove_file()
        return not self.is_element()

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

            Returns "True" if file isn't there anymore and "False" otherwise.

            Examples:

            >>> Handler(location=__file_path__).copy(
            ...     target=__test_folder__ + 'remove_file.py')
            True

            >>> handler = Handler(location=__test_folder__ + 'remove_file.py')
            >>> handler.is_file()
            True

            >>> handler.remove_file()
            True
            >>> handler.is_file()
            False
        '''
        if self:
            operating_system =\
                boostNode.extension.system.Platform().operating_system
            if(self.is_symbolic_link(allow_portable_link=False) and
               self.is_directory() and operating_system == 'windows'):
                return self.remove_directory()
            path = self._path
            if self._path.endswith('/'):
                path = self._path[:-1]
            try:
                os.remove(path, *arguments, **keywords)
            except:
                return False
        return not self.is_file()

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def change_right(self, right=770):
    def change_right(
        self: boostNode.extension.type.Self, right=770
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

            >>> Handler(location=__file_path__).copy(
            ...     target=__test_folder__ + 'change_right.py')
            True
            >>> Handler(
            ...     location=__test_folder__ + 'change_right.py').change_right(
            ...         right=766) # doctest: +ELLIPSIS
            Object of "Handler" with path "...change_right.py...

            >>> Handler(
            ...     __test_folder__ + 'change_right_folder',
            ...     make_directory=True
            ... ).copy(target=__test_folder__ + 'change_right_folder_2')
            True
            >>> Handler(
            ...     location=__test_folder__ + 'change_right_folder_2'
            ... ).change_right(right=766) # doctest: +ELLIPSIS
            Object of "Handler" with path "...change_right_folder_2..." (di...
        '''
        os.chmod(self._path, builtins.eval('0o%d' % right))
        if self.is_directory():
            self.iterate_directory(
                function=self.change_right.__name__, right=right)
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def copy(self, target, right=770, *arguments, **keywords):
    def copy(
        self: boostNode.extension.type.Self,
        target: (boostNode.extension.type.SelfClassObject,
                 builtins.str),
        right=770, *arguments: builtins.object,
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
        '''
        target = self.__class__(location=target, must_exist=False)
        if self.is_file():
            shutil.copy2(self._path, target._path, *arguments, **keywords)
        else:
            shutil.copytree(self._path, target._path)
        target.change_right(right)
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
            Makes a new directory in each case. If current directory name
            already exists the given wrapper pattern is used as long resulting
            name is unique. The Filehandler which creates the folder will be
            given back.
        '''
        location = self.__class__(self, must_exist=False)
        while location:
            path = location.directory_path + '/' + wrapper_pattern.format(
                file_name=location.name)
            location = self.__class__(location=path, must_exist=False)
        location.make_directory()
        return location

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def make_directory(self, right=770, *arguments, **keywords):
    def make_directory(
        self: boostNode.extension.type.Self, right=770,
        *arguments: builtins.object, **keywords: builtins.object
    ) -> builtins.bool:
##
        '''
            Implements the pythons native "os.mkdir()" method in an object
            oriented way.

            Create a directory named path with numeric mode. The default
            mode is "770" (octal). If the directory already exists, "OSError"
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
        '''
        os.mkdir(self._path, right, *arguments, **keywords)
        self.change_right(right)
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
            ...     __test_folder__ + 'make_softlink', must_exist=False)
            >>> Handler(
            ...     location=__test_folder__ + 'make_softlink_test_directory',
            ...     make_directory=True
            ... ).make_symbolic_link(target, force=True)
            True
            >>> target.is_symbolic_link()
            True

            >>> target = Handler(
            ...     __test_folder__ + 'make_softlink2', must_exist=False)
            >>> source = Handler(
            ...     location=__test_folder__ + 'make_softlink_test_file',
            ...     must_exist=False)
            >>> source.content = ' '
            >>> source.make_symbolic_link(target, force=True)
            True
            >>> Handler(target).is_symbolic_link()
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
            ...     __test_folder__ + 'make_hardlink2', must_exist=False)
            >>> source = Handler(
            ...     location=__test_folder__ + 'make_hardlink_test_file',
            ...     must_exist=False)
            >>> source.content = ' '
            >>> source.make_hardlink(target, force=True)
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

            >>> Handler(location=__file_path__).make_symbolic_link(
            ...     target=__test_folder__ + 'read_link.py', force=True)
            True

            >>> Handler(
            ...     location=__test_folder__ + 'read_link.py'
            ... ).read_symbolic_link() # doctest: +ELLIPSIS
            '...file.py'

            >>> Handler(
            ...     location=__test_folder__ + 'read_link.py'
            ... ).read_symbolic_link(as_object=True) # doctest: +ELLIPSIS
            Object of "Handler" with path "...file.py" (file).
        '''
        path = self._path[:-1] if self._path[-1] == os.sep else self._path
        if self.is_symbolic_link(allow_portable_link=False):
            link = os.readlink(path, *arguments, **keywords)
        else:
            link = self.read_portable_link()
        if link[-1] != os.sep and os.path.isdir(link):
            link += '/'
        link = link[builtins.len(self.__class__.root_path) - 1:]
        if as_object:
            if not self.is_referenced_via_absolute_path(location=link):
                return self.__class__(
                    location=self.directory_path + os.sep + link,
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
        **keywords: builtins.object
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
            ...     location=__test_folder__ + 'deep_copy/sub_dir',
            ...     make_directory=True
            ... ) # doctest: +ELLIPSIS
            Object of "Handler" with path "...deep_copy...sub_di..." (d...
            >>> Handler(
            ...     location=__test_folder__ + 'deep_copy/second_sub_dir',
            ...     make_directory=True
            ... ) # doctest: +ELLIPSIS
            Object of "Handler" with path "...deep_copy...second_sub_di...

            >>> dir = Handler(
            ...     location=__test_folder__ + 'deep_copy_dir',
            ...     must_exist=False)
            >>> dir.remove_deep()
            True
            >>> handler.deep_copy(target=dir) # doctest: +ELLIPSIS
            Object of "Handler" with path "...deep_copy..." (directory).
            >>> Handler(location=dir.path + 'sub_dir').is_directory()
            True
            >>> Handler(
            ...     location=dir.path + '/second_sub_dir'
            ... ).is_directory()
            True
        '''
        shutil.copytree(
            src=self._path, dst=self.get_path(location=target),
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
            "#!/bin/bash\\n\\n# Handler portable link file\\n\\nsize...\\n..."

            >>> target = Handler(
            ...     location=__test_folder__ + 'directory_link',
            ...     must_exist=False)
            >>> Handler(
            ...     __test_folder__ + 'directory', make_directory=True
            ... ).make_portable_link(target, force=True)
            True
            >>> target.content # doctest: +ELLIPSIS
            "#!/bin/bash\\n\\n# Handler portable link file\\n\\nsize...\\n..."
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
        '''
        return self.iterate_directory(function=self.remove_deep.__name__)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def iterate_directory(
##         self, function, recursive=False, recursive_in_link=True,
##         *arguments, **keywords
##     ):
    def iterate_directory(
        self: boostNode.extension.type.Self,
        function: (builtins.str, types.FunctionType,
                   types.MethodType),
        recursive=False, recursive_in_link=True,
        *arguments: builtins.object, **keywords: builtins.object
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
            current dimension will be stoped. If function's return value is
            "None", current file object is a directory and recursion is
            enabled the iteration will not enter current directory.

            Examples:

            >>> Handler().iterate_directory(function=lambda file: file)
            True

            >>> Handler().iterate_directory(function=lambda file: False)
            False

            >>> elements = list()
            >>> Handler().iterate_directory(
            ...     function=lambda file: elements.append(file.name))
            True
            >>> elements # doctest: +ELLIPSIS
            [...'file.py'...]
        '''
        for file in self:
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
                    function, recursive, *arguments, **keywords)
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
            if file.is_directory():
                '''
                    Take this method type by another instance of
                    this class via introspection.
                '''
                builtins.getattr(file, inspect.stack()[0][3])(*patterns)
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
            self._path).validate_shell()
        if builtins.hasattr(os, 'open'):
            return boostNode.extension.system.Platform.run(
                command='open', command_arguments=(shell_file,))
        return boostNode.extension.system.Platform.run(
            command='xdg-open', command_arguments=(shell_file,))

        # endregion

        # region protected methods

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
    ):
##
        '''
            Makes hard or softlinks and handles the optional force option.
        '''
## python2.7
##         force = False
##         if 'force' in keywords:
##             force = keywords['force']
##             del keywords['force']
##         relative = None
##         if 'relative' in keywords:
##             relative = keywords['relative']
##             del keywords['relative']
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
##     def _is_equivalent_folder(self, other):
    def _is_equivalent_folder(
        self: boostNode.extension.type.Self,
        other: boostNode.extension.type.SelfClassObject
    ) -> builtins.bool:
##
        '''
            Returns "True" if given folder contains likewise content.
            Serves as helper method.
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
        return True

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def _prepend_root_path(self):
    def _prepend_root_path(
        self: boostNode.extension.type.Self
    ) -> builtins.str:
##
        '''
            Preprends root path prefix to current file path.

            Examples:

            >>> root_path_save = Handler.root_path

            >>> Handler.root_path = '/tmp/sandbox/'
            >>> handler = Handler('/test', must_exist=False)
            >>> handler._path # doctest: +ELLIPSIS
            '...tmp...sandbox...test'
            >>> handler.path # doctest: +ELLIPSIS
            '...test'

            >>> handler = Handler('/tmp/sandbox/test', must_exist=False)
            >>> handler._path # doctest: +ELLIPSIS
            '...tmp...sandbox...tmp...sandbox...test'
            >>> handler.path # doctest: +ELLIPSIS
            '...tmp...sandbox...test'

            >>> Handler(
            ...     '/tmp/sandbox/test', must_exist=False,
            ...     respect_root_path=False
            ... )._path # doctest: +ELLIPSIS
            '...tmp...sandbox...test'

            >>> Handler(
            ...     '/test/', must_exist=False, respect_root_path=False
            ... )._path # doctest: +ELLIPSIS
            '...test'

            >>> Handler.root_path = '/tmp/sandbox/'
            >>> handler = Handler('test', must_exist=False)
            >>> handler._path # doctest: +ELLIPSIS
            '...tmp...sandbox...test'
            >>> handler.path # doctest: +ELLIPSIS
            '...test'

            >>> Handler.root_path = root_path_save
        '''
        '''Determine if given location has root path inside.'''
        root_exists = self._initialized_path.startswith(
            self.__class__.root_path[:-1])
        '''
            Prepend root path to given path location, if it wasn't given as
            root path.
        '''
        operating_system =\
            boostNode.extension.system.Platform().operating_system
        if(self._respect_root_path and (root_exists or
           not self._path.startswith(self.__class__.root_path)) and
           not ('windows' == operating_system and
                re.compile('[a-zA-Z]:\\.*').match(self._path) and
                self.__class__.root_path == os.sep)):
            if self._path.startswith(os.sep):
                self._path = self.__class__.root_path[:-1] + self._path
            else:
                self._path = self.__class__.root_path + self._path
        return self._path

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
##     def _initialize_root_path(self):
    def _initialize_root_path(
        self: boostNode.extension.type.Self
    ) -> boostNode.extension.type.Self:
##
        '''
            Normalizes root path.

            Examples:

            >>> root_path_save = Handler.root_path

            >>> Handler().root_path # doctest: +ELLIPSIS
            '...'

            >>> Handler.root_path = '~'
            >>> Handler(must_exist=False).root_path # doctest: +ELLIPSIS
            '...'

            >>> Handler.root_path = 'test'
            >>> Handler(must_exist=False).root_path # doctest: +ELLIPSIS
            '...test...'

            >>> Handler.root_path = root_path_save
        '''
        if(not self.is_referenced_via_absolute_path(
           location=self.__class__.root_path)):
            self.__class__.root_path = os.path.abspath(os.path.expanduser(
                self.__class__.root_path))
        if self.__class__.root_path[-1] != os.sep:
            self.__class__.root_path += os.sep
        return self

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
        '''
        if self == target:
            raise __exception__('It isn\'t possible to link to itself.')
        if target:
            target.remove_deep()
        if not self:
            '''
                Create a necessary dummy path to create symbolic links pointing
                to nothing.
            '''
            path = ''
            for path_part in self._path[1:].split(os.sep):
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

            >>> Handler()._make_platform_dependent_link(
            ...     symbolic=True,
            ...     target=Handler(
            ...         __test_folder__ +
            ...         '_make_platform_dependent_link',
            ...         must_exist=False),
            ...     relative=False
            ... ) # doctest: +ELLIPSIS
            True
        '''
        target_path = target._path
        if target._path[-1] == os.sep:
            target_path = target._path[:-1]
        source_path = self._determine_relative_path(relative, target_path)
        if source_path.endswith(os.sep):
            source_path = source_path[:-1]
        operating_system =\
            boostNode.extension.system.Platform().operating_system
        if symbolic:
            try:
                if operating_system == 'windows':
## python2.7
##                     create_symbolic_link =\
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
           builtins.isinstance(path, builtins.unicode)):
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
            ...     'temp_not_existsing', must_exist=False
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
##     def _initialize_platform_dependencies(self):
    def _initialize_platform_dependencies(
        self: boostNode.extension.type.Self
    ):
##
        '''
            Handles platform specified stuff like determining inode size.

            Examples:

            >>> Handler()._initialize_platform_dependencies(
            ... ) # doctest: +ELLIPSIS +SKIP
            posix.statvfs_result(f_bsize=..., f_frsize=..., f_blocks=..., ...)
        '''
        os_statvfs = None
        if((os.path.isfile(self._path) or os.path.isdir(self._path)) and
           builtins.hasattr(os, 'statvfs')):
            os_statvfs = os.statvfs(self._path)
            self.__class__.BLOCK_SIZE_IN_BYTE = os_statvfs.f_bsize
            self.__class__.MAX_FILE_NAME_LENGTH = os_statvfs.f_namemax
            operating_system =\
                boostNode.extension.system.Platform().operating_system
            if operating_system == 'macintosh':
                self.DECIMAL = True
        return os_statvfs

            # endregion

        # endregion

    # endregion

# endregion

# region footer

boostNode.extension.dependent.Resolve(
    name=__name__, frame=inspect.currentframe(), default_caller=False)

# endregion
