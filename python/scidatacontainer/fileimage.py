##########################################################################
# Copyright (c) 2023 Reinhard Caspary                                    #
# <reinhard.caspary@phoenixd.uni-hannover.de>                            #
# This program is free software under the terms of the MIT license.      #
##########################################################################
#
# This module provides data conversion classes for image files. All
# data conversion classes should inherit from filebase.AbstractFile and must
# provide three methods:
#
# encode(): Return data encoded as bytes string.
# decode(data): Decode and store given bytes string data.
# hash(): Return SHA256 hash from data as hex string.
#
# The hash implementation shoud make sure that semantically equivalent
# data results in the same hash.
#
##########################################################################


import cv2 as cv
import numpy as np
from h5py import Dataset as h5Dataset
from h5py import Group as h5Group

from .filebase import AbstractFile


class PngFile(AbstractFile):
    """Data conversion class for PNG image."""

    def encode_zip(self):
        """Convert image to bytes string."""

        return cv.imencode(".png", self.data)[1].tobytes()

    def decode_zip(self, data):
        """Decode image from bytes string."""
        flags = cv.IMREAD_ANYDEPTH | cv.IMREAD_ANYCOLOR
        self.data = np.frombuffer(data, dtype=np.uint8)
        self.data = cv.imdecode(self.data, flags=flags)

    def encode_hdf5(self, group: h5Group, name: str):
        """Create image byte string as htf5 dataset."""
        group.create_dataset(name, data=np.void(self.encode_zip()))

    def decode_hdf5(self, dataset: h5Dataset):
        self.decode_zip(dataset[()].tobytes())


register = [
    ("png", PngFile, None),
]
