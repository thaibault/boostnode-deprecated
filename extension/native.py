#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# region vim modline

# vim: set tabstop=4 shiftwidth=4 expandtab:
# vim: foldmethod=marker foldmarker=region,endregion:

# endregion

# region header

'''
    Extension is a high level interface for interaction with pythons native \
    builtins. This class provides a full object oriented way to handle string \
    objects. Besides a number of new supported interactions with strings it \
    offers all core file system methods by the pythons native "builtins.str" \
    object.
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
import __builtin__ as builtins
##
import collections
import copy
import encodings
import functools
import inspect
import os
import re
import sys
## python3.3 import types
pass

'''Make boostNode packages and modules importable via relative paths.'''
for number in (3, 4):
    sys.path.append(os.path.abspath(sys.path[0] + number * ('..' + os.sep)))

import boostNode
## python3.3
## from boostNode.extension.type import Self, SelfClass, SelfClassObject
pass
##
from boostNode.paradigm.aspectOrientation import FunctionDecorator, JointPoint
from boostNode.paradigm.objectOrientation import Class

# endregion


# region classes

class PropertyInitializer(FunctionDecorator):
    '''
        Decorator class for automatically setting instance properties for \
        corresponding arguments of wrapped function.
    '''

    # region properties

    EXCLUDED_ARGUMENT_NAMES = 'self',
    '''
        Defines all argument names which will be ignored by generating \
        instance properties.
    '''

    # endregion

    # region dynamic methods

        # region public

    @JointPoint
## python3.3
##     def get_wrapper_function(
##         self: Self
##     ) -> (types.FunctionType, types.MethodType):
    def get_wrapper_function(self):
##
        '''
            This methods returns the wrapped function.

            Examples:

            >>> class A:
            ...     def a(self): pass
            ...     def __init__(self): pass
            ...     __init__.__func__ = a
            ...     __init__ = PropertyInitializer(__init__)

            >>> A() # doctest: +ELLIPSIS
            <__main__.A ... at ...>
        '''
        @functools.wraps(self.__func__)
        def wrapper_function(*arguments, **keywords):
            '''Wrapper function for initializing instance properties.'''
            '''Unpack wrapper methods.'''
            while builtins.hasattr(self.__func__, '__func__'):
                self.__func__ = self.__func__.__func__
            arguments = self._determine_arguments(arguments)
            for name, value in inspect.getcallargs(
                self.__func__, *arguments, **keywords
            ).items():
                if not name in self.EXCLUDED_ARGUMENT_NAMES:
                    self.object.__dict__[name] = value
            return self.__func__(*arguments, **keywords)
## python3.3         pass
        wrapper_function.__wrapped__ = self.__func__
        return wrapper_function

        # endregion

    # endregion


class Object(Class):
    '''This class extends all native python classes.'''

    # region dynamic methods

        # region public

            # region special

    @JointPoint(PropertyInitializer)
## python3.3
##     def __init__(
##         self: Self, content=None,
##         *arguments: (builtins.object, builtins.type),
##         **keywords: (builtins.object, builtins.type)
##     ) -> None:
    def __init__(self, content=None, *arguments, **keywords):
##
        '''
            Generates a new high level wrapper around given object.

            Examples:

            >>> object = Object('hans')

            >>> object
            Object of "str" ('hans').
            >>> object.content
            'hans'
        '''

                # region properties

        '''Saves a copy of currently saved object.'''
        self._content_copy = {}

                # endregion

    @JointPoint
## python3.3     def __repr__(self: Self) -> builtins.str:
    def __repr__(self):
        '''Invokes if this object should describe itself by a string.'''
        return 'Object of "{class_name}" ({content}).'.format(
            class_name=self.content.__class__.__name__,
            content=builtins.repr(self.content))

    @JointPoint
## python3.3     def __str__(self: Self) -> builtins.str:
    def __str__(self):
        '''
            Is triggered if this object should be converted to string.

            Examples:

            >>> str(Object(['hans']))
            "['hans']"
        '''
        return builtins.str(self.content)

            # endregion

    @JointPoint
## python3.3     def copy(self: Self) -> builtins.dict:
    def copy(self):
        '''
            Copies a given object's attributes and returns them.

            Examples:

            >>> class A: pass
            >>> a = A()
            >>> a.string = 'hans'
            >>> object_copy = Object(a).copy()
            >>> for key, value in object_copy.items():
            ...     if 'string' == key:
            ...         print(value)
            hans

            >>> class B: hans = 'A'
            >>> object = Object(B())
            >>> object_copy = object.copy()
            >>> object.content.hans = 'B'
            >>> object.content.hans
            'B'
            >>> object_copy['hans']
            'A'
        '''
        self._content_copy = {}
        for attribute_name in builtins.dir(self.content):
            attribute = builtins.getattr(self.content, attribute_name)
            if not ((attribute_name.startswith('__') and
                     attribute_name.endswith('__')) or
                    builtins.callable(attribute)):
                self._content_copy[attribute_name] = copy.copy(
                    builtins.getattr(self.content, attribute_name))
        return self._content_copy

    @JointPoint
## python3.3     def restore(self: Self) -> (builtins.object, builtins.type):
    def restore(self):
        '''
            Restores a given object's attributes by a given copy are last \
            copied item.

            Examples:

            >>> class A: pass
            >>> A.string = 'hans'
            >>> object = Object(A)
            >>> object.copy()
            {'string': 'hans'}
            >>> A.string = 'peter'
            >>> object.restore() # doctest: +ELLIPSIS
            <class ...A...>
            >>> A.string
            'hans'

            >>> class A:
            ...     hans = 'A'
            ...     __special__ = 'B'
            >>> object = Object(A())
            >>> object_copy = object.copy()
            >>> object.content.hans = 'B'
            >>> object.content.hans
            'B'
            >>> object.restore().hans
            'A'
        '''
        for attribute, value in self._content_copy.items():
            builtins.setattr(self.content, attribute, value)
        return self.content

    @JointPoint
## python3.3     def is_binary(self: Self) -> builtins.bool:
    def is_binary(self):
        '''
            Determines if given data is binary.

            Examples:

            >>> Object('A').is_binary()
            False

            >>> if sys.version_info.major < 3:
            ...     Object(chr(1)).is_binary()
            ... else:
            ...     Object(bytes('A', 'utf_8')).is_binary()
            True

            >>> if sys.version_info.major < 3:
            ...     Object(unicode('hans')).is_binary()
            ... else:
            ...     Object('hans').is_binary()
            False
        '''
        # NOTE: This is a dirty workaround to handle python2.7 lack of
        # differentiation between "string" and "bytes" objects.
## python3.3
##         return builtins.isinstance(self.content, builtins.bytes)
        content = self.content
        if builtins.isinstance(self.content, builtins.unicode):
            content = self.content.encode(encoding='utf_8')
        text_chars = ''.join(builtins.map(
            builtins.chr,
            builtins.range(7, 14) + [27] + builtins.range(0x20, 0x100)))
        return builtins.bool(content.translate(None, text_chars))
##

        # endregion

    # endregion

    # region static methods

        # region public

    @JointPoint(builtins.classmethod)
## python3.3
##     def determine_abstract_method_exception(
##         cls: SelfClass, abstract_class_name: builtins.str, class_name=None
##     ) -> builtins.NotImplementedError:
    def determine_abstract_method_exception(
        cls, abstract_class_name, class_name=None
    ):
##
        '''
            Generates a suitable exception for raising if a method is called \
            initially indented to be overwritten.

            Examples:

            >>> class A(Object):
            ...     @classmethod
            ...     def abstract_method(cls):
            ...         raise cls.determine_abstract_method_exception(
            ...             A.__name__)
            >>> class B(A): pass
            >>> B.abstract_method() # doctest: +ELLIPSIS
            Traceback (most recent call last):
            ...
            NotImplementedError: Method "abstract_method" wasn't implemented...

            >>> class A:
            ...     @classmethod
            ...     def abstract_method(cls):
            ...         raise Object.determine_abstract_method_exception(
            ...             A.__name__, cls.__name__)
            >>> class B(A): pass
            >>> B.abstract_method() # doctest: +ELLIPSIS
            Traceback (most recent call last):
            ...
            NotImplementedError: Method "..." wasn't implemented...
        '''
        '''
            NOTE: fetch third frame "inspect.stack()[2]" \
                0: this \
                1: Decorator wrapper \
                2: caller
        '''
        if class_name is None:
            class_name = cls.__name__
        stack_level = 1 if sys.flags.optimize else 2
        return builtins.NotImplementedError(
            'Method "{name}" wasn\'t implemented by "{class_name}" and is '
            'necessary for abstract class "{abstract_class}".'.format(
                name=inspect.stack()[stack_level][3], class_name=class_name,
                abstract_class=abstract_class_name))

        # endregion

    # endregion


class String(Object, builtins.str):
    '''
        The string class inherits besides the interface class all pythons \
        native string methods. NOTE: This class has to implement inherited \
        special methods like "__str__()" and "__len__()" because they have to \
        use the "content" property which could be manipulated by not \
        inherited methods.
    '''

    # region properties

    IMPORTANT_ENCODINGS = 'ascii', 'utf_8', 'latin_1', 'utf_16'
    '''
        Defines generally important encodings. Which should be tried at first.
    '''
    NON_STANDARD_SPECIAL_URL_SEQUENCES = {
        '%1000': '#', '%1001': '&', '%1002': '=', '%1003': '%', '%1004': '+'}
    '''All chars wich should be handle during dealing with web urls.'''
    SPECIAL_SHELL_SEQUENCES = (
        '"', "'", '`', '(', ')', ' ', '&', '$', '-')
    '''
        All chars which should be observed by handling with shell command. \
        Note that the escape sequence must not be defined.
    '''
    SPECIAL_REGEX_SEQUENCES = (
        '-', '[', ']', '(', ')', '^', '$', '*', '+', '.', '{', '}')
    '''
        All chars which should be observed by handling with regex sequences. \
        Note that the escape sequence must not be defined.
    '''
    SPECIAL_URL_SEQUENCES = {
        '+': ' ', '%20': ' ', '%22': '"', '%2F': '/', '%7E': '~',
        '%C3%A4': 'ä', '%C3%84': 'Ä',
        '%C3%B6': 'ö', '%C3%96': 'Ö',
        '%C3%BC': 'ü', '%C3%9C': 'Ü'}
    '''All chars wich should be observed by handling with url sequences.'''
    SPECIAL_HTML_SEQUENCES = {
        # Note only needed in very old browsers.
        #'&': '&amp;',
        #' ': '&nbsp;',
        # Note: is only shown if word is to long.
        #'"soft hyphen"': '&shy;',
        "'": '&apos;', '´': '&acute;', '¯': '&macr;',

        '<': '&lt;', '>': '&gt;',

        'º': '&ordm;', '¹': '&sup1;', '²': '&sup2;', '³': '&sup3;',

        '¼': '&frac14;', '½': '&frac12;', '¾': '&frac34;',

        'À': '&Agrave;', 'Á': '&Aacute;', 'Â': '&Acirc;', 'Ã': '&Atilde;',
        'Ä': '&Auml;', 'Å': '&Aring;', 'Æ': '&AElig;',

        'È': '&Egrave;', 'É': '&Eacute;', 'Ê': '&Ecirc;', 'Ë': '&Euml;',

        'Ì': '&Igrave;', 'Í': '&Iacute;', 'Î': '&Icirc;', 'Ï': '&Iuml;',

        'Ò': '&Ograve;', 'Ó': '&Oacute;', 'Ô': '&Ocirc;', 'Õ': '&Otilde;',
        'Ö': '&Ouml;', 'Ø': '&Oslash;',

        'Ù': '&Ugrave;', 'Ú': '&Uacute;', 'Û': '&Ucirc;', 'Ü': '&Uuml;',

        'à': '&agrave;', 'á': '&aacute;', 'â': '&acirc;', 'ã': '&atilde;',
        'ä': '&auml;', 'å': '&aring;', 'æ': '&aelig;',

        'è': '&egrave;', 'é': '&eacute;', 'ê': '&ecirc;', 'ë': '&euml;',

        'ì': '&igrave;', 'í': '&iacute;', 'î': '&icirc;', 'ï': '&iuml;',

        'ò': '&ograve;', 'ó': '&oacute;', 'ô': '&ocirc;', 'õ': '&otilde;',
        'ö': '&ouml;', 'ø': '&oslash;',

        'ù': '&ugrave;', 'ú': '&uacute;', 'û': '&ucirc;', 'ü': '&uuml;',

        'ý': '&yacute;', 'ÿ': '&yuml;',

        '¡': '&iexcl;',
        '¢': '&cent;',
        '£': '&pound;',
        '¤': '&curren;',
        '¥': '&yen;',
        '¦': '&brvbar;',
        '§': '&sect;',
        '¨': '&uml;',
        '©': '&copy;',
        'ª': '&ordf;',
        '«': '&laquo;',
        '¬': '&not;',
        '®': '&reg;',
        '°': '&deg;',
        '±': '&plusmn;',
        'µ': '&micro;',
        '¶': '&para;',
        '·': '&middot;',
        '¸': '&cedil;',
        '»': '&raquo;',
        '¿': '&iquest;',
        '×': '&times;',
        '÷': '&divide;',
        'Ç': '&Ccedil;',
        'Ð': '&ETH;',
        'Ñ': '&Ntilde;',
        'Ý': '&Yacute;',
        'Þ': '&THORN;',
        'ß': '&szlig;',
        'ç': '&ccedil;',
        'ð': '&eth;',
        'ñ': '&ntilde;',
        'þ': '&thorn;'}
    '''All chars wich should be observed by handling with html sequences.'''

    # endregion

    # region static methods

        # region public

    @JointPoint(builtins.classmethod)
    @Class.pseudo_property
## python3.3
##     def get_escaping_replace_dictionary(
##         cls: SelfClass, sequence: collections.Iterable,
##         escape_sequence='\{symbole}'
##     ) -> builtins.dict:
    def get_escaping_replace_dictionary(
        cls, sequence, escape_sequence='\{symbole}'
    ):
##
        '''
            Creates a replacement dictionary form a given iterable. Every \
            element will be associated with its escaped version. This method \
            is useful for using before give "self.replace()" a dictionary.

            "sequence"        - is an iterable with elements to be escaped.

            "escape_sequence" - is an escape sequence for each element from \
                                "sequence".

            Examples:

            >>> String.get_escaping_replace_dictionary(
            ...     ('"', 'a', 'b')
            ... ) == {'a': '\\\\a', '"': '\\\\"', 'b': '\\\\b'}
            True

            >>> String.get_escaping_replace_dictionary(
            ...     ('A', 'B', 'C'), escape_sequence='[{symbole}]'
            ... ) == {'A': '[A]', 'B': '[B]', 'C': '[C]'}
            True
        '''
        escaping_dictionary = {}
        for element in sequence:
            escaping_dictionary[element] = escape_sequence.format(
                symbole=element)
        return escaping_dictionary

        # endregion

    # endregion

    # region dynamic methods

        # region public

            # region special

    @JointPoint
## python3.3
##     def __init__(
##         self: Self, content=None, *arguments: builtins.object,
##         **keywords: builtins.object
##     ) -> None:
    def __init__(self, content=None, *arguments, **keywords):
##
        '''
            Initialize a new "String" object.

            Examples:

            >>> String('hans').content
            'hans'

            >>> String().content
            ''

            >>> String(['A', 5]).content
            "['A', 5]"
        '''

                # region properties

        '''Saves the current line for the "readline()" method.'''
        self._current_line_number = 0
        '''The main string property. It saves the current string.'''
        if content is None:
            content = ''
        if(not builtins.isinstance(content, (builtins.str, builtins.bytes)) or
           builtins.isinstance(content, String)):
            content = builtins.str(content)
        self.content = content

                # endregion

    @JointPoint
## python3.3     def __repr__(self: Self) -> builtins.str:
    def __repr__(self):
        '''
            Invokes if this object should describe itself by a string.

            Examples:

            >>> repr(String('hans'))
            'Object of "String" with "hans" saved.'
        '''
        return 'Object of "{class_name}" with "{content}" saved.'.format(
            class_name=self.__class__.__name__, content=self.content)

    @JointPoint
## python3.3     def __len__(self: Self) -> builtins.int:
    def __len__(self):
        '''
            Triggers if the pythons native "builtins.len()" function tries to \
            handle current instance. Returns the number of symbols given in \
            the current string representation of this object.

            Examples:

            >>> len(String())
            0

            >>> len(String('hans'))
            4
        '''
        return builtins.len(self.__str__())

    @JointPoint
## python3.3     def __str__(self: Self) -> builtins.str:
    def __str__(self):
        '''
            Triggers if the current object should be directly interpreted as \
            pythons native string implementation.

            Examples:

            >>> str(String('hans'))
            'hans'

            >>> str(String())
            ''
        '''
        return self.content

    @JointPoint
## python3.3     def __bool__(self: Self) -> builtins.bool:
    def __nonzero__(self):
        '''
            Triggers if the current object should be interpreted as a boolean \
            value directly.

            Examples:

            >>> not String()
            True

            >>> not String('hans')
            False

            >>> bool(String('hans'))
            True
        '''
        return builtins.bool(self.content)

            # endregion

            # region getter

    @JointPoint(Class.pseudo_property)
## python3.3     def get_encoding(self: Self) -> builtins.str:
    def get_encoding(self):
        '''
            Guesses the encoding used in current string (bytes). Encodings \
            are checked in alphabetic order.

            Examples:

            >>> String().encoding == String.IMPORTANT_ENCODINGS[0]
            True

            >>> String('hans').encoding == String.IMPORTANT_ENCODINGS[0]
            True

            >>> String('hans').encoding == String.IMPORTANT_ENCODINGS[0]
            True

            >>> String(b'hans').encoding == String.IMPORTANT_ENCODINGS[0]
            True

            >>> if sys.version_info.major < 3:
            ...     String(
            ...         u'ä'.encode('latin1')
            ...     ).encoding == String.IMPORTANT_ENCODINGS[0]
            ... else:
            ...     String(
            ...         'ä'.encode('latin1')
            ...     ).encoding  == String.IMPORTANT_ENCODINGS[0]
            False
        '''
        if self.content and builtins.isinstance(self.content, builtins.bytes):
            for encoding in builtins.list(
                self.IMPORTANT_ENCODINGS
            ) + builtins.sorted(builtins.filter(
                lambda encoding: encoding not in self.IMPORTANT_ENCODINGS,
                builtins.set(encodings.aliases.aliases.values())
            )):
                try:
                    self.content.decode(encoding)
                except builtins.UnicodeDecodeError:
                    pass
                else:
                    return encoding
        return self.IMPORTANT_ENCODINGS[0]

            # endregion

            # region validation

    @JointPoint
## python3.3     def validate_shell(self: Self) -> Self:
    def validate_shell(self):
        '''
            Validates the current string for using as a command in shell. \
            Special shell command chars will be escaped.

            Examples:

            >>> String(
            ...     'a new folder with special signs "&"'
            ... ).validate_shell() # doctest: +ELLIPSIS
            Object of "String" with "a\ new\ fol...ial\ signs\ \\"\&\\"" saved.

            >>> String(
            ...     ''
            ... ).validate_shell().content
            ''

            >>> if sys.version_info[0] > 3:
            ...     String(
            ...         """[\"'`´()&$ -]"""
            ...     ).validate_shell().content == ('[\\\\"\\\\\\'\\\\`\\\\´'
            ...         '\\\\(\\\\)\\\\&\\\\$\\\\ \\\\-]')
            ... else:
            ...     True
            True
        '''
        '''The escape sequence must be escaped at first.'''
        self.replace('\\', '\\\\')
        return self.replace(
            search=self.__class__.get_escaping_replace_dictionary(
                self.SPECIAL_SHELL_SEQUENCES))

    @JointPoint
## python3.3     def validate_html(self: Self) -> Self:
    def validate_html(self):
##
        '''
            Validates current string for using as snippet in a html document.

            Examples:

            >>> String('<html></html>').validate_html().content
            '&lt;html&gt;&lt;/html&gt;'
        '''
        return self.replace(self.SPECIAL_HTML_SEQUENCES)

    @JointPoint
## python3.3     def validate_regex(self: Self, exclude_symbols=()) -> Self:
    def validate_regex(self, exclude_symbols=()):
        '''
            Validates the current string for using in a regular expression \
            pattern. Special regular expression chars will be escaped.

            Examples:

            >>> String("that's no regex: .*$").validate_regex()
            Object of "String" with "that's no regex: \.\*\$" saved.

            >>> String().validate_regex(exclude_symbols=()).content
            ''

            >>> String('-\[]()^$*+.}-').validate_regex(('}',)).content
            '\\\\-\\\\\\\\\\\\[\\\\]\\\\(\\\\)\\\\^\\\\$\\\\*\\\\+\\\\.}\\\\-'

            >>> String('-\[]()^$*+.{}-').validate_regex(
            ...     ('[', ']', '(', ')', '^', '$', '*', '+', '.', '{')
            ... ).content
            '\\\\-\\\\\\\\[]()^$*+.{\\\\}\\\\-'

            >>> String('-').validate_regex(('\\\\',)).content
            '\\\\-'
        '''
        '''The escape sequence must also be escaped; but at first.'''
        if not '\\' in exclude_symbols:
            self.replace('\\', '\\\\')
        return self.replace(
            search=self.__class__.get_escaping_replace_dictionary(
                builtins.tuple(
                    builtins.set(self.SPECIAL_REGEX_SEQUENCES) -
                    builtins.set(exclude_symbols))))

    @JointPoint
## python3.3     def validate_format(self: Self) -> Self:
    def validate_format(self):
        '''
            Validates the current string for using in a string with \
            placeholder like "{name}". It will be escaped to not interpreted \
            as placeholder like "\{name\}".

            Examples:

            >>> String("that's no {placeholder}").validate_format()
            Object of "String" with "that's no \{placeholder\}" saved.

            >>> String().validate_format().content
            ''
        '''
        self.content = re.compile('{([a-z]+)}').sub(r'\\{\1\\}', self.content)
        return self

    @JointPoint
## python3.3     def validate_url(self: Self) -> Self:
    def validate_url(self):
        '''
            Validates a given url by escaping special chars.

            Examples:

            >>> String(
            ...     'here%20is%20no%20%22url%22%20present!+'
            ... ).validate_url()
            Object of "String" with "here is no "url" present! " saved.

            >>> String('').validate_url().content
            ''

            >>> if sys.version_info[0] > 3:
            ...     String(
            ...         '[+%20%22%2F%7E%C3%A4%C3%84%C3%B6]'
            ...     ).validate_url().content == '[  "/~äÄö]'
            ... else:
            ...     True
            True

            >>> if sys.version_info[0] > 3:
            ...     String('[%C3%96%C3%BC%C3%9C]').validate_url(
            ...         ).content == '[ÖüÜ]'
            ... else:
            ...     True
            True
        '''
        search = self.SPECIAL_URL_SEQUENCES
        search.update(self.NON_STANDARD_SPECIAL_URL_SEQUENCES)
        return self.replace(search)

            # endregion

    @JointPoint
## python3.3     def camel_case_capitalize(self: Self) -> Self:
    def camel_case_capitalize(self):
        '''
            Acts like pythons native "builtins.str.capitalize()" method but \
            preserves camel case characters.

            Examples:

            >>> String().camel_case_capitalize().content
            ''

            >>> String('haNs').camel_case_capitalize().content
            'HaNs'
        '''
        if self.content:
            self.content = self.content[0].upper() + self.content[1:]
        return self

    @JointPoint
## python3.3
##     def find_python_code_end_bracket(
##         self: Self
##     ) -> (builtins.int, builtins.bool):
    def find_python_code_end_bracket(self):
##
        '''
            Searches for the next not escaped closing end clamped in current \
            string interpreted as python code.

            Examples:

            >>> string = 'hans () peter)'
            >>> String(
            ...     'hans () peter)'
            ... ).find_python_code_end_bracket() == string.rfind(')')
            True

            >>> String().find_python_code_end_bracket()
            False
        '''
        brackets = skip = index = 0
        quote = False
        for char in self.content:
            result = self._handle_char_to_find_end_bracket(
                index, char, quote, skip, brackets)
            if builtins.isinstance(result, builtins.int):
                return result
            index, char, quote, skip, brackets = result
        return False

    @JointPoint
## python3.3
##     def replace(
##         self: Self, search: (builtins.str, builtins.dict),
##         replace='', *arguments: builtins.object, **keywords: builtins.object
##     ) -> Self:
    def replace(self, search, replace='', *arguments, **keywords):
##
        '''
            Implements the pythons native string method "str.replace()" in an \
            object orientated way. This method serves additionally \
            dictionaries as "search" parameter for multiple replacements. If \
            you use dictionaries, the second parameter "replace" becomes \
            useless.

            Return a copy of the string with all occurrences of substring old \
            replaced by new. If an optional argument count is given, only the \
            first count occurrences are replaced.

            Examples:

            >>> String('hans').replace('ans', 'ut')
            Object of "String" with "hut" saved.

            >>> String().replace('hans', 'peter')
            Object of "String" with "" saved.

            >>> String().replace('hans', 'peter').content
            ''

            >>> String('hans').replace('hans', 'peter').content
            'peter'
        '''
        if builtins.isinstance(search, builtins.dict):
            for search_string, replacement in search.items():
                self.content = self.content.replace(
                    builtins.str(search_string), builtins.str(replacement),
                    *arguments, **keywords)
        else:
            self.content = self.content.replace(
                search, replace, *arguments, **keywords)
        return self

    @JointPoint
## python3.3
##     def sub(
##         self: Self, search: (builtins.str, builtins.dict), replace='',
##         *arguments: builtins.object, **keywords: builtins.object
##     ) -> Self:
    def sub(self, search, replace='', *arguments, **keywords):
##
        '''
            Implements the pythons native "re.sub()" method in an object \
            oriented way. This method serves additionally dictionaries as \
            "search" parameter for multiple replacements. If you use \
            dictionaries, the second parameter "replace" becomes useless.

            Return the string obtained by replacing the leftmost \
            non-overlapping occurrences of pattern in string by the \
            replacement "replace". If the pattern isn’t found, string is \
            returned unchanged. "replace" can be a string or a function;

            If "replace" is a string, any backslash escapes in it are \
            processed. That means "\n" is converted to a single newline \
            character, "\r" is converted to a linefeed, and so forth. Unknown \
            escapes such as "\j" are left alone. Backreferences, such as \
            "\6", are replaced with the substring matched by group 6 in the \
            pattern.

            If "replace" is a function, it is called for every \
            non-overlapping occurrence of pattern. The function takes a \
            single match object argument, and returns the replacement string.

            The pattern may be a string or an RE object. The optional \
            argument count is the maximum number of pattern occurrences to be \
            replaced; count must be a non-negative integer. If omitted or \
            zero, all occurrences will be replaced. Empty matches for the \
            pattern are replaced only when not adjacent to a previous match, \
            so sub('x*', '-', 'abc') returns '-a-b-c-'.

            In addition to character escapes and back references as described \
            above, "\g<name>" will use the substring matched by the group \
            named name, as defined by the "(?P<name>...)" syntax. \
            "\g<number>" uses the corresponding group number; "\g<2>" is \
            therefore equivalent to "\2", but isn’t ambiguous in a \
            replacement such as "\g<2>0". "\20" would be interpreted as a \
            reference to group 20, not a reference to group 2 followed by the \
            literal character "0". The backreference "\g<0>" substitutes in \
            the entire substring matched by the RE.

            Examples:

            >>> String('hans').sub('([^a]+)', ' jau-suffix ')
            Object of "String" with " jau-suffix a jau-suffix " saved.

            >>> String('hans').sub('n', 'l')
            Object of "String" with "hals" saved.

            >>> String().sub('n', 'l').content
            ''

            >>> String('hans').sub('hans', 'peter').content
            'peter'

            >>> String('hans').sub({'hans': 'peter'}).content
            'peter'
        '''
        if builtins.isinstance(search, builtins.dict):
            for search_string, replacement in search.items():
                '''Take this method name via introspection.'''
                self.content = builtins.getattr(
                    re.compile(builtins.str(search_string)),
                    inspect.stack()[0][3]
                )(
                    builtins.str(replacement), self.content, *arguments,
                    **keywords)
        else:
            '''
                Take this method name from regular expression object via \
                introspection.
            '''
            self.content = builtins.getattr(
                re.compile(builtins.str(search)), inspect.stack()[0][3]
            )(builtins.str(replace), self.content, *arguments, **keywords)
        return self

    @JointPoint
## python3.3
##     def subn(
##         self: Self, search: (builtins.str, builtins.dict), replace='',
##         *arguments: builtins.object, **keywords: builtins.object
##     ) -> builtins.tuple:
    def subn(self, search, replace='', *arguments, **keywords):
##
        '''
            Implements the pythons native "re.subn()" method in an object \
            oriented way. This method serves additionally dictionaries as \
            "search" parameter for multiple replacements. If you use \
            dictionaries, the second parameter "replace" becomes useless.

            Perform the same operation as "self.sub()", but returns a tuple: \
            ("new_string", "number_of_subs_made"").

            Examples:

            >>> result = String().subn('a')
            >>> result[0].content
            ''
            >>> result[1]
            0

            >>> result = String('hans').subn({'a': 'b', 'n': 'c'})
            >>> result[0].content
            'hbcs'
            >>> result[1]
            2
        '''
        if builtins.isinstance(search, builtins.dict):
            number_of_replaces = 0
            for search_string, replacement in search.items():
                self.content, temp_number_of_replaces = builtins.getattr(
                    re.compile(builtins.str(search_string)),
                    inspect.stack()[0][3]
                )(
                    builtins.str(replacement), self.content, *arguments,
                    **keywords)
                number_of_replaces += temp_number_of_replaces
        else:
            self.content, number_of_replaces = builtins.getattr(
                re.compile(builtins.str(search)),
                inspect.stack()[0][3]
            )(builtins.str(replace), self.content, *arguments, **keywords)
        return self, number_of_replaces

    @JointPoint
## python3.3     def readline(self: Self) -> (SelfClassObject, builtins.bool):
    def readline(self):
        '''
            Implements the pythons native "bz2.BZ2File.readline()" method in \
            an object oriented way.

            Return the next line from the string, as a string object, \
            retaining newline.

            Returns "False" on EOF.

            Examples:

            >>> string = String('hans\\npeter\\nklaus and sally\\n')
            >>> string.readline()
            Object of "String" with "hans" saved.
            >>> string.readline()
            Object of "String" with "peter" saved.
            >>> string.readline().content
            'klaus and sally'
            >>> string.readline()
            False

            >>> String('hans').readline()
            Object of "String" with "hans" saved.

            >>> string = String('hans')
            >>> string.readline().content
            'hans'
            >>> string.readline()
            False
        '''
        self._current_line_number += 1
        if builtins.len(self.readlines()) >= self._current_line_number:
            return self.__class__(
                self.readlines()[self._current_line_number - 1])
        return False

    @JointPoint
## python3.3
##     def readlines(
##         self: Self, *arguments: builtins.object, **keywords: builtins.object
##     ) -> builtins.list:
    def readlines(self, *arguments, **keywords):
##
        '''
            Implements the pythons native "builtins.str.splitlines()" method \
            in an object oriented way.

            Return a list of all lines in a string, breaking at line \
            boundaries. Line breaks are not included in the resulting list \
            unless "keepends" is given and "True".

            Examples:

            >>> lines = String('hans\\npeter\\nklaus and sally\\n')
            >>> lines.readlines(True)
            ['hans\\n', 'peter\\n', 'klaus and sally\\n']

            >>> lines.readlines()
            ['hans', 'peter', 'klaus and sally']

            >>> String('hans').readlines()
            ['hans']

            >>> String().readlines()
            []
        '''
        return self.content.splitlines(*arguments, **keywords)

    @JointPoint
## python3.3     def delete_variables_from_regex(self: Self) -> Self:
    def delete_variables_from_regex(self):
        '''
            Removes python supported variables in regular expression strings. \
            This method is useful if a python regular expression should be \
            given to another regular expression engine which doesn't support \
            variables.

            Examples:

            >>> String('^--(?P<name>.+)--$').delete_variables_from_regex()
            Object of "String" with "^--(.+)--$" saved.

            >>> String(
            ...     '^--(?P<a>.+)--(?P<b>.+)--$'
            ... ).delete_variables_from_regex()
            Object of "String" with "^--(.+)--(.+)--$" saved.
        '''
        return self.subn('\(\?P<[a-z]+>(?P<pattern>.+?)\)', '(\g<pattern>)')[0]

        # endregion

        # region protected

            # region find python code end bracket helper

    @JointPoint
## python3.3
##     def _handle_char_to_find_end_bracket(
##         self: Self, index: builtins.int, char: builtins.str,
##         quote: (builtins.str, builtins.bool), skip: builtins.int,
##         brackets: builtins.int
##     ) -> (builtins.tuple, builtins.int):
    def _handle_char_to_find_end_bracket(
        self, index, char, quote, skip, brackets
    ):
##
        '''
            Helper method for "find_python_code_end_bracket()".

            Examples:

            >>> String()._handle_char_to_find_end_bracket(
            ...     0, '\\\\', True, 0, 0)
            (1, '\\\\', True, 1, 0)

            >>> String()._handle_char_to_find_end_bracket(
            ...     1, 'a', True, 1, 0)
            (2, 'a', True, 0, 0)

            >>> String()._handle_char_to_find_end_bracket(
            ...     1, 'a', True, 0, 0)
            (2, 'a', True, 0, 0)

            >>> String()._handle_char_to_find_end_bracket(
            ...     1, '"', True, 0, 0)
            (2, '"', True, 0, 0)

            >>> String()._handle_char_to_find_end_bracket(
            ...     1, '(', True, 0, 0)
            (2, '(', True, 0, 0)

            >>> String()._handle_char_to_find_end_bracket(
            ...     1, '"', False, 0, 0)
            (2, '"', '"', 0, 0)
        '''
        if char == '\\':
            '''Handle escape sequences.'''
            skip = 1
        elif skip:
            skip -= 1
        elif quote:
            char, quote, skip = self._handle_quotes_to_find_end_bracket(
                index, char, quote, skip)
        elif char == ')':
            '''Handle ending brackets.'''
            if brackets:
                brackets -= 1
            else:
                return index
        elif char in ('"', "'"):
            quote, skip = self._handle_start_quotes_to_find_end_bracket(
                index, char, quote, skip)
        elif char == '(':
            '''Handle opening brackets.'''
            brackets += 1
        return index + 1, char, quote, skip, brackets

    @JointPoint
## python3.3
##     def _handle_start_quotes_to_find_end_bracket(
##         self: Self, index: builtins.int, char: builtins.str,
##         quote: (builtins.str, builtins.bool), skip: builtins.int
##     ) -> builtins.tuple:
    def _handle_start_quotes_to_find_end_bracket(
        self, index, char, quote, skip
    ):
##
        '''
            Helper method for "find_python_code_end_bracket()".

            Examples:

            >>> String('aaa')._handle_start_quotes_to_find_end_bracket(
            ...     0, 'a', True, 0)
            ('aaa', 2)
        '''
        if self.content[index:index + 3] == 3 * char:
            quote = char * 3
            skip = 2
        else:
            quote = char
        return quote, skip

    @JointPoint
## python3.3
##     def _handle_quotes_to_find_end_bracket(
##         self: Self, index: builtins.int, char: builtins.str,
##         quote: (builtins.str, builtins.bool), skip: builtins.int
##     ) -> builtins.tuple:
    def _handle_quotes_to_find_end_bracket(self, index, char, quote, skip):
##
        '''
            Helper method for "find_python_code_end_bracket()".

            Examples:

            >>> String()._handle_quotes_to_find_end_bracket(0, '"', '"', 0)
            ('"', False, 0)

            >>> String('aaa')._handle_quotes_to_find_end_bracket(
            ...     0, 'a', 'aaa', 0)
            ('a', False, 2)
        '''
        if char == quote:
            quote = False
        elif self.content[index:index + 3] == quote:
            skip = 2
            quote = False
        return char, quote, skip

            # endregion

        # endregion

    # endregion


class Dictionary(Object, builtins.dict):
    '''This class extends the native dictionary object.'''

    # region dynamic methods

        # region public

            # region special

    @JointPoint
## python3.3
##     def __init__(
##         self: Self, content: collections.Iterable,
##         *arguments: builtins.object, **keywords: builtins.object
##     ) -> None:
    def __init__(self, content, *arguments, **keywords):
##
        '''
            Generates a new high level wrapper around given object.

            Examples:

            >>> Dictionary((('hans', 5), (4, 3))) # doctest: +ELLIPSIS
            Object of "Dictionary" (...hans...5...).
        '''

            # region properties

        '''The main property. It saves the current dictionary.'''
        self.content = builtins.dict(content)

            # endregion

        '''Take this method type by the abstract class via introspection.'''
        return builtins.getattr(
            builtins.super(self.__class__, self), inspect.stack()[0][3]
        )(content, *arguments, **keywords)

    @JointPoint
## python3.3     def __repr__(self: Self) -> builtins.str:
    def __repr__(self):
        '''
            Invokes if this object should describe itself by a string.

            Examples:

            >>> repr(Dictionary({'a': 'hans'}))
            'Object of "Dictionary" ({\\'a\\': \\'hans\\'}).'
        '''
        return 'Object of "{class_name}" ({content}).'.format(
            class_name=self.__class__.__name__,
            content=builtins.repr(self.content))

    @JointPoint
## python3.3     def __hash__(self: Self) -> builtins.int:
    def __hash__(self):
        '''
            Invokes if this object should describe itself by a hash value.

            Examples:

            >>> isinstance(hash(Dictionary({'a': 'hans'})), int)
            True
        '''
        return builtins.hash(self.immutable)

    @JointPoint
## python3.3
##     def __getitem__(
##         self: Self, key: (builtins.object, builtins.type)
##     ) -> (builtins.object, builtins.type):
    def __getitem__(self, key):
##
        '''
            Invokes if this object should returns current value stored at \
            given key.

            Examples:

            >>> Dictionary({'a': 'hans'})['a']
            'hans'
        '''
        return self.content[key]

            # endregion

            # region getter methods

    @JointPoint(Class.pseudo_property)
## python3.3     def get_immutable(self: Self) -> builtins.tuple:
    def get_immutable(self):
        '''
            Generates an immutable copy of the current dictionary. Mutable \
            iterables are generally translated to sorted tuples.
        '''
        immutable = copy.copy(self.content)
        for key, value in immutable.items():
            immutable[key] = self._immutable_helper(value)
        return builtins.tuple(builtins.sorted(
            immutable.items(), key=builtins.str))

            # endregion

    @JointPoint
## python3.3
##     def pop(
##         self: Self, name: builtins.str, default_value=None
##     ) -> builtins.tuple:
    def pop(self, name, default_value=None):
##
        '''
            Get a keyword element as it would be set by a default value. If \
            name is present in current saved dictionary its value will be \
            returned in a tuple with currently saved dictionary. The \
            corresponding data will be erased from dictionary.

            Examples:

            >>> dictionary = Dictionary({'hans': 'peter', 5: 3})
            >>> dictionary.pop('hans', 5)
            ('peter', {5: 3})

            >>> dictionary.pop('hans', 5)
            (5, {5: 3})

            >>> Dictionary({5: 3}).pop('hans', True)
            (True, {5: 3})
        '''
        if name in self.content:
            result = self.content[name]
            del self.content[name]
            return result, self.content
        return default_value, self.content

        # endregion

        # region protected methods

    @JointPoint
## python3.3
##     def _immutable_helper(
##         self: Self, value: (builtins.object, builtins.type)
##     ) -> (builtins.object, builtins.type):
    def _immutable_helper(self, value):
##
        '''
            Helper methods for potential immutable given value.

            Examples:

            >>> Dictionary({})._immutable_helper({5: 'hans'})
            ((5, 'hans'),)

            >>> Dictionary({})._immutable_helper([5, 'hans'])
            (5, 'hans')
        '''
        if builtins.isinstance(value, builtins.dict):
            value = self.__class__(content=value).immutable
        elif(builtins.isinstance(value, collections.Iterable) and
             not builtins.isinstance(value, builtins.str)):
            value = copy.copy(value)
            for key, sub_value in builtins.enumerate(value):
                value[key] = self._immutable_helper(value=sub_value)
        if not (builtins.hasattr(value, '__hash__') and
                builtins.callable(builtins.getattr(value, '__hash__'))):
            value = builtins.tuple(builtins.sorted(value, key=builtins.str))
        return value

        # endregion

    # endregion


class Module(Object):
    '''This class add some features for dealing with modules.'''

    # region properties

## python3.3
##     HIDDEN_BUILTIN_CALLABLES = ()
    HIDDEN_BUILTIN_CALLABLES = (
        'GFileDescriptorBased', 'GInitiallyUnowned', 'GPollableInputStream',
        'GPollableOutputStream')
##
    '''Stores all magically defined globals.'''
    PREFERED_ENTRY_POINT_FUNCTION_NAMES = (
        'main', 'init', 'initialize', 'run', 'start')
    '''
        Stores a priority order of preferred callable name as starting point \
        in a initialized module.
    '''

    # endregion

    # region static methods

        # region public

            # region special

    @JointPoint(builtins.classmethod)
## python3.3     def __repr__(cls: SelfClass) -> builtins.str:
    def __repr__(cls):
        '''
            Invokes if this object should describe itself by a string.

            Examples:

            >>> repr(Module()) # doctest: +ELLIPSIS
            'Object of "Module" with hidden builtin callables "..." saved.'
        '''
        return 'Object of "{class_name}" with hidden builtin callables '\
               '"{hidden_builtin_callables}" saved.'.format(
                   class_name=cls.__name__,
                   hidden_builtin_callables='", "'.join(
                       cls.HIDDEN_BUILTIN_CALLABLES))

            # endregion

            # region getter

    # NOTE: This method couldn't have a joint point for avoiding to have cyclic
    # dependencies.
    @builtins.classmethod
    @Class.pseudo_property
## python3.3
##     def get_context_path(
##         cls: SelfClass, path=None, frame=inspect.currentframe(),
##     ) -> builtins.str:
    def get_context_path(cls, path=None, frame=inspect.currentframe()):
##
        '''
            Determines the package and module level context path to a given \
            context or file.

            Examples:

            >>> Module.get_context_path(
            ...     frame=inspect.currentframe()
            ... ) # doctest: +ELLIPSIS
            '...boostNode.extension...doctest...Module'

            >>> Module.get_context_path(path='./native') # doctest: +ELLIPSIS
            '...boostNode.extension.native'

            >>> Module.get_context_path(path='.') # doctest: +ELLIPSIS
            '...boostNode.extension'
        '''
        if path is None:
            path = frame.f_code.co_filename
        path = os.path.abspath(os.path.normpath(path))
        context_path = os.path.basename(path)
        if '.' in context_path:
            context_path = context_path[:context_path.rfind('.')]
        while cls.is_package(path=path[:path.rfind(os.sep)]):
            path = path[:path.rfind(os.sep)]
            context_path = '%s.%s' % (os.path.basename(path), context_path)
        return context_path

    @JointPoint(builtins.classmethod)
    @Class.pseudo_property
## python3.3
##     def get_name(
##         cls: SelfClass, frame=None, module=None, extension=False, path=False
##     ) -> builtins.str:
    def get_name(cls, frame=None, module=None, extension=False, path=False):
##
        '''
            Returns name of the given context "frame". If no frame is defined \
            this module's context will be selected. If "base" is set "True" \
            the modules name is given back without any file extension.

            Examples:

            >>> Module().name
            'native'

            >>> Module.get_name(extension=True)
            'native.py'

            >>> Module.get_name(path=True) # doctest: +ELLIPSIS
            '...boostNode...extension...native'

            >>> Module.get_name(path=True, extension=True) # doctest: +ELLIPSIS
            '...boostNode...extension...native.py'
        '''
        file = cls._get_module_file(frame, module)
        if path and extension:
            return file.path
        if extension:
            return file.name
        if path:
            return file.directory_path + file.basename
        return file.basename

    @JointPoint(builtins.classmethod)
    @Class.pseudo_property
## python3.3
##     def get_package_name(
##         cls: SelfClass, frame=inspect.currentframe(), path=False
##     ) -> builtins.str:
    def get_package_name(cls, frame=inspect.currentframe(), path=False):
##
        '''
            Determines package context of given frame. If current context \
            isn't in any package context an empty string is given back.

            Examples:

            >>> Module().package_name
            'extension'

            >>> Module.get_package_name(path=True) # doctest: +ELLIPSIS
            '...boostNode...extension...'

            >>> Module.get_package_name(
            ...     frame=inspect.currentframe(), path=True
            ... ) # doctest: +ELLIPSIS
            '...boostNode...extension...'
        '''
        from boostNode.extension.file import Handler as FileHandler
        '''
            NOTE: "must_exist=False" is necessary for supporting frozen \
            executables.
        '''
        file = FileHandler(
            location=frame.f_code.co_filename, respect_root_path=True)
        if cls.is_package(path=file.directory_path) or not file:
            if not file:
                file = FileHandler(
                    location=sys.argv[0], respect_root_path=True)
            if path:
                return file.directory_path
            return FileHandler(location=file.directory_path).name
        return ''

    @JointPoint(builtins.classmethod)
    @Class.pseudo_property
## python3.3
##     def get_file_path(
##         cls: SelfClass, context_path: builtins.str, only_source_files=False
##     ) -> (builtins.str, builtins.bool):
    def get_file_path(
        cls, context_path, only_source_files=False
    ):
##
        '''
            Returns the path to given module name.

            Examples:

            >>> Module.get_file_path('doctest') # doctest: +ELLIPSIS
            '...doctest.py...'

            >>> Module.get_file_path(
            ...     'doctest', only_source_files=True) # doctest: +ELLIPSIS
            '...doctest.py'

            >>> Module.get_file_path('module_that_does_not_exists')
            False

            >>> Module.get_file_path('')
            False
        '''
        from boostNode.extension.file import Handler as FileHandler
        if context_path:
            for search_path in sys.path:
                location = FileHandler(
                    location=search_path, respect_root_path=False)
                if location.is_directory():
                    location = cls._search_library_file(
                        location, context_path, only_source_files)
                    if location:
                        return location
        return False

            # endregion

            # region boolean

    @builtins.classmethod
## python3.3
##     def is_package(cls: SelfClass, path: builtins.str) -> builtins.bool:
    def is_package(cls, path):
##
        '''
            Checks if given location is pointed to a python package.

            Examples:

            >>> Module.is_package(__file_path__)
            False
        '''
        if os.path.isdir(path):
            for file_name in os.listdir(path):
                basename = os.path.basename(file_name)
                if '.' in basename:
                    basename = basename[:basename.rfind('.')]
                if(os.path.isfile(path + os.sep + file_name) and
                   basename == '__init__' and
                   file_name[file_name.rfind('.') + 1:] in
                   ('py', 'pyc', 'pyw')):
                    return True
        return False

            # endregion

    @JointPoint(builtins.classmethod)
## python3.3
##     def determine_caller(
##         cls: SelfClass, callable_objects: collections.Iterable, caller=None
##     ) -> (builtins.bool, builtins.str, builtins.type(None)):
    def determine_caller(cls, callable_objects, caller=None):
##
        '''
            Searches for a useful caller object in given module objects via \
            "module_objects".

            Examples:

            >>> Module.determine_caller([]) is None
            True

            >>> Module.determine_caller(['A', 'B'], 'B')
            'B'

            >>> Module.determine_caller(['A', 'B'], None)
            'A'

            >>> Module.determine_caller(['A', 'Main'], None)
            'Main'

            >>> Module.determine_caller(['A'], False)
            False

            >>> Module.determine_caller(['AError', 'A'], None)
            'A'
        '''
        if not (caller or caller is False):
            for object in callable_objects:
                if object.lower() in cls.PREFERED_ENTRY_POINT_FUNCTION_NAMES:
                    return object
            if builtins.len(callable_objects):
                index = 0
                while(builtins.len(callable_objects) > index + 1 and
                      callable_objects[index].endswith('Error')):
                    index += 1
                return callable_objects[index]
        return caller

    @JointPoint(builtins.classmethod)
    @Class.pseudo_property
## python3.3
##     def get_defined_callables(
##         cls: SelfClass, scope: (builtins.type, builtins.object),
##         only_module_level=True
##     ) -> builtins.list:
    def get_defined_callables(cls, scope, only_module_level=True):
##
        '''
            Takes a module and gives a list of objects explicit defined in \
            this module.

            Examples:

            >>> Module.get_defined_callables(
            ...     sys.modules['__main__']
            ... ) # doctest: +ELLIPSIS
            [...'Module'...]

            >>> class A:
            ...     a = 'hans'
            ...     def b():
            ...         pass
            ...     def __A__():
            ...         pass
            >>> Module.get_defined_callables(A, only_module_level=False)
            ['b']

            >>> @JointPoint
            ... def b():
            ...     pass
            >>> temporary_object = object
            >>> a = A()
            >>> a.b = b
            >>> Module.get_defined_callables(a, only_module_level=False)
            ['b']
        '''
        callables = []
        for object_name in builtins.set(builtins.dir(scope)):
            object = cls._determine_object(object=builtins.getattr(
                scope, object_name))
            if(builtins.callable(object) and
               not (object_name.startswith('__') and
                    object_name.endswith('__')) and
               not (inspect.ismodule(object) or
                    object_name in cls.HIDDEN_BUILTIN_CALLABLES or
                    inspect.isbuiltin(object) or
                    object_name in sys.modules or
                    object_name in sys.builtin_module_names or
                    (only_module_level and inspect.getmodule(object) !=
                        scope))):
                callables.append(object_name)
        return callables

    @JointPoint(builtins.classmethod)
## python3.3
##     def execute_program_for_modules(
##         cls: SelfClass, program_type: builtins.str, program: builtins.str,
##         modules: collections.Iterable, arguments=(), extension='py',
##         delimiter=', ', log=True, **keywords: builtins.object
##     ) -> builtins.tuple:
    def execute_program_for_modules(
        cls, program_type, program, modules, arguments=(),
        extension='py', delimiter=', ', log=True, **keywords
    ):
##
        '''
            Runs a given program for every given module. Returns "False" if \
            no modules were found or given program isn't installed.

            Examples:

            >>> import boostNode.extension

            >>> Module.execute_program_for_modules(
            ...     'linter', 'pyflakes', boostNode.extension.__all__
            ... ) # doctest: +SKIP
            [(..., ...), ...]

            >>> Module.execute_program_for_modules(
            ...     'program', 'not_existing', boostNode.extension.__all__,
            ...     error=False
            ... ) # doctest: +ELLIPSIS
            ('', ...)

            >>> Module.execute_program_for_modules(
            ...     'program', 'ls', boostNode.extension.__all__,
            ...     error=False
            ... ) # doctest: +ELLIPSIS
            (..., ...)
        '''
        from boostNode.extension.file import Handler as FileHandler
        from boostNode.extension.system import Platform
        results = []
        for module in modules:
            module_file = FileHandler(location=module + os.extsep + extension)
            results.append(Platform.run(
                command=program,
                command_arguments=builtins.list(
                    arguments
                ) + [module_file.path],
                log=log, **keywords))
        result = ['', '']
        first_standard_output = first_error_output = True
        for result_element in results:
            if result_element['standard_output'].strip():
                if not first_standard_output:
                    result[0] += delimiter
                result[0] += result_element['standard_output'].strip()
                first_standard_output = False
            if result_element['error_output'].strip():
                if not first_error_output:
                    result[1] += delimiter
                result[1] += result_element['error_output'].strip()
                first_error_output = False
        return builtins.tuple(result)

    @JointPoint(builtins.classmethod)
## python3.3
##     def extend(
##         cls: SelfClass, name=__name__, frame=None, module=None,
##         post_extend_others=True
##     ) -> builtins.dict:
    def extend(
        cls, name=__name__, frame=None, module=None, post_extend_others=True
    ):
##
        '''
            Extends a given scope of an module for useful things like own \
            exception class, a logger instance, variable to indicate if \
            module is running in test mode and a variable that saves the \
            current module name.

            Returns a dictionary with new module's scope and module name.

            Examples:

            >>> import logging

            >>> Module.extend() # doctest: +ELLIPSIS
            {...native...}
            >>> __logger__ # doctest: +ELLIPSIS
            <logging.Logger object at 0x...>
            >>> __exception__ # doctest: +ELLIPSIS
            <class '...NativeError'>
            >>> __module_name__
            'native'
            >>> raise __exception__(
            ...     '%s', 'hans'
            ... ) # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            NativeError: hans

            >>> Module.extend(
            ...     __name__, module=sys.modules['doctest']
            ... ) # doctest: +ELLIPSIS
            {...'name': 'doctest'...}
        '''
        from boostNode.extension.output import Logger
        if module is None:
            module = sys.modules[name]
        else:
            name = module.__name__
        module.__logger__ = Logger.get(name)
        if(not builtins.hasattr(module, '__module_name__') or
           module.__module_name__ is None):
            module.__module_name__ = cls.get_name(frame, module)
        module.__exception__ = builtins.type(
            String(module.__module_name__).camel_case_capitalize().content +
            'Error', (builtins.Exception,),
            {'__init__': lambda self, message,
                *arguments: builtins.Exception.__init__(
                    self, message % arguments
                ) if arguments else builtins.Exception.__init__(
                    self, message)})
        module.__test_mode__ = False
        module.__file_path__ = cls.get_name(
            frame, module, path=True, extension=True)
        '''Extend imported modules which couldn't be extended yet.'''
        if post_extend_others:
            for imported_name, imported_module in sys.modules.items():
                if(imported_name.startswith(boostNode.__name__ + '.') and
                   builtins.hasattr(imported_module, '__module_name__') and
                   imported_module.__module_name__ is None):
                    '''Take this method via introspection.'''
                    builtins.getattr(cls, inspect.stack()[0][3])(
                        name=imported_name, module=imported_module,
                        post_extend_others=False)
        return {'name': name, 'scope': module}

    @JointPoint(builtins.classmethod)
## python3.3
##     def default(
##         cls: SelfClass, name: builtins.str, frame: types.FrameType,
##         default_caller=None, caller_arguments=(), caller_keywords={}
##     ) -> SelfClass:
    def default(
        cls, name, frame, default_caller=None, caller_arguments=(),
        caller_keywords={}
    ):
##
        '''
            Serves a common way to extend a given module. The given module's \
            scope will be extended and a common meta command line interface \
            is provided to test or run objects in given module.

            Examples:

            >>> command_line_arguments_save = copy.copy(sys.argv)
            >>> sys.argv += ['--module-object', Module.__name__]
            >>> if not 'native' in sys.modules:
            ...     sys.modules['native'] = sys.modules[__name__]
            >>> Module.default(
            ...     'native', inspect.currentframe()
            ... ) # doctest: +ELLIPSIS
            <class '...Module'>
            >>> sys.argv = command_line_arguments_save
        '''
        from boostNode.extension.system import CommandLine
        CommandLine.generic_module_interface(
            module=cls.extend(name, frame),
            default_caller=default_caller, caller_arguments=caller_arguments,
            caller_keywords=caller_keywords)
        return cls

    @JointPoint(builtins.classmethod)
## python3.3
##     def default_package(
##         cls: SelfClass, name: builtins.str, frame: types.FrameType,
##         *arguments: builtins.object, **keywords: builtins.object
##     ) -> (builtins.tuple, builtins.bool):
    def default_package(
        cls, name, frame, command_line_arguments=(), *arguments, **keywords
    ):
##
        '''
            Serves a common way to extend a given package. The given \
            package's scope will be extended and a common meta command line \
            interface is provided to test, lint or document modules.

            Examples:

            >>> Module.default_package(
            ...     'not_existing', inspect.currentframe())
            Traceback (most recent call last):
            ...
            KeyError: 'not_existing'

            >>> Module.default_package('doctest', inspect.currentframe())
            False
        '''
        from boostNode.extension.system import CommandLine
        cls.extend(name, frame)
        return CommandLine.generic_package_interface(
            name, frame, *arguments, **keywords)

        # endregion

        # region protected

    @JointPoint(builtins.classmethod)
## python3.3
##     def _determine_object(
##         cls: SelfClass, object: (builtins.type, builtins.object)
##     ) -> (builtins.object, builtins.type):
    def _determine_object(cls, object):
##
        '''Determines a potentially wrapped object.'''
        if(builtins.isinstance(JointPoint, builtins.type) and
           builtins.isinstance(object, JointPoint)):
            return object.__func__
        return object

    @JointPoint(builtins.classmethod)
## python3.3
##     def _get_module_file(
##         cls: SelfClass, frame: (builtins.type(None), types.FrameType),
##         module: (builtins.type(None), types.ModuleType)
##     ) -> (Class, builtins.bool):
    def _get_module_file(cls, frame, module):
##
        '''
            Determines the file of a given module or frame context.

            Examples:

            >>> Module._get_module_file(
            ...     inspect.currentframe(), None
            ... ) # doctest: +ELLIPSIS
            Object of "Handler" with path "..." and initially given path "...
        '''
        from boostNode.extension.file import Handler as FileHandler
        file = False
        if module:
            file = FileHandler(
                location=inspect.getsourcefile(module),
                respect_root_path=False)
        if not file:
            if frame is None:
                frame = inspect.currentframe()
            file = FileHandler(
                location=frame.f_code.co_filename, respect_root_path=False)
        if not file:
            file = FileHandler(
                location=sys.argv[0], respect_root_path=False)
        return file

    @JointPoint(builtins.classmethod)
## python3.3
##     def _search_library_file(
##         cls: SelfClass, location: Class, context_path: builtins.str,
##         only_source_files: builtins.bool
##     ) -> (builtins.str, builtins.bool):
    def _search_library_file(
        cls, location, context_path, only_source_files=False
    ):
##
        '''
            Searches for full path to a given context path in given locations.
        '''
        for sub_module in context_path.split('.'):
            found_last_sub_module = False
            for sub_location in location:
                if(sub_location.basename == sub_module and
                   not (only_source_files and
                        sub_location.extension in ('pyc', 'pyo', 'pyd'))):
                    found_last_sub_module = True
                    location = sub_location
                    break
            if not found_last_sub_module:
                return False
        return sub_location.path

        # endregion

    # endregion

# endregion

# region footer

'''
    Preset some variables given by introspection letting the linter know what \
    globale variables are available.
'''
__logger__ = __exception__ = __module_name__ = __file_path__ = \
    __test_mode__ = None
'''
    Extends this module with some magic environment variables to provide \
    better introspection support. A generic command line interface for some \
    code preprocessing tools is provided by default.
'''
if __name__ == '__main__':
    Module.default(
        name=__name__, frame=inspect.currentframe(), default_caller=False)

# endregion
