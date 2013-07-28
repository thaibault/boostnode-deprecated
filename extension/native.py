#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-

# region vim modline

# vim: set tabstop=4 shiftwidth=4 expandtab:
# vim: foldmethod=marker foldmarker=region,endregion:

# endregion

# region header

'''
    Extension is a high level interface for interaction with pythons native
    builtins.
    This class provides a full object oriented way to handle string objects.
    Besides a number of new supported interactions with strings it offers all
    core file system methods by the pythons native "builtins.str" object.
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
import encodings
import inspect
import os
import re
import sys
## python2.7 pass
import types

for number in (3, 4):
    sys.path.append(os.path.abspath(sys.path[0] + number * ('..' + os.sep)))

import boostNode.extension.dependent
import boostNode.extension.output
import boostNode.extension.file
import boostNode.extension.system
import boostNode.extension.type
import boostNode.paradigm.aspectOrientation
import boostNode.paradigm.objectOrientation

# endregion


# region classes

class Object(boostNode.paradigm.objectOrientation.Class):
    '''
        This class extends all native python classes.
    '''

    # region dynamic properties

        # region public properties

    object = None

        # endregion

        # region protected properties

    _object_copy = {}

        # endregion

    # endregion

    # region dynamic methods

        # region public methods

            # region special methods

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def __init__(self, object=None):
    def __init__(
        self: boostNode.extension.type.Self, object=None
    ) -> None:
##
        '''
            Generates a new high level wrapper around given object.

            Examples:

            >>> Object('hans') # doctest: +ELLIPSIS
            Object of "str" ('hans').
        '''
        self.object = object

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def __repr__(self):
    def __repr__(self: boostNode.extension.type.Self) -> builtins.str:
##
        '''
            Invokes if this object should describe itself by a string.
        '''
        return 'Object of "{class_name}" ({object}).'.format(
            class_name=self.object.__class__.__name__,
            object=builtins.repr(self.object))

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def __str__(self):
    def __str__(self: boostNode.extension.type.Self) -> builtins.str:
##
        '''
            Is triggered if this object should be converted to string.

            Examples:

            >>> str(Object(['hans']))
            "['hans']"
        '''
        return builtins.str(self.object)

            # endregion

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def copy(self):
    def copy(self: boostNode.extension.type.Self) -> builtins.dict:
##
        '''
            Copies a given object's attributes and returns them.

            Examples:

            >>> class A:
            ...     pass
            >>> a = A()
            >>> a.string = 'hans'
            >>> object_copy = Object(a).copy()
            >>> for key, value in object_copy.items():
            ...     if 'string' == key:
            ...         print(value)
            hans

            >>> class B:
            ...     hans = 'A'
            >>> object = Object(B())
            >>> object_copy = object.copy()
            >>> object.object.hans = 'B'
            >>> object.object.hans
            'B'
            >>> object_copy['hans']
            'A'
        '''
        self._object_copy = {}
        for attribute in builtins.dir(self.object):
            if not (attribute.startswith('__') and attribute.endswith('__')):
                self._object_copy[attribute] = builtins.getattr(
                    self.object, attribute)
        return self._object_copy

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7     def restore(self):
    def restore(self: boostNode.extension.type.Self):
        '''
            Restores a given object's attributes by a given copy are last
            copied item.

            Examples:

            >>> class A:
            ...     pass
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
            >>> object = Object(A())
            >>> object_copy = object.copy()
            >>> object.object.hans = 'B'
            >>> object.object.hans
            'B'
            >>> object.restore().hans
            'A'
        '''
        for attribute, value in self._object_copy.items():
            if not (attribute.startswith('__') and attribute.endswith('__')):
                builtins.setattr(self.object, attribute, value)
        return self.object

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def is_binary(self):
    def is_binary(self: boostNode.extension.type.Self) -> builtins.bool:
##
        '''
            Determines if given data is binary.
        '''
        # NOTE: This is a dirty workaround to handle python2.7 lack of
        # differentiation between "string" and "bytes" objects.
## python2.7
##         object = self.object
##         if builtins.isinstance(self.object, builtins.unicode):
##             object = self.object.encode(encoding='utf_8')
##         text_chars = ''.join(builtins.map(
##             builtins.chr,
##             builtins.range(7, 14) + [27] + builtins.range(0x20, 0x100)))
##         return builtins.bool(object.translate(None, text_chars))
        return builtins.isinstance(self.object, builtins.bytes)
##

        # endregion

    # endregion

    # region static methods

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python2.7
##     def determine_abstract_method_exception(cls, abstract_class_name):
    def determine_abstract_method_exception(
        cls: boostNode.extension.type.SelfClass,
        abstract_class_name: builtins.str
    ) -> builtins.NotImplementedError:
##
        '''
            Generates a suitable exception for raising if a method is called
            initially indented to be overwritten.
        '''
        '''
            Note: fetch third frame "inspect.stack()[2]"
                0: this
                1: Decorator wrapper
                2: caller
        '''
        return builtins.NotImplementedError(
            'Method "{name}" wasn\'t implemented by "{class_name}" and is '
            'necessary for abstract class "{abstract_class}".'.format(
                name=inspect.stack()[2][3], class_name=cls.__name__,
                abstract_class=abstract_class_name))

    # endregion


class String(Object, builtins.str):
    '''
        The string class inherits besides the interface class all pythons
        native string methods.
    '''

    # region constant properties

        # region public properties

    '''
        Defines generally important encodings. Which should be tried at first.
    '''
    IMPORTANT_ENCODINGS = 'ascii', 'utf_8', 'latin_1', 'utf_16'
    '''All chars wich should be handle during dealing with web urls.'''
    NON_STANDARD_SPECIAL_URL_SEQUENCES = {
        '%1000': '#', '%1001': '&', '%1002': '=', '%1003': '%', '%1004': '+'}
    '''
        All chars which should be observed by handling with shell command.
        Note that the escape sequence must not be defined.
    '''
    SPECIAL_SHELL_SEQUENCES = (
        '"', "'", '`', '(', ')', ' ', '&', '$', '-')
    '''
        All chars which should be observed by handling with regex sequences.
        Note that the escape sequence must not be defined.
    '''
    SPECIAL_REGEX_SEQUENCES = (
        '-', '[', ']', '(', ')', '^', '$', '*', '+', '.', '{', '}')
    '''ALl chars wich should be observed by handling with url sequences.'''
    SPECIAL_URL_SEQUENCES = {
        '+': ' ', '%20': ' ', '%22': '"', '%2F': '/', '%7E': '~',
        '%C3%A4': 'ä', '%C3%84': 'Ä',
        '%C3%B6': 'ö', '%C3%96': 'Ö',
        '%C3%BC': 'ü', '%C3%9C': 'Ü'}
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

        # endregion

    # endregion

    # region dynamic properties

        # region public properties

    '''The main string property. It saves the current string.'''
    content = ''

        # endregion

        # region protected properties

    '''Saves the current line for the "readline()" method.'''
    _current_line_number = 0

        # endregion

    # endregion

    # region dynamic methods

        # region public methods

            # region special methods

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def __init__(self, content=None, *arguments, **keywords):
    def __init__(
        self: boostNode.extension.type.Self, content=None,
        *arguments: builtins.object, **keywords: builtins.object
    ) -> None:
##
        '''
            Initialize a new "String" object.

            Examples:

            >>> string = String('hans')
            >>> string.content
            'hans'

            >>> string = String()
            >>> string.content
            ''
        '''
        if content is None:
            content = ''
        self.content = builtins.str(content)
        '''
            Take this method type by the abstract class via introspection.
        '''
        return builtins.getattr(
            builtins.super(self.__class__, self), inspect.stack()[0][3]
        )(content, *arguments, **keywords)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def __repr__(self):
    def __repr__(self: boostNode.extension.type.Self) -> builtins.str:
##
        '''
            Invokes if this object should describe itself by a string.

            Examples:

            >>> repr(String('hans'))
            'Object of "String" with "hans" saved.'
        '''
        return 'Object of "{class_name}" with "{content}" saved.'.format(
            class_name=self.__class__.__name__, content=self.content)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def __len__(self):
    def __len__(self: boostNode.extension.type.Self) -> builtins.int:
##
        '''
            Triggers if the pythons native "builtins.len()" function tries to
            handle current instance.
            Returns the number of symbols given in the current string
            representation of this object.

            Examples:

            >>> len(String())
            0

            >>> len(String('hans'))
            4
        '''
        return builtins.len(self.__str__())

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def __str__(self):
    def __str__(self: boostNode.extension.type.Self) -> builtins.str:
##
        '''
            Triggers if the current object should be directly interpreted as
            pythons native string implementation.

            Examples:

            >>> str(String('hans'))
            'hans'

            >>> str(String())
            ''
        '''
        return self.content

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def __nonezero__(self):
    def __bool__(self: boostNode.extension.type.Self) -> builtins.bool:
##
        '''
            Triggers if the current object should be interpreted as
            a boolean value directly.

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

        # endregion

    # endregion

    # region static methods

        # region public methods

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python2.7
##     def get_escaping_replace_dictionary(
##         cls, sequence, escape_sequence='\{symbole}'
##     ):
    def get_escaping_replace_dictionary(
        cls: boostNode.extension.type.SelfClass,
        sequence: collections.Iterable, escape_sequence='\{symbole}'
    ) -> builtins.dict:
##
        '''
            Creates a replacement dictionary form a given iterable. Every
            element will be associated with its escaped version. This method
            is useful for using before give "self.replace()" a dictionary.

            "sequence" is an iterable with elements to be escaped.
            "escape_sequence" is an escape sequence for each element from
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

        # region public methods

            # region validation methods.

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def validate_shell(self):
    def validate_shell(
        self: boostNode.extension.type.Self
    ) -> boostNode.extension.type.Self:
##
        '''
            Validates the current string for using as a command in shell.
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

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def validate_html(self):
    def validate_html(
        self: boostNode.extension.type.Self
    ) -> boostNode.extension.type.Self:
##
        '''
            Validates current string for using as snippet in a html document.
        '''
        return self.replace(self.SPECIAL_HTML_SEQUENCES)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def validate_regex(self, exclude_symbols=()):
    def validate_regex(
        self: boostNode.extension.type.Self, exclude_symbols=()
    ) -> boostNode.extension.type.Self:
##
        '''
            Validates the current string for using in a regular expression
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
        '''
        '''The escape sequence must also be escaped; but at first.'''
        if not '\\' in exclude_symbols:
            self.replace('\\', '\\\\')
        return self.replace(
            search=self.__class__.get_escaping_replace_dictionary(
                builtins.tuple(
                    builtins.set(self.SPECIAL_REGEX_SEQUENCES) -
                    builtins.set(exclude_symbols))))

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def validate_format(self):
    def validate_format(
        self: boostNode.extension.type.Self
    ) -> boostNode.extension.type.Self:
##
        '''
            Validates the current string for using in a string with placeholder
            like "{name}". It will be escaped to not interpreted as
            placeholder like "\{name\}".

            Examples:

            >>> String("that's no {placeholder}").validate_format()
            Object of "String" with "that's no \{placeholder\}" saved.

            >>> String().validate_format().content
            ''
        '''
        self.content = re.compile('{([a-z]+)}').sub(r'\\{\1\\}', self.content)
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def validate_url(self):
    def validate_url(
        self: boostNode.extension.type.Self
    ) -> boostNode.extension.type.Self:
##
        '''
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

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def determine_encoding(self):
    def determine_encoding(
        self: boostNode.extension.type.Self
    ) -> builtins.str:
##
        '''
            Gueses the encoding used in current string. Encodings are checked
            in alphabetic order.
        '''
        if self.content:
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

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def camel_case_capitalize(self):
    def camel_case_capitalize(
        self: boostNode.extension.type.Self
    ) -> boostNode.extension.type.Self:
##
        '''
            Acts like pythons native "builtins.str.capitalize()" method but
            preserves camel case characters.
        '''
        if self.content:
            self.content = self.content[0].upper() + self.content[1:]
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def find_python_code_end_bracket(self):
    def find_python_code_end_bracket(
        self: boostNode.extension.type.Self
    ) -> (builtins.int, builtins.bool):
##
        '''
            Searches for the next not escaped closeing end bracked in current
            string interpreted as python code.
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

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def replace(self, search, replace='', *arguments, **keywords):
    def replace(
        self: boostNode.extension.type.Self,
        search: (builtins.str, builtins.dict),
        replace='', *arguments, **keywords
    ) -> boostNode.extension.type.Self:
##
        '''
            Implements the pythons native string method "str.replace()" in an
            object orientated way. This method serves additionally dictionaries
            as "search" parameter for multiple replacements. If you use
            dictionaries, the second parameter "replace" becomes useless.

            Return a copy of the string with all occurrences of substring old
            replaced by new. If an optional argument count is given, only the
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

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def sub(self, search, replace='', *arguments, **keywords):
    def sub(
        self: boostNode.extension.type.Self, search: builtins.str,
        replace='', *arguments, **keywords
    ) -> boostNode.extension.type.Self:
##
        '''
            Implements the pythons native "re.sub()" method in an object
            oriented way. This method serves additionally dictionaries
            as "search" parameter for multiple replacements. If you use
            dictionaries, the second parameter "replace" becomes useless.

            Return the string obtained by replacing the leftmost
            non-overlapping occurrences of pattern in string by the
            replacement "replace". If the pattern isn’t found, string is
            returned unchanged. "replace" can be a string or a function;

            If "replace" is a string, any backslash escapes in it are
            processed.
            That means "\n" is converted to a single newline character,
            "\r" is converted to a linefeed, and so forth. Unknown
            escapes such as "\j" are left alone. Backreferences, such as "\6",
            are replaced with the substring matched by group 6 in the pattern.

            If "replace" is a function, it is called for every non-overlapping
            occurrence of pattern. The function takes a single match object
            argument, and returns the replacement string.

            The pattern may be a string or an RE object.
            The optional argument count is the maximum number of pattern
            occurrences to be replaced; count must be a non-negative integer.
            If omitted or zero, all occurrences will be replaced. Empty
            matches for the pattern are replaced only when not adjacent to a
            previous match, so sub('x*', '-', 'abc') returns '-a-b-c-'.

            In addition to character escapes and backreferences as described
            above, "\g<name>" will use the substring matched by the group
            named name, as defined by the "(?P<name>...)" syntax. "\g<number>"
            uses the corresponding group number; "\g<2>" is therefore
            equivalent to "\2", but isn’t ambiguous in a replacement such as
            "\g<2>0". "\20" would be interpreted as a reference to group 20,
            not a reference to group 2 followed by the literal character "0".
            The backreference "\g<0>" substitutes in the entire substring
            matched by the RE.

            Examples:

            >>> String('hans').sub('([^a]+)', ' jau-suffix ')
            Object of "String" with " jau-suffix a jau-suffix " saved.

            >>> String('hans').sub('n', 'l')
            Object of "String" with "hals" saved.

            >>> String().sub('n', 'l').content
            ''

            >>> String('hans').sub('hans', 'peter').content
            'peter'
        '''
        if builtins.isinstance(search, builtins.dict):
            for search_string, replacement in search.items():
                '''
                    Take this method name via introspection.
                '''
                self.content = builtins.getattr(
                    self, inspect.stack()[0][3]
                )(
                    builtins.str(search_string), builtins.str(replacement),
                    *arguments, **keywords)
        else:
            '''
                Take this method name from regex object via introspection.
            '''
            self.content = builtins.getattr(
                re.compile(builtins.str(search)),
                inspect.stack()[0][3]
            )(builtins.str(replace), self.content, *arguments, **keywords)
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def subn(self, search, replace='', *arguments, **keywords):
    def subn(
        self: boostNode.extension.type.Self, search: builtins.str,
        replace='', *arguments, **keywords
    ) -> builtins.tuple:
##
        '''
            Implements the pythons native "re.subn()" method in an object
            oriented way. This method serves additionally dictionaries
            as "search" parameter for multiple replacements. If you use
            dictionaries, the second parameter "replace" becomes useless.

            Perform the same operation as "self.sub()", but returns a tuple:
            ("new_string", "number_of_subs_made"").
        '''
        if builtins.isinstance(search, builtins.dict):
            number_of_replaces = 0
            for search_string, replacement in search.items():
                self.content, temp_number_of_replaces = builtins.getattr(
                    self, inspect.stack()[0][3]
                )(builtins.str(search_string), builtins.str(replacement),
                  *arguments, **keywords)
                number_of_replaces += temp_number_of_replaces
        else:
            self.content, number_of_replaces = builtins.getattr(
                re.compile(builtins.str(search)),
                inspect.stack()[0][3]
            )(builtins.str(replace), self.content, *arguments, **keywords)
        return (self, number_of_replaces)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def readline(self):
    def readline(
        self: boostNode.extension.type.Self
    ) -> (boostNode.extension.type.SelfClassObject, builtins.bool):
##
        '''
            Implements the pythons native "bz2.BZ2File.readline()" method in an
            object oriented way.

            Return the next line from the string, as a string object, retaining
            newline.

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

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def readlines(self, *arguments, **keywords):
    def readlines(
        self: boostNode.extension.type.Self, *arguments: builtins.object,
        **keywords: builtins.object
    ) -> builtins.list:
##
        '''
            Implements the pythons native "builtins.str.splitlines()" method in
            an object oriented way.

            Return a list of all lines in a string, breaking at line
            boundaries. Line breaks are not included in the resulting list
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

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def delete_variables_from_regex(self):
    def delete_variables_from_regex(
        self: boostNode.extension.type.Self
    ) -> boostNode.extension.type.Self:
##
        '''
            Removes python supported varibales in regex strings.
            This method is useful if apython regex should be given to another
            regex engine which doesn't support variables.

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

        # region protected methods

            # region find python code end brackted helper methods

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def _handle_char_to_find_end_bracket(
##         self, index, char, quote, skip, brackets
##     ):
    def _handle_char_to_find_end_bracket(
        self: boostNode.extension.type.Self, index: builtins.int,
        char: builtins.str, quote: (builtins.str, builtins.bool),
        skip: builtins.int, brackets: builtins.int
    ) -> (builtins.tuple, builtins.int):
##
        '''
            Helper method for "self.find_python_code_end_bracket()".
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
            '''Handle openening brackets.'''
            brackets += 1
        return index + 1, char, quote, skip, brackets

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def _handle_start_quotes_to_find_end_bracket(
##         self, index, char, quote, skip
##     ):
    def _handle_start_quotes_to_find_end_bracket(
        self: boostNode.extension.type.Self, index: builtins.int,
        char: builtins.str, quote: (builtins.str, builtins.bool),
        skip: builtins.int
    ) -> builtins.tuple:
##
        '''
            Helper method for "self.find_python_code_end_bracket()".
        '''
        if self.content[index:index + 3] == 3 * char:
            quote = char * 3
            skip = 2
        else:
            quote = char
        return quote, skip

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def _handle_quotes_to_find_end_bracket(self, index, char, quote, skip):
    def _handle_quotes_to_find_end_bracket(
        self: boostNode.extension.type.Self, index: builtins.int,
        char: builtins.str, quote: (builtins.str, builtins.bool),
        skip: builtins.int
    ) -> builtins.tuple:
##
        '''
            Helper method for "self.find_python_code_end_bracket()".
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
    '''
        This class extends the native dictionary object.
    '''

    # region dynamic properties

        # region public properties

    '''The main property. It saves the current dictionary.'''
    content = {}

        # endregion

    # endregion

    # region dynamic methods

        # region public methods

            # region special methods

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def __init__(self, content):
    def __init__(
        self: boostNode.extension.type.Self, content: collections.Iterable
    ) -> None:
##
        '''
            Generates a new high level wrapper around given object.

            Examples:

            >>> Dictionary((('hans', 5), (4, 3))) # doctest: +ELLIPSIS
            Object of "Dictionary" (...hans...5...).
        '''
        self.content = builtins.dict(content)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def __repr__(self):
    def __repr__(self: boostNode.extension.type.Self) -> builtins.str:
##
        '''
            Invokes if this object should describe itself by a string.
        '''
        return 'Object of "{class_name}" ({content}).'.format(
            class_name=self.__class__.__name__,
            content=builtins.repr(self.content))

            # endregion

    @boostNode.paradigm.aspectOrientation.JointPoint
## python2.7
##     def pop(self, name, default_value=None):
    def pop(
        self: boostNode.extension.type.Self, name: builtins.str,
        default_value=None
    ) -> builtins.tuple:
##
        '''
            Get a keyword element as it would be set by a default value.
            If name is present in current saved dictionary its value will be
            returned in a tuple with currently saved dictionary.
            The corresponding data will be erased from dictionary.

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

    # endregion


class Module(Object):
    '''
        This class add some features for dealing with modules.
    '''

    # region constant properties

         # region public properties

## python2.7
##     HIDDEN_BUILTIN_CALLABLES = (
##         'GFileDescriptorBased', 'GInitiallyUnowned', 'GPollableInputStream',
##         'GPollableOutputStream')
    HIDDEN_BUILTIN_CALLABLES = ()
##
    PREFERED_ENTRY_POINT_FUNCTION_NAMES = (
        'main', 'init', 'initialize', 'run', 'start')

         # endregion

    # endregion

    # region dynamic properties

        # region protected properties

    _context_path = _name = _package_name = _file_path = ''

        # endregion

    # endregion

    # region static methods

        # region public methods

            # region special methods

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python2.7
##     def __repr__(cls):
    def __repr__(cls: boostNode.extension.type.SelfClass) -> builtins.str:
##
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

            # region getter methods

    @builtins.classmethod
## python2.7
##     def get_context_path(cls, path=None, frame=inspect.currentframe()):
    def get_context_path(
        cls: boostNode.extension.type.SelfClass,
        frame=inspect.currentframe(), path=None
    ) -> builtins.str:
##
        '''
            Determines the package and module level context path to a given
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
        cls._context_path = os.path.basename(path)
        if '.' in cls._context_path:
            cls._context_path = cls._context_path[:cls._context_path.rfind(
                '.')]
        while cls.is_package(path=path[:path.rfind(os.sep)]):
            path = path[:path.rfind(os.sep)]
            cls._context_path = os.path.basename(path) + '.' +\
                cls._context_path
        return cls._context_path

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python2.7
##     def get_name(cls, frame=None, extension=False, path=False):
    def get_name(
        cls: boostNode.extension.type.SelfClass, frame=None,
        extension=False, path=False
    ) -> builtins.str:
##
        '''
            Returns name of the given context "frame". If no frame is defined
            this module's context will be selected.
            if "base" is set "True" the modules name is given back without any
            file extension.

            Examples:

            >>> Module.get_name(extension=True)
            'native.py'

            >>> Module.get_name(path=True) # doctest: +ELLIPSIS
            '...boostNode...extension...native'

            >>> Module.get_name(path=True, extension=True) # doctest: +ELLIPSIS
            '...boostNode...extension...native.py'
        '''
        if frame is None:
            frame = inspect.currentframe()
        '''
            NOTE: "must_exist" is necessary for supporting freezed executables.
        '''
        file = boostNode.extension.file.Handler(
            location=frame.f_code.co_filename, respect_root_path=False,
            must_exist=False)
        if not file:
            file = boostNode.extension.file.Handler(
                location=sys.argv[0], respect_root_path=False)
        if path and extension:
            return file.path
        if extension:
            return file.name
        if path:
            return file.directory_path + file.basename
        return file.basename

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python2.7
##     def get_package_name(cls, frame=inspect.currentframe(), path=False):
    def get_package_name(
        cls: boostNode.extension.type.SelfClass,
        frame=inspect.currentframe(), path=False
    ) -> builtins.str:
##
        '''
            Determines package context of given frame. If current context
            isn't in any package context an empty string is given back.

            Examples:

            >>> Module.get_package_name()
            'extension'

            >>> Module.get_package_name(path=True) # doctest: +ELLIPSIS
            '...boostNode...extension...'
        '''
        '''
            NOTE: "must_exist" is necessary for supporting freezed executables.
        '''
        file = boostNode.extension.file.Handler(
            location=frame.f_code.co_filename, respect_root_path=True,
            must_exist=False)
        if cls.is_package(path=file.directory_path):
            if path:
                return file.directory_path
            return boostNode.extension.file.Handler(
                location=file.directory_path
            ).name
        elif not file:
            fallback_location = boostNode.extension.file.Handler(
                location=sys.argv[0], respect_root_path=True)
            if path:
                return fallback_location.directory_path
            return boostNode.extension.file.Handler(
                location=fallback_location.directory_path
            ).name
        return ''

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python2.7
##     def get_file_path(
##         cls, context_path, only_source_files=False
##     ):
    def get_file_path(
        cls: boostNode.extension.type.SelfClass,
        context_path: builtins.str, only_source_files=False
    ) -> (builtins.str, builtins.bool):
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
        '''
        if context_path:
            for search_path in sys.path:
                location = boostNode.extension.file.Handler(
                    location=search_path, must_exist=False,
                    respect_root_path=False)
                if location.is_directory():
                    location = cls._search_library_file(
                        location, context_path, only_source_files)
                    if location:
                        return location
        return False

            # endregion

            # region boolean methods

    @builtins.classmethod
## python2.7
##     def is_package(cls, path):
    def is_package(
        cls: boostNode.extension.type.SelfClass, path: builtins.str
    ) -> builtins.bool:
##
        '''
            Checks if given location is pointed to a python package.
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

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python2.7
##     def determine_caller(cls, callable_objects, caller=None):
    def determine_caller(
        cls: boostNode.extension.type.SelfClass,
        callable_objects: collections.Iterable, caller=None
    ) -> (builtins.bool, builtins.str, builtins.type(None)):
##
        '''
            Searches for a useful caller object in given module objects via
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

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python2.7
##     def get_defined_callables(cls, scope, only_module_level=True):
    def get_defined_callables(
        cls: boostNode.extension.type.SelfClass,
        scope: (types.ModuleType, builtins.type, builtins.object),
        only_module_level=True
    ) -> builtins.list:
##
        '''
            Takes a module and gives a list of objects explicit defined in
            this module.

            Examples:

            >>> Module.get_defined_callables(
            ...     sys.modules['__main__']) # doctest: +ELLIPSIS
            [...'Module'...]

            >>> class A:
            ...     a = 'hans'
            ...     def b():
            ...         pass
            ...     def __A__():
            ...         pass
            >>> Module.get_defined_callables(A, only_module_level=False)
            ['b']
        '''
        callables = []
        for object_name in builtins.set(builtins.dir(scope)):
            object = builtins.getattr(scope, object_name)
            if builtins.isinstance(
                object, boostNode.paradigm.aspectOrientation.JointPoint
            ):
                object = object.function
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

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python2.7
##     def execute_program_for_modules(
##         cls, program_type, program, modules, arguments=(),
##         extension='py', delimiter=', ', log=True, **keywords
##     ):
    def execute_program_for_modules(
        cls: boostNode.extension.type.SelfClass,
        program_type: builtins.str, program: builtins.str,
        modules: collections.Iterable, arguments=(),
        extension='py', delimiter=', ', log=True, **keywords
    ) -> builtins.tuple:
##
        '''
            Runs a given program for every given module.
            Returns false if no modules were found or given programm isn't
            installed.

            Examples:

            >>> Module.execute_program_for_modules(
            ...     'linter', 'pyflakes', boostNode.extension.__all__
            ... ) # doctest: +SKIP
            [(..., ...), ...]

            >>> Module.execute_program_for_modules(
            ...     'program', 'not_existing', boostNode.extension.__all__,
            ...     error=False) # doctest: +ELLIPSIS
            ('', ...)
        '''
        results = []
        for module in modules:
            module_file = boostNode.extension.file.Handler(
                location=module + '.' + extension)
            results.append(boostNode.extension.system.Platform.run(
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

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python2.7
##     def extend(cls, name=__name__, frame=None, module=None):
    def extend(
        cls: boostNode.extension.type.SelfClass, name=__name__,
        frame=None, module=None
    ) -> builtins.dict:
##
        '''
            Extends a given scope of an module for useful things like own
            exception class, a logger instance, variable to indicate if module
            is running in test mode and a variable that saves the current
            module name.

            Returns a dictionary with new module's scope and module name.

            Examples:

            >>> Module.extend() # doctest: +ELLIPSIS
            {...native...}
            >>> __logger__ # doctest: +ELLIPSIS
            <logging.Logger object at 0x...>
            >>> __exception__ # doctest: +ELLIPSIS
            <class 'boostNode.extension.native.NativeError'>
            >>> __module_name__
            'native'

            >>> Module.extend(
            ...     __name__, module=sys.modules['doctest']
            ... ) # doctest: +ELLIPSIS
            {...'name': 'doctest'...}

            >>> Module.extend(
            ...     __name__, module=sys.modules['doctest'],
            ...     frame=inspect.currentframe()) # doctest: +SKIP
            {...'name': 'doctest'...}
        '''
        if module is None:
            module = sys.modules[name]
        else:
            name = module.__name__
        module.__logger__ = boostNode.extension.output.Logger.get(name)
        if not (builtins.hasattr(module, '__module_name__') and frame is None):
            module.__module_name__ = cls.get_name(frame)
        module_name = String(
            module.__module_name__
        ).camel_case_capitalize().content
        module.__exception__ = builtins.type(
            module_name + 'Error', (builtins.Exception,),
            {'__init__': lambda self, message,
                *arguments: builtins.Exception.__init__(
                    self, message % arguments
                ) if arguments else builtins.Exception.__init__(
                    self, message)})
        module.__test_mode__ = False
        module.__loaded__ = True
        module.__file_path__ = cls.get_name(frame, path=True, extension=True)
        return {'name': name, 'scope': module}

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python2.7
##     def default(
##         cls, name, frame, default_caller=None, caller_arguments=(),
##         caller_keywords={}
##     ):
    def default(
        cls: boostNode.extension.type.SelfClass, name: builtins.str,
        frame: types.FrameType, default_caller=None,
        caller_arguments=(), caller_keywords={}
    ) -> boostNode.extension.type.SelfClass:
##
        '''
            Serves a common way to extend a given module. The given module's
            scope will be extended and a common meta command line interface is
            provided to test or run objects in given module.

            Examples:

            >>> Module.default(
            ...     __name__, inspect.currentframe()) # doctest: +SKIP

            >>> Module.default(
            ...     __name__, inspect.currentframe(), default_caller='Main'
            ... ) # doctest: +SKIP
        '''
        boostNode.extension.system.CommandLine.generic_module_interface(
            module=cls.extend(name, frame),
            default_caller=default_caller, caller_arguments=caller_arguments,
            caller_keywords=caller_keywords)
        return cls

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python2.7
##     def default_package(
##         cls, name, frame, command_line_arguments=(), *arguments, **keywords
##     ):
    def default_package(
        cls: boostNode.extension.type.SelfClass, name: builtins.str,
        frame: types.FrameType, *arguments: builtins.object,
        **keywords: builtins.object
    ) -> (builtins.tuple, builtins.bool):
##
        '''
            Serves a common way to extend a given package. The given package's
            scope will be extended and a common meta command line interface is
            provided to test, lint or document modules.

            Examples:

            >>> Module.default_package(
            ...     'not_existing', inspect.currentframe()) # doctest: +SKIP
            False

            >>> Module.default_package(
            ...     'doctest', inspect.currentframe()) # doctest: +SKIP
            (True, Namespace(), '...')
        '''
        cls.extend(name, frame)
        return boostNode.extension.system.CommandLine\
            .generic_package_interface(
                name, frame, *arguments, **keywords)

        # endregion

        # region protected methods

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python2.7
##     def _search_library_file(
##         cls, location, context_path, only_source_files=False
##     ):
    def _search_library_file(
        cls: boostNode.extension.type.SelfClass,
        location: boostNode.extension.file.Handler,
        context_path: builtins.str, only_source_files: builtins.bool
    ) -> (builtins.str, builtins.bool):
##
        '''
            Searches for full path to a given context path in given locations.
        '''
        for sub_module in context_path.split('.'):
            found_last_sub_module = False
            for sub_location in location:
                if(sub_location.basename == sub_module and
                   not (only_source_files and
                        sub_location.extension == 'pyc')):
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

'''Resolve cyclic dependency issues.'''
boostNode.extension.dependent.Resolve(
    name=__name__, frame=inspect.currentframe(), default_caller=False)

# endregion
