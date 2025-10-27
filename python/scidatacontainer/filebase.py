##########################################################################
# Copyright (c) 2023 Reinhard Caspary                                    #
# <reinhard.caspary@phoenixd.uni-hannover.de>                            #
# This program is free software under the terms of the MIT license.      #
##########################################################################
#
# This module provides the base data conversion class AbstractFile and
# standard text conversion classes. All data conversion classes should
# inherit from AbstractFile and must provide three methods:
#
# encode_zip(): Return data encoded as bytes string.
# decode_zip(data): Decode and store given bytes string data.
# hash(): Return SHA256 hash from data as hex string.
#
# The hash implementation shoud make sure that semantically equivalent
# data results in the same hash.
#
##########################################################################

import hashlib
import json
import typing
import warnings
from abc import ABC, ABCMeta

import numpy as np
from h5py import Dataset as h5Dataset
from h5py import Group as h5Group

##########################################################################
# Data conversion classes


class _AbstractFileMeta(ABCMeta):
    def __init__(cls, name, bases, namespace, **kwargs):
        # Don't check abstract class
        if name == "AbstractFile":
            super().__init__(name, bases, namespace, **kwargs)
            return

        if "encode" not in namespace and "encode_zip" not in namespace:
            cls.encode_zip = lambda x: (_ for _ in ()).throw(
                NotImplementedError(f"{name} does not implement zip encoding.")
            )
            namespace["encode_zip"] = cls.encode_zip
        if "decode" not in namespace and "decode_zip" not in namespace:
            cls.decode_zip = lambda x, y: (_ for _ in ()).throw(
                NotImplementedError(f"{name} does not implement zip decoding.")
            )
            namespace["decode_zip"] = cls.decode_zip

        if "encode_zip" not in namespace:
            warnings.warn(
                f"Overwriting {name}.encode() is deprecated and might be removed in future versions. Please overwrite {name}.encode_zip() instead.",
                DeprecationWarning,
                stacklevel=2,
            )

        if "decode_zip" not in namespace:
            warnings.warn(
                f"Overwriting {name}.decode() is deprecated and might be removed in future versions. Please overwrite {name}.decode_zip() instead.",
                DeprecationWarning,
                stacklevel=2,
            )
        super().__init__(name, bases, namespace, **kwargs)


class AbstractFile(ABC, metaclass=_AbstractFileMeta):
    """Base class for converting datatypes to their file representation."""

    def __init__(self, data):
        """Constructor to create an instance of the converter class."""
        if isinstance(data, bytes):
            self.decode_zip(data)
        elif isinstance(data, h5Dataset):
            self.decode_hdf5(data)
        else:
            self.data = data

    def hash(self) -> str:
        """Return hex digest of SHA256 hash.

        Returns:
            str: Hex digest of this object as string.
        """

        return hashlib.sha256(self.encode_zip()).hexdigest()

    def encode(self) -> bytes:
        """Encode the Container content to bytes.

        This is function ensures compatibility to conversion classes created before version 1.2.0 and might be removed in the future!

        Returns:
            bytes: Byte string representation of the object.
        """
        return self.encode_zip()

    def decode(self, data: bytes):
        """Decode the Container content from bytes.

        This is function ensures compatibility to conversion classes created before version 1.2.0 and might be removed in the future!

        Args:
            data: bytes from a zip file.
        """
        return self.decode_zip(data)

    def encode_zip(self) -> bytes:
        """Encode the Container content to bytes.

        This is an abstract method and it needs to be overwritten by inheriting class.

        Returns:
            bytes: Byte string representation of the object.
        """
        return self.encode()

    def decode_zip(self, data: bytes):
        """Decode the Container content from bytes.

        This is an abstract method and it neets to be overwritten by inheriting class.

        Args:
            data: bytes from a zip file.
        """
        return self.decode(data)

    def encode_hdf5(self, group: h5Group, name: str):
        """Encode the Container content to a representation for an hdf5 file.

        This method should be overwritten by an inheriting class to provide hdf5 support.

        Args:
            group: HDF5 Group in which to store the data.
            name: name of the dataset to be created.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement hdf5 encoding."
        )

    def decode_hdf5(self, dataset: h5Dataset):
        """Decode the Container content from an HDF5 dataset.

        This method should be overwritten by an inheriting class to provide hdf5 support.

        Args:
            dataset: HDF5 Dataset object.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement hdf5 decoding."
        )


class BinaryFile(AbstractFile):
    """Data conversion class for a binary file."""

    def encode_zip(self) -> bytes:
        """Return byte string stored in this class.

        Returns:
            bytes: Byte string representation of the object.
        """
        return self.data

    def decode_zip(self, data: bytes):
        """Store bytes in this class.

        Args:
            data: bytes read from a zip file.
        """
        self.data = data

    def encode_hdf5(self, group: h5Group, name: str):
        """Store bytes content in this class in an hdf5 Dataset.

        Args:
            group: HDF5 Group in which to store the data.
            name: name of the dataset to be created.
        """
        group.create_dataset(name, data=np.void(self.data))

    def decode_hdf5(self, dataset: h5Dataset):
        """Read bytes content from an hdf5 dataset.

        Args:
            dataset: HDF5 Dataset object.
        """
        self.data = dataset[()].tobytes()


class TextFile(AbstractFile):
    """Data conversion class for a text file."""

    charset = "utf8"
    """charset (str): Character encoding used for translation from text to\
                      bytes."""

    def encode_zip(self) -> bytes:
        """Encode text to bytes string.

        Returns:
            bytes: Byte string representation of the object.
        """

        return bytes(self.data, self.charset)

    def decode_zip(self, data: bytes):
        """Decode text from given bytes string.

        Args:
            data: bytes read from a zip file.
        """

        self.data = data.decode(self.charset)

    def encode_hdf5(self, group: h5Group, name: str):
        """Store text in an HDF5 dataset.

        Args:
            group: HDF5 Group in which to store the data.
            name: name of the dataset to be created.
        """
        group.create_dataset(name, data=bytes(self.data, self.charset))

    def decode_hdf5(self, dataset: h5Dataset):
        """Read text from an HDF5 Dataset.

        Args:
            dataset: HDF5 Dataset object.
        """
        self.data = dataset[()].decode(self.charset)


class JsonFile(AbstractFile):
    """Data conversion class for a JSON file represented as Python
    dictionary."""

    indent = 4
    """indent (int): Indentation of exported JSON files."""
    charset = "utf8"
    """charset (str): Character encoding used for translation from text to\
                      bytes."""

    def sortit(self, data: typing.Union[dict, list, tuple]) -> str:
        """Return compact string representation with keys of all
        sub-dictionaries sorted.

        Args:
            data: Dictionary, list or tuple to convert to string"

        Returns:
            str: String representation of `data`
        """

        if isinstance(data, dict):
            keys = sorted(data.keys())
            data = [k + ": " + self.sortit(data[k]) for k in keys]
            data = ", ".join(data)
            data = "{" + data + "}"
            return data
        elif isinstance(data, (list, tuple)):
            data = [self.sortit(v) for v in data]
            data = ", ".join(data)
            data = "[" + data + "]"
            return data
        return repr(data)

    def hash(self) -> str:
        """Return hex digest of the SHA256 hash calculated from the
        sorted compact representation. This should result in the same
        hash for semantically equal data dictionaries.

        Returns:
            str: Hex digest of this object as string.
        """

        data = bytes(self.sortit(self.data), self.charset)
        return hashlib.sha256(data).hexdigest()

    def encode_zip(self) -> bytes:
        """Convert dictionary to pretty string representation with
        indentation and return it as bytes string.

        Returns:
            bytes: Byte string representation of the object.
        """

        data = json.dumps(
            self.data, sort_keys=True, indent=self.indent, ensure_ascii=False
        )
        return bytes(data, self.charset)

    def decode_zip(self, data: bytes):
        """Decode dictionary from given bytes string.

        Args:
            data: bytes read from a zip file.
        """

        self.data = json.loads(data.decode(self.charset))

    def encode_hdf5(self, group: h5Group, name: str):
        """Store dictionary in an HDF5 dataset.

        This stores the string content inside the dataset.
        Additionally, the first level of attributes are set as HDF5 attributes.

        Args:
            group: HDF5 Group in which to store the data.
            name: name of the dataset to be created.
        """
        ds = group.create_dataset(name, data=self.encode_zip())
        ds.attrs.update({key: json.dumps(val) for key, val in self.data.items()})

    def decode_hdf5(self, dataset: h5Dataset):
        """Read json encoded dictionaries from an HDF5 Dataset.

        Args:
            dataset: HDF5 Dataset object.
        """
        self.data = json.loads(dataset[()].decode(self.charset))


class TabSeparatedValuesFile(AbstractFile):
    """Data conversion class for a tab-separated value file."""

    charset = "utf8"
    """charset (str): Character encoding used for translation from a list of\
                      lists to bytes."""

    def encode_zip(self) -> bytes:
        """Encode 2D array (list of lists) to bytes string.

        Returns:
            bytes: Byte string representation of the object.
        """
        s = "\n".join(["\t".join([str(v) for v in a]) for a in self.data])

        return bytes(s, self.charset)

    def decode_zip(self, data: bytes):
        """Decode 2D array (list of lists) from given bytes string.

        Args:
            data: bytes read from a zip file.
        """

        s = data.decode(self.charset)
        self.data = [[float(x) for x in a.split("\t")] for a in s.split("\n")]

    def encode_hdf5(self, group: h5Group, name: str):
        """Store 2D array in an HDF5 dataset.

        This stores the bytes that would be written to a zip file to an HDF5 dataset.

        Args:
            group: HDF5 Group in which to store the data.
            name: name of the dataset to be created.
        """
        group.create_dataset(name, data=self.encode_zip())

    def decode_hdf5(self, dataset: h5Dataset):
        """Read tsv content from an HDF5 Dataset.

        Args:
            dataset: HDF5 Dataset object.
        """
        self.decode_zip(dataset[()])


class Dataset(AbstractFile):
    """Data conversion class for HDF5 datasets."""

    def hash(self) -> str:
        """Return hex digest of the SHA256 hash of the underlying numpy array.

        Returns:
            str: Hex digest of this object as string.
        """
        return hashlib.sha256(self.data.data).hexdigest()

    def encode_hdf5(self, group: h5Group, name: str):
        """Store numpy array in an HDF5 dataset.

        This uses the representation provided by the h5py library.

        Args:
            group: HDF5 Group in which to store the data.
            name: name of the dataset to be created.
        """
        group.create_dataset(name, data=self.data)

    def decode_hdf5(self, dataset: h5Dataset):
        """Read numpy array from an HDF5 Dataset.

        Args:
            dataset: HDF5 Dataset object.
        """
        self.data = dataset[:]


register = [
    ("bin", BinaryFile, bytes),
    ("json", JsonFile, dict),
    ("txt", TextFile, str),
    ("log", TextFile, None),
    ("pgm", "txt", None),
    ("tsv", TabSeparatedValuesFile, None),
    ("dataset", Dataset, None),
]
