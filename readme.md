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

Use case<!--deDE:Einsatz--><!--frFR:Utilisier-->
------------------------------------------------

boostNode is a high level python library. This library supports python2.7+ and
python3.3+ environments. And will always try to use every new cutting edge
python features! The main goal of boostNode is to support all typical use cases
for applications in a full generic, reusable and very solid way.
<!--deDE:
    boostNode ist eine sehr einfach zu verwendende intuitive python Bibliothek.
    Momentan unterstützt sie sowohl python2.7+ als auch python3.3+ Umgebungen.
    Konzept ist es durch Automatisierung immer die neusten cutting edge
    features der neusten Python Versionen in einer Bibliothek zu verwenden und
    dabei alle typischen Anwendungstypen durch rein generische Module durch
    Hochzuverlässige Bausteine zu unterstützen.
-->

Content<!--deDE:Inhalt-->
-------------------------

<!--Place for automatic generated table of contents.-->
[TOC]

Features
--------

* Very high code quality
    * 100% platform independent reachable branch coverage tested!
    * Signature based type checking in development mode
    * Each unit(function) has a cyclomatic complexity less than 8!
    * Every function, class, module, package has a short straight
      documentation.
* Always compatible
    * Always compatible to newest stable python release with newest features
      included.
    * Always compatible to last major stable python release. You can switch
      between both versions via the embedded macro languages
      (see runnabel/macro.py).
* Platform independent web-based gui-toolkit (see runnable/webToWindow.py).
* Smart, very secure and multiprocessing web-server supporting gzip, htaccess,
  ssl file parsing, directory listing, thread-based and process-based
  cgi-script handling. Can run every executable script as cgi-script out of the
  box. You don't need any sockets like FastCGI or WebSocket
  (see runnable/server.py).
* Macro processor for maintaining multiple versions of text based files in one
  place (see runnable/macro.py).
* File synchronisation and reflection via native and platform independent
  symbolic file linking (see runnable/synchronisation.py).
* Many extended language feature like signature checking, joint points for
  aspect orientated programming, automatic getter or setter generation.
  (see aspect/signature, paradigm/aspectOrientation.py or
  paradigm/objectOrientation.py).
* Many additional introspection features and native type extensions
  (see extension/native.py and extension/type.py).
* Very high-level file abstraction layer with sandboxing support, and backup
  mechanisms (see extension/file.py).
* Highlevel code file handling (see runnable/codeRunner.py). Run every
  source code without manually compiling code.
* Template engine with embedded python code in any text based file supporting
  every python syntax and additional file-include statement
  (see runnable/template.py).
* Full featured global logging mechanism handling (see extension/system.py)
* Very generic full featured command line argument parsing interface written
  on top of python's native "ArgumentParser" module
  (see extension/system.py and extension/output.py).
* Many tools to bring the dry concept to the highest possible level.

Usage<!--deDE:Verwendung-->
---------------------------

Copy this folder to your projects directory and write something like:

    #!/usr/bin/env python

    from boostNode.extension.file import Handler as FileHandler
    from boostNode.extension.native import Dictionary, Module, \
        PropertyInitializer, String
    from boostNode.extension.output import Buffer, Print
    from boostNode.extension.system import CommandLine, Runnable
    ## python3.3 from boostNode.extension.type import Self, SelfClass
    pass
    from boostNode.paradigm.aspectOrientation import JointPoint
    from boostNode.paradigm.objectOrientation import Class

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

License<!--deDE:Lizenz-->
-------------------------

see header in ./\_\_init\_\_.py
