#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-

# region vim modline

# vim: set tabstop=4 shiftwidth=4 expandtab:
# vim: foldmethod=marker foldmarker=region,endregion:

# endregion

# region header

'''
    Offers a higher level for common tasks. Most of the modules are written
    on top of python's native implementations.
'''
"""
Copyright

    Torben Sickert 16.12.2012

License

    boostNode von Torben Sickert steht unter einer Creative Commons
    Namensnennung 3.0 Unported Lizenz.

    see http://creativecommons.org/licenses/by/3.0/deed.de

Conventions (bcX := boostNode convention number X)

    - bc1 Capitalized variables are constant and shouldn't be mutable.
    - bc2 Properties with preceding underscores shouldn't be accessed from
          the outer scope. They could accessed in inherited objects
          (protected attributes).
    - bc3 Property with two preceding underscore shouldn't be accessed from
          any location then the object itself (private attributes).
    - bc4 Follow the python object orientated programming conventions like
          camel-case class-names or underscore separated methods and property
          names.
    - bc5 Class-names have a leading upper case letter.
    - bc6 Methods and functions are complete lower case.
    - bc7 Do not use more chars then 79 in one line.
    - bc8 Use short and/or long description doc-strings for all definitions.
    - bc9 Write doctest for each unit it is possible and try to reach 100% path
          coverage.
    - bc10 Every temporary generated file (e.g. for mockups) should have its
           name prefixed with "temp_" to support automatic clean up after
           running automated test cases.
    - bc11 Sorting imports as following:
               1. Import all standard modules and packages,
               2. then all from third party,
               3. now import your own modules or packages.
               4. Sort import names alphabetically and separate the previous
                  defined parts with blank lines.
    - bc12 Import everthing by its whole name and reference path and use it by
           its full reference path (even builtin units).
    - bc13 Don't use any abbreviations.
    - bc14 Follow the pep8 standards.
    - bc15 Try to use small cyclomatic complexity in all units.
           (e.g. less than 20 or 30).
    - bc16 Use the modules pattern described below.
    - bc17 Use the area statement syntax to structure your code and make it
           possible to fold them in many IDE's
           (see Structure of meta documenting below).
           If you are forced to indent an area nearer to left border as in
           the logic of meta structuring use one "#" for each less of
           indention.
    - bc18 If a module could offer a usable command line interface to provide
           their functionality directly for other programs
           (maybe not written in python) implement the "Runnable" interface
           from "boostNode.extension.system.Runnable".
    - bc19 Make every script or package standalone runnable. That means you
           should use relative import references or append your own import path
           dynamically generated.
    - bc20 Always think that code is more read than written.
    - bc21 By choosing witch quotes to use follow this priority.
               1. Single quote (')
               2. Double quote (")
               3. Triple single quote (''')
               4. Triple double quote (three times ")
    - bc22 Indent function parameter which doesn't match in one line like:

           function_name(
               parameter1, parameter2, parameter3,
               parameter4)

           instead of:

           function_name(parameter1,
                         parameter2,
                         parameter3,
                         parameter4)

    - bc22 Indent function call brackets like:

        function_name(
            parameter1, parameter2, parameter3
        ).method_name()

        instead of:

        function_name(
            parameter1, parameter2, parameter3).method_name()

Structure of meta documenting classes. (see bc16 and bc17)

    # region header

    import ia

    # endregion

    # region function

    def a:
        ...


    def b:
        ...

    # endregion

    # region abstract classes

    class AA:

        # region (Static|Dynamic) (properties|methods)

            # region (Public|Protected)

                # region Property of method or property group

                    # region Subproperty of method or property group

        ...

                    # endregion

                # endregion

            #+ region compensate right indention

        ...

            #+ endregion

    #+++ region compensate more right indention

        ...

                # endregion

                    #- compensate left indention

        ...

                # endregion

            # endregion

        # endregion

    # endregion

    # region classes

    class A:

        # region (static|dynamic) (properties|methods)

            # region (public|protected)

                # region property of method or property group

                    # region subproperty of method or property group

        ...

                    # endregion

                # endregion

            # endregion

        # endregion

    # endregion

    # region footer

    if __name__ == '__main__':
        ...

    # endregion

Structure of dependencies

    0.  builtins
    1.  boostNode.extension.dependent
    1.  boostNode.extension.type
    2.  boostNode.aspect.signature
    3.  boostNode.paradigm.aspectOrientation
    4.  boostNode.paradigm.objectOrientation
    5.  boostNode.extension.native
    6.  boostNode.extension.file
    7.  boostNode.extension.output
    8.  boostNode.extension.system
    9.  boostNode.*
    10. yourOwnModulesOrPackages.*

    This means that a module in level "i" could only import a full module
    in its header in level "j" if "j < i" holds.
    If your try to import a module from a higher level ("j < i") you could
    try to use the "from ... import ..." statement in the needed context
    dependent scope or your can use the "dependent" module to define
    dependencies and let code waiting till all there dependencies are
    imported.

Module pattern (see bc16)

    #!/usr/bin/env python3.2
    # -*- coding: utf-8 -*-

    # region header

    '''
        Module documentation which should be useable as help message for
        modules which supports command line interfaces
        (see Runnable implementation interface).
    '''
    '''
        For conventions see "boostNode/__init__.py" on
        https://github.com/thaibault/boostNode
    '''

    __author__ = 'FULL NAME'
    __copyright__ = 'see boostNode/__init__.py'
    __credits__ = ('FIRST NAME', 'SECOND NAME', ...)
    __license__ = 'see boostNode/__init__.py'
    __maintainer__ = 'FULL NAME'
    __maintainer_email__ = 'EMAIL ADDRESS'
    __status__ = 'e.g. "Beta"'
    __version__ = 'e.g. 0.9'

    ## python2.7 pass
    import builtins
    import inspect

    ## python2.7 builtins = sys.modules['__main__'].__builtins__
    pass

    '''see bc18'''
    sys.path.append(os.path.abspath(sys.path[0] + 2 * ('..' + os.sep)))

    import boostNode.extension.system

    # endregion

    # region functions

    def Main():
        builtins.print('Hello world!')

    # endregion

    # region footer

    boostNode.extension.system.CommandLine.package(
        name=__name__, frame=inspect.currentframe())

    # endregion
"""

__author__ = 'Torben Sickert'
__copyright__ = 'see docstring'
__credits__ = 'Torben Sickert',
__license__ = 'see docstring'
__maintainer__ = 'Torben Sickert'
__maintainer_email__ = 't.sickert@gmail.com'
__status__ = 'stable'
__version__ = '1.0'

## python2.7 import __builtin__ as builtins
import builtins
import inspect
import logging
import os
import sys

'''Make boostNode packages and modules importable via relative paths.'''
sys.path.append(os.path.abspath(sys.path[0] + 2 * ('..' + os.sep)))

'''
    Prevents python from creating ".pyc" or ".pyo" files during importing
    modules.
'''
sys.dont_write_bytecode = True

if not builtins.getattr(builtins, "WindowsError", None):
    class WindowsError(builtins.OSError):
        pass
try:
    import boostNode.aspect.signature
    import boostNode.extension.system
    import boostNode.extension.native
except WindowsError as exception:
    logging.error(
        "Running subprocesses on windows without being administrator isn't "
        'possible. %s: %s', exception.__class__.__name__,
        builtins.str(exception))
    sys.exit(1)

# endregion

'''
    Add signature checking for all functions and methods with joint points in
    this package.
'''
boostNode.aspect.signature.add_check(
    point_cut='^%s\..*$' % boostNode.extension.native.Module.get_package_name(
        frame=inspect.currentframe()))

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
boostNode.extension.system.CommandLine.generic_package_interface(
    name=__name__, frame=inspect.currentframe())

# endregion
