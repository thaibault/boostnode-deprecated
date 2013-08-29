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
This library supports python2.7+ and python3.3+ environments.
And will always try to use every new cutting edge python features!

Features
--------

* Platform independent web-based gui-toolkit (see runnable/webToWindow.py).
* Smart, very secure and multiprocessing web-server supporting gzip, htaccess,
  ssl file parsing, directory listing, thread-based and process-based
  cgi-script handling. Can run every executable script as cgi-script out of the
  box (see runnable/server.py).
* Macro processor for text based files (see runnable/macro.py).
* File synchronisation (see runnable/synchronisation.py).
* Many extended language feature like signature checking, joint points for
  aspect orientated programming automatic getter or setter generation.
  (see aspect/signature, paradigm/aspectOrientation.py or
  paradigm/objectOrientation.py).
* Many additional introspection features and native type extensions
  (see extension/native.py).
* Very high-level file abstraction layer with sandboxing support, and backup
  mechanisms (see extension/file.py).
* Highlevel code file handling (see runnable/codeRunner.py). Run every
  source code without manually compiling code.
* Template engine with embedded python code in any text based file supporting
  every python syntax and additionally file-include as indention-control
  (see runnable/template.py).
* Finer grained import mechanism support (see extension/dependent.py).
* Full featured global logging mechanism handling (see extension/system.py)
* Very generic full featured command line argument parsing interface written
  on top of python's native "ArgumenParser"-modul
  (see extension/system.py and extension/output.py).

Usage
-----

Copy this folder to your projects directory and write something like:

    #!/usr/bin/env python

    import boostNode.extension.native
    # some stuff using imported boostNode components...

For advanced usage see the recommended module pattern described in
"path/to/boosNode/\_\_init\_\_.py".

BoostNode is able to switch itself between python2.X and python3.X.
To switch boostNode version between python3.X and python 2.X use this
command:

```bash
>>> /path/to/boostNode/runnable/macro.py -p /path/to/boostNode -e py
```

Note that you have to temporary support the needed python environment
of given boostNode version to convert to the other one.

Writing own code supporting two different interpreter version is very easy.
Follow one of the two following syntax examples:

    #!/usr/bin/env interpreterA

    ## interpreterB
    ## if True || False do {
    ##     something();
    ## }
    # Your multiline code supported by interpreterA
    if True or False do
        something()
    endif
    ##

    # Your two version of any one line code supportted by interpreterA or
    # interpreterB
    ## interpreterB functionCall();
    functionCall()

Have Fun with boostNode!

Copyright
---------

see header in ./\_\_init\_\_.py

License
-------

see header in ./\_\_init\_\_.py
