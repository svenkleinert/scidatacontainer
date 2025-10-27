====================
SciDataContainer API
====================

.. currentmodule:: scidatacontainer

Container classes
=================

.. autoclass:: Container
    :show-inheritance:
    :inherited-members:

.. autoclass:: AbstractContainer
    :show-inheritance:
    :inherited-members:

File type support
=================

.. autofunction:: register

.. _python-builtin-converters:

Built-in conversion classes
---------------------------

.. currentmodule:: scidatacontainer.filebase

.. autoclass:: AbstractFile
    :members:
    :inherited-members:

.. autoclass:: BinaryFile
    :show-inheritance:
    :inherited-members:

.. autoclass:: TextFile
    :show-inheritance:
    :inherited-members:

.. autoclass:: JsonFile
    :show-inheritance:
    :inherited-members:

.. autoclass:: Dataset 
    :show-inheritance:
    :inherited-members:

Convenience functions
=====================

.. currentmodule:: scidatacontainer

.. autofunction:: timestamp

.. currentmodule:: scidatacontainer.config

.. autofunction:: load_config

Metadata validation
===================

.. currentmodule:: scidatacontainer.jsonschema

.. autofunction:: validate

.. automodule:: scidatacontainer.jsonschema
   :members: content, meta
