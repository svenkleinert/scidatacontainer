Data Container Concept
======================

The basic concept of the data container is that it keeps the raw dataset, parameter data and meta data together. Parameter data is every data which scientists traditionally record in lab books like a description of the test setup, measurement settings, simulation parameters or evaluation parameters. The intention behind the container concept is to make datasets self-contained.

Each data container is identified by a `UUID <https://en.wikipedia.org/wiki/Universally_unique_identifier>`_. The **Container** file is a `ZIP package file <https://en.wikipedia.org/wiki/ZIP_(file_format)>`_. The data in the container is stored in **Items** (files in ZIP package), which are organized in **Parts** (folders in ZIP package). The standard file extension of a container file is ``.zdc``.

There are no restrictions regarding data formats inside the container, but items should be stored in the `JSON <https://en.wikipedia.org/wiki/JSON>`_ format, whenever possible. This makes the data readable for humans as well as machines. Furthermore, it allows to inspect, use and even create data container files with the tools provided by the operating system without any special software. We call the keys of JSON objects data **Attributes**.

Only the two items ``content.json`` and ``meta.json`` are required and must be located in the root part of the container. The optional root item ``license.txt`` may be used to store the text of the license for the dataset.

The data payload of a container consisting of the dataset and the parameter data should be stored in certain parts of the container. Although there are no restrictions in using parts, you should restrict yourself to a set of `suggested parts <#parts>`_.

Container Parameters
--------------------
The parameters describing the container itself are stored in the required root item ``content.json``, which contains a single JSON object. The following set of attributes is currently defined for this item:

- ``uuid``: required UUID
- ``replaces``: optional UUID of the predecessor of this dataset
- ``containerType``: required container type object

    + ``name``: required container name (`camel case <https://en.wikipedia.org/wiki/Camel_case>`_ format)
    + ``id``: optional identifier for standardized containers
    + ``version``: required standard version, if ``id`` is given

- ``created``: required creation timestamp (see `format <#timestamp>`_)
- ``storageTime``: required timestamp of storage or freeze (see `format <#timestamp>`_)
- ``static``: required boolean flag (see `container variants <#variants>`_)
- ``complete``: required boolean flag (see `container variants <#variants>`_)
- ``hash``: optional hex digest of SHA256 hash, required for `static containers <#variants>`_
- ``usedSoftware``: optional list of software objects

    - ``name``: required software name
    - ``version``: required software version
    - ``id``: optional software identifier (e.g. UUID or URL)
    - ``idType``: required type of identifier, if ``id`` is given

- ``modelVersion``: required data model version

Dataset Description
-------------------

The meta data describing the data payload of the container is stored in the required root item ``meta.json``, which contains a single JSON object. The following set of attributes is currently defined for this item:

- ``author``: required name of the author
- ``email``: required e-mail address of the author
- ``orcid``: optional ORCID of the author
- ``organization``: optional affiliation of the author
- ``comment``: optional comments on the dataset
- ``title``: required title of the dataset
- ``keywords``: optional list of keywords
- ``description``: optional abstract for the dataset
- ``timestamp``: optional creation timestamp of the dataset (see `format <#timestamp>`_)
- ``doi``: optional digital object identifier of the dataset
- ``license``: optional data license name (e.g. `"MIT" <https://en.wikipedia.org/wiki/MIT_License>`_ or `"CC-BY" <https://creativecommons.org/licenses/by/4.0/>`_)
- ``authors``:  optional list of author information objects to represent multiple authors of a dataset

    - ``name``: required author name
    - ``email``: optional e-mail address of the author
    - ``orcid``: optional ORCID of the author
    - ``organization``: optional affiliation of the author

.. _timestamp:

Timestamp Format
----------------

An `ISO 8601 <https://en.wikipedia.org/wiki/ISO_8601>`_ compatible string in a certain format is expected as value of timestamp attributes in ``content.json`` and ``meta.json``. The required format contains the UTC date and time and the local timezone. For example::

"2023-02-17T15:23:57+0100"

.. _parts:

Suggested Parts
---------------

Standardization simplifies data exchange as well as reuse of data. Therefore, it is suggested to store the data payload of a container in the following part structure:

- ``/info``: informative parameters
- ``/sim``: raw simulation results
- ``/meas``: raw measurement results
- ``/data``: parameters and data required to achieve results in ``/sim`` or ``/meas``
- ``/eval``: evaluation results derived from ``/sim`` and/or ``/meas``
- ``/log``: log files or other unstructured data


.. _variants:

Container Variants
------------------

Our data model currently supports three variants of data containers, based on certain use cases. The distinction is mainly relevant for data storage and therefore of particular interest when you upload the container to a storage server. The respective variant is selected using the boolean attributes ``static`` and ``complete`` of the item ``content.json``:

.. csv-table:: 
  :header: ``static``, ``complete``, Container variant

  true, true, static container
	true, false, (not allowed)
	false, true, normal completed container
	false, false, incomplete container

The **normal container** is generated and completed in a single step. This matches the typical workflow of generating data and saving all of it in one shot. However, if the data acquisition runs over a very long time like days or weeks, you may want to store also **incomplete containers**. In that case you can mark the container as containing incomplete data and update it as needed with increasing attribute ``storageTime``. Each server upload will replace the previous container. With your final upload you mark the container as being complete.

**Static containers** are intended to carry static parameters in contrast to measurement or simulation data. An example would be a detailed description of a measurement setup, which is used for many measurements. Instead of including the large setup data with each individual measurement dataset, the whole setup may be stored as a single static dataset and referenced by its UUID as measurement parameter in subsequent containers. Static containers must contain a hash string. The data storage server refuses the upload of multiple containers with same ``containerType`` and ``hash``.
