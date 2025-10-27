Advanced Usage
==============

Convenience Methods
-------------------

The ``Container`` class provides a couple of convenience methods, which make it behave very similar to a dictionary:

	>>> dc = Container(items=items)
	>>> dc["content.json"]["uuid"]
	'306e2c2d-a9f6-4306-8851-1ee0fceeb852'
	>>> dc["log/console.txt"] = "Hello World!"
	>>> "log/console.txt" in dc
	True
	>>> del dc["log/console.txt"]
	>>> "log/console.txt" in dc
	False

The method ``keys()`` returns a list of all full item names including the respective parts, ``values()`` a list of all item objects, and ``items()`` a list of all (name, item) tuples as you would expect from a dictionary object.

You may use the method ``hash()`` to calculate an SHA256 hash of the container content. The hex digest of this value is stored in the attribute ``hash`` of the item ``container.json``.

Container objects generated from an items dictionary using the parameter ``items=...`` are mutable, which means that you can add, modify and delete items. As soon as you call one of the methods ``write()``, ``upload()``, ``freeze()``, or ``hash()``, the container becomes immutable. Containers loaded from a local file or a server are immutable as well.

An immutable container will throw an exception if you try to modify its content. However, this feature is not bulletproof. The ``Container`` class is not aware of any internal modifications of item objects.

You can convert an immutable container into a mutable one by calling its method ``release()``.
This generates a new UUID and resets the attributes ``replaces``, ``created``, ``storageTime``, ``hash`` and ``modelVersion``.


Server Storage
--------------

It is most convenient to store the server name and the API key in the `configuration file <../configuration.html#scidata>`_. 
However, both values can also be specified as method parameters::

    >>> dc.upload(server="...", key="...")
    >>> dc = Container(uuid="306e2c2d-a9f6-4306-8851-1ee0fceeb852", server="...", key="...")


File Formats
------------

The ``Container`` class can handle virtually any file format. However, in order to store and read a certain file format, it needs to know how to convert the respective Python object into a bytes stream (ZIP container) or dataset (HDF5 container) and vice versa. File formats are identified by their file extension. The following file extensions are currently supported by the package ``scidatacontainer`` out of the box:

.. csv-table:: 

	:header: Extension, File format, Python object, Required packages
	.json, JSON file (UTF-8 encoding), dictionary or others,
	.txt, Text file (UTF-8 encoding), string,
	.log, Text file (UTF-8 encoding), string,
	.pgm, Text file (UTF-8 encoding), string,
	.png, PNG image file,  NumPy array, cv2
	.npy, NumPy array, NumPy array,
	.bin, Raw binary data file, bytes,
  .dataset, HDF5 dataset, NumPy array,

Native support for image objects is only available when your Python environment contains the `cv2 <https://pypi.org/project/opencv-python/>`_ package. The container class tries to guess the format of items with unknown extension. However, it is more reliable to use the function ``register()`` to add alternative file extensions to already known file formats. The following commands will register the extension ``.py`` as a text file:

	>>> from scidatacontainer import register
	>>> register("py", "txt")

If you want to register another Python object, you need to provide a conversion class which can convert this object to and from a bytes string. This class must inherit from the class ``AbstractFile``. A custom class to store NumPy arrays in ZIP and HDF5 containers may be realized by the following code:

.. code-block:: python
  :linenos:

  import io
  
  import numpy as np
  from scidatacontainer import AbstractFile, register
  from h5py import Group as h5Group
  from h5py import Dataset as h5Dataset
  
  
  class NpyFile(AbstractFile):
      """Data conversion class for NumPy arrays (ndarray)."""
  
      allow_pickle = False
  
      def encode_zip(self) -> bytes:
          """Convert NumPy array to bytes string."""
  
          with io.BytesIO() as fp:
              np.save(fp, self.data, allow_pickle=self.allow_pickle)
              fp.seek(0)
              data = fp.read()
          return data
  
      def decode_zip(self, data: bytes):
          """Decode NumPy array from bytes string."""
  
          with io.BytesIO() as fp:
              fp.write(data)
              fp.seek(0)
              self.data = np.load(fp, allow_pickle=self.allow_pickle)
  
      def encode_hdf5(self, group: h5Group, name: str):
          """Create an hdf5 dataset to represent a NumPy array."""
          ds = group.create_dataset(name, data=self.data)
          ds.attrs["description"] = "I can write some attributes, too."

      def decode_hdf5(self, dataset: h5Dataset):
          """Load numpy array from hdf5 dataset"""
          self.data = dataset[:]
          # I could also handle attributes here!

      def hash(self) -> str:
          return hashlib.sha256(self.data.data).hexdigest()


  register("mynpy", NpyFile, np.ndarray)

The third argument of the function ``register()`` sets this conversion class as default for NumPy array objects overriding any previous default class. This argument is optional.

Hash values are usually derived from the bytes string of an encoded object. If you require a different behaviour, you may also override the method ``hash()`` of the class ``AbstractFile``.
