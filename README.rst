Crestron Cleanup
================

Clean up signal names and other parts of a messy Crestron SIMPL Windows program.

Requirements:
-------------

- Console:
    - `Python 2.7 or 3 <https://www.python.org>`_
- GUI:
    - `Python 2.7 <https://www.python.org>`_
    - `wxPython (classic) 3.0.2.0 <http://wxpython.org/>`_

Console Usage:
--------------

::

    usage: crestroncleanup [-h] [-o] [-b] filename

    Clean up signals in a messy Crestron SIMPL file.

    positional arguments:
      filename         Name of file to process

    optional arguments:
      -h, --help       show this help message and exit
      -o, --overwrite  Overwrite the existing file
      -b, --backup     Backup existing file before overwriting

The SIMPL Windows file will examine and process all signals and produce a report 
detailing modified objects.

GUI Usage:
----------

::

    usage: python crestroncleanup

The GUI will launch and the user can open a file from the `File` menu (cmd+o). 
Interesting objects will be shown in a data table. Click the `play` button to 
process the signals and product a report. Click the `save` button to open the
save dialog and save the file.

TODO:
-----

- Allow editing of signal names from data table.
- Decode password protected SIMPL Windows files.
- Upgrade GUI to `wxPython Phoenix <http://wxpython.org/Phoenix/docs/html/index.html>`_ (currently pre-release) and `Python 3 <https://www.python.org>`_
