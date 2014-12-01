#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# region header

'''
    Provides web api parsers and a simple webserver to offer the prepared data.
'''

# # python3.4
# # pass
from __future__ import absolute_import, division, print_function, \
    unicode_literals
# #

__author__ = 'Torben Sickert'
__copyright__ = 'see module docstring'
__credits__ = 'Torben Sickert',
__license__ = 'see module docstring'
__maintainer__ = 'Torben Sickert'
__maintainer_email__ = 't.sickert["~at~"]gmail.com'
__status__ = 'stable'
__version__ = '1.0'

from collections import Iterable
import inspect
import os

# # python3.4 pass
from boostNode import convert_to_string, convert_to_unicode
from boostNode.extension.file import Handler as FileHandler
from boostNode.extension.native import Dictionary, Module
from boostNode.runnable.template import Parser as TemplateParser
from boostNode.paradigm.objectOrientation import Class


# # python3.4
# # # NOTE: Should be removed if we drop python2.X support.
# # String = StringExtension
String = lambda content: StringExtension(convert_to_string(content))
# #

# endregion


# region constants

ROOT_PATH = '/'

# endregion


# region functions

# # region template parser

def TemplateParser__load_template(self):
    '''Load the given template into ram for rendering.'''
    if self.string:
        self.content = self.template
    else:
        if isinstance(self.template, FileHandler):
            path = ROOT_PATH + self.template.path
        else:
            path = ROOT_PATH + self.template
        path += '.tpl'
        if os.path.isfile(path):
            self.file = FileHandler(
                location='%s%s' % (self.template, '.tpl'),
                encoding=self.file_encoding)
        else:
            path = path[:-4]
            self.file = FileHandler(
                location=self.template, encoding=self.file_encoding)
        with open(path, 'r') as file:
            self.content = convert_to_unicode(file.read())
    return self
TemplateParser._load_template = TemplateParser__load_template


def TemplateParser_render(
    self, mapping={}, prevent_rendered_python_code=False, **keywords
):
    '''
        Renders the template. Searches for python code snippets and handles \
        correct indenting. Wraps plain text with a print function.
    '''
    if '<%' not in self.content:
        self.output = self.content
        return self
    mapping.update({'__builtins__': self.builtins})
    mapping.update(keywords)
    if self.cache:
        if self.string:
            template_hash = str(hash(self.content))
        else:
            template_hash = self.file.path.replace(os.sep, '_')
        if self.full_caching:
            full_cache_dir_path = ROOT_PATH + self.cache.path + \
                template_hash
            if not os.path.isdir(full_cache_dir_path):
                os.mkdir(full_cache_dir_path)
            '''
                NOTE: Hack to improve caching caused by no changing scope \
                values.
            '''
            if 'accountData' in mapping:
                del mapping['accountData']['lastUpdateDateTime']
                del mapping['accountData']['sessionExpirationDateTime']
            full_cache_file_path = '%s/%s.txt' % (
                full_cache_dir_path, str(hash(Dictionary(
                    content=mapping
                ).get_immutable(exclude=self._builtins.keys() + [
                    'userPropertyNames', 'options', 'templates',
                    'styleFileBasenames', 'availableOutputTemplateNames']))))
            if os.path.isfile(full_cache_file_path):
                with open(full_cache_file_path, 'r') as file:
                    self._output.content = file.read()
                return self
        cache_file_path = '%s%s.py' % (
            ROOT_PATH + self.cache.path, template_hash)
        if os.path.isfile(cache_file_path):
            execfile(cache_file_path, mapping)
        else:
            self.rendered_python_code = self._render_content()
            with open(cache_file_path, 'w') as file:
                file.write(convert_to_string(
                    '# -*- coding: utf-8 -*-\n' + self.rendered_python_code))
            exec(self.rendered_python_code, mapping)
        if self.full_caching:
            with open(full_cache_file_path, 'w') as file:
                file.write(self._output.content)
    else:
        self.rendered_python_code = self._render_content()
        self._run_template(
            prevent_rendered_python_code, template_scope=mapping)
    return self
TemplateParser.render = TemplateParser_render

# # endregion

# # region file handler

@Class.pseudo_property
def FileHandler_get_name(self, *arguments, **keywords):
    '''
        Determines the current file name without directory path. Same \
        possible parameters as native python method "os.path.name()".
    '''
    path = self.get_path(output_with_root_prefix=False)
    if len(path) and path.endswith(os.sep):
        path = path[:-len(os.sep)]
    return os.path.basename(path)
FileHandler.get_name = FileHandler_get_name

# # endregion

# # region native dictionary

def Dictionary_convert(
    self, key_wrapper=lambda key, value: key,
    value_wrapper=lambda key, value: value,
    no_wrap_indicator='__no_wrapping__', remove_wrap_indicator=True
):
    for key, value in self.content.items():
        if key == no_wrap_indicator:
            if remove_wrap_indicator:
                self.content = value
            else:
                self.content[key] = value
            return self
        del self.content[key]
        key = key_wrapper(key, value)
        if isinstance(value, dict):
            self.content[key] = self.__class__(value).convert(
                key_wrapper, value_wrapper, no_wrap_indicator,
                remove_wrap_indicator
            ).content
# # python3.4
# #         elif(isinstance(value, Iterable) and
# #              not isinstance(value, (bytes, str))):
        elif(isinstance(value, Iterable) and
             not isinstance(value, (unicode, str))):
# #
            self.content[key] = Dictionary__convert_iterable(
                self.__class__, iterable=value, key_wrapper=key_wrapper,
                value_wrapper=value_wrapper,
                no_wrap_indicator=no_wrap_indicator,
                remove_wrap_indicator=remove_wrap_indicator)
        else:
            self.content[key] = value_wrapper(key, value)
    return self
Dictionary.convert = Dictionary_convert


def Dictionary__convert_iterable(
    cls, iterable, key_wrapper, value_wrapper, no_wrap_indicator,
    remove_wrap_indicator
):
    '''
        Converts all keys or values and nested keys or values with given \
        callback function in a given iterable.
    '''
    if isinstance(iterable, set):
        return cls._convert_set(iterable, key_wrapper, value_wrapper)
# # python3.4
# #     if isinstance(iterable, range):
# #         iterable = list(iterable)
    pass
# #
    try:
        for key, value in enumerate(iterable):
            if isinstance(value, dict):
                iterable[key] = cls(value).convert(
                    key_wrapper, value_wrapper, no_wrap_indicator,
                    remove_wrap_indicator
                ).content
# # python3.4
# #             elif isinstance(value, Iterable) and not isinstance(value, (
# #                 bytes, str
# #             )):
            elif isinstance(value, Iterable) and not isinstance(value, (
                unicode, str
            )):
# #
                iterable[key] = Dictionary__convert_iterable(
                    cls, iterable=value, key_wrapper=key_wrapper,
                    value_wrapper=value_wrapper,
                    no_wrap_indicator=no_wrap_indicator,
                    remove_wrap_indicator=remove_wrap_indicator)
            else:
                iterable[key] = value_wrapper(key, value)
    except TypeError as exception:
        '''
            NOTE: We have visited a non indexable value (e.g. an uploaded
            file).
        '''
# # python3.4
# #         __logger__.debug(
# #             '%s: %s (%s)', exception.__class__.__name__,
# #             str(exception), type(iterable))
        __logger__.debug(
            '%s: %s (%s)', exception.__class__.__name__,
            convert_to_unicode(exception), type(iterable))
# #
    return iterable
Dictionary._convert_iterable = Dictionary__convert_iterable

# # endregion

# endregion

# region footer

'''
    Preset some variables given by introspection letting the linter know what \
    globale variables are available.
'''
__logger__ = __exception__ = __module_name__ = __file_path__ = \
    __test_mode__ = __test_buffer__ = __test_folder__ = __test_globals__ = \
    __request_arguments__ = None
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
