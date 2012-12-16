#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# region header

'''
    Provides a web-browser-based technology to show web-pages as desktop
    window.
'''
'''Conventions: see "../__init__.py"'''

__author__ = 'Torben Sickert'
__copyright__ = 'see ../__init__.py'
__credits__ = ('Torben Sickert',)
__maintainer__ = 'Torben Sickert'
__maintainer_email__ = 't.sickert@gmail.com'
__status__ = 'stable'
__version__ = '1.0'

## python3.3 import builtins
pass
import collections
import inspect
import os
import re
import sys
## python3.3 import types
pass
import webbrowser

## python3.3 pass
builtins = sys.modules['__main__'].__builtins__

try:
    '''Note: Web cache is stored in "~/.cache/webkitgtk/applications/"'''
    import gtk
    import webkit
except builtins.ImportError:
    gtk = None
try:
    import PyQt4.QtCore
    import PyQt4.QtWebKit
    import PyQt4.QtGui
except builtins.ImportError:
    qt = None
else:
    qt = True

sys.path.append(os.path.abspath(sys.path[0] + 3 * ('..' + os.sep)))
sys.path.append(os.path.abspath(sys.path[0] + 4 * ('..' + os.sep)))

import library.extension.native
import library.extension.system
import library.extension.type
import library.paradigm.aspectOrientation
import library.paradigm.objectOrientation

# endregion


# region classes

class Browser(
    library.paradigm.objectOrientation.Class,
    library.extension.system.Runnable
):
    '''
        Provides a webkit browser without any browser typical visual
        properties. Its only a very simple window for showing web pages.
        The main goal is to make a web-interface look and behave like
        a real desktop application.
    '''

    # region constant properties

        # region public properties

    '''
        Holds all command line interface argument informations.
    '''
    COMMAND_LINE_ARGUMENTS = (
        {'arguments': ('url',),
         'keywords': {
             'action': 'store',
             #'required': False,
             'help': 'Select an url to request and interpret with the '
                     'web browser.',
             #'dest': 'url',
             'metavar': 'URL'}},
        {'arguments': ('-w', '--width'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'choices': builtins.range(1, 50000),
             'required': False,
             'help': 'Defines the width of the given window in pixel.',
             'dest': 'width_in_pixel',
             'metavar': 'NUMBER_OF_PIXELS'}},
        {'arguments': ('-y', '--height'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'choices': builtins.range(1, 50000),
             'required': False,
             'help': 'Defines the height of the given window in pixel.',
             'dest': 'height_in_pixel',
             'metavar': 'NUMBER_OF_PIXELS'}},
        {'arguments': ('-f', '--fullscreen'),
         'keywords': {
             'action': 'store_true',
             'default': {'execute': '__initializer_default_value__'},
             'help': 'If set window will be started in fullscreen.',
             'dest': 'fullscreen'}},
        {'arguments': ('-n', '--no-window-decoration'),
         'keywords': {
             'action': 'store_true',
             'default': {'execute': '__initializer_default_value__'},
             'help': 'If set no window decoration (e.g. title bar) will be '
                     'shown.',
             'dest': 'no_window_decoration'}},
        {'arguments': ('-g', '--default-gui-toolkit'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': builtins.str,
             'choices': {'execute': 'self._determine_gui_toolkits()'},
             'required': False,
             'help': 'Defines default toolkit. Others will only run as '
                     'fallback.',
             'dest': 'default_gui_toolkit',
             'metavar': 'GUI_TOOLKIT'}},
        {'arguments': ('-b', '--no-progress-bar'),
         'keywords': {
             'action': 'store_true',
             'default': False,
             'help': 'If set no progress bar for showing website rendering '
                     'state is shown.',
             'dest': 'no_progress_bar'}},
        {'arguments': ('-d', '--default-title'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': False,
             'help': 'Defines which string should be shown in window '
                     'decoration if no site with title node was loaded.',
             'dest': 'default_title',
             'metavar': 'TITLE'}},)

        # endregion

    # endregion

    # region dynamic properties

        # region public properties

    '''Dynamic runtime objects for constructing a simple web window.'''
    window = scroller = vbox = progress_bar = browser = None
    '''
        Saves all initialized instances of this class.
    '''
    webview_instances = []

        # endregion

        # region protected properties

    '''If set gtk will be prefered to show webview otherwise qt.'''
    _default_gui_toolkit = ''
    '''Holds the current url location.'''
    _url = ''
    '''Defines dimensions of webview.'''
    _width_in_pixel = 0
    _height_in_pixel = 0
    _fullscreen = False
    _no_window_decoration = False
    '''A list of functions or methods called when window is closed.'''
    _close_handler = []
    '''If setted "True" window will be closed on next gtk main iteration.'''
    _gtk_close = False
    '''Defines weather a progress bar for page loading should be shown.'''
    _no_progress_bar = False
    '''Defines which gui toolkit should be used.'''
    _gui_toolkit = ''
    '''Saves the default title if no title was set via markup.'''
    _default_title = ''

        # endregion

    # endregion

    # region dynamic methods

        # region public methods

            # region special methods

    @library.paradigm.aspectOrientation.JointPoint
## python3.3
##     def __repr__(self: library.extension.type.Self) -> builtins.str:
    def __repr__(self):
##
        '''
            Invokes if this object should describe itself by a string.

            Examples:

            >>> repr(Browser(
            ...     url='http://www.google.de/', width_in_pixel=300,
            ...     height_in_pixel=100
            ... )) # doctest: +ELLIPSIS
            'Object of "Browser" with url "http://www.google... x 100 pixel...'
        '''
        return 'Object of "{class_name}" with url "{url}" in {width} pixel x '\
               '{height} pixel and gui toolkit "{gui_toolkit}".'.format(
                   class_name=self.__class__.__name__, url=self._url,
                   width=self._width_in_pixel, height=self._height_in_pixel,
                   gui_toolkit=self.gui_toolkit)

            # endregion

            # region getter methods

    @library.paradigm.aspectOrientation.JointPoint
## python3.3
##     def get_gui_toolkit(self: library.extension.type.Self) -> builtins.str:
    def get_gui_toolkit(self):
##
        '''
            Determines available gui toolkit.
        '''
        if not self._default_gui_toolkit:
            return 'undefined'
        elif self._default_gui_toolkit == 'default':
            return self._default_gui_toolkit
        elif builtins.globals()[self._default_gui_toolkit] is not None:
            return self._default_gui_toolkit
        elif qt:
            return 'qt'
        elif gtk:
            return 'gtk'
        return 'default'

            # endregion

            # region setter methods

    @library.paradigm.aspectOrientation.JointPoint
## python3.3
##     def set_url(
##         self: library.extension.type.Self, url: builtins.str
##     ) -> builtins.str:
    def set_url(self, url):
##
        '''
            Setter for current url.
        '''
        if re.compile('^[a-zA-Z]+://.*$').match(url):
            self._url = url
        else:
            self._url = 'http://' + url
        return self._url

    @library.paradigm.aspectOrientation.JointPoint
## python3.3
##     def set_close_handler(
##         self: library.extension.type.Self,
##         handler: (collections.Iterable, types.FunctionType,
##                   types.MethodType)
##     ) -> builtins.list:
    def set_close_handler(self, handler):
##
        '''
            Setter for close handler. Methods in the close handler list will
            be called before gtk is closed.
        '''
        if builtins.isinstance(handler, collections.Iterable):
            self._close_handler = builtins.list(handler)
        else:
            self._close_handler = [handler]
        return self._close_handler

            # endregion

    @library.paradigm.aspectOrientation.JointPoint
## python3.3
##     def close(
##         self: library.extension.type.Self
##     ) -> library.extension.type.Self:
    def close(self):
##
        '''
            Closes all created webviews. Note that in case of using the default
            installed browser fallback this instance couldn't be destroyed.
        '''
        self._gtk_close = True
        if self.gui_toolkit == 'qt':
            self.window.closeAllWindows()
        return self

        # endregion

        # region protected methods

            # region runnable implementation

    @library.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _run(
##         self: library.extension.type.Self
##     ) -> library.extension.type.Self:
    def _run(self):
##
        '''
            Entry point for command line call of this progam.
            Initializes all window and webkit components.

            Examples:

            >>> Browser(
            ...     url='http://www.google.com/', width_in_pixel=300,
            ...     height_in_pixel=100) # doctest: +ELLIPSIS
            Object of "Browser" with url "http://www.google.com/" in 300 pi...
        '''
        return self._initialize(**self._command_line_arguments_to_dictionary(
            namespace=library.extension.system.CommandLine.argument_parser(
                module_name=__name__, scope={'self': self},
                arguments=self.COMMAND_LINE_ARGUMENTS)))

    @library.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _initialize(
##         self: library.extension.type.Self, url: builtins.str,
##         width_in_pixel=800, height_in_pixel=600, fullscreen=False,
##         no_window_decoration=False, default_gui_toolkit='qt',
##         no_progress_bar=False, default_title='No gui loaded.',
##         close_handler=None, **keywords: builtins.object
##     ) -> library.extension.type.Self:
    def _initialize(
            self, url, width_in_pixel=800, height_in_pixel=600,
            fullscreen=False, no_window_decoration=False,
            default_gui_toolkit='qt', no_progress_bar=False,
            default_title='No gui loaded.', close_handler=None, **keywords):
##
        '''
            Initializes a webview or tries to open a default browser if
            no gui suitable gui toolkit is available.
        '''
        if close_handler is not None:
            self.close_handler = close_handler
        self.url = url
        self._width_in_pixel = width_in_pixel
        self._height_in_pixel = height_in_pixel
        self._fullscreen = fullscreen
        self._no_window_decoration = no_window_decoration
        self._default_gui_toolkit = default_gui_toolkit
        self._no_progress_bar = no_progress_bar
        self.__class__.webview_instances.append(self)
        __logger__.info('Start webgui with "%s"', self.gui_toolkit)
        if not __test_mode__:
            builtins.getattr(
                self, '_initialize_%s_browser' % self.gui_toolkit)()
        return self

            # endregion

            # region native webview components

    @library.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _initialize_default_browser(
##         self: library.extension.type.Self
##     ) -> library.extension.type.Self:
    def _initialize_default_browser(self):
##
        '''
            Starts the default browser with currently stored url.
        '''
        self.browser = webbrowser
        self.browser.open(self._url)
        return self

    @library.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _initialize_qt_browser(
##         self: library.extension.type.Self
##     ) -> library.extension.type.Self:
    def _initialize_qt_browser(self):
##
        '''
            Starts the qt webkit webview thread.
        '''
        self.window = PyQt4.QtGui.QApplication(sys.argv)
        self.browser = PyQt4.QtWebKit.QWebView()
        if self._no_window_decoration:
            self.browser.setWindowFlags(PyQt4.QtCore.Qt.CustomizeWindowHint)
        if self._fullscreen:
            self.browser.showFullScreen()
        self.browser.load(PyQt4.QtCore.QUrl(self._url))
        self.browser.show()
        self.browser.setWindowTitle(self._default_title)
        self.browser.titleChanged.connect(self._on_qt_title_changed)
        self.browser.resize(self._width_in_pixel, self._height_in_pixel)
        self._initialize_qt_progress_bar().window.lastWindowClosed.connect(
            self._on_qt_close)
        self.window.exec_()
        return self

    @library.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _initialize_qt_progress_bar(
##         self: library.extension.type.Self
##     ) -> library.extension.type.Self:
    def _initialize_qt_progress_bar(self):
##
        '''
            Initializes the progress bar for qt on bottom of the window for
            showing current state of website rendering.
        '''
        if not self._no_progress_bar:
            self.progress_bar = PyQt4.QtGui.QProgressBar()
            self.progress_bar.setMinimum(1)
            self.progress_bar.setMaximum(100)
            self.progress_bar.setTextVisible(False)
            self.progress_bar.setVisible(False)

            main_layout = PyQt4.QtGui.QGridLayout()
            main_layout.addWidget(self.progress_bar)
            main_layout.setAlignment(PyQt4.QtCore.Qt.AlignBottom)
            main_layout.setMargin(0)

            self.browser.setLayout(main_layout)
            self.browser.loadStarted.connect(self._on_qt_load_started)
            self.browser.loadProgress.connect(
                self._on_qt_load_progress_changed)
            self.browser.loadFinished.connect(self._on_qt_load_finished)
        return self

    @library.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _initialize_gtk_browser(
##         self: library.extension.type.Self
##     ) -> library.extension.type.Self:
    def _initialize_gtk_browser(self):
##
        '''
            Sets various event-handlers for browser and window objects.
        '''
        self.window = gtk.Window()
        self.vbox = gtk.VBox()
        self.scroller = gtk.ScrolledWindow()
        self.browser = webkit.WebView()
        self.browser.connect('title-changed', self._on_gtk_title_changed)
        self.vbox.pack_start(self.scroller)
        self._initialize_gtk_progress_bar().scroller.add(self.browser)
        self.browser.open(self._url)
        self.window.connect('delete_event', self._on_gtk_close)
        self.window.add(self.vbox)
        self.window.set_title(self._default_title)
        self.window.resize(
            width=self._width_in_pixel, height=self._height_in_pixel)
        if self._fullscreen:
            self.window.fullscreen()
        if self._no_window_decoration:
            self.window.set_decorated(False)
        self.window.show_all()
        gtk.idle_add(self._check_for_gtk_closing_flag)
        # Alternative more low-level implementation.
        #while True:
        #    gtk.main_iteration(block=False)
        #    if gtk.events_pending() and self._gtk_close:
        #        break
        gtk.main()
        return self

    @library.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _initialize_gtk_progress_bar(
##         self: library.extension.type.Self
##     ) -> library.extension.type.Self:
    def _initialize_gtk_progress_bar(self):
##
        '''
            Initializes the progress bar for gtk on bottom of the window for
            showing current state of website rendering.
        '''
        self.progress_bar = gtk.ProgressBar()
        self.browser.connect(
            'load-progress-changed', self._on_gtk_load_progress_changed)
        self.browser.connect('load-started', self._on_gtk_load_started)
        self.browser.connect('load-finished', self._on_gtk_load_finished)
        if not self._no_progress_bar:
            self.vbox.pack_start(self.progress_bar, False)
        return self

    @library.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _check_for_gtk_closing_flag(
##         self: library.extension.type.Self
##     ) -> builtins.bool:
    def _check_for_gtk_closing_flag(self):
##
        '''
            Checks if gtk should be closed after the last gtk main iteration.
        '''
        if self._gtk_close:
            gtk.main_quit()
        return True

                # region event methods

                    # region window methods

    @library.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _on_qt_close(
##         self: library.extension.type.Self
##     ) -> library.extension.type.Self:
    def _on_qt_close(self):
##
        '''
            Triggers if the current window will be closed.
        '''
        if self._close_handler:
            for close_handler in self._close_handler:
                close_handler(self)
        return self

    @library.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _on_gtk_close(
##         self: library.extension.type.Self, window,  # : gtk.Window,
##         event,  # : gtk.gdk.Event
##     ) -> library.extension.type.Self:
    def _on_gtk_close(self, window, event):
##
        '''
            Triggers if the current window will be closed.
        '''
        if self._close_handler:
            for close_handler in self._close_handler:
                close_handler(self, window, event)
        gtk.main_quit()
        return self

                    # endregion

                    # region webkit event methods

    @library.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _on_qt_title_changed(
##         self: library.extension.type.Self, title  # : builtins.str
##     ) -> library.extension.type.Self:
    def _on_qt_title_changed(self, title):
##
        '''
            Triggers if the current title (normally defined in the web page's
            markup).
        '''
        self.browser.setWindowTitle(title)
        return self

    @library.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _on_gtk_title_changed(
##         self: library.extension.type.Self, webview,  # : webkit.WebView,
##         frame,  # : webkit.WebFrame,
##         title: builtins.str
##     ) -> library.extension.type.Self:
    def _on_gtk_title_changed(self, webview, frame, title):
##
        '''
            Triggers if the current title (normally defined in the web page's
            markup).
        '''
        self.window.set_title(title)
        return self

    @library.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _on_qt_load_started(
##         self: library.extension.type.Self
##     ) -> library.extension.type.Self:
    def _on_qt_load_started(self):
##
        '''
            Triggers if browser starts to load a new web page.
        '''
        self.progress_bar.text = ''
        self.progress_bar.setVisible(True)
        return self

    @library.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _on_gtk_load_started(
##         self: library.extension.type.Self,
##         webview,  # : webkit.WebView,
##         frame,  # : webkit.WebFrame
##     ) -> library.extension.type.Self:
    def _on_gtk_load_started(self, webview, frame):
##
        '''
            Triggers if browser starts to load a new web page.
        '''
        self.progress_bar.set_fraction(0 / 100.0)
        self.progress_bar.set_visible(True)
        return self

    @library.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _on_qt_load_progress_changed(
##         self: library.extension.type.Self, status: builtins.int
##     ) -> library.extension.type.Self:
    def _on_qt_load_progress_changed(self, status):
##
        '''
            Triggers if the current web page load process was changed.
        '''
        self.progress_bar.setValue(status)
        return self

    @library.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _on_gtk_load_progress_changed(
##         self: library.extension.type.Self,
##         webview,  # : webkit.WebView,
##         amount,  # : builtins.int
##     ) -> library.extension.type.Self:
    def _on_gtk_load_progress_changed(self, webview, amount):
##
        '''
            Triggers if the current web page load process was changed.
        '''
        self.progress_bar.set_fraction(amount / 100.0)
        return self

    @library.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _on_qt_load_finished(
##         self: library.extension.type.Self, successful: builtins.bool
##     ) -> library.extension.type.Self:
    def _on_qt_load_finished(self, successful):
##
        '''
            Triggers if a page load process has finished.
        '''
        self.progress_bar.setVisible(False)
        return self

    @library.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _on_gtk_load_finished(
##         self: library.extension.type.Self,
##         webview,  # : webkit.WebView,
##         frame,  # : webkit.WebFrame
##     ) -> library.extension.type.Self:
    def _on_gtk_load_finished(self, webview, frame):
##
        '''
            Triggers if a page load process has finished.
        '''
        self.progress_bar.set_fraction(100.0 / 100.0)
        self.progress_bar.set_visible(False)
        return self

                    # endregion

                # endregion

            # endregion

    @library.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _determine_gui_toolkits(
##         self: library.extension.type.Self
##     ) -> builtins.list:
    def _determine_gui_toolkits(self):
##
        '''
            Determines all supported gui toolkits.

            Examples:

            >>> Browser('www.google.de')._determine_gui_toolkits()
            ['default', 'gtk', 'qt']
        '''
        toolkits = []
        for attribute in builtins.dir(self):
            match = re.compile('^_initialize_(?P<name>[a-z]+)_browser$').match(
                attribute)
            if match:
                toolkits.append(match.group('name'))
        return toolkits

        # endregion

    # endregion

# endregion

# region footer

library.extension.native.Module.default(
    name=__name__, frame=inspect.currentframe())

# endregion
