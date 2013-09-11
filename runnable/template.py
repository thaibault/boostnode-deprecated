#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# region vim modline

# vim: set tabstop=4 shiftwidth=4 expandtab:
# vim: foldmethod=marker foldmarker=region,endregion:

# endregion

# region header

'''
    This module provides classes to handle text-based files and string
    parsing.
'''

## python3.3 pass
from __future__ import print_function

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
import json
import logging
import os
import re
import string as native_string
import sys
import traceback

'''Make boostNode packages and modules importable via relative paths.'''
for number in (3, 4):
    sys.path.append(os.path.abspath(sys.path[0] + number * ('..' + os.sep)))

from boostNode.extension.file import Handler as FileHandler
from boostNode.extension.native import Dictionary, Module, String
from boostNode.extension.output import Buffer, Print
from boostNode.extension.system import CommandLine, Runnable
## python3.3 from boostNode.extension.type import Self
pass
from boostNode.paradigm.aspectOrientation import JointPoint
from boostNode.paradigm.objectOrientation import Class

# endregion


# region classes

class Parser(Class, Runnable):
    '''
        This class can parse a string or file to interpret it as template
        for replacing containing placeholder and rendering embedded python
        script snippets.
    '''

    # region constant properties

        # region public

    '''
        Holds all command line interface argument informations.
    '''
    COMMAND_LINE_ARGUMENTS = (
        {'arguments': ('template',),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             #'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Select a template file to execute.',
             #'dest': 'template',
             'metavar': 'TEMPLATE'}},
        {'arguments': ('-s', '--string'),
         'keywords': {
             'action': 'store_true',
             'default': {'execute': '__initializer_default_value__'},
             'help': 'Determine if given template should be interpreted as '
                     'template or a file name pointing to a template file.',
             'dest': 'string'}},
        {'arguments': ('-p', '--placeholder-name-pattern'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Define the regex pattern of a template placeholder '
                     'name.',
             'dest': 'placeholder_name_pattern',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-o', '--command-line-placeholder-name-pattern'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Define the regex pattern of a template placeholder '
                     'name given via the command line interface.',
             'dest': 'command_line_placeholder_name_pattern',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-d', '--left-code-delimiter'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Defines left delimiter for placeholder and code lines.',
             'dest': 'left_code_delimiter',
             'metavar': 'STRING'}},
        {'arguments': ('-e', '--right-code-delimiter'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Defines right delimiter for placeholder.',
             'dest': 'right_code_delimiter',
             'metavar': 'STRING'}},
        {'arguments': ('-r', '--right-escaped'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Defines the string which indicates on the right side of '
                     "a code delimiter that it shouldn't be evaluated as "
                     'code delimiter.',
             'dest': 'right_escaped',
             'metavar': 'STRING'}},
        {'arguments': ('-f', '--placeholder-pattern'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Defines template placeholder pattern.',
             'dest': 'placeholder_pattern',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-j', '--template-context-default-indent'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Defines default indents to define pythonic semantics.',
             'dest': 'template_context_default_indent',
             'metavar': 'NUMBER'}},
        {'arguments': ('-a', '--template-pattern'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Defines the general syntax of given template.',
             'dest': 'template_pattern',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-i', '--command-line-placeholder-pattern'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Defines the given placeholder pattern.',
             'dest': 'command_line_placeholder_pattern',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-n', '--native-template-pattern'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': "Defines template pattern for python's native template "
                     'engine.',
             'dest': 'native_template_pattern',
             'metavar': 'REGEX_PATTERN'}},
        {'arguments': ('-b', '--builtins'),
         'keywords': {
             'action': 'store',
             'nargs': '*',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Defines which python native object should be available '
                     'in template scope.',
             'dest': 'builtins',
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

        # endregion

    # endregion

    # region dynamic properties

        # region public

    '''Holds the given template as string.'''
    content = ''
    '''Holds the given template as rendered (runnable python code) string.'''
    rendered_content = ''
    '''Pythons native template object.'''
    native_template_object = None
    '''Template file handler.'''
    file = None
    '''Saves previous initially defined escape symbols.'''
    right_escaped = ''

        # endregion

        # region protected

    '''Holds a name space of every argument given by the command line.'''
    _command_line_arguments = None
    '''
        Holds several static informations for template parsing at runtime.
        In general it defines the syntax.
    '''
    _placeholder_name_pattern = ''
    _command_line_placeholder_name_pattern = ''
    _left_code_delimiter = ''
    _right_code_delimiter = ''
    _placeholder_pattern = ''
    _template_pattern = ''
    _native_template_pattern = ''
    _template_context_default_indent = 0
    '''Defines how to parse placholder meanings through the command line.'''
    _command_line_placeholder_pattern = ''
    '''Defines which builtin variables should be available in templates.'''
    _builtins = {}
    '''Saves the output of running executed template.'''
    _output = None
    '''Indicates if last rendered code snippet was a full line.'''
    _new_line = True
    '''
        Holds number of white spaces to indent a context dependent code block
        in templates.
    '''
    _indent = 0
    _count_lines = 0
    _count_no_lines = 0
    _code_dependend_indents = []
    _pretty_indent = False
    '''
        A list of tuple holding the number of phantom lines till its
        corresponding real line in source code.
        That's necessary for mapping exception line in compiled template to
        lines in source code template because the number of lines in source
        code are more compact as in compiled pendant.
    '''
    _line_shifts = []
    '''
        Buffers empty lines by parsing template source code. The list is used
        as queue. Empty lines will be written finally to compiled source code
        if there dependence membership is resolved.
    '''
    _empty_lines = []
    '''
        Saves needed informations give a line number to each rendered content.
    '''
    _current_rendered_content_line_number = 0
    _number_of_rendered_content_lines = 0

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

            >>> repr(Parser(template='test', string=True))
            'Object of "Parser" with template "test".'
        '''
        return 'Object of "{class_name}" with template "{template}".'.format(
            class_name=self.__class__.__name__, template=self.content)

    @JointPoint
## python3.3     def __str__(self: Self) -> builtins.str:
    def __str__(self):
        '''
            Triggers if an instance is tried to be interpreted as a string.

            Examples:

            >>> str(Parser(template='hans', string=True))
            'hans'
        '''
        return self.content

    @JointPoint
## python3.3     def __len__(self: Self) -> builtins.int:
    def __len__(self):
        '''
            Triggers if the pythons native "builtins.len()" function tries to
            handle current instance.
            Returns the number of symbols given in the current string
            representation of this object.

            Examples:

            >>> len(Parser(template='hans', string=True))
            4
        '''
        return builtins.len(self.__str__())

            # endregion

            # region getter

    @JointPoint
## python3.3     def get_indent(self: Self) -> builtins.int:
    def get_indent(self):
        '''
            Returns a string of white spaces representing current context.
        '''
        if not self._indent and self.content:
            self._indent = self._template_context_default_indent
            match = re.compile(
                '^<% *__indent__ *= *(?P<number_of_indents>[1-9][0-9]*)'
                '(?:;|\n)?.*?$'
            ).match(String(self.content).readline())
            if match:
                self._indent = builtins.int(match.group('number_of_indents'))
        return self._indent

    @JointPoint
## python3.3     def get_output(self: Self) -> builtins.str:
    def get_output(self):
        '''
            Gets the current output buffer. It consists everything printed out
            in code snippets rendered by the template instance or exists as
            plain text in given template.

            Examples:

            >>> template = Parser(
            ...     'hans says\\n<% print("who is hans?")', string=True)
            >>> template.render().output
            'hans says\\nwho is hans?\\n'
        '''
        if self._output is None:
            self._output = Buffer()
        return self._output.content

    @JointPoint
## python3.3     def get_builtins(self: Self) -> builtins.dict:
    def get_builtins(self):
        '''
            Defines minimum needed native python features for each template
            scope. It adds user-defined additionally python functions. The
            minimum needed functions (e.g. "print()") will never be
            overwritten.

            Examples:

            >>> template = Parser(template='hans', string=True)
            >>> template.builtins # doctest: +ELLIPSIS
            {...'print': ..._print...}
        '''
        self._builtins.update({
            '__indent__': self.indent, 'FileHandler': FileHandler,
            'print': self._print, 'include': self._include,
            'str': builtins.str, 'len': builtins.len, 'json': json,
            'False': False, 'True': True, 'locals': builtins.locals})
        return self._builtins

            # endregion

            # region wrapper

    @JointPoint
## python3.3
##     def substitute(
##         self: Self, *arguments: builtins.str, **keywords: builtins.object
##     ) -> Self:
    def substitute(self, *arguments, **keywords):
##
        '''
            Wrapper method for pythons native "string.Template.substitute()"
            method.

            Examples:

            >>> template = Parser(
            ...     template='hans <%placeholder%>', string=True)
            >>> template.substitute(placeholder='also hans')
            Object of "Parser" with template "hans <%placeholder%>".
            >>> template.output
            'hans also hans'

            >>> template = Parser(
            ...     template='hans', string=True)
            >>> template.substitute()
            Object of "Parser" with template "hans".
            >>> template.output
            'hans'

            >>> template = Parser(
            ...     template='hans <%not_hans%>', string=True)
            >>> template.substitute()
            Traceback (most recent call last):
            ...
            KeyError: 'not_hans'
        '''
        self._output.write(self.native_template_object.substitute(
            *arguments, **keywords))
        return self

    @JointPoint
## python3.3
##     def safe_substitute(
##         self: Self, *arguments: builtins.str, **keywords: builtins.object
##     ) -> Self:
    def safe_substitute(self, *arguments, **keywords):
##
        '''
            Wrapper method for pythons native
            "string.Template.safe_substitute()" method.

            Examples:

            >>> template = Parser(
            ...     template='hans <%placeholder%>', string=True)
            >>> template.safe_substitute(placeholder='also hans')
            Object of "Parser" with template "hans <%placeholder%>".
            >>> template.output
            'hans also hans'

            >>> template = Parser(
            ...     template='hans', string=True)
            >>> template.safe_substitute()
            Object of "Parser" with template "hans".

            >>> template = Parser(
            ...     template='hans <%not_hans%>', string=True)
            >>> template.safe_substitute()
            Object of "Parser" with template "hans <%not_hans%>".
        '''
## python3.3
##         self._output.write(self.native_template_object.safe_substitute(
##             *arguments, **keywords))
        def substitute(match):
            '''
                Substitution replacement for native pendant with no
                exception raising.
            '''
            if match.group('variable_name') in keywords:
                return builtins.str(
                    keywords[match.group('variable_name')])
            return match.group(0)
        self._output.write(re.compile(self._placeholder_pattern.format(
            left_delimiter=self._left_code_delimiter,
            right_delimiter=self._right_code_delimiter,
            placeholder=self._placeholder_name_pattern)
        ).sub(substitute, self.content))
##
        return self

            # endregion

            # region parsing

    @JointPoint
## python3.3     def substitute_all(self: Self, replacement='') -> Self:
    def substitute_all(self, replacement=''):
        '''
            Substitutes every placeholder in template with a given replacement
            string.

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
        self._output.write(re.compile(self._placeholder_pattern.format(
            left_delimiter=self._left_code_delimiter,
            right_delimiter=self._right_code_delimiter,
            placeholder=self._placeholder_name_pattern)
        ).sub(replacement, self.content))
        return self

    @JointPoint
## python3.3
##     def render(
##         self: Self, mapping={}, **keywords: builtins.object
##     ) -> Self:
    def render(self, mapping={}, **keywords):
##
        '''
            Renders the template. Searches for python code snippets and handles
            correct indenting.
            Wraps plain text with a print function.

            Examples:

            >>> tpl = Parser(
            ...     'hans says\\n<% print("who the fu.. is hans?")',
            ...     string=True)
            >>> tpl.render() # doctest: +ELLIPSIS
            Object of "Parser" with template "hans says...who the fu.. is ha...
        '''
        self.rendered_content = re.compile(
            self._template_pattern.format(
                left_delimiter=String(
                    self._left_code_delimiter
                ).validate_regex(),
                right_delimiter=String(
                    self._right_code_delimiter
                ).validate_regex(),
                placeholder=self._placeholder_name_pattern,
                right_escaped=self.right_escaped)
        ).sub(self._render_code, self.content).strip()
        mapping.update(keywords)
        return self._run_template(template_scope=mapping)

    @JointPoint
## python3.3     def represent_rendered_content(self: Self) -> builtins.str:
    def represent_rendered_content(self):
        '''
            This method adds line numbers to rendered contend which is
            visible if an template exception occurs in debug mode.
        '''
        self._number_of_rendered_content_lines = builtins.len(
            String(self.rendered_content).readlines())

        @JointPoint
## python3.3
##         def replace_rendered_content_line(
##             match: builtins.type(re.compile('').match(''))
##         ) -> builtins.str:
        def replace_rendered_content_line(match):
##
            '''
                Prepends a line numbers to each line of rendered python
                code.
            '''
            self._current_rendered_content_line_number += 1
            number_of_whitspaces = builtins.len(builtins.str(
                self._number_of_rendered_content_lines)
            ) - builtins.len(builtins.str(
                self._current_rendered_content_line_number))
            return number_of_whitspaces * ' ' + builtins.str(
                self._current_rendered_content_line_number
            ) + ' | ' + match.group('line')
        return re.compile('^(?P<line>.*)$', re.MULTILINE).sub(
            replace_rendered_content_line, self.rendered_content)

            # endregion

        # endregion

        # region protected

            # region runnable implementation

    @JointPoint
## python3.3     def _run(self: Self) -> Self:
    def _run(self):
        '''
            Entry point for command line call of this program.
            Loads the given template. If it is given by the command line it
            will be interpreted directly.

            Examples:

            >>> FileHandler(
            ...     __test_folder__ + '_run', must_exist=False
            ... ).content = 'hans <%placeholder%>'
            >>> template = Parser(
            ...     template=__test_folder__ + '_run')
            >>> template.substitute(placeholder='also hans')
            Object of "Parser" with template "hans <%placeholder%>".
            >>> template.output
            'hans also hans'
        '''
        self._command_line_arguments = CommandLine.argument_parser(
            arguments=self.COMMAND_LINE_ARGUMENTS, module_name=__name__,
            scope={'self': self})
        initializer_arguments = self._command_line_arguments_to_dictionary(
            namespace=self._command_line_arguments)
        if(initializer_arguments['builtins'] and
           builtins.isinstance(initializer_arguments['builtins'][0],
                               builtins.str)):
            initializer_arguments['builtins'] = builtins.map(
                lambda builtin: builtins.eval(builtin),
                initializer_arguments['builtins'])
        self._initialize(**initializer_arguments).render(
            **self._generate_scope_variables())
        Print(self.output)
        return self

    @JointPoint
## python3.3
##     def _initialize(
##         self: Self, template: (builtins.str, FileHandler),
##         string=False,
##         placeholder_name_pattern='[a-zA-Z0-9_\[\]\'"\.()\\\\,\-+ :/={}]+',
##         command_line_placeholder_name_pattern='(?s)'
##                                               '[a-zA-Z0-9_\[\]\.(),\-+]+',
##         placeholder_pattern='{left_delimiter}[ \t]*'
##                             '(?P<variable_name>{placeholder})'
##                             '[ \t]*{right_delimiter}',
##         template_pattern='(?m)(?P<ESCAPED_DELIMITER>'
##                          '(?P<before_escaped>'  # in brackets
##                          '(?P<indent_escaped>[ \t]*)'  # in two brackets
##                          '(?!{left_delimiter})'  # in two brackets
##                          '(?:.(?!{left_delimiter}))*?.?'  # in two brackets
##                          ')?{left_delimiter}{right_escaped}'  # in brackets
##                          '(?P<escaped_end>\n?)'  # in brackets
##                          ')|(?P<PLACEHOLDER>'
##                          '(?P<before_placeholder>'  # in brackets
##                          '(?P<indent_placeholder>[ \t]*)'  # in two brackets
##                          '(?!{left_delimiter})'  # in two brackets
##                          '(?:.(?!{left_delimiter}))*?.?'  # in two brackets
##                          ')?{left_delimiter}[ \t]*'  # in brackets
##                          '(?P<placeholder>{placeholder})'  # in brackets
##                          '[ \t]*'  # in brackets
##                          '{right_delimiter}'  # in brackets
##                          '(?P<placeholder_end>\n?)'  # in brackets
##                          ')|(?P<CODE>'
##                          '^(?P<indent_code>[ \t]*)'  # in brackets
##                          '{left_delimiter}'  # in brackets
##                          '(?P<code>.+)$'  # in brackets
##                          ')|(?P<NONE_CODE>'
##                          '(?P<none_code>'  # in brackets
##                          '(?P<indent_none_code>'  # in two brackets
##                          '[ \t]*'
##                          ').+'  # in two brackets
##                          ')'  # in brackets
##                          '(?P<none_code_end>\n|$)'  # in brackets
##                          ')|(?P<EMPTY_LINE>^(?P<indent_line>[ \t]*)\n)',
##         command_line_placeholder_pattern='^(?P<variable_name>{placeholder})'
##                                          '(?P<separator>.)(?P<value>.+)$',
##         native_template_pattern='<%[ \t]*(?:'
##                                 '(?P<escaped>%)|'  # in brackets
##                                 '(?:(?P<named>[a-zA-Z0-9_]+)'  # in brackets
##                                 '[ \t]*% >)|'  # in two brackets
##                                 '(?:'  # in brackets
##                                 '(?P<braced>'  # in two brackets
##                                 '[a-zA-Z0-9_]+)'  # in tree brackets
##                                 '[ \t]*%>)|'  # in two brackets
##                                 '(?P<invalid>)'  # in brackets
##                                 ')',
##         left_code_delimiter='<%', right_code_delimiter='%>',
##         right_escaped='%',  # For example: "<%%" evaluates to "<%"
##         template_context_default_indent=4,
##         builtins=(builtins.all, builtins.filter, builtins.map,
##                   builtins.enumerate, builtins.range, builtins.locals),
##         pretty_indent=False, **keywords: builtins.object
##     ) -> Self:
    def _initialize(
        self, template, string=False,
        placeholder_name_pattern='[a-zA-Z0-9_\[\]\'"\.()\\\\,\-+ :/={}]+',
        command_line_placeholder_name_pattern='(?s)'
                                              '[a-zA-Z0-9_\[\]\.(),\-+]+',
        placeholder_pattern='{left_delimiter}[ \t]*'
                            '(?P<variable_name>{placeholder})[ \t]'
                            '*{right_delimiter}',
        template_pattern='(?m)(?P<ESCAPED_DELIMITER>'
                         '(?P<before_escaped>'  # in brackets
                         '(?P<indent_escaped>[ \t]*)'  # in two brackets
                         '(?!{left_delimiter})'  # in two brackets
                         '(?:.(?!{left_delimiter}))*?.?'  # in two brackets
                         ')?{left_delimiter}{right_escaped}'  # in brackets
                         '(?P<escaped_end>\n?)'  # in brackets
                         ')|(?P<PLACEHOLDER>'
                         '(?P<before_placeholder>'  # in brackets
                         '(?P<indent_placeholder>[ \t]*)'  # in two brackets
                         '(?!{left_delimiter})'  # in two brackets
                         '(?:.(?!{left_delimiter}))*?.?'  # in two brackets
                         ')?{left_delimiter}[ \t]*'  # in brackets
                         '(?P<placeholder>{placeholder})'  # in brackets
                         '[ \t]*'  # in brackets
                         '{right_delimiter}'  # in brackets
                         '(?P<placeholder_end>\n?)'  # in brackets
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
                         '(?P<none_code_end>\n|$)'  # in brackets
                         ')|(?P<EMPTY_LINE>^(?P<indent_line>[ \t]*)\n)',
        command_line_placeholder_pattern='^(?P<variable_name>{placeholder})'
                                         '(?P<separator>.)(?P<value>.+)$',
        native_template_pattern='<%[ \t]*(?:'
                                '(?P<escaped>%)|'  # in brackets
                                '(?:(?P<named>[a-zA-Z0-9_]+)'  # in brackets
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
        builtins=(builtins.all, builtins.filter, builtins.map,
                  builtins.enumerate, builtins.range, builtins.locals),
        pretty_indent=False, **keywords
    ):
##
        '''
            Initializes output buffer and template scope.
            NOTE: "(?s...)" and "(?m...)" is equivalent for regular expression
            flag "re.DOTALL" and "re.MULTILINE".
            NOTE: This regular expression patterns assumes that the delimiter
            has at least a length of two.

            Documentation of template pattern:

                Line 1-3: Escaped None code
                Line 4-8: Placeholder
                Line 9-10: Code
                Line 11-12: None code
                Line 13: Empty Line
        '''
        '''Make needed runtime properties to instance properties.'''
        self._new_line = self.__class__._new_line
        self._indent = self.__class__._indent
        self._count_lines = self.__class__._count_lines
        self._count_no_lines = self.__class__._count_no_lines
        self._current_rendered_content_line_number = \
            self.__class__._current_rendered_content_line_number
        self._code_dependend_indents = self.__class__._code_dependend_indents
        self._line_shifts = self.__class__._line_shifts
        self._empty_lines = self.__class__._empty_lines

        self.right_escaped = right_escaped

        self._pretty_indent = pretty_indent
        self._placeholder_name_pattern = placeholder_name_pattern
        self._command_line_placeholder_name_pattern = \
            command_line_placeholder_name_pattern
        self._left_code_delimiter = left_code_delimiter
        self._right_code_delimiter = right_code_delimiter
        self._placeholder_pattern = placeholder_pattern
        self._template_context_default_indent = template_context_default_indent
        self._template_pattern = template_pattern
        self._command_line_placeholder_pattern = \
            command_line_placeholder_pattern
        self._native_template_pattern = native_template_pattern
        self._output = Buffer()
        return self._set_builtins(builtins)._load_template(template, string)

            # endregion

    @JointPoint
## python3.3
##     def _set_builtins(
##         self: Self, builtins: collections.Iterable
##     ) -> Self:
    def _set_builtins(self, builtins):
##
        '''
            Generates a dictionary representing the templates scope from given
            defined builtins.
        '''
        '''
            NOTE: Necessary to make "self._builtins" an instance
            (not only class) variable.
        '''
        self._builtins = {}
        for builtin in builtins:
            self._builtins[builtin.__name__] = builtin
        return self

    @JointPoint
## python3.3     def _generate_scope_variables(self: Self) -> builtins.dict:
    def _generate_scope_variables(self):
        '''
            Generates scope variables given by the command line interface and
            embeds them into the template.

            Examples:

            >>> import argparse
            >>> tpl = Parser(template='hans', string=True)
            >>> tpl._command_line_arguments = argparse.Namespace(
            ...     scope_variables=('hans=peter', 'peter=hans'))
            >>> tpl._generate_scope_variables() # doctest: +ELLIPSIS
            {...'hans': 'peter'...}
        '''
        keywords = {}
        for variable in self._command_line_arguments.scope_variables:
            pattern = self._command_line_placeholder_pattern.format(
                placeholder=self._command_line_placeholder_name_pattern)
            match = re.compile(pattern).match(variable)
            if match:
                keywords.update(
                    {match.group('variable_name'): match.group('value')})
            else:
                raise __exception__(
                    'Given placeholder value tuple "%s" couldn\'t be parsed. '
                    'Your string have to match "%s".', variable, pattern)
        return keywords

    @JointPoint
## python3.3
##     def _load_template(
##         self: Self, template: (builtins.str, FileHandler),
##         string: builtins.bool
##     ) -> Self:
    def _load_template(self, template, string):
##
        '''
            Load the given template into ram for rendering.

            "template" the given template as file path or string.
            "is_string" determines if the "template" should be interpreted as
                        string or file path.

            Examples:

            >>> tpl = Parser(
            ...     template='hans', string=True)
            >>> tpl._load_template(template=tpl.content, string=True)
            Object of "Parser" with template "hans".
        '''
        if string:
            self.content = template
        else:
            self.file = FileHandler(location=template, must_exist=False)
            if not self.file.is_file():
                self.file = FileHandler(
                    location=template + '.tpl', must_exist=False)
            if not self.file.is_file():
                raise __exception__(
                    'No suitable template found with given name "%s" in "%s".',
                    template, self.file.directory_path)
            self.content = self.file.content
        self.native_template_object = native_string.Template(self.content)
        self.native_template_object.pattern = re.compile(
            self._native_template_pattern)
        self.native_template_object.delimiter = self._left_code_delimiter
        return self

    @JointPoint
## python3.3
##     def _run_template(self: Self, template_scope: builtins.dict) -> Self:
    def _run_template(self, template_scope):
##
        '''
            Runs the compiled template in its given scope.
            All error will be cached and error messages depending on source
            template will be derived on produced exceptions based in the
            compiled template.
        '''
        template_scope.update({'__builtins__': self.builtins})
        try:
## python3.3
##             builtins.exec(self.rendered_content, template_scope)
            exec(self.rendered_content, template_scope)
##
        except __exception__ as exception:
            '''Propagate nested template exceptions.'''
            line_number = self._get_exception_line(exception)
            rendered_content = ''
            if not builtins.hasattr(exception, 'has_template_info'):
                rendered_content = (
                    '\nrendered content:\n-----------------\n\n%s\n' %
                    self.represent_rendered_content())
## python3.3
##             raise __exception__(
##                 'Error with %s in include statement in line %s '
##                 '(line in compiled template: %s).\n%s: %s',
##                 self._determine_template_description(),
##                 line_number[0], line_number[1], __exception__.__name__,
##                 builtins.str(exception)
##             ) from None
            raise __exception__(
                'Error with %s in include statement in line %s '
                '(line in compiled template: %s).\n%s: %s%s',
                self._determine_template_description(),
                line_number[0], line_number[1], __exception__.__name__,
                builtins.str(exception), rendered_content)
##
        except builtins.Exception as exception:
            line_info, exception_message, native_exception_description = \
                self._handle_template_exception(exception)
            self._raise_template_exception(
                line_info, exception_message, native_exception_description,
                native_exception=exception)
        '''Make sure that all outputs during template execution are done.'''
        sys.stdout.flush()
        return self

    @JointPoint
## python3.3
##     def _handle_template_exception(
##         self: Self, exception: builtins.Exception
##     ) -> builtins.tuple:
    def _handle_template_exception(self, exception):
##
        '''
            If an exception is raising during running generated template
            (python) code this methods will handle it to map exception line
            number to template's source code line number.
        '''
        line_info = ''
        exception_message = '%s: %s' % (
            exception.__class__.__name__,
            String(exception).camel_case_capitalize().replace(
                "'", '"'
            ).content)
        line_number = self._get_exception_line(exception)
        if line_number:
            line_info = ' in line %d (line in compiled template: %d)' %\
                (line_number[0], line_number[1])
        native_exception_description = ''
        if sys.flags.debug or __logger__.isEnabledFor(logging.DEBUG):
            for property in builtins.dir(exception):
                if not (property.startswith('__') and property.endswith('__')):
                    native_exception_description += \
                        property + ': "' + builtins.str(
                            builtins.getattr(exception, property)
                        ) + '"\n'
            native_exception_description = (
                '\n\nNative exception object:\n\n%s' %
                native_exception_description)
        return line_info, exception_message, native_exception_description

    @JointPoint
## python3.3
##     def _determine_template_description(self: Self) -> builtins.str:
    def _determine_template_description(self):
##
        '''Determines a useful description for current template.'''
        if self.file:
            return '"%s"' % self.file.path
        return 'given template string'

    @JointPoint
## python3.3
##     def _raise_template_exception(
##         self: Self, line_info: builtins.str,
##         exception_message: builtins.str,
##         native_exception_description: builtins.str,
##         native_exception: builtins.Exception
##     ) -> None:
    def _raise_template_exception(
        self, line_info, exception_message, native_exception_description,
        native_exception
    ):
##
        '''
            Performs a wrapper exception for exception raising in template
            context.
        '''
        rendered_content = ''
        if sys.flags.debug or __logger__.isEnabledFor(logging.DEBUG):
            rendered_content = '\nrendered content:\n\n%s\n' % \
                self.represent_rendered_content()
## python3.3
##         exception = __exception__(
##             'Error with {template_description}{line_info}.\n'
##             '{exception_message}{native_exception_description}'
##             '{rendered_content}'.format(
##                 template_description=self._determine_template_description(),
##                 line_info=line_info,
##                 exception_message=exception_message,
##                 native_exception_description=native_exception_description,
##                 rendered_content=rendered_content))
        exception = __exception__(
            'Error with {template_description}{line_info}.\n'
            '{exception_message}{native_exception_description}'
            '{rendered_content}'.format(
                template_description=self._determine_template_description(),
                line_info=line_info,
                exception_message=exception_message,
                native_exception_description=native_exception_description,
                rendered_content=rendered_content))
##
        exception.has_template_info = True
## python3.3         raise exception from None
        raise exception

    @JointPoint
## python3.3
##     def _get_exception_line(
##         self: Self, exception: builtins.Exception
##     ) -> builtins.tuple:
    def _get_exception_line(self, exception):
##
        '''
            Determines the line where the given exception was raised.
            If in the responsible line in compiled template was found, a tuple
            with the resulting line in source template and compiled template
            will be given back.
        '''
        '''
            Search traceback for a context ran from "builtins.exec()" and begin
            from the nearest context.
        '''
        line_number = self._determine_exec_string_exception_line(exception)
        for line_shift in self._line_shifts:
            line_number_in_python_code = line_shift[0] + line_shift[1]
            if line_number == line_number_in_python_code:
                return line_shift[0], line_number
            if line_number < line_number_in_python_code:
                return line_number - line_shift[1] + 1, line_number
        if line_number and self._line_shifts:
            return line_number - self._line_shifts[-1][1], line_number
        return line_number, line_number

    @JointPoint
## python3.3
##     def _determine_exec_string_exception_line(
##         self: Self, exception: builtins.Exception
##     ) -> builtins.int:
    def _determine_exec_string_exception_line(self, exception):
##
        '''
            Determines the line number where the exception (in exec statement)
            occurs from the given exception.
        '''
## python3.3
##         exception_traceback = traceback.extract_tb(exception.__traceback__)
        exception_traceback = traceback.extract_tb(sys.exc_info()[2])
##
        exception_traceback.reverse()
        for context in exception_traceback:
            if context[0] == '<string>':
                return context[1]
        if builtins.hasattr(exception, 'lineno'):
            return exception.lineno
        return 0

            # region wrapper methods for template context

    # NOTE: This method is heavily used during rendering. It should be as fast
    # as possible. So the JointPoint is deactivated.
    # @JointPoint
## python3.3
##     def _print(
##         self: Self, *arguments: builtins.object, indent=True,
##         indent_space='', **keywords: builtins.object
##     ) -> None:
    def _print(self, *arguments, **keywords):
##
        '''
            Represents the print function which will be used for all plain text
            wraps and print expressions by compiling the source template.

            Examples:

            >>> tpl = Parser(template='test', string=True)
            >>> tpl._print('hans')
            >>> tpl._print(' and klaus', end='\\n')
            >>> tpl._print('fritz is also present.', end='')
            >>> tpl.output
            'hans\\n and klaus\\nfritz is also present.'
        '''
        if self._pretty_indent:
## python3.3
##             pass
            keywords_dictionary = Dictionary(content=keywords)
            indent, keywords = keywords_dictionary.pop(
                name='indent', default_value=True)
            indent_space, keywords = keywords_dictionary.pop(
                name='indent_space', default_value='')
##
            if indent and indent_space:
                '''
                    If an indent level was given prepend given indent space to
                    each line.
                '''
                print_buffer = Buffer()
                codewords = copy.deepcopy(keywords)
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
## python3.3
##     def _include(
##         self: Self, template_file_path: builtins.str, scope={}, end='\n',
##         indent=True, indent_space='', **keywords: builtins.object
##     ) -> None:
    def _include(
        self, template_file_path, scope={}, end='\n', indent=True,
        indent_space='', **keywords
    ):
##
        '''
            Performs a template include. This method is implemented for using
            in template context.
        '''
        scope.update(keywords)
        root_path = ''
        if self.file:
            root_path = self.file.directory_path
        self._print(
            self.__class__(
                template=root_path + template_file_path
            ).render(mapping=scope).output,
            end=end, indent=indent, indent_space=indent_space)

            # endregion

            # region callback

    @JointPoint
## python3.3
##     def _render_code(
##         self: Self, match: builtins.type(re.compile('').match(''))
##     ) -> builtins.str:
    def _render_code(self, match):
##
        '''
            Helper method for rendering the source template file.
        '''
        if match.group():
            '''
                This has been sorted by their average frequency for improving
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
            if match.group('ESCAPED_DELIMITER'):
                return self._render_escaped_none_code_line(match)
        raise __exception__(
            'Given template "%s" isn\'t valid formated.', self.content)

                # endregion

                # region helper

    @JointPoint
## python3.3
##     def _render_empty_line(
##         self: Self, match: builtins.type(re.compile('').match(''))
##     ) -> builtins.str:
    def _render_empty_line(self, match):
##
        '''
            Handles empty lines.
        '''
        self._new_line = True
        self._count_lines += 1
        self._empty_lines.append(self._render_none_code(
            string=match.group('EMPTY_LINE'), end=''))
        return ''

    @JointPoint
## python3.3
##     def _render_none_code_line(
##         self: Self, match: builtins.type(re.compile('').match(''))
##     ) -> builtins.str:
    def _render_none_code_line(self, match):
##
        '''
            Handles none code.
        '''
        indent = self._get_code_indent(
            current_indent=match.group('indent_none_code'), mode='passiv')
        last_empty_lines = self._flush_empty_lines(indent)
        was_new_line = self._new_line
        self._new_line = False
        if match.group('none_code_end'):
            self._new_line = True
            self._count_lines += 1
        slice = 0
        if was_new_line and self._code_dependend_indents:
            slice = builtins.len(
                self._code_dependend_indents) * self.indent
        return last_empty_lines + indent + self._render_none_code(
            string=match.group('none_code')[slice:],
            end=self._get_new_line())

    @JointPoint
## python3.3
##     def _render_code_line(
##         self: Self, match: builtins.type(re.compile('').match(''))
##     ) -> builtins.str:
    def _render_code_line(self, match):
##
        '''Compiles a template python code line.'''
        was_new_line = self._new_line
        self._new_line = True
        self._count_lines += 1
        code_line = match.group('code').strip()
        mode = 'passiv'
        if code_line.endswith(':') and not code_line.startswith('#'):
            mode = 'activ'
        indent = self._get_code_indent(
            current_indent=match.group('indent_code'), mode=mode)
        code_line = self._save_output_method_indent_level(
            code_line, was_new_line, match)
        return self._flush_empty_lines(indent) + indent + code_line

    @JointPoint
## python3.3
##     def _save_output_method_indent_level(
##         self: Self, code_line: builtins.str, was_new_line: builtins.bool,
##         match: builtins.type(re.compile('').match(''))
##     ) -> builtins.str:
    def _save_output_method_indent_level(
        self, code_line, was_new_line, match
    ):
##
        '''
            Gives all output methods found in template code their indent level.
        '''
        if code_line.startswith('print(') or code_line.startswith('include('):
            slice = 0
            if was_new_line:
                slice = builtins.len(
                    self._code_dependend_indents
                ) * self.indent
            if code_line.startswith('print('):
                return self._handle_print_output_indent_level(
                    code_line, match, slice)
            return self._handle_include_output_indent_level(
                code_line, match, slice)
        return code_line

    @JointPoint
## python3.3
##     def _handle_include_output_indent_level(
##         self: Self, code_line: builtins.str,
##         match: builtins.type(re.compile('').match('')), slice: builtins.int
##     ) -> builtins.str:
    def _handle_include_output_indent_level(self, code_line, match, slice):
##
        '''
            Returns a string representing from include function call in
            generated python code with their indent level given.
        '''
        length_of_include_call = String(
            code_line[builtins.len('include('):]
        ).find_python_code_end_bracket()
        slice_position = builtins.len('include(') + length_of_include_call
        if code_line[builtins.len('include('):slice_position]:
            slice_position = builtins.len('include(') + \
                length_of_include_call + 1
            return (
                'include(' + code_line[builtins.len('include('):builtins.len(
                    'include('
                ) + length_of_include_call] + ", indent_space='" +
                match.group('indent_code')[slice:] + "')" +
                code_line[slice_position:])
        return (
            "include(indent_space='" + match.group('indent_code')[slice:] +
            "')" +
            code_line[builtins.len('include(') + length_of_include_call + 1:])

    @JointPoint
## python3.3
##     def _handle_print_output_indent_level(
##         self: Self, code_line: builtins.str,
##         match: builtins.type(re.compile('').match('')), slice: builtins.int
##     ) -> builtins.str:
    def _handle_print_output_indent_level(self, code_line, match, slice):
##
        '''
            Returns a string representing from print function call in
            generated python code with their indent level given.
        '''
        length_of_print_call = String(
            code_line[builtins.len('print('):]
        ).find_python_code_end_bracket()
        if(code_line[builtins.len('print('):builtins.len(
           'print(') + length_of_print_call]):
            return (
                'print(' + code_line[builtins.len('print('):builtins.len(
                    'print('
                ) + length_of_print_call] + ", indent_space='" +
                match.group('indent_code')[slice:] + "')" +
                code_line[builtins.len('print(') + length_of_print_call + 1:])
        return (
            "print(indent_space='" + match.group('indent_code')[slice:] +
            "')" +
            code_line[builtins.len('print(') + length_of_print_call + 1:])

    @JointPoint
## python3.3
##     def _render_escaped_none_code_line(
##         self: Self, match: builtins.type(re.compile('').match(''))
##     ) -> builtins.str:
    def _render_escaped_none_code_line(self, match):
##
        '''
            Handles escaped none code.
        '''
        indent = self._get_code_indent(
            current_indent=match.group('indent_escaped'), mode='passiv')
        last_empty_lines = self._flush_empty_lines(indent)
        was_new_line = self._new_line
        if match.group('escaped_end'):
            self._new_line = True
            self._count_lines += 1
        else:
            self._new_line = False
            self._count_no_lines += 1
            self._line_shifts.append((self._count_lines, self._count_no_lines))
        slice = 0
        if was_new_line:
            slice = builtins.len(self._code_dependend_indents) * self.indent
        content_before = match.group('before_escaped')[slice:]
        return last_empty_lines + indent + self._render_none_code(
            string=content_before + self._left_code_delimiter, end='')

    @JointPoint
## python3.3
##     def _render_placeholder(
##         self: Self, match: builtins.type(re.compile('').match(''))
##     ) -> builtins.str:
    def _render_placeholder(self, match):
##
        '''Handles placeholder.'''
        indent = self._get_code_indent(
            current_indent=match.group('indent_placeholder'), mode='passiv')
        last_empty_lines = self._flush_empty_lines(indent)
        if match.group('before_placeholder'):
            self._count_no_lines += 1
            self._line_shifts.append((self._count_lines, self._count_no_lines))
        was_new_line = self._new_line
        if match.group('placeholder_end'):
            self._new_line = True
            self._count_lines += 1
        else:
            self._new_line = False
            self._count_no_lines += 1
            self._line_shifts.append((self._count_lines, self._count_no_lines))
        before_placeholder = ''
        if match.group('before_placeholder'):
            '''
                Only cut code dependent indents if placeholder is
                the first statement in current line.
            '''
            slice = 0
            if was_new_line:
                slice = builtins.len(
                    self._code_dependend_indents) * self.indent
            before_placeholder = indent + self._render_none_code(
                string=match.group('before_placeholder')[slice:], end='')
        return (last_empty_lines + before_placeholder + indent + 'print(str(' +
                match.group('placeholder').strip() + ")%s, end='')\n" %
                ('+"\\n"' if self._get_new_line() else ''))

    @JointPoint
## python3.3
##     def _flush_empty_lines(
##         self: Self, indent: builtins.str
##     ) -> builtins.str:
    def _flush_empty_lines(self, indent):
##
        '''
            Flushes the empty line stack needed for right line mapping through
            template code and generated python code.
        '''
        result = ''
        for empty_line in self._empty_lines:
            result += indent + empty_line
        self._empty_lines = []
        return result

    @JointPoint
## python3.3     def _get_new_line(self: Self) -> builtins.str:
    def _get_new_line(self):
        '''
            Returns a new line string if necessary for the correct template
            compiling to native python code.
        '''
        if(self._new_line and
           self._count_lines != builtins.len(self.content.splitlines())):
            return '\n'
        return ''

    @JointPoint
## python3.3
##     def _get_code_indent(
##         self: Self, current_indent: (builtins.type(None), builtins.str),
##         mode='passiv'
##     ) -> builtins.str:
    def _get_code_indent(self, current_indent, mode='passiv'):
##
        '''
            Returns the right indent in code as string depending on the
            current indention level and context.

            "mode" can have three different states.
                passiv: This mode describes the ability to close or continue
                        the current context by their level of indention.
                activ: Means a new code depending context is open.
                       The following code is depended on this line.
        '''
        if current_indent is None:
            current_indent = ''
        indent = ''
        if self._code_dependend_indents:
            if self._new_line:
                slice = 0
                indents = builtins.enumerate(self._code_dependend_indents)
                for counter, dependend_indent in indents:
                    if(builtins.len(current_indent) >
                       builtins.len(dependend_indent)):
                        indent = (counter + 1) * ' '
                        slice = counter + 1
                '''Close code indent blocks.'''
                self._code_dependend_indents = \
                    self._code_dependend_indents[:slice]
            else:
                '''Prepend code dependent indent to get right context.'''
                indent = builtins.len(self._code_dependend_indents) * ' '
        if mode == 'activ':
            '''Expect a new dependent indented code block.'''
            self._code_dependend_indents.append(current_indent)
        return indent

    @JointPoint
## python3.3
##     def _render_none_code(
##         self: Self, string: builtins.str, end='\n'
##     ) -> builtins.str:
    def _render_none_code(self, string, end='\n'):
##
        '''
            Wraps a print function around plain text for compiling
            templates.
        '''
        delimiters = ("'", '"', "'''", '"""')
        counter = 0
        delimiter = delimiters[0]
        while delimiter in string:
            counter += 1
            delimiter = delimiters[counter]
            if counter + 1 == builtins.len(delimiters):
                string = string.replace('"""', '"\""')
                break
        if string.startswith(delimiter[0]):
            string = '\\' + string
        if string.endswith(delimiter[0]):
            string = string[0:-1] + '\\' + string[-1]
        return ("print(%s, end='')\n" % (
            delimiter + string.replace('\n', '\\n') +
            end.replace('\n', '\\n') + delimiter))

                # endregion

            # endregion

    # endregion

# endregion

# region footer

'''
    Preset some variables given by introspection letting the linter know what
    globale variables are available.
'''
__logger__ = __test_mode__ = __exception__ = __module_name__ = \
    __file_path__ = None
'''
    Extends this module with some magic environment variables to provide better
    introspection support. A generic command line interface for some code
    preprocessing tools is provided by default.
'''
Module.default(name=__name__, frame=inspect.currentframe())

# endregion
