Crestron Cleanup
================

Clean up signal names and other parts of a messy Crestron SIMPL Windows program.

Requirements:
-------------

- Console:
    - `Python <https://www.python.org>`_ 2.7 or 3
- GUI:
    - `Python <https://www.python.org>`_ 2.7
    - `wxPython <http://wxpython.org/>`_ (classic) 3.0.2.0

Console Usage:
--------------

.. code:: bash

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

.. code:: bash

    usage: python crestroncleanup

The GUI will launch and the user can open a file from the `File` menu (cmd+o). 
Interesting objects will be shown in a data table. Click the `play` button to 
process the signals and product a report. Click the `save` button to open the
save dialog and save the file.
