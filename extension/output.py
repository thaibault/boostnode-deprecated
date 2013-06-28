#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# region vim modline

# vim: set tabstop=4 shiftwidth=4 expandtab:
# vim: foldmethod=marker foldmarker=region,endregion:

# endregion

# region header

## python3.3 pass
from __future__ import print_function

'''
    This module provides classes for dealing with python's way to transport
    strings to any output stream.
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

## python3.3 import builtins
pass
import copy
import inspect
import logging
import multiprocessing
import os
import sys
import threading
## python3.3 import queue as native_queue
import Queue as native_queue

## python3.3 pass
builtins = sys.modules['__main__'].__builtins__

for number in (3, 4):
    sys.path.append(os.path.abspath(sys.path[0] + number * ('..' + os.sep)))

import boostNode.extension.dependent
import boostNode.extension.file
import boostNode.extension.type
import boostNode.paradigm.aspectOrientation
import boostNode.paradigm.objectOrientation

# endregion


# region classes

class Buffer(
    boostNode.paradigm.objectOrientation.Class, logging.StreamHandler
):
    '''
        This class represents a layer for writing and reading to an output
        buffer realized as file, queue or variable.

        Examples:

        >>> buffer = Buffer(file=__test_folder__ + 'buffer')
        >>> buffer.clear() # doctest: +ELLIPSIS
        '...'
        >>> print('hans', file=buffer, end='+')
        >>> buffer.content
        'hans+'
    '''

    # region dynamic properties

        # region public properties

    '''Saves the queue instance for writing content into.'''
    queue = None
    '''Saves the last written input.'''
    last_written = ''

        # endregion

        # region protected properties

    '''
        A lock object to guarantee that no other thread read from buffer
        during truncating or writing.
    '''
    _lock = None
    '''Saves the current buffer content.'''
    _content = ''
    '''Saves the file handler instance for writing content into.'''
    _file = None

        # endregion

    # endregion

    # region dynamic methods

        # region public methods

            # region special methods

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def __init__(
##         self: boostNode.extension.type.Self, file=None, queue=None,
##         support_multiprocessing=False
##     ) -> None:
    def __init__(
        self, file=None, queue=None, support_multiprocessing=False
    ):
##
        '''
            Saves the file path in the current instance. If "file" is "None"
            an instance variable is used as buffer.

            Examples:

            >>> Buffer(
            ...     file=__test_folder__ + 'buffer').file # doctest: +ELLIPSIS
            Object of "Handler" with path "...buffer" (file).
        '''
        self._lock = threading.Lock()
        if support_multiprocessing:
            self._lock = multiprocessing.Lock()
        self.queue = self._file = None
        self.last_written = ''
        self._content = ''
        if queue is not None:
            self.queue = native_queue.Queue()
            if support_multiprocessing:
                self.queue = multiprocessing.Queue()
            if(builtins.isinstance(queue, native_queue.Queue) or
               support_multiprocessing and
               builtins.isinstance(queue, multiprocessing.queues.Queue)):
                self.queue = queue
        elif file is not None:
            self._file = boostNode.extension.file.Handler(
                location=file, must_exist=False)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def __repr__(self: boostNode.extension.type.Self) -> builtins.str:
    def __repr__(self):
##
        '''
            Invokes if this object should describe itself by a string.

            Examples:

            >>> repr(Buffer())
            'Object of "Buffer" (memory buffered) with content "".'

            >>> buffer = Buffer(file=__test_folder__ + 'buffer')
            >>> buffer.write('hans') # doctest: +ELLIPSIS
            Object of "Buffer" (file buffered with "...buffer" (file)."...

            >>> repr(Buffer(queue=True))
            'Object of "Buffer" (queue buffered) with content "".'

            >>> repr(Buffer(queue=native_queue.Queue()))
            'Object of "Buffer" (queue buffered) with content "".'
        '''
        buffer_type = 'memory'
        type_addition = ''
        if self.file:
            buffer_type = 'file'
            type_addition = ' with "%s"' % builtins.repr(self.file)
        elif self.queue:
            buffer_type = 'queue'
        return 'Object of "{class_name}" ({type} buffered{type_addition}) '\
               'with content "{content}".'.format(
                   class_name=self.__class__.__name__, type=buffer_type,
                   type_addition=type_addition, content=self.content)

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def __str__(self: boostNode.extension.type.Self) -> builtins.str:
    def __str__(self):
##
        '''
            Invokes if this object is tried to interpreted as string.

            Examples:

            >>> str(Buffer().write('test'))
            'test'
        '''
        return self.content

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def __bool__(self: boostNode.extension.type.Self) -> builtins.bool:
    def __nonzero__(self):
##
        '''
            Invokes if this object is tried to interpreted as boolean.

            Examples:

            >>> bool(Buffer().write('test'))
            True

            >>> bool(Buffer())
            False
        '''
        return builtins.bool(self.content)

            # endregion

        # endregion

        # region getter methods

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def get_content(self: boostNode.extension.type.Self) -> builtins.str:
    def get_content(self):
##
        '''
            Getter for the current content.

            Examples:

            >>> Buffer().write('test').content
            'test'
        '''
        with self._lock:
            if self.file is not None:
                self._content = self.file.content
            elif self.queue:
                self._content = ''
                temp_buffer = []
                while not self.queue.empty():
                    temp_buffer.append(self.queue.get())
                    self._content += temp_buffer[-1]
                for content in temp_buffer:
                    self.queue.put(content)
        return self._content

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def get_file(
##         self: boostNode.extension.type.Self
##     ) -> (boostNode.extension.file.Handler, builtins.type(None)):
    def get_file(self):
##
        '''
            Getter for current file path if file buffering is selected.

            Examples:

            >>> Buffer(
            ...     file=__test_folder__ + 'buffer').file # doctest: +ELLIPSIS
            Object of "Handler" with path "...buffer" (undefined).

            >>> Buffer(file=__test_folder__ + 'buffer').write(
            ...     'test').file # doctest: +ELLIPSIS
            Object of "Handler" with path "...buffer" (file).
        '''
        if self._file and not self._file.is_file():
            raise __exception__(
                'Buffer isn\'t pointing to file ("{path}" is a '
                '{type}).'.format(path=self._file.path, type=self._file.type))
        return self._file

        # endregion

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def write(
##         self: boostNode.extension.type.Self, content: builtins.str
##     ) -> boostNode.extension.type.Self:
    def write(self, content):
##
        '''
            Writes content to the current output buffer file.
            If the current given file "Buffer.file"
            doesn't exists it will be created.

            Examples:

            >>> buffer = Buffer(file=__test_folder__ + 'buffer')
            >>> buffer.clear() # doctest: +ELLIPSIS
            '...'
            >>> buffer.write('hans') # doctest: +ELLIPSIS
            Object of "Buffer" (file buffered with "...buffer...nt "hans".
            >>> buffer.content
            'hans'

            >>> buffer = Buffer()
            >>> buffer.write('hans')
            Object of "Buffer" (memory buffered) with content "hans".
            >>> buffer.content
            'hans'
        '''
        with self._lock:
            self.last_written = content
            if self.file is not None:
                self.file.content += self.last_written
            elif self.queue:
                self.queue.put(self.last_written)
            else:
                self._content += self.last_written
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def flush(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def flush(self):
##
        '''
            Flush methods usually called to guarantee that all objects putted
            to "write()" are materialized on their provided media.
            This implementation exists only for compatibility reasons.

            Examples:

            >>> Buffer().flush()
            Object of "Buffer" (memory buffered) with content "".
        '''
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def clear(
##         self: boostNode.extension.type.Self, delete=True
##     ) -> builtins.str:
    def clear(self, delete=True):
##
        '''
            Removes the current output buffer content.

            Examples:

            >>> buffer = Buffer(file=__test_folder__ + 'buffer')
            >>> buffer.clear() # doctest: +ELLIPSIS
            '...'
            >>> buffer.write('hans') # doctest: +ELLIPSIS
            Objec...(file buffered with "...buffer...with content "hans".
            >>> buffer.clear()
            'hans'
            >>> buffer.content
            ''

            >>> buffer = Buffer()
            >>> buffer.write('hans')
            Object of "Buffer" (memory buffered) with content "hans".
            >>> buffer.clear()
            'hans'
            >>> buffer.content
            ''
        '''
        with self._lock:
            if self.file is not None:
                content = self.file.content
                if delete:
                    self.file.remove_file()
                else:
                    self.file.content = ''
            elif self.queue:
                content = ''
                while not self.queue.empty():
                    content += self.queue.get()
            else:
                content = self._content
                self._content = ''
        return content

    # endregion


class Print(boostNode.paradigm.objectOrientation.Class):
    '''
        Provids a high level printing class on top of pythons native print
        function.
    '''

    # region dynamic properties

        # region public properties

    '''
        Print this string before every first argument to every "put()"
        call.
    '''
    start = ''
    '''
        Print this string between every given element to one "put()" call.
    '''
    seperator = ' '
    '''
        Print this string after every last argument to every "put()" call.
    '''
    end = '\n'
    '''Redirect print output to this buffer.'''
    buffer = sys.stdout
    '''
        Redirect print output to this buffer if no buffer is defined for
        current instance.
    '''
    default_buffer = sys.stdout

        # endregion

    # endregion

    # region dynamic methods

        # region public methods

            # region special methods

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def __init__(
##         self: boostNode.extension.type.Self, *output: builtins.object,
##         **codewords: builtins.object
##     ) -> None:
    def __init__(self, *output, **codewords):
##
        '''
            Writes something to the output buffer or prints to standard
            output.

            "output" are the strings which should be printed or saved.
            "codewords" represents all possible optional arguments.
                "codeword['start']"
                "codeword['seperator']"
                "codeword['end']"
                "codeword['flush']"
                "codeword['buffer']" could be any instance as buffer which
                                     implements a "write()" method.

            Returns the given string or the last element if an iterable object
            was given.

            Examples:

            >>> Print.default_buffer = Buffer()
            >>> Print('hans', 'hans again') # doctest: +ELLIPSIS
            Object of "Print" with "Object of "Buffer" (mem... "hans hans again
            ".".

            >>> buffer = Buffer()
            >>> Print(
            ...     'hans,', 'peter', end=' and klaus', sep=' ', buffer=buffer
            ... ) # doctest: +ELLIPSIS
            Object of "Print" with "Object of "Buffer" (memory buffered...".".

            >>> buffer # doctest: +ELLIPSIS
            Object ... (memory buffered) with content "hans, peter and klaus".
        '''
        keywords = {'start': self.__class__.start,
                    'seperator': self.__class__.seperator,
                    'end': self.__class__.end,
                    'buffer': self.__class__.default_buffer,
                    'flush': False}
        keywords.update(codewords)
        self.buffer = keywords['buffer']
        output = builtins.list(output)
        for index, out in builtins.enumerate(output):
            if builtins.isinstance(out, native_queue.Queue):
                result = ''
                while not out.empty():
                    if index != 0 and keywords['seperator']:
                        result += builtins.str(keywords['seperator'])
                    result += builtins.str(out.get())
                output[index] = result
            elif index == 0:
                output[index] = builtins.str(out)
            else:
                output[index] = builtins.str(keywords['seperator']) +\
                    builtins.str(out)
        output = [keywords['start']] + output + [keywords['end']]
## python3.3
##         builtins.print(
##             *output, sep='', end='', file=keywords['buffer'],
##             flush=keywords['flush'])
        builtins.print(*output, sep='', end='', file=keywords['buffer'])
        if keywords['flush']:
            sys.stdout.flush()
##

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def __str__(self: boostNode.extension.type.Self) -> builtins.str:
    def __str__(self):
##
        '''
            Is triggered if this object should be converted to string.

            Examples:

            >>> str(Print('peter', buffer=Buffer()))
            'peter\\n'
        '''
        if builtins.isinstance(self.buffer, Buffer):
            return builtins.str(self.buffer)
        return ''

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def __repr__(self: boostNode.extension.type.Self) -> builtins.str:
    def __repr__(self):
##
        '''
            Invokes if this object should describe itself by a string.

            Examples:

            >>> repr(Print(buffer=Buffer())) # doctest: +ELLIPSIS
            'Object of "Print" with "Object of "Buffer"..." and default "Ob...'
        '''
        return 'Object of "{class_name}" with "{buffer}" and default '\
               '"{default_buffer}".'.format(
                   class_name=self.__class__.__name__,
                   buffer=builtins.repr(self.buffer),
                   default_buffer=builtins.repr(self.__class__.default_buffer))

            # endregion

        # endregion

    # endregion


class Logger(boostNode.paradigm.objectOrientation.Class):
    '''
        This class provides handling with all components dealing with
        logger object. It stores all logger components in a single
        data structure.
    '''

    # region dynamic properties

        # region public properties

    '''Defining all default components of the logger objects.'''
    default_level = 'critical',
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    terminator = '\n',
    buffer = sys.stdout,
    instances = []

        # endregion

    # endregion

    # region static methods

        # region public methods

            # region special methods

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def __str__(cls: boostNode.extension.type.SelfClass) -> builtins.str:
    def __str__(cls):
##
        '''
            Is triggered if a "Logger" object should be converted to string.

            Examples:

            >>> str(Logger()) # doctest: +ELLIPSIS
            ''
        '''
        if builtins.isinstance(cls.buffer, Buffer):
            return builtins.str(cls.buffer)
        return ''

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def __repr__(cls: boostNode.extension.type.SelfClass) -> builtins.str:
    def __repr__(cls):
##
        '''
            Invokes if this object should describe itself by a string.

            Examples:

            >>> repr(Logger()) # doctest: +ELLIPSIS
            '...Logger...logger "...", handler "...", formatter "..." and ...'
        '''
        counter = 1
        logger_string = handler_string = formatter_string = ''
        for logger, handler, formatter in cls.instances:
            start = '"'
            end = '"'
            if counter == builtins.len(cls.instances):
                start = 'and "'
                end = ''
            elif counter == 0:
                end = start = ''
            logger_string += start + builtins.repr(logger) + end
            handler_string += start + builtins.repr(handler) + end
            formatter_string += start + builtins.repr(formatter) + end
            counter += 1
        return ('Object of "{class_name}" with logger "{logger}", handler '
                '"{handler}", formatter "{formatter}" and buffer '
                '"{buffer}".'.format(
                    class_name=cls.__name__, logger=logger_string,
                    handler=handler_string, formatter=formatter_string,
                    buffer=builtins.repr(cls.buffer)))

            # endregion

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def flush(
##         cls: boostNode.extension.type.SelfClass
##     ) -> boostNode.extension.type.SelfClass:
    def flush(cls):
##
        '''
            Flushes all buffers in all logger handlers.
        '''
        for logger in cls.instances:
            for handler in logger.handlers:
                handler.stream.flush()
        return cls

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def get(
##         cls: boostNode.extension.type.SelfClass, name=__name__, level=(),
##         buffer=(), terminator=(), format=()
##     ) -> logging.getLoggerClass():
    def get(
        cls, name=__name__, level=(), buffer=(), terminator=(), format=()
    ):
##
        '''
            Returns a new or existing instance of a logger with given
            properties. If a logger was already registered under given name
            the existing instance is given back and a new instance otherwise.

            Examples:

            >>> logger_a = Logger.get('test', buffer=(__test_buffer__,))
            >>> logger_b = Logger.get('test')
            >>> logger_a is logger_b
            True

            >>> __test_buffer__.clear() # doctest: +ELLIPSIS
            '...'
            >>> logger_a.critical('Log some information.')
            >>> __test_buffer__.content # doctest: +ELLIPSIS
            '... - test - CRITICAL - Log some information.\\n'
        '''
        for logger in cls.instances:
            if logger.name == name:
                if level or buffer or terminator or format:
                    cls.instances[cls.instances.index(
                        logger
                    )] = cls._generate_logger(
                        name, level, buffer, terminator, format)
                return logger
        cls.instances.append(cls._generate_logger(
            name, level, buffer, terminator, format))
        return cls.instances[-1]

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def change_all(
##         cls: boostNode.extension.type.SelfClass, level=(), buffer=(),
##         terminator=(), format=()
##     ) -> boostNode.extension.type.SelfClass:
    def change_all(cls, level=(), buffer=(), terminator=(), format=()):
##
        '''
            This method changes the given properties to all created logger
            instances and saves the given properties as default properties for
            future created logger instances.

            Note that every argument except buffer setted to "None" will not
            edit this logger component. If you don't want to change buffer
            leave it "False".

            Examples:

            >>> Logger.change_all() # doctest: +ELLIPSIS
            <class ...Logger...>
        '''
        cls._set_properties(level, buffer, terminator, format)
        for index, logger in builtins.enumerate(cls.instances):
## python3.3             new_handler = logger.handlers.copy()
            new_handler = copy.copy(logger.handlers)
            if buffer:
                new_handler = []
                for new_buffer in cls.buffer:
                    new_handler.append(logging.StreamHandler(
                        stream=new_buffer))
            for handler, level, terminator, format in builtins.zip(
                new_handler, cls.default_level, cls.terminator, cls.format
            ):
                handler.setFormatter(logging.Formatter(format))
                handler.terminator = terminator
                handler.setLevel(level.upper())
            for handler in logger.handlers:
                logger.removeHandler(handler)
            for handler in new_handler:
                logger.addHandler(handler)
            logger.setLevel(builtins.getattr(
                logging, cls.default_level[0].upper()))
        return cls

        # endregion

        # region protected  methods

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _set_properties(
##         cls: boostNode.extension.type.SelfClass, level: builtins.tuple,
##         buffer: builtins.tuple, terminator: builtins.tuple,
##         format: builtins.tuple
##     ) -> boostNode.extension.type.SelfClass:
    def _set_properties(cls, level, buffer, terminator, format):
##
        '''
            This method sets the class properties.
        '''
        if level:
            cls.default_level = level
        if buffer:
            cls.buffer = buffer
        if terminator:
            cls.terminator = terminator
        if format:
            cls.format = format
        return cls

    @boostNode.paradigm.aspectOrientation.JointPoint(builtins.classmethod)
## python3.3
##     def _generate_logger(
##         cls: boostNode.extension.type.SelfClass, name: builtins.str,
##         level: builtins.tuple, buffer: builtins.tuple,
##         terminator: builtins.tuple, format: builtins.tuple
##     ) -> logging.getLoggerClass():
    def _generate_logger(cls, name, level, buffer, terminator, format):
##
        '''
            Creates a new logger instance by initializing all its components
            with given arguments or default properties saved as class
            properties.
        '''
        if not level:
            level = cls.default_level
        if not buffer:
            buffer = cls.buffer
        if not terminator:
            terminator = cls.terminator
        if not format:
            format = cls.format
        for handler in logging.getLogger(name).handlers:
            logging.getLogger(name).removeHandler(handler)
        logger = logging.getLogger(name)
        for _buffer, _terminator, _level, _format in builtins.zip(
            buffer, terminator, level, format
        ):
            handler = logging.StreamHandler(stream=_buffer)
            handler.terminator = _terminator
            handler.setLevel(_level.upper())
            handler.setFormatter(logging.Formatter(_format))
            logger.addHandler(handler)
        '''Set meta logger level to first given level.'''
        logger.setLevel(builtins.getattr(logging, level[0].upper()))
        return logger

        # endregion

    # endregion

# endregion

# region footer

'''Resolve cyclic dependency issues.'''
boostNode.extension.dependent.Resolve(
    name=__name__, frame=inspect.currentframe(), default_caller=False)

# endregion