<!-- region vim modline

vim: set tabstop=4 shiftwidth=4 expandtab:
vim: foldmethod=marker foldmarker=region,endregion:

endregion

region header

Copyright Torben Sickert 16.12.2012

License
   This library written by Torben Sickert stand under a creative commons
   naming 3.0 unported license.
   see http://creativecommons.org/licenses/by/3.0/deed.de

endregion -->

boostNode
=========

boostNode is a high level python library.
This library supports python2.7+ and python3.3+ environements.

Features
--------

* Platform independent webbased gui toolkit (see runnable/webToWindow.py).
* Smart, very secure and multiprocessing webserver (see runnable/server.py).
* Macro processor for text based files (see runnable/macro.py).
* File synchronisation (see runnable/synchronisation.py).
* Many extended language feature like signature checking, jointpoints for
  aspect orientated programming automatic getter or setter generation.
  (see aspect/signature, paradigm/aspectOrientation.py or
   paradigm/objectOrientation.py).
* Many additional introspection features and native type extensions.
  (see extension/native.py).
* Very highlevel file abstraction layer with sanboxing support
  (see extension/file.py).
* Highlevel code file handling (see runnable/codeFile.py).
* Template engine with embedded python code in any text based file
  (see runnable/template.py).
* Finer grained import mechanism support (see extension/dependent.py).
* Full featured global logging mechanism handling (see extension/system.py)
* Very generic full featured command line argument parsing interface (
  see extension/system.py and extension/output.py).

Usage
-----

Copy this folder to your projects directory and write something like:

    import boostNode.extension.native
    # some stuff using imported boostNode components...

For advanced usage see the recommended module pattern described in
"path/to/boosNode/__init__.py".

BoostNode is able to witch itself between python2.X and python3.X.
To switch boostNode version between python3.X and python 2.X use this
command:

    /path/to/boostNode/runnable/macro.py -p /path/to/boostNode -e py

Copyright
---------

see ./__init__.py

License
-------

see ./__init__.py
