#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# region vim modline

# vim: set tabstop=4 shiftwidth=4 expandtab:
# vim: foldmethod=marker foldmarker=region,endregion:

# endregion

# region header

'''
    Provides a web-browser-based technology to show web-pages as desktop
    window.
'''
'''
    For conventions see "boostNode/__init__.py" on
    https://github.com/thaibault/boostNode
'''

__author__ = 'Torben Sickert'
__copyright__ = 'see boostNode/__init__.py'
__credits__ = 'Torben Sickert',
__maintainer__ = 'Torben Sickert'
__maintainer_email__ = 't.sickert@gmail.com'
__status__ = 'stable'
__version__ = '1.0'

## python3.3 import builtins
import __builtin__ as builtins
import collections
import inspect
import os
import re
import sys
import threading
## python3.3 import types
pass
import webbrowser

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

for number in (3, 4):
    sys.path.append(os.path.abspath(sys.path[0] + number * ('..' + os.sep)))

import boostNode.extension.native
import boostNode.extension.system
import boostNode.extension.type
import boostNode.paradigm.aspectOrientation
import boostNode.paradigm.objectOrientation

# endregion


# region classes

class Browser(
    boostNode.paradigm.objectOrientation.Class,
    boostNode.extension.system.Runnable
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
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Defines the width of the given window in pixel.',
             'dest': 'width_in_pixel',
             'metavar': 'NUMBER_OF_PIXELS'}},
        {'arguments': ('-y', '--height'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'choices': builtins.range(1, 50000),
             'required': {'execute': '__initializer_default_value__ is None'},
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
             'action': {'execute': "'store_true' if "
                                   '__initializer_default_value__ else '
                                   "'store_false'"},
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
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Defines default toolkit. Others will only run as '
                     'fallback.',
             'dest': 'default_gui_toolkit',
             'metavar': 'GUI_TOOLKIT'}},
        {'arguments': ('-b', '--no-progress-bar'),
         'keywords': {
             'action': {'execute': "'store_true' if "
                                   '__initializer_default_value__ else '
                                   "'store_false'"},
             'default': {'execute': '__initializer_default_value__'},
             'help': 'If set no progress bar for showing website rendering '
                     'state is shown.',
             'dest': 'no_progress_bar'}},
        {'arguments': ('-d', '--default-title'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': 'Defines which string should be shown in window '
                     'decoration if no site with title node was loaded.',
             'dest': 'default_title',
             'metavar': 'TITLE'}},
        {'arguments': ('-s', '--stop-order'),
         'keywords': {
             'action': 'store',
             'default': {'execute': '__initializer_default_value__'},
             'type': {'execute': 'type(__initializer_default_value__)'},
             'required': {'execute': '__initializer_default_value__ is None'},
             'help': {'execute': '"""Saves a cli-command for shutting down '
                                 'the server (default: "%s").""" % '
                                 '__initializer_default_value__'},
             'dest': 'stop_order',
             'metavar': 'STRING'}})

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
    '''Saves a cli-command for shutting down the server.'''
    stop_order = ''

        # endregion

        # region protected properties

    '''If set gtk will be preferred to show webview otherwise qt.'''
    _default_gui_toolkit = ''
    '''Holds the current url location.'''
    _url = ''
    '''Defines dimensions of webview.'''
    _width_in_pixel = 0
    _height_in_pixel = 0
    _fullscreen = False
    _no_window_decoration = False
    '''If setted "True" window will be closed on next gtk main iteration.'''
    _gtk_close = False
    '''Defines weather a progress bar for page loading should be shown.'''
    _no_progress_bar = False
    '''Defines which gui toolkit should be used.'''
    _gui_toolkit = ''
    '''Saves the default title if no title was set via markup.'''
    _default_title = ''
    '''
        This lock object handles to wait until all gtk windows are closed
         before the program terminates.
    '''
    _close_gtk_windows_lock = None

        # endregion

    # endregion

    # region dynamic methods

        # region public methods

            # region special methods

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def __repr__(self: boostNode.extension.type.Self) -> builtins.str:
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
        return('Object of "{class_name}" with url "{url}" in {width} pixel x '
               '{height} pixel, stop order "{stop_order}" and gui toolkit '
               '"{gui_toolkit}".'.format(
                   class_name=self.__class__.__name__, url=self._url,
                   width=self._width_in_pixel, height=self._height_in_pixel,
                   stop_order=self.stop_order, gui_toolkit=self.gui_toolkit))

            # endregion

            # region getter methods

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def get_gui_toolkit(
##         self: boostNode.extension.type.Self
##     ) -> builtins.str:
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

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def set_url(
##         self: boostNode.extension.type.Self, url: builtins.str
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

            # endregion

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def stop(
##         self: boostNode.extension.type.Self, *arguments: builtins.object,
##         reason='', **keywords: builtins.object
##     ) -> boostNode.extension.type.Self:
    def stop(self, *arguments, **keywords):
##
        '''
            Closes all created webviews. Note that in case of using the default
            installed browser fall-back this instance couldn't be destroyed.
        '''
## python3.3
##         pass
        reason, keywords = boostNode.extension.native.Dictionary(
            content=keywords
        ).pop(name='reason', default_value='')
##
        if self.window is not None:
            if self.gui_toolkit == 'qt':
                self.window.closeAllWindows()
                if not (builtins.len(arguments) or reason):
                    reason = 'clicking qt close button'
            elif self.gui_toolkit == 'gtk':
                self._gtk_close = True
                if builtins.len(arguments) and builtins.isinstance(
                    arguments[0], gtk.Window
                ):
                    reason = 'clicking gtk close button'
                else:
                    '''
                        NOTE: We got a close trigger from another thread as
                        where the main gtk loop is present. We have to wait
                        until gtk has finished it's closing procedures.
                    '''
                    self._close_gtk_windows_lock.acquire()
        __logger__.info('All "%s" windows closed.', self.gui_toolkit)
        '''
            Take this method type by the abstract class via introspection.
        '''
        return builtins.getattr(
            builtins.super(self.__class__, self), inspect.stack()[0][3]
        )(*arguments, reason=reason, **keywords)

        # endregion

        # region protected methods

            # region runnable implementation

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _run(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
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
            namespace=boostNode.extension.system.CommandLine.argument_parser(
                module_name=__name__, scope={'self': self},
                arguments=self.COMMAND_LINE_ARGUMENTS)))

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _initialize(
##         self: boostNode.extension.type.Self, url: builtins.str,
##         width_in_pixel=800, height_in_pixel=600, fullscreen=False,
##         no_window_decoration=False, default_gui_toolkit='qt',
##         no_progress_bar=False, default_title='No gui loaded.',
##         stop_order='stop', **keywords: builtins.object
##     ) -> boostNode.extension.type.Self:
    def _initialize(
            self, url, width_in_pixel=800, height_in_pixel=600,
            fullscreen=False, no_window_decoration=False,
            default_gui_toolkit='qt', no_progress_bar=False,
            default_title='No gui loaded.', stop_order='stop', **keywords):
##
        '''
            Initializes a webview or tries to open a default browser if
            no gui suitable gui toolkit is available.
        '''
        self.url = url
        self.stop_order = stop_order
        self._width_in_pixel = width_in_pixel
        self._height_in_pixel = height_in_pixel
        self._fullscreen = fullscreen
        self._no_window_decoration = no_window_decoration
        self._default_gui_toolkit = default_gui_toolkit
        self._no_progress_bar = no_progress_bar
        self.__class__.webview_instances.append(self)
        __logger__.info(
            'Start webgui with gui toolkit "%s".', self.gui_toolkit)
        if not __test_mode__:
            self._close_gtk_windows_lock = threading.Lock()
            self._close_gtk_windows_lock.acquire()
## python3.3
##             browser_thread = threading.Thread(
##                 target=builtins.getattr(
##                     self, '_initialize_%s_browser' % self.gui_toolkit),
##                 daemon=True
##             ).start()
            browser_thread = threading.Thread(target=builtins.getattr(
                self, '_initialize_%s_browser' % self.gui_toolkit))
            browser_thread.daemon = True
            browser_thread.start()
##
            if self.stop_order:
                self.wait_for_order()
        return self

            # endregion

            # region native webview components

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _initialize_default_browser(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def _initialize_default_browser(self):
##
        '''
            Starts the default browser with currently stored url.
        '''
        self.browser = webbrowser
        self.browser.open(self._url)
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _initialize_qt_browser(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
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
            self.trigger_stop)
        self.window.exec_()
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _initialize_qt_progress_bar(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
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

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _initialize_gtk_browser(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
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
        self.window.connect('delete_event', self.trigger_stop)
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

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _initialize_gtk_progress_bar(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
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

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _check_for_gtk_closing_flag(
##         self: boostNode.extension.type.Self
##     ) -> builtins.bool:
    def _check_for_gtk_closing_flag(self):
##
        '''
            Checks if gtk should be closed after the last gtk main iteration.
            If we return a "False" this method will not be triggered in future.
            time.
        '''
        if self._gtk_close:
            gtk.main_quit()
            self._close_gtk_windows_lock.release()
        return not self._gtk_close

                # region event methods

                    # region webkit event methods

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _on_qt_title_changed(
##         self: boostNode.extension.type.Self, title  # : builtins.str
##     ) -> boostNode.extension.type.Self:
    def _on_qt_title_changed(self, title):
##
        '''
            Triggers if the current title (normally defined in the web page's
            markup).
        '''
        self.browser.setWindowTitle(title)
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _on_gtk_title_changed(
##         self: boostNode.extension.type.Self, webview,  # : webkit.WebView,
##         frame,  # : webkit.WebFrame,
##         title: builtins.str
##     ) -> boostNode.extension.type.Self:
    def _on_gtk_title_changed(self, webview, frame, title):
##
        '''
            Triggers if the current title (normally defined in the web page's
            markup).
        '''
        self.window.set_title(title)
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _on_qt_load_started(
##         self: boostNode.extension.type.Self
##     ) -> boostNode.extension.type.Self:
    def _on_qt_load_started(self):
##
        '''
            Triggers if browser starts to load a new web page.
        '''
        self.progress_bar.text = ''
        self.progress_bar.setVisible(True)
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _on_gtk_load_started(
##         self: boostNode.extension.type.Self,
##         webview,  # : webkit.WebView,
##         frame,  # : webkit.WebFrame
##     ) -> boostNode.extension.type.Self:
    def _on_gtk_load_started(self, webview, frame):
##
        '''
            Triggers if browser starts to load a new web page.
        '''
        self.progress_bar.set_fraction(0 / 100.0)
        self.progress_bar.set_visible(True)
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _on_qt_load_progress_changed(
##         self: boostNode.extension.type.Self, status: builtins.int
##     ) -> boostNode.extension.type.Self:
    def _on_qt_load_progress_changed(self, status):
##
        '''
            Triggers if the current web page load process was changed.
        '''
        self.progress_bar.setValue(status)
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _on_gtk_load_progress_changed(
##         self: boostNode.extension.type.Self,
##         webview,  # : webkit.WebView,
##         amount,  # : builtins.int
##     ) -> boostNode.extension.type.Self:
    def _on_gtk_load_progress_changed(self, webview, amount):
##
        '''
            Triggers if the current web page load process was changed.
        '''
        self.progress_bar.set_fraction(amount / 100.0)
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _on_qt_load_finished(
##         self: boostNode.extension.type.Self, successful: builtins.bool
##     ) -> boostNode.extension.type.Self:
    def _on_qt_load_finished(self, successful):
##
        '''
            Triggers if a page load process has finished.
        '''
        self.progress_bar.setVisible(False)
        return self

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _on_gtk_load_finished(
##         self: boostNode.extension.type.Self,
##         webview,  # : webkit.WebView,
##         frame,  # : webkit.WebFrame
##     ) -> boostNode.extension.type.Self:
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

    @boostNode.paradigm.aspectOrientation.JointPoint
## python3.3
##     def _determine_gui_toolkits(
##         self: boostNode.extension.type.Self
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

'''
    Extends this module with some magic environment variables to provide better
    introspection support. A generic command line interface for some code
    preprocessing tools is provided by default.
'''
boostNode.extension.native.Module.default(
    name=__name__, frame=inspect.currentframe())

# endregion
