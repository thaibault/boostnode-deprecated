#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# region header

'''
    This module provides classes to handle text-based files and string parsing.
'''

# # python3.4 pass
from __future__ import print_function

'''
    For conventions see "boostNode/__init__.py" on \
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

# # python3.4
# # import builtins
# # import collections
import __builtin__ as builtins
# #
from copy import copy, deepcopy
from datetime import datetime as DateTime
import time
import inspect
import json
import logging
import os
import re
import string as native_string
import sys
import traceback
# # python3.4 import urllib.request
import urllib

'''Make boostNode packages and modules importable via relative paths.'''
sys.path.append(os.path.abspath(sys.path[0] + 2 * (os.sep + '..')))

from boostNode.extension.file import Handler as FileHandler
from boostNode.extension.native import Dictionary, Module, \
    InstancePropertyInitializer, String
from boostNode.extension.output import Buffer, Print
from boostNode.extension.system import CommandLine, Runnable
# # python3.4 from boostNode.extension.type import Self, SelfClass
pass
from boostNode.paradigm.aspectOrientation import JointPoint
from boostNode.paradigm.objectOrientation import Class

# endregion


# region classes

class Parser(Class, Runnable):

    '''
        This class can parse a string or file to interpret it as template for \
        replacing containing placeholder and rendering embedded python script \
        snippets.

        NOTE: "(?s...)" and "(?m...)" is equivalent for regular expression \
        flag "re.DOTALL" and "re.MULTILINE". NOTE: This regular expression \
        patterns assumes that the delimiter has at least a length of two.

        **template**                              - A template string, path \
                                                    to template file or file \
                                                    object pointing to a \
                                                    template file.

        **cache_path**                            - Indicates weather to \
                                                    cache the compiled \
                                                    template in given path.

        **string**                                - Indicates weather \
                                                    "template" is a template \
                                                    string or file path.

        **file_encoding**                         - Encoding used for reading \
                                                    template file and writing \
                                                    rendered output.

        **placeholder_name_pattern**              - Regular expression \
                                                    pattern to specify a \
                                                    placeholder name format.

        **command_line_placeholder_name_pattern** - Regular expression to \
                                                    specify a placeholder \
                                                    name given via command \
                                                    line interface.

        **command_line_placeholder_pattern**      - Regular expression \
                                                    pattern to identify a \
                                                    placeholder value tuple \
                                                    in command line interface.

        **placeholder_pattern**                   - Pattern to specify a \
                                                    placeholder in template \
                                                    string.

        **template_pattern**                      - Regular expression to \
                                                    identify each template \
                                                    identify syntax.

        **native_template_pattern**               - Regular expression \
                                                    pattern to used for \
                                                    pythons native template \
                                                    engine.

        **left_code_delimiter**                   - Left code delimiter to \
                                                    identify a code starting \
                                                    point of a code line.

        **right_escaped**                         - Escape symbol to mask a \
                                                    delimiter symbol.

        **template_context_default_indent**       - Expected indention used \
                                                    for interpreting code \
                                                    blocks.

        **builtin_names**                         - A tuple of function and \
                                                    variables available in \
                                                    template engine.

        **pretty_indent**                         - Indicates if we should \
                                                    spend time on rendering \
                                                    pretty indented code in \
                                                    each case.

        Examples:

        >>> file = FileHandler(__test_folder__.path + '_run')
        >>> file.content = 'hans <%placeholder%>'
        >>> template = Parser(template=file)
        >>> template.substitute(placeholder='also hans')
        Object of "Parser" with template "hans <%placeholder%>".
        >>> template.output
        'hans also hans'

        >>> Parser(
        ...     "<% include('', **{})", string=True
        ... ).render() # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        boostNode.extension.native.TemplateError: Error with given template ...
    '''

    # region properties

    COMMAND_LINE_ARGUMENTS = (
        {'arguments': ('template',),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             # 'required': {
             #     'execute': '__initializer_default_value__ is None'},
             'help': 'Select a template file to execute.',
             # 'dest': 'template',
             'metavar': 'TEMPLATE'}},
        {'arguments': ('-s', '--string'),
         'keywords': {
             'action': 'store_true',
             'default': {'execute': '__initializer_default_value__'},
             'help': 'Determine if given template should be interpreted as '
                     'template or a file name pointing to a template file.',
             'dest': 'string'}},
        {'arguments': ('-u', '--cache-path'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Determines if a cached compiled version of template '
                     'should be saved in given path. This make sense for big '
                     'templates with more than 100 lines.',
             'dest': 'cache_path',
             'metavar': 'PATH'}},
        {'arguments': ('-w', '--full-caching'),
         'keywords': {
             'action': 'store_true',
             'default': {'execute': '__initializer_default_value__'},
             'help': 'Only takes affect if a cache path is provided. It '
                     'caches the complete template result. This makes sense '
                     "if given scope variables doesn't change very often.",
             'dest': 'full_caching'}},
        {'arguments': ('-y', '-propagate-full-caching'),
         'keywords': {
             'action': 'store_true',
             'default': {'execute': '__initializer_default_value__'},
             'help': 'Indicates if an activated full caching should be '
                     'propagated to nested template includes.',
             'dest': 'propagate_full_caching'}},
        {'arguments': ('-u', '--cache-path'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Determines if a cached compiled version of template '
                     'should be saved in given path.',
             'dest': 'cache_path',
             'metavar': 'PATH'}},
        {'arguments': ('-q', '--file-encoding'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': {
                 'execute': "'Defines the encoding of a given template file "
                            '''(default: "%s").' % '''
                            '__initializer_default_value__'},
             'dest': 'file_encoding',
             'metavar': 'ENCODING'}},
        {'arguments': ('-p', '--placeholder-name-pattern'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': {
                 'execute': "'Define the regular expression pattern of a "
                            '''template placeholder name (default: "%s").' %'''
                            " __initializer_default_value__.replace('%', "
                            "'%%')"},
             'dest': 'placeholder_name_pattern',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-o', '--command-line-placeholder-name-pattern'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': {
                 'execute': "'Define the regular expression pattern of a "
                            'template placeholder name given via the command '
                            '''line interface (default: "%s").' % '''
                            "__initializer_default_value__.replace('%', "
                            "'%%')"},
             'dest': 'command_line_placeholder_name_pattern',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-d', '--left-code-delimiter'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': {
                 'execute': "'Defines left delimiter for placeholder and code "
                            '''lines (default: "%s").' % '''
                            "__initializer_default_value__.replace('%', "
                            "'%%')"},
             'dest': 'left_code_delimiter',
             'metavar': 'STRING'}},
        {'arguments': ('-e', '--right-code-delimiter'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': {
                 'execute': "'Defines right delimiter for placeholder (default"
                            ''' "%s").' % '''
                            "__initializer_default_value__.replace('%', "
                            "'%%')"},
             'dest': 'right_code_delimiter',
             'metavar': 'STRING'}},
        {'arguments': ('-r', '--right-escaped'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': {
                 'execute': "'Defines the string which indicates on the right "
                            "side of a code delimiter that it shouldn\\'t be "
                            '''evaluated as code delimiter (default "%s").' '''
                            "% __initializer_default_value__.replace('%', "
                            "'%%')"},
             'dest': 'right_escaped',
             'metavar': 'STRING'}},
        {'arguments': ('-f', '--placeholder-pattern'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': {
                 'execute': "'Defines template placeholder pattern (default "
                            '''"%s").' % '''
                            "__initializer_default_value__.replace('%', "
                            "'%%')"},
             'dest': 'placeholder_pattern',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-j', '--template-context-default-indent'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': {
                 'execute': "'Defines default indents to define pythonic "
                            '''semantics (default "%d").' % '''
                            '__initializer_default_value__'},
             'dest': 'template_context_default_indent',
             'metavar': 'NUMBER'}},
        {'arguments': ('-a', '--template-pattern'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': {
                 'execute': "'Defines the general syntax of given template "
                            '''(default: "%s").' % '''
                            "__initializer_default_value__.replace('%', "
                            "'%%')"},
             'dest': 'template_pattern',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-i', '--command-line-placeholder-pattern'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': {
                 'execute': "'Defines the given placeholder pattern (default: "
                            '''"%s").' % '''
                            "__initializer_default_value__.replace('%', "
                            "'%%')"},
             'dest': 'command_line_placeholder_pattern',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-n', '--native-template-pattern'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': {
                 'execute': "'Defines template pattern for python\\'s "
                            '''native template engine (default: "%s").' % '''
                            "__initializer_default_value__.replace('%', "
                            "'%%')"},
             'dest': 'native_template_pattern',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-b', '--builtins'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': {
                 'execute': "'Defines which python native object should be "
                            "available in template scope (default: \"%s\").' %"
                            ' \'", "\'.join(map(lambda builtin: '
                            "builtin.__name__.replace('%', '%%'), "
                            '__initializer_default_value__))'},
             'dest': 'builtin_names',
             'metavar': 'BUILTIN'}},
        {'arguments': ('-g', '--scope-variables'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': (),
             'type': builtins.str,
             'required': False,
             'help': 'Select scope variables for the given template file.',
             'dest': 'scope_variables',
             'metavar': 'VARIABLES'}},
        {'arguments': ('-k', '--pretty-indent'),
         'keywords': {
             'action': 'store_true',
             'default': {'execute': '__initializer_default_value__'},
             'help': 'Spend time on generating right indented output.',
             'dest': 'pretty_indent'}})
    '''Holds all command line interface argument informations.'''
    PYTHON_CODE_TEMPLATE = (
        '#!/usr/bin/env python%d.%d\n# -*- coding: utf-8 -*-\n\n%%s' %
        sys.version_info[:2])
    '''
        Saves a generic python code template used for saving python code \
        caches.
    '''
    DEFAULT_FILE_EXTENSION_SUFFIX = 'tpl'
    '''Saves the default template file extension suffix.'''

    # endregion

    # region static methods

    # # region protected

    # # # region helper

    @JointPoint(builtins.classmethod)
# # python3.4
# #     def _render_none_code(
# #         cls: SelfClass, string: builtins.str, end='\n'
# #     ) -> builtins.str:
    def _render_none_code(cls, string, end='\n'):
# #
        '''
            Wraps a print function around plain text for compiling templates.

            Examples:

            >>> parser = Parser('', string=True)

            >>> parser._render_none_code('hans')
            "print('hans\\\\n', end='')\\n"

            >>> parser._render_none_code("ha'ns")
            'print("ha\\'ns\\\\n", end=\\'\\')\\n'

            >>> parser._render_none_code("""h'a"ns""")
            'print(\\'\\'\\'h\\'a"ns\\\\n\\'\\'\\', end=\\'\\')\\n'

            >>> parser._render_none_code("""h'a"n'\''s""")
            'print("""h\\'a"n\\'\\'\\'s\\\\n""", end=\\'\\')\\n'

            >>> parser._render_none_code('h"a\\'\\'\\'\\'n"""s')
            'print("""h"a\\'\\'\\'\\'n"\\\\""s\\\\n""", end=\\'\\')\\n'

            >>> parser._render_none_code("""'a"b'""")
            'print(\\'\\'\\'\\\\\\'a"b\\\\\\'\\\\n\\'\\'\\', end=\\'\\')\\n'
        '''
        delimiters = "'", '"', "'''", '"""'
        counter = 0
        delimiter = delimiters[0]
        while delimiter in string:
            counter += 1
            delimiter = delimiters[counter]
            if counter + 1 == builtins.len(delimiters):
                string = string.replace('"""', '"\\""')
                break
        '''
            Check if chosen delimiter collides with another delimiter like \
            """ + " at the string border.
        '''
        if string.startswith(delimiter[-1]):
            string = '\\' + string
        if string.endswith(delimiter[-1]):
            string = string[:-1] + '\\' + string[-1]
        return("print(%s, end='')\n" % (
            delimiter + string.replace('\n', '\\n') +
            end.replace('\n', '\\n') + delimiter))

        # # endregion

        # endregion

    # endregion

    # region dynamic methods

        # region public

        # # region special

    @JointPoint
# # python3.4     def __repr__(self: Self) -> builtins.str:
    def __repr__(self):
        '''
            Invokes if this object should describe itself by a string.

            Examples:

            >>> repr(Parser(template='test', string=True))
            'Object of "Parser" with template "test".'
        '''
        return 'Object of "{class_name}" with template "{template}".'.format(
            class_name=self.__class__.__name__, template=self.content)

    @JointPoint
# # python3.4     def __str__(self: Self) -> builtins.str:
    def __str__(self):
        '''
            Triggers if an instance is tried to be interpreted as a string.

            Examples:

            >>> str(Parser(template='hans', string=True))
            'hans'
        '''
        return self.content

    @JointPoint
# # python3.4     def __len__(self: Self) -> builtins.int:
    def __len__(self):
        '''
            Triggers if the pythons native "builtins.len()" function tries to \
            handle current instance. Returns the number of symbols given in \
            the current string representation of this object.

            Examples:

            >>> len(Parser(template='hans', string=True))
            4
        '''
        return builtins.len(self.__str__())

        # # endregion

        # # region getter

    @JointPoint
# # python3.4     def get_indent(self: Self) -> builtins.int:
    def get_indent(self):
        '''
            Returns a string of white spaces representing current context.

            Examples:

            >>> Parser('hans\\n<%__indent__ = 2\\npeter', string=True).indent
            2

            >>> Parser('hans\\n<% __indent__=8;peter', string=True).indent
            8
        '''
        if not self._indent and self.content:
            self._indent = self.template_context_default_indent
# # python3.4
# #             match = re.compile(
# #                 '(.*\n)?%s *__indent__ *= *'
# #                 '(?P<number_of_indents>[1-9][0-9]*) *(?:;+|\n).*' %
# #                 String(self.left_code_delimiter).validate_regex().content,
# #                 re.DOTALL
# #             ).fullmatch(self.content)
            match = re.compile(
                '(.*\n)?%s *__indent__ *= *'
                '(?P<number_of_indents>[1-9][0-9]*) *(?:;+|\n).*$' %
                String(self.left_code_delimiter).validate_regex().content,
                re.DOTALL
            ).match(self.content)
# #
            if match:
                self._indent = builtins.int(match.group('number_of_indents'))
        return self._indent

    @JointPoint
# # python3.4     def get_output(self: Self) -> builtins.str:
    def get_output(self):
        '''
            Gets the current output buffer. It consists everything printed \
            out in code snippets rendered by the template instance or exists \
            as plain text in given template.

            Examples:

            >>> Parser(
            ...     'klaus says\\n<% print("who is hans?")', string=True
            ... ).render().output
            'klaus says\\nwho is hans?\\n'
        '''
        return self._output.content

    @JointPoint
# # python3.4     def get_builtins(self: Self) -> builtins.dict:
    def get_builtins(self):
        '''
            Defines minimum needed native python features for each template \
            scope. It adds user-defined additionally python functions. The \
            minimum needed functions (e.g. "print()") will never be \
            overwritten.

            Examples:

            >>> template = Parser(template='hans', string=True)
            >>> template.builtins # doctest: +ELLIPSIS
            {...'print': ..._print...}
        '''
        now = DateTime.now()
# # python3.4
# #         self._builtins.update({
# #             '__indent__': self.indent, '__file__': self.file,
# #             '__time_stamp__': time.mktime(
# #                 now.timetuple()
# #             ) + now.microsecond / 1000 ** 2, 'DateTime': DateTime,
# #             'time': time, 'FileHandler': FileHandler, 'print': self._print,
# #             'include': self._include, 'String': builtins.str,
# #             'length': builtins.len, 'Json': json,
# #             'path_name_to_url': urllib.request.pathname2url,
# #             'false': False, 'true': True, 'locals': builtins.locals,
# #             'type': builtins.type, 'sort': builtins.sorted,
# #             'is_type_of': builtins.isinstance, 'Tuple': builtins.tuple,
# #             'Dictionary': builtins.dict, 'RegularExpression': re.compile,
# #             'copy': copy, 'deepCopy': deepcopy,
# #             'DictionaryExtension': Dictionary, 'StringExtension': String,
# #             'List': builtins.list, 'hasAttribute': builtins.hasattr})
        self._builtins.update({
            '__indent__': self.indent, '__file__': self.file,
            '__time_stamp__': time.mktime(
                now.timetuple()
            ) + now.microsecond / 1000 ** 2, 'DateTime': DateTime,
            'time': time, 'FileHandler': FileHandler, 'print': self._print,
            'include': self._include, 'String': builtins.str,
            'length': builtins.len, 'Json': json,
            'path_name_to_url': urllib.pathname2url, 'false': False,
            'true': True, 'locals': builtins.locals, 'type': builtins.type,
            'sort': builtins.sorted, 'is_type_of': builtins.isinstance,
            'Tuple': builtins.tuple, 'Dictionary': builtins.dict,
            'RegularExpression': re.compile, 'copy': copy,
            'deepCopy': deepcopy, 'DictionaryExtension': Dictionary,
            'StringExtension': String, 'List': builtins.list,
            'hasAttribute': builtins.hasattr})
# #
        return self._builtins

        # # endregion

        # # region wrapper

    @JointPoint
# # python3.4
# #     def substitute(
# #         self: Self, *arguments: builtins.str, **keywords: builtins.object
# #     ) -> Self:
    def substitute(self, *arguments, **keywords):
# #
        '''
            Wrapper method for pythons native "string.Template.substitute()" \
            method.

            Arguments and keywords are forwarded to pythons native \
            "string.Template.substitute()" method.

            Examples:

            >>> template = Parser(
            ...     template='hans <%placeholder%>', string=True)
            >>> template.substitute(placeholder='also hans')
            Object of "Parser" with template "hans <%placeholder%>".
            >>> template.output
            'hans also hans'

            >>> template = Parser(template='hans', string=True)
            >>> template.substitute()
            Object of "Parser" with template "hans".
            >>> template.output
            'hans'

            >>> template = Parser(template='hans <%not_hans%>', string=True)
            >>> template.substitute()
            Traceback (most recent call last):
            ...
            KeyError: 'not_hans'
        '''
        self._output.write(self.native_template_object.substitute(
            *arguments, **keywords))
        return self

    @JointPoint
# # python3.4
# #     def safe_substitute(
# #         self: Self, *arguments: builtins.str, **keywords: builtins.object
# #     ) -> Self:
    def safe_substitute(self, *arguments, **keywords):
# #
        '''
            Wrapper method for pythons native \
            "string.Template.safe_substitute()" method.

            Arguments and keywords are forwarded to pythons native \
            "string.Template.safe_substitute()" method.

            Examples:

            >>> template = Parser(template='hans <%placeholder%>', string=True)
            >>> template.safe_substitute(placeholder='also hans')
            Object of "Parser" with template "hans <%placeholder%>".
            >>> template.output
            'hans also hans'

            >>> template = Parser(template='hans', string=True)
            >>> template.safe_substitute()
            Object of "Parser" with template "hans".

            >>> template = Parser(template='hans <%not_hans%>', string=True)
            >>> template.safe_substitute()
            Object of "Parser" with template "hans <%not_hans%>".
        '''
# # python3.4
# #         self._output.write(self.native_template_object.safe_substitute(
# #             *arguments, **keywords))
        def substitute(match):
            '''
                Substitution replacement for native pendant with no \
                exception raising.
            '''
            if match.group('variable_name') in keywords:
                return builtins.str(
                    keywords[match.group('variable_name')])
            return match.group(0)
        self._output.write(re.compile(self.placeholder_pattern.format(
            left_delimiter=self.left_code_delimiter,
            right_delimiter=self.right_code_delimiter,
            placeholder=self.placeholder_name_pattern)
        ).sub(substitute, self.content))
# #
        return self

        # # endregion

        # # region parsing

    @JointPoint
# # python3.4     def substitute_all(self: Self, replacement='') -> Self:
    def substitute_all(self, replacement=''):
        '''
            Substitutes every placeholder in template with a given \
            replacement string.

            **replacement** - String to replace with every placeholder.

            Examples:

            >>> template = Parser(
            ...     template='test <%hans%> <%a%> <%b%>', string=True)
            >>> template.substitute_all().output
            'test   '

            >>> template = Parser(
            ...     template='test <%hans%> <%a%> <%b%>', string=True)
            >>> template.substitute_all(replacement='hans').output
            'test hans hans hans'
        '''
        self._output.write(re.compile(self.placeholder_pattern.format(
            left_delimiter=self.left_code_delimiter,
            right_delimiter=self.right_code_delimiter,
            placeholder=self.placeholder_name_pattern)
        ).sub(replacement, self.content))
        return self

    @JointPoint
# # python3.4
# #     def render(
# #         self: Self, mapping={}, prevent_rendered_python_code=False,
# #         **keywords: builtins.object
# #     ) -> Self:
    def render(
        self, mapping={}, prevent_rendered_python_code=False, **keywords
    ):
# #
        '''
            Renders the template. Searches for python code snippets and \
            handles correct indenting. Wraps plain text with a print function.

            **mapping** - A dictionary containing a mapping from placeholder \
                          name to value.

            Additional keywords are used as additional mapping tuples.

            Examples:

            >>> Parser(
            ...     'hans says\\n<% print("who the fu.. is hans?")',
            ...     string=True
            ... ).render() # doctest: +ELLIPSIS
            Object of "Parser" with template "hans says...who the fu.. is ha...

            >>> Parser(
            ...     'hans says\\n<% print("who the fu.. is hans?")',
            ...     string=True, cache_path=__test_folder__
            ... ).render() # doctest: +ELLIPSIS
            Object of "Parser" with template "hans says...who the fu.. is ha...

            >>> Parser(
            ...     'hans says\\n<% print("who the fu.. is hans?")',
            ...     string=True, cache_path=__test_folder__
            ... ).render() # doctest: +ELLIPSIS
            Object of "Parser" with template "hans says...who the fu.. is ha...

            >>> Parser(
            ...     'hans says\\n<% print("who the fu.. is hans?")',
            ...     string=True, cache_path=__test_folder__, full_caching=True
            ... ).render() # doctest: +ELLIPSIS
            Object of "Parser" with template "hans says...who the fu.. is ha...

            >>> Parser(
            ...     'hans says\\n<% print("who the fu.. is hans?")',
            ...     string=True, cache_path=__test_folder__, full_caching=True
            ... ).render() # doctest: +ELLIPSIS
            Object of "Parser" with template "hans says...who the fu.. is ha...

            >>> file = FileHandler(__test_folder__.path + 'render')
            >>> file.content = 'hans says\\n<% print("who the fu.. is hans?")'
            >>> Parser(
            ...     file, cache_path=__test_folder__, full_caching=True
            ... ).render() # doctest: +ELLIPSIS
            Object of "Parser" with template "hans says...who the fu.. is ha...

            >>> Parser(
            ...     'hans says\\n<% end', string=True
            ... ).render() # doctest: +ELLIPSIS
            Object of "Parser" with template "hans says...<% end...
        '''
        mapping = copy(mapping)
        mapping.update({'__builtins__': self.builtins})
        mapping.update(keywords)
        if self.cache:
            if self.string:
                template_hash = builtins.str(builtins.hash(self.content))
            else:
                template_hash = self.file.path.replace(os.sep, '_')
            if self.full_caching:
                full_cache_file = FileHandler(
                    location='%s/%s.txt' % (
                        FileHandler(
                            location=self.cache.path + template_hash,
                            make_directory=True
                        ).path, builtins.str(
                            builtins.hash(Dictionary(
                                content=mapping
                            ).get_immutable(exclude=('include', 'print'))))))
                if full_cache_file:
                    self._output.write(full_cache_file.content)
                    return self
            cache_file = FileHandler(
                location='%s%s.py' % (self.cache.path, template_hash))
            if cache_file:
                self.rendered_python_code = cache_file.content[builtins.len(
                    self.PYTHON_CODE_TEMPLATE) - builtins.len('%s'):]
            else:
                self.rendered_python_code = self._render_content()
                cache_file.content = self.PYTHON_CODE_TEMPLATE % \
                    self.rendered_python_code
            self._run_template(
                prevent_rendered_python_code, template_scope=mapping)
            if self.full_caching:
                full_cache_file.content = self.output
        else:
            self.rendered_python_code = self._render_content()
            self._run_template(
                prevent_rendered_python_code, template_scope=mapping)
        return self

    @JointPoint
# # python3.4
# #     def represent_rendered_python_code(self: Self) -> builtins.str:
    def represent_rendered_python_code(self):
# #
        '''
            This method adds line numbers to rendered contend which is \
            visible if an template exception occurs in debug mode. Code \
            representation is returned as string.

            Examples:

            >>> Parser('', string=True).represent_rendered_python_code()
            ''

            >>> Parser('', string=True).render(
            ... ).represent_rendered_python_code()
            ''

            >>> Parser('klaus', string=True).render(
            ... ).represent_rendered_python_code() # doctest: +ELLIPSIS
            "\\nrendered python code...-\\n\\n1 | print('klaus', end='')\\n"
        '''
        self._number_of_rendered_python_code_lines = builtins.len(
            String(self.rendered_python_code).readlines())

        @JointPoint
# # python3.4
# #         def replace_rendered_python_code_line(
# #             match: builtins.type(re.compile('').match(''))
# #         ) -> builtins.str:
        def replace_rendered_python_code_line(match):
# #
            '''
                Prepends a line numbers to given line matching object of \
                rendered python code.
            '''
            self._current_rendered_python_code_line_number += 1
            number_of_whitspaces = builtins.len(builtins.str(
                self._number_of_rendered_python_code_lines)
            ) - builtins.len(builtins.str(
                self._current_rendered_python_code_line_number))
            return number_of_whitspaces * ' ' + builtins.str(
                self._current_rendered_python_code_line_number
            ) + ' | ' + match.group('line')
        if self._number_of_rendered_python_code_lines:
            headline = 'rendered python code of %s:' % (
                self._determine_template_description())
            return('\n%s\n%s\n\n%s\n' % (
                headline, builtins.len(headline) * '-', re.compile(
                    '^(?P<line>.*)$', re.MULTILINE
                ).sub(
                    replace_rendered_python_code_line,
                    self.rendered_python_code)))
        return ''

        # # endregion

        # endregion

        # region protected

        # # region runnable implementation

    @JointPoint
# # python3.4     def _run(self: Self) -> Self:
    def _run(self):
        '''
            Entry point for command line call of this program. Loads the \
            given template. If it is given by the command line it will be \
            interpreted directly.

            Examples:

            >>> sys_argv_backup = sys.argv

            >>> sys.argv[1:] = ['hans', '--string']
            >>> Parser.run()
            Object of "Parser" with template "hans".

            >>> sys.argv[1:] = ['repr(hans)', '--string', '--builtins', 'repr']
            >>> Parser.run()
            Object of "Parser" with template "repr(hans)".

            >>> sys.argv = sys_argv_backup
        '''
        '''Holds a name space of every argument given by the command line.'''
        self._command_line_arguments = CommandLine.argument_parser(
            arguments=self.COMMAND_LINE_ARGUMENTS, module_name=__name__,
            scope={'self': self})
        initializer_arguments = self._command_line_arguments_to_dictionary(
            namespace=self._command_line_arguments)
        if(initializer_arguments['builtin_names'] and
           builtins.isinstance(
               initializer_arguments['builtin_names'][0], builtins.str)):
            initializer_arguments['builtin_names'] = builtins.tuple(
                builtins.map(
                    lambda builtin: builtins.eval(builtin),
                    initializer_arguments['builtin_names']))
        self._initialize(**initializer_arguments).render(
            **self._generate_scope_variables())
        Print(self.output)
        return self

    @JointPoint(InstancePropertyInitializer)
# # python3.4
# #     def _initialize(
# #         self: Self, template: (builtins.str, FileHandler), string=None,
# #         cache_path=None, full_caching=False, propagate_full_caching=False,
# #         file_encoding=FileHandler.DEFAULT_ENCODING,
# #         placeholder_name_pattern='[a-zA-Z0-9_\[\]\'"\.()\\\\,\-+ :/={}$]+',
# #         command_line_placeholder_name_pattern='(?s)'
# #                                               '[a-zA-Z0-9_\[\]\.(),\-+]+',
# #         command_line_placeholder_pattern=(
# #             '^(?P<variable_name>{placeholder})'
# #             '(?P<separator>.)(?P<value>.*)'),
# #         placeholder_pattern='{left_delimiter}[ \t]*'
# #                             '(?P<variable_name>{placeholder})'
# #                             '[ \t]*{right_delimiter}',
# #         template_pattern='(?m)(?P<ESCAPED_DELIMITER>'
# #                          '(?P<before_escaped>'  # in brackets
# #                          '(?P<indent_escaped>[ \t]*)'  # in two brackets
# #                          '(?!{left_delimiter})'  # in two brackets
# #                          '(?:.(?!{left_delimiter}))*?.?'  # in two brackets
# #                          ')?{left_delimiter}{right_escaped}'  # in brackets
# #                          '(?P<after_escaped>\n?)'  # in brackets
# #                          ')|(?P<PLACEHOLDER>'
# #                          '(?P<before_placeholder>'  # in brackets
# #                          '(?P<indent_placeholder>'  # in two brackets
# #                          '[ \t]*)'  # in two brackets
# #                          '(?!{left_delimiter})'  # in two brackets
# #                          '(?:.(?!{left_delimiter}))*?.?'  # in two brackets
# #                          ')?{left_delimiter}[ \t]*'  # in brackets
# #                          '(?P<placeholder>{placeholder})'  # in brackets
# #                          '[ \t]*'  # in brackets
# #                          '{right_delimiter}'  # in brackets
# #                          '(?P<after_placeholder>\n?)'  # in brackets
# #                          ')|(?P<CODE>'
# #                          '^(?P<indent_code>[ \t]*)'  # in brackets
# #                          '{left_delimiter}'  # in brackets
# #                          '(?P<code>.+)$'  # in brackets
# #                          ')|(?P<NONE_CODE>'
# #                          '(?P<none_code>'  # in brackets
# #                          '(?P<indent_none_code>'  # in two brackets
# #                          '[ \t]*'
# #                          ').+'  # in two brackets
# #                          ')'  # in brackets
# #                          '(?P<after_none_code>\n|$)'  # in brackets
# #                          ')|(?P<EMPTY_LINE>^(?P<indent_line>[ \t]*)\n)',
# #         native_template_pattern='<%[ \t]*(?:'
# #                                 '(?P<escaped>%)|'  # in brackets
# #                                 '(?:(?P<named>'  # in brackets
# #                                 '[a-zA-Z0-9_]+)'  # in brackets
# #                                 '[ \t]*% >)|'  # in two brackets
# #                                 '(?:'  # in brackets
# #                                 '(?P<braced>'  # in two brackets
# #                                 '[a-zA-Z0-9_]+)'  # in tree brackets
# #                                 '[ \t]*%>)|'  # in two brackets
# #                                 '(?P<invalid>)'  # in brackets
# #                                 ')',
# #         left_code_delimiter='<%', right_code_delimiter='%>',
# #         right_escaped='%',  # For example: "<%%" evaluates to "<%"
# #         template_context_default_indent=4,
# #         builtin_names=(builtins.all, builtins.filter, builtins.map,
# #                        builtins.enumerate, builtins.range),
# #         pretty_indent=False, **keywords: builtins.object
# #     ) -> Self:
    def _initialize(
        self, template, string=None, cache_path=None, full_caching=False,
        propagate_full_caching=False,
        file_encoding=FileHandler.DEFAULT_ENCODING,
        placeholder_name_pattern='[a-zA-Z0-9_\[\]\'"\.()\\\\,\-+ :/={}$]+',
        command_line_placeholder_name_pattern='(?s)'
                                              '[a-zA-Z0-9_\[\]\.(),\-+]+',
        command_line_placeholder_pattern='^(?P<variable_name>'
                                         '{placeholder})'
                                         '(?P<separator>.)(?P<value>.*)',
        placeholder_pattern='{left_delimiter}[ \t]*'
                            '(?P<variable_name>{placeholder})[ \t]'
                            '*{right_delimiter}',
        template_pattern='(?m)(?P<ESCAPED_DELIMITER>'
                         '(?P<before_escaped>'  # in brackets
                         '(?P<indent_escaped>[ \t]*)'  # in two brackets
                         '(?!{left_delimiter})'  # in two brackets
                         '(?:.(?!{left_delimiter}))*?.?'  # in two brackets
                         ')?{left_delimiter}{right_escaped}'  # in brackets
                         '(?P<after_escaped>\n?)'  # in brackets
                         ')|(?P<PLACEHOLDER>'
                         '(?P<before_placeholder>'  # in brackets
                         '(?P<indent_placeholder>'  # in two brackets
                         '[ \t]*)'  # in two brackets
                         '(?!{left_delimiter})'  # in two brackets
                         '(?:.(?!{left_delimiter}))*?.?'  # in two brackets
                         ')?{left_delimiter}[ \t]*'  # in brackets
                         '(?P<placeholder>{placeholder})'  # in brackets
                         '[ \t]*'  # in brackets
                         '{right_delimiter}'  # in brackets
                         '(?P<after_placeholder>\n?)'  # in brackets
                         ')|(?P<CODE>'
                         '^(?P<indent_code>[ \t]*)'  # in brackets
                         '{left_delimiter}'  # in brackets
                         '(?P<code>.+)$'  # in brackets
                         ')|(?P<NONE_CODE>'
                         '(?P<none_code>'  # in brackets
                         '(?P<indent_none_code>'  # in two brackets
                         '[ \t]*'
                         ').+'  # in two brackets
                         ')'  # in brackets
                         '(?P<after_none_code>\n|$)'  # in brackets
                         ')|(?P<EMPTY_LINE>^(?P<indent_line>[ \t]*)\n)',
        native_template_pattern='<%[ \t]*(?:'
                                '(?P<escaped>%)|'  # in brackets
                                '(?:(?P<named>'  # in brackets
                                '[a-zA-Z0-9_]+)'  # in brackets
                                '[ \t]*% >)|'  # in two brackets
                                '(?:'  # in brackets
                                '(?P<braced>'  # in two brackets
                                '[a-zA-Z0-9_]+)'  # in tree brackets
                                '[ \t]*%>)|'  # in two brackets
                                '(?P<invalid>)'  # in brackets
                                ')',
        left_code_delimiter='<%', right_code_delimiter='%>',
        right_escaped='%',  # For example: "<%%" evaluates to "<%"
        template_context_default_indent=4,
        builtin_names=(builtins.all, builtins.filter, builtins.map,
                       builtins.enumerate, builtins.range),
        pretty_indent=False, **keywords
    ):
# #
        '''Initializes output buffer and template scope.'''

        # # # region properties

        '''Holds the given template as string.'''
        self.content = ''
        '''
            Holds the given template as rendered (runnable python code) string.
        '''
        self.rendered_python_code = ''
        '''Template file handler.'''
        self.file = None
        '''Indicates if last rendered code snippet was a full line.'''
        self._new_line = True
        '''
            Holds number of white spaces to indent a context dependent code \
            block in templates.
        '''
        self._indent = 0
        '''Holds the number of lines in generated python code.'''
        self._number_of_generated_lines = 0
        '''
            Holds the number of lines which will be generated in python code \
            but doesn't occur in template code.
        '''
        self._number_of_generated_phantom_lines = 0
        '''
            Saves the number of logical python code indents to distinguish \
            between style indents and logical indents.
        '''
        self._code_dependent_indents = []
        '''
            A list of tuples holding the number of generated python code \
            lines and the number of generated phantom python code lines which \
            doesn't appear in template source code.
        '''
        self._line_shifts = []
        '''
            Buffers empty lines by parsing template source code. The list is \
            used as queue. Empty lines will be written finally to compiled \
            source code if there dependence membership is resolved.
        '''
        self._empty_lines = []
        '''
            Saves needed informations give a line number to each rendered \
            content.
        '''
        self._current_rendered_python_code_line_number = 0
        self._number_of_rendered_python_code_lines = 0
        '''Saves the output of running executed template.'''
        self._output = Buffer()
        '''
            Holds a mapping from available builtin names and their references \
            in template scope.
        '''
        self._builtins = {}
        '''Saves a rendered python code for caching.'''
        self.cache = None
        if self.cache_path:
            self.cache = FileHandler(
                location=self.cache_path, make_directory=True)

        # # # endregion

        return self._set_builtins(self.builtin_names)._load_template()

        # # endregion

    @JointPoint
# # python3.4     def _render_content(self: Self) -> builtins.str:
    def _render_content(self):
        '''Generates runnable python code from current template.'''
        return re.compile(
            self.template_pattern.format(
                left_delimiter=String(
                    self.left_code_delimiter
                ).validate_regex(),
                right_delimiter=String(
                    self.right_code_delimiter
                ).validate_regex(),
                placeholder=self.placeholder_name_pattern,
                right_escaped=self.right_escaped)
        ).sub(self._render_code, self.content).strip()

    @JointPoint
# # python3.4
# #     def _set_builtins(
# #         self: Self, builtins: collections.Iterable
# #     ) -> Self:
    def _set_builtins(self, builtins):
# #
        '''
            Generates a dictionary representing the templates scope from \
            given defined builtins.
        '''
        for builtin in builtins:
            self._builtins[builtin.__name__] = builtin
        return self

    @JointPoint
# # python3.4     def _generate_scope_variables(self: Self) -> builtins.dict:
    def _generate_scope_variables(self):
        '''
            Generates scope variables given by the command line interface and \
            embeds them into the template.

            Examples:

            >>> import argparse

            >>> parser = Parser(template='hans', string=True)
            >>> parser._command_line_arguments = argparse.Namespace(
            ...     scope_variables=('hans=peter', 'peter=hans'))
            >>> parser._generate_scope_variables() # doctest: +ELLIPSIS
            {...'hans': 'peter'...}

            >>> parser._command_line_arguments = argparse.Namespace(
            ...     scope_variables=('a',))
            >>> parser._generate_scope_variables(
            ... ) # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            TemplateError: Given placeholder value tuple "a" couldn't be ...

            >>> parser._command_line_arguments = argparse.Namespace(
            ...     scope_variables=('ab',))
            >>> parser._generate_scope_variables(
            ... ) # doctest: +IGNORE_EXCEPTION_DETAIL
            {'a': ''}
        '''
        keywords = {}
        for variable in self._command_line_arguments.scope_variables:
            pattern = self.command_line_placeholder_pattern.format(
                placeholder=self.command_line_placeholder_name_pattern)
# # python3.4
# #             match = re.compile(pattern).fullmatch(variable)
            match = re.compile('(?:%s)$' % pattern).match(variable)
# #
            if match:
                keywords.update(
                    {match.group('variable_name'): match.group('value')})
            else:
                raise __exception__(
                    'Given placeholder value tuple "%s" couldn\'t be parsed. '
                    'Your string have to match "%s".', variable, pattern)
        return keywords

    @JointPoint
# # python3.4     def _load_template(self: Self) -> Self:
    def _load_template(self):
        '''
            Load the given template into ram for rendering.

            **template**  - the given template as file path or string.

            **is_string** - determines if the "template" should be \
                            interpreted as string or file path.

            Examples:

            >>> file = FileHandler(
            ...     __test_folder__.path + '_load_template.tpl')
            >>> file.content = 'hans'

            >>> Parser(file).render().output
            'hans'

            >>> Parser(file.directory_path + file.basename)
            Object of "Parser" with template "hans".

            >>> Parser(
            ...     __test_folder__.path + 'not_existing'
            ... ) # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            TemplateError:No suitable template found with given name "...".
        '''
        if self.string:
            self.content = self.template
        else:
            self.file = FileHandler(
                location=self.template, encoding=self.file_encoding)
            if not self.file.is_file():
                self.file = FileHandler(
                    location='%s%s%s' % (
                        self.file.path, os.extsep,
                        self.DEFAULT_FILE_EXTENSION_SUFFIX),
                    encoding=self.file_encoding)
            if not self.file.is_file():
                raise __exception__(
                    'No suitable template file found with given path "%s".',
                    self.template)
            self.content = self.file.content
        self.native_template_object = native_string.Template(self.content)
        self.native_template_object.pattern = re.compile(
            self.native_template_pattern)
        self.native_template_object.delimiter = self.left_code_delimiter
        return self

    @JointPoint
# # python3.4
# #     def _run_template(
# #         self: Self, prevent_rendered_python_code: builtins.bool,
# #         template_scope: builtins.dict
# #     ) -> Self:
    def _run_template(self, prevent_rendered_python_code, template_scope):
# #
        '''
            Runs the compiled template in its given scope. All error will be \
            cached and error messages depending on source template will be \
            derived on produced exceptions based in the compiled template.

            Examples:

            >>> nested_nested_file = FileHandler(
            ...     __test_folder__.path  + '_run_template_nested_nested')
            >>> nested_nested_file.content = '<% hans'
            >>> nested_file = FileHandler(
            ...     __test_folder__.path  + '_run_template_nested')
            >>> nested_file.content = (
            ...     "<% include('" + nested_nested_file.name + "', **{})")
            >>> file = FileHandler(__test_folder__.path + '_run_template')

            >>> Parser(
            ...     '<% peter = 5\\n'
            ...     "<% include('" + nested_nested_file.path + "', hans=5, "
            ...     "locals=('peter',), full_caching=false)",
            ...     string=True
            ... ).render() # doctest: +ELLIPSIS
            Object of "Parser" with template "...<% include('...', hans=5, ...

            >>> Parser(
            ...     '<% peter = 5\\n'
            ...     "<% include('" + nested_nested_file.path + "', hans=5, "
            ...     "locals=('peter',), full_caching=false, "
            ...     "propagate_full_caching=false)",
            ...     string=True
            ... ).render() # doctest: +ELLIPSIS
            Object of "Parser" with template "...<% include('...', hans=5, ...

            >>> Parser(
            ...     '<% peter = 5\\n'
            ...     "<% include('" + nested_nested_file.path + "', hans=5, "
            ...     "locals=('peter',), propagate_full_caching=true)",
            ...     string=True
            ... ).render() # doctest: +ELLIPSIS
            Object of "Parser" with template "...<% include('...', hans=5, ...

            >>> file.content = "<% include('" + nested_nested_file.name + "')"
            >>> Parser(file).render(
            ...     prevent_rendered_python_code=True
            ... ) # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            TemplateError: Error with "..._run_template" in include statemen...
            TemplateError: Error with "..._run_template_nested_nested" in ...
            NameError: Name "hans" is not defined

            >>> file.content = "<% include('" + nested_file.name + "')"
            >>> Parser(file).render() # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            TemplateError: Error with "..._run_template" in include statemen...
            TemplateError: Error with "..._run_template_nested" in line 1 ...
            TemplateError: Error with "..._run_template_nested_nested" in ...
            NameError: Name "hans" is not defined
            <BLANKLINE>
            rendered python code ...:
            ---------------------...
            <BLANKLINE>
            1 | hans
            <BLANKLINE>

            >>> Parser(
            ...     "<% include('" + __test_folder__.path +
            ...     "_run_template_not_existing')",
            ...     string=True
            ... ).render() # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            TemplateError: Error with given template string in include ...
            TemplateError: No suitable template found with given name "...
            rendered python code ...:
            ---------------------...
            <BLANKLINE>
            1 | include('..._run_template_not_existing', indent_space='')
            <BLANKLINE>
        '''
        try:
# # python3.4
# #             builtins.exec(self.rendered_python_code, template_scope)
            exec self.rendered_python_code in template_scope
# #
        except __exception__ as exception:
            '''Propagate nested template exceptions.'''
            '''
                NOTE: We only want to show one rendered content representation.
            '''
            source_line, mapped_line = self._get_exception_line(exception)
            rendered_python_code = ''
            if not prevent_rendered_python_code and (
                __test_mode__ or sys.flags.debug or
                __logger__.isEnabledFor(logging.DEBUG)
            ):
                rendered_python_code = self.represent_rendered_python_code()
# # python3.4
# #             exception = __exception__(
# #                 'Error with %s in include statement in line %s '
# #                 '(line in compiled template: %s).\n%s: %s%s',
# #                 self._determine_template_description(),
# #                 source_line, mapped_line, __exception__.__name__,
# #                 builtins.str(exception), rendered_python_code)
# #             raise exception from None
            exception = __exception__(
                'Error with %s in include statement in line %s '
                '(line in compiled template: %s).\n%s: %s%s',
                self._determine_template_description(),
                source_line, mapped_line, __exception__.__name__,
                builtins.str(exception), rendered_python_code)
            raise exception
# #
        except builtins.BaseException as exception:
            line_info, exception_message, native_exception_description = \
                self._handle_template_exception(exception)
            self._raise_template_exception(
                line_info, exception_message, native_exception_description,
                native_exception=exception)
        '''Make sure that all outputs during template execution are done.'''
        sys.stdout.flush()
        return self

    @JointPoint
# # python3.4
# #     def _handle_template_exception(
# #         self: Self, exception: builtins.BaseException,
# #         force_native_exception=False
# #     ) -> builtins.tuple:
    def _handle_template_exception(
        self, exception, force_native_exception=False
    ):
# #
        '''
            If an exception is raising during running generated template \
            (python) code this methods will handle it to map exception line \
            number to template's source code line number.

            Examples:

            >>> parser = Parser('<% hans', string=True)

            >>> parser._handle_template_exception(
            ...     __exception__('test'), force_native_exception=True
            ... ) # doctest: +ELLIPSIS
            (...Native exception object:...)

            >>> if sys.version_info.major > 2:
            ...     def unicode(value, dummy): return value
            >>> class TestException(Exception):
            ...     property = unicode('ä', 'utf_8')
            >>> parser._handle_template_exception(
            ...     TestException('test'), force_native_exception=True
            ... ) # doctest: +ELLIPSIS
            (...Native exception object:...)
        '''
        exception_message = '%s: %s' % (
            exception.__class__.__name__,
            String(exception).get_camel_case_capitalize().replace(
                "'", '"'
            ).content)
        native_exception_description = ''
        if(force_native_exception or sys.flags.debug or
           __logger__.isEnabledFor(logging.DEBUG)):
            for property_name in builtins.dir(exception):
                if not (
                    property_name.startswith('__') and
                    property_name.endswith('__')
                ):
                    value = builtins.getattr(exception, property_name)
# # python3.4
# #                     pass
                    if builtins.isinstance(value, builtins.unicode):
                        value = value.encode('utf_8')
# #
                    native_exception_description += '%s: "%s"\n' % (
                        property_name, builtins.str(value))
            native_exception_description = (
                '\n\nNative exception object:\n\n%s' %
                native_exception_description)
        return(
            (' in line %d (line in compiled template: %d)' %
             self._get_exception_line(exception)), exception_message,
            native_exception_description)

    @JointPoint
# # python3.4
# #     def _determine_template_description(self: Self) -> builtins.str:
    def _determine_template_description(self):
# #
        '''Determines a useful description for current template.'''
        if self.file:
            return '"%s"' % self.file.path
        return 'given template string'

    @JointPoint
# # python3.4
# #     def _raise_template_exception(
# #         self: Self, line_info: builtins.str,
# #         exception_message: builtins.str,
# #         native_exception_description: builtins.str,
# #         native_exception: builtins.BaseException,
# #         prevent_rendered_python_code=False
# #     ) -> None:
    def _raise_template_exception(
        self, line_info, exception_message, native_exception_description,
        native_exception, prevent_rendered_python_code=False
    ):
# #
        '''
            Performs a wrapper exception for exception raising in template \
            context.

            Examples:

            >>> parser = Parser('<% hans', string=True)
            >>> parser._raise_template_exception(
            ...     '', '', '', IOError('test'), True
            ... ) # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            TemplateError: Error with given template string.
            <BLANKLINE>
        '''
        rendered_python_code = ''
        if not prevent_rendered_python_code and (
            __test_mode__ or sys.flags.debug or
            __logger__.isEnabledFor(logging.DEBUG)
        ):
            rendered_python_code = self.represent_rendered_python_code()
# # python3.4
# #         exception = __exception__(
# #             'Error with {template_description}{line_info}.\n'
# #             '{exception_message}{native_exception_description}'
# #             '{rendered_python_code}'.format(
# #                 template_description=self._determine_template_description(
# #                 ), line_info=line_info,
# #                 exception_message=exception_message,
# #                 native_exception_description=native_exception_description,
# #                 rendered_python_code=rendered_python_code))
# #         raise exception from None
        exception = __exception__(
            'Error with {template_description}{line_info}.\n'
            '{exception_message}{native_exception_description}'
            '{rendered_python_code}'.format(
                template_description=self._determine_template_description(
                ), line_info=line_info,
                exception_message=exception_message,
                native_exception_description=native_exception_description,
                rendered_python_code=rendered_python_code))
        raise exception
# #

    @JointPoint
# # python3.4
# #     def _get_exception_line(
# #         self: Self, exception: builtins.BaseException
# #     ) -> builtins.tuple:
    def _get_exception_line(self, exception):
# #
        '''
            Determines the line where the given exception was raised. If in \
            the responsible line in compiled template was found, a tuple with \
            the resulting line in source template and compiled template will \
            be given back.

            Examples:

            >>> parser = Parser('', string=True)
            >>> parser._line_shifts = [(10, 5)]
            >>> parser._get_exception_line(IOError('test'))
            (0, 0)

            >>> parser = Parser('', string=True)
            >>> parser._line_shifts = [(3, 0)]
            >>> exception = IOError('test')
            >>> exception.lineno = 4
            >>> parser._get_exception_line(exception)
            (4, 4)
        '''
        '''
            NOTE: A tuple with line matching (a, b) means that till python \
            code line a + b we have b number of lines which doesn't occur in \
            source code.
        '''
        old_number_of_phantom_lines = 0
        line_number = self._determine_exec_string_exception_line(exception)
        for number_of_lines, number_of_phantom_lines in self._line_shifts:
            line_number_in_python_code = number_of_lines + \
                number_of_phantom_lines
            if line_number <= line_number_in_python_code:
                __logger__.debug('Grap line number by between range hit.')
                return line_number - old_number_of_phantom_lines, line_number
            old_number_of_phantom_lines = number_of_phantom_lines
        if line_number and self._line_shifts:
            __logger__.debug('Grap line number by last mapping.')
            return line_number - self._line_shifts[-1][1], line_number
        __logger__.debug(
            'Get equal line number for compiled and source code version '
            'by assuming there are no line shifts.')
        return line_number, line_number

    @JointPoint
# # python3.4
# #     def _determine_exec_string_exception_line(
# #         self: Self, exception: builtins.BaseException
# #     ) -> builtins.int:
    def _determine_exec_string_exception_line(self, exception):
# #
        '''
            Determines the line number where the exception (in exec \
            statement) occurs from the given exception.
        '''
# # python3.4
# #         exception_traceback = traceback.extract_tb(exception.__traceback__)
        exception_traceback = traceback.extract_tb(sys.exc_info()[2])
# #
        '''
            Search traceback for a context ran from "builtins.exec()" and \
            begin from the nearest context.
        '''
        exception_traceback.reverse()
        for context in exception_traceback:
            if context[0] == '<string>':
                return context[1]
        if builtins.hasattr(exception, 'lineno'):
            return exception.lineno
        return 0

        # # region wrapper methods for template context

    # NOTE: This method is heavily used during rendering. It should be as fast
    # as possible. So the JointPoint is deactivated.
    # @JointPoint
# # python3.4
# #     def _print(
# #         self: Self, *arguments: builtins.object, indent=True,
# #         indent_space='', **keywords: builtins.object
# #     ) -> None:
    def _print(self, *arguments, **keywords):
# #
        '''
            Represents the print function which will be used for all plain \
            text wraps and print expressions by compiling the source template.

            Examples:

            >>> parser = Parser(
            ...     template='test', string=True, pretty_indent=True)

            >>> parser._print('hans')
            >>> parser._print('and klaus', end='\\n', indent_space=' ')
            >>> parser._print('fritz is also present.', end='')
            >>> parser._output.clear()
            'hans\\n and klaus\\nfritz is also present.'

            >>> parser._print('hans', end='', indent_space='  ')
            >>> parser.output
            '  hans'
        '''
        if self.pretty_indent:
# # python3.4
# #             pass
            keywords_dictionary = Dictionary(content=keywords)
            indent, keywords = keywords_dictionary.pop(
                name='indent', default_value=True)
            indent_space, keywords = keywords_dictionary.pop(
                name='indent_space', default_value='')
# #
            if indent and indent_space:
                '''
                    If an indent level was given prepend given indent space \
                    to each line.
                '''
                print_buffer = Buffer()
                codewords = copy(keywords)
                codewords.update({'buffer': print_buffer})
                Print(*arguments, **codewords)
                arguments = (indent_space + print_buffer.content.replace(
                    '\n', '\n' + indent_space),)
                if print_buffer.content.endswith('\n'):
                    arguments = [arguments[0][:-builtins.len(
                        '\n' + indent_space)] + '\n'] + list(arguments[1:])
                keywords['end'] = ''
            keywords['file'] = self._output
            return builtins.print(*arguments, **keywords)
        return builtins.print(
            *arguments, file=self._output, end=keywords.get('end'))

    @JointPoint
# # python3.4
# #     def _include(
# #         self: Self, template_file_path: builtins.str, scope={},
# #         locals=(), end='\n', full_caching=None,
# #         propagate_full_caching=None, indent=True, indent_space='',
# #         **keywords: builtins.object
# #     ) -> builtins.dict:
    def _include(
        self, template_file_path, scope={}, locals=(), end='\n',
        full_caching=None, propagate_full_caching=None, indent=True,
        indent_space='', **keywords
    ):
# #
        '''
            Performs a template include. This method is implemented for using \
            in template context.
        '''
        '''
            NOTE: Force python to swap reference to default scope value. This \
            enables a real namespace for included files.
        '''
        internal_scope = copy(scope)
        internal_scope.update(keywords)
        for local in locals:
            if sys.flags.optimize:
                internal_scope[local] = \
                    inspect.currentframe().f_back.f_locals[local]
            else:
                internal_scope[local] = \
                    inspect.currentframe().f_back.f_back.f_locals[local]
        root_path = ''
        if self.file:
            root_path = self.file.directory_path
        shortcut = self.template_context_default_indent
        if propagate_full_caching is None:
            propagate_full_caching = self.propagate_full_caching
        if full_caching is None:
            full_caching = False
            if propagate_full_caching:
                full_caching = self.full_caching
        self._print(
            self.__class__(
                template=root_path + template_file_path,
                cache_path=self.cache_path, full_caching=full_caching,
                propagate_full_caching=propagate_full_caching,
                file_encoding=self.file_encoding,
                placeholder_name_pattern=self.placeholder_name_pattern,
                placeholder_pattern=self.placeholder_pattern,
                template_pattern=self.template_pattern,
                left_code_delimiter=self.left_code_delimiter,
                right_code_delimiter=self.right_code_delimiter,
                right_escaped=self.right_escaped,
                template_context_default_indent=shortcut,
                builtin_names=self.builtin_names,
                pretty_indent=self.pretty_indent
            ).render(mapping=internal_scope).output,
            end=end, indent=indent, indent_space=indent_space)
        return internal_scope

        # # endregion

        # # region callback

    @JointPoint
# # python3.4
# #     def _render_code(
# #         self: Self, match: builtins.type(re.compile('').match(''))
# #     ) -> builtins.str:
    def _render_code(self, match):
# #
        '''
            Helper method for rendering the source template file.

            Examples:

            >>> Parser('<%hans%>', string=True).render(hans=5).output
            '5'
            >>> Parser('number:<%hans%>\\n', string=True).render(hans=5).output
            'number:5'
            >>> Parser('<%hans%>number:<%hans%>', string=True).render(
            ...     hans=5
            ... ).output
            '5number:5'
            >>> Parser(
            ...     '<% if true:\\n    <%hans%><%hans%>', string=True
            ... ).render(hans=5).output
            '55'
            >>> Parser('\\n\\n<%hans%>', string=True).render(hans=5).output
            '\\n\\n5'
            >>> Parser(
            ...     '<% if true:\\n<%hans%>', string=True
            ... ).render(hans=5).output # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            TemplateError: Error with given template string in line 2 (line ...
            IndentationError: Expected an indented block (<string>, line 2)
            rendered python code ...:
            ---------------------...
            <BLANKLINE>
            1 | if true:
            2 | print(String(hans), end='')
            <BLANKLINE>

            >>> Parser('<% print(hans)', string=True).render(hans=5).output
            '5\\n'
            >>> Parser(
            ...     '<% include()', string=True
            ... ).render().output # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            TemplateError: Error with given template string in line 1 (line ...
            TypeError: _include() takes at least 2 arguments (2 given)
            rendered python code ...:
            ---------------------...
            <BLANKLINE>
            1 | include(indent_space='')
            <BLANKLINE>

            >>> Parser('<% if true:\\n    hans', string=True).render(
            ...     hans=5
            ... ).output
            'hans'
            >>> Parser('<% print()', string=True).render().output
            '\\n'

            >>> Parser('<%% print(hans)', string=True).render().output
            '<% print(hans)'
            >>> Parser('<%%\\n', string=True).render().output
            '<%'
            >>> Parser('<%%<%%', string=True).render().output
            '<%<%'
            >>> Parser(' <%%', string=True).render().output
            ' <%'

            >>> Parser('\\n', string=True).render().output
            ''
        '''
        '''
            This has been sorted by their average frequency for improving \
            performance.
        '''
        if match.group('NONE_CODE'):
            return self._render_none_code_line(match)
        if match.group('PLACEHOLDER'):
            return self._render_placeholder(match)
        if match.group('EMPTY_LINE'):
            return self._render_empty_line(match)
        if match.group('CODE'):
            return self._render_code_line(match)
        # NOTE: Implicit case: if match.group('ESCAPED_DELIMITER'):
        return self._render_escaped_none_code_line(match)

        # # # endregion

        # # # region helper

        # # # # region line renderer

    @JointPoint
# # python3.4
# #     def _render_escaped_none_code_line(
# #         self: Self, match: builtins.type(re.compile('').match(''))
# #     ) -> builtins.str:
    def _render_escaped_none_code_line(self, match):
# #
        '''Handles escaped none code.'''
        indent = self._get_code_indent(
            current_indent=match.group('indent_escaped'), mode='passiv')
        last_empty_lines = self._flush_empty_lines(indent)
        was_new_line = self._new_line
        if match.group('after_escaped'):
            self._new_line = True
            self._number_of_generated_lines += 1
        else:
            self._new_line = False
            self._number_of_generated_phantom_lines += 1
        slice = 0
        if was_new_line:
            slice = builtins.len(self._code_dependent_indents) * self.indent
        content_before = ''
        if match.group('before_escaped'):
            content_before = match.group('before_escaped')[slice:]
        return last_empty_lines + indent + self._render_none_code(
            string=content_before + self.left_code_delimiter, end='')

    @JointPoint
# # python3.4
# #     def _render_placeholder(
# #         self: Self, match: builtins.type(re.compile('').match(''))
# #     ) -> builtins.str:
    def _render_placeholder(self, match):
# #
        '''Handles placeholder.'''
        indent = self._get_code_indent(
            current_indent=match.group('indent_placeholder'), mode='passiv')
        last_empty_lines = self._flush_empty_lines(indent)
        was_new_line = self._new_line
        '''
            NOTE: We can have zero one or two phantom lines for one \
            placeholder.
        '''
        if match.group('before_placeholder'):
            self._number_of_generated_phantom_lines += 1
            self._line_shifts.append(
                (self._number_of_generated_lines,
                 self._number_of_generated_phantom_lines))
        if match.group('after_placeholder'):
            self._new_line = True
            self._number_of_generated_lines += 1
        else:
            self._new_line = False
            self._number_of_generated_phantom_lines += 1
        before_placeholder = ''
        if match.group('before_placeholder'):
            '''
                Only cut code dependent indents if placeholder is the first \
                statement in current line.
            '''
            slice = 0
            if was_new_line:
                slice = builtins.len(
                    self._code_dependent_indents
                ) * self.indent
            before_placeholder = indent + self._render_none_code(
                string=match.group('before_placeholder')[slice:], end='')
        self._line_shifts.append(
            (self._number_of_generated_lines,
             self._number_of_generated_phantom_lines))
        return "%s%s%sprint(String(%s)%s, end='')\n" % (
            last_empty_lines, before_placeholder, indent,
            match.group('placeholder').strip(),
            ('+"\\n"' if self._get_new_line() else ''))

    @JointPoint
# # python3.4
# #     def _render_empty_line(
# #         self: Self, match: builtins.type(re.compile('').match(''))
# #     ) -> builtins.str:
    def _render_empty_line(self, match):
# #
        '''Handles empty lines.'''
        self._new_line = True
        self._number_of_generated_lines += 1
        self._empty_lines.append(self._render_none_code(
            string=match.group('EMPTY_LINE'), end=''))
        return ''

    @JointPoint
# # python3.4
# #     def _render_none_code_line(
# #         self: Self, match: builtins.type(re.compile('').match(''))
# #     ) -> builtins.str:
    def _render_none_code_line(self, match):
# #
        '''Handles none code.'''
        indent = self._get_code_indent(
            current_indent=match.group('indent_none_code'), mode='passiv')
        last_empty_lines = self._flush_empty_lines(indent)
        was_new_line = self._new_line
        if match.group('after_none_code'):
            self._new_line = True
            self._number_of_generated_lines += 1
        else:
            self._new_line = False
            self._number_of_generated_phantom_lines += 1
        slice = 0
        if was_new_line and self._code_dependent_indents:
            slice = builtins.len(
                self._code_dependent_indents
            ) * self.indent
        return last_empty_lines + indent + self._render_none_code(
            string=match.group('none_code')[slice:],
            end=self._get_new_line())

    @JointPoint
# # python3.4
# #     def _render_code_line(
# #         self: Self, match: builtins.type(re.compile('').match(''))
# #     ) -> builtins.str:
    def _render_code_line(self, match):
# #
        '''Compiles a template python code line.'''
        was_new_line = self._new_line
        self._new_line = True
        self._number_of_generated_lines += 1
        code_line = match.group('code').strip()
        '''Support alternate "end" keyword to finish a code block.'''
        if code_line == 'end':
            code_line = 'pass'
        mode = 'passiv'
        if code_line.endswith(':') and not code_line.startswith('#'):
            mode = 'activ'
        indent = self._get_code_indent(
            current_indent=match.group('indent_code'), mode=mode)
        code_line = self._save_output_method_indent_level(
            code_line, was_new_line, match)
        return self._flush_empty_lines(indent) + indent + code_line

        # # # # endregion

    @JointPoint
# # python3.4
# #     def _save_output_method_indent_level(
# #         self: Self, code_line: builtins.str, was_new_line: builtins.bool,
# #         match: builtins.type(re.compile('').match(''))
# #     ) -> builtins.str:
    def _save_output_method_indent_level(
        self, code_line, was_new_line, match
    ):
# #
        '''Gives indent level to all output methods found in template code.'''
        if code_line.startswith('print(') or code_line.startswith('include('):
            slice = builtins.len(
                self._code_dependent_indents
            ) * self.indent
            if code_line.startswith('print('):
                return self._handle_print_output_indent_level(
                    code_line, match, slice)
            return self._handle_include_output_indent_level(
                code_line, match, slice)
        return code_line

    @JointPoint
# # python3.4
# #     def _handle_include_output_indent_level(
# #         self: Self, code_line: builtins.str,
# #         match: builtins.type(re.compile('').match('')), slice: builtins.int
# #     ) -> builtins.str:
    def _handle_include_output_indent_level(self, code_line, match, slice):
# #
        '''
            Returns a string representing from include function call in \
            generated python code with their indent level given.
        '''
        length_of_include_call = String(
            code_line[builtins.len('include('):]
        ).find_python_code_end_bracket()
        slice_position = builtins.len('include(') + length_of_include_call
        indent_space = match.group('indent_code')[slice:]
        arguments = code_line[builtins.len('include('):slice_position]
        regex = re.compile('(?:, *)?\*\*[^ ]+$')
        match = regex.search(arguments)
        if match:
            arguments = regex.sub('', arguments)
        post_code = code_line[slice_position + 1:]
        if arguments:
            return("include(%s, indent_space='%s'%s)%s" % (
                arguments, indent_space, match.group() if match else '',
                post_code))
        return("include(indent_space='%s')%s" % (indent_space, post_code))

    @JointPoint
# # python3.4
# #     def _handle_print_output_indent_level(
# #         self: Self, code_line: builtins.str,
# #         match: builtins.type(re.compile('').match('')), slice: builtins.int
# #     ) -> builtins.str:
    def _handle_print_output_indent_level(self, code_line, match, slice):
# #
        '''
            Returns a string representing from print function call in \
            generated python code with their indent level given.
        '''
        length_of_print_call = String(
            code_line[builtins.len('print('):]
        ).find_python_code_end_bracket()
        slice_position = builtins.len('print(') + length_of_print_call
        if code_line[builtins.len('print('):slice_position]:
            return(
                'print(' + code_line[builtins.len('print('):slice_position] +
                ", indent_space='" + match.group('indent_code')[slice:] +
                "')" + code_line[slice_position + 1:])
        return(
            "print(indent_space='" + match.group('indent_code')[slice:] +
            "')" + code_line[slice_position + 1:])

    @JointPoint
# # python3.4
# #     def _flush_empty_lines(
# #         self: Self, indent: builtins.str
# #     ) -> builtins.str:
    def _flush_empty_lines(self, indent):
# #
        '''
            Flushes the empty line stack needed for right line mapping \
            through template code and generated python code.
        '''
        result = ''
        for empty_line in self._empty_lines:
            result += indent + empty_line
        self._empty_lines = []
        return result

    @JointPoint
# # python3.4     def _get_new_line(self: Self) -> builtins.str:
    def _get_new_line(self):
        '''
            Returns a new line string if necessary for the correct template \
            compiling to native python code.
        '''
        if(self._new_line and
           self._number_of_generated_lines !=
           builtins.len(self.content.splitlines())):
            return '\n'
        return ''

    @JointPoint
# # python3.4
# #     def _get_code_indent(
# #         self: Self, current_indent: (builtins.type(None), builtins.str),
# #         mode='passiv'
# #     ) -> builtins.str:
    def _get_code_indent(self, current_indent, mode='passiv'):
# #
        '''
            Returns the right indent in code as string depending on the \
            current indention level and context.

            **mode** - can have three different states. \
                passiv: This mode describes the ability to close or continue \
                        the current context by their level of indention. \
                activ: Means a new code depending context is open. The \
                       following code is depended on this line.
        '''
        if current_indent is None:
            current_indent = ''
        indent = ''
        if self._code_dependent_indents:
            if self._new_line:
                slice = 0
                indents = builtins.enumerate(self._code_dependent_indents)
                for counter, dependent_indent in indents:
                    if(builtins.len(current_indent) >
                       builtins.len(dependent_indent)):
                        indent = (counter + 1) * ' '
                        slice = counter + 1
                '''Close code indent blocks.'''
                self._code_dependent_indents = \
                    self._code_dependent_indents[:slice]
            else:
                '''Prepend code dependent indent to get right context.'''
                indent = builtins.len(self._code_dependent_indents) * ' '
        if mode == 'activ':
            '''Expect a new dependent indented code block.'''
            self._code_dependent_indents.append(current_indent)
        return indent

        # # # endregion

        # # endregion

    # endregion

# endregion

# region footer

'''
    Preset some variables given by introspection letting the linter know what \
    globale variables are available.
'''
__logger__ = __exception__ = __module_name__ = __file_path__ = \
    __test_mode__ = __test_buffer__ = __test_folder__ = __test_globals__ = None
'''
    Extends this module with some magic environment variables to provide \
    better introspection support. A generic command line interface for some \
    code preprocessing tools is provided by default.
'''
Module.default(name=__name__, frame=inspect.currentframe())

# endregion

# region vim modline

# vim: set tabstop=4 shiftwidth=4 expandtab:
# vim: foldmethod=marker foldmarker=region,endregion:

# endregion
