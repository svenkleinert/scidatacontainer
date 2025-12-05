Configuration
=============

Container File Extension
------------------------

On Microsoft Windows you may inspect ZDC files with a double-click in the Windows Explorer. This requires that you register the extension ``.zdc`` in the same way as ``.zip``. Run the following on the command prompt to achieve this behaviour:

.. code-block:: powershell

    reg copy HKCR\.zip HKCR\.zdc /s /f

.. _scidata:

Configuration File
------------------

Using a SciDataContainer software library or the GUI application makes the usage of data containers much more convenient. They can initialize and manage many container attributes automatically. The libraries and the GUI are also able to take some user specific attributes and parameters either from environment variables or a config file.

Name and location of the configuration file is ``%USERPROFILE%\scidata.cfg`` on Microsoft Windows and ``~/.scidata`` on other operating systems. The file is expected to be a text file. Leading and trailing white space is ignored, as well as lines starting with ``#``. Parameters are taken from lines in the form ``<key>=<value>``. White space before and after the equal sign is ignored. The keywords are case-insensitive.

The following parameters are supported:

.. csv-table:: 
  :header: Environment variable, Configuration key, Content

  ``DC_AUTHOR``, ``author``, name of the dataset's author
	``DC_EMAIL``, ``email``, e-mail address of the author
  ``DC_ORCID``, ``orcid``, orcid of the author
  ``DC_ORGANIZATION``, ``organization``, affiliation of the author
	``DC_SERVER``, ``server``, name or address of the data storage server
	``DC_KEY``, ``key``, key for the storage server API

A value in the configuration file supersedes the content of the respective environment variable.


Example Configuration File
--------------------------

.. code-block:: cfg

    author = Jane Doe
    email = jane.doe@example.com
    server = data.example.com
    key = 487cadbdcca5302b5d24f94609dbadda4f5b034d2f863ec22f9caa739b12690b

