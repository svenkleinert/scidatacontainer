import os
from unittest import TestCase

import numpy as np
from h5py import File as h5File

from scidatacontainer import Container, register
from scidatacontainer.filenumpy import NpyFile

from . import get_test_container


class FileNumpyTest(TestCase):
    def test_encode_decode_zip(self):
        a = get_test_container(fileformat="zip")

        data = np.random.randint(0, 256, (100, 100, 3))

        a["data/test.npy"] = data

        a.write("test.zdc")

        b = Container(file="test.zdc")
        os.remove("test.zdc")

        self.assertTrue(np.allclose(a["data/test.npy"], b["data/test.npy"]))

    def test_encode_decode_hdf5(self):
        a = get_test_container(fileformat="hdf5")

        data = np.random.randint(0, 256, (100, 100, 3))

        a["data/test.npy"] = data

        a.write("test.h5dc")

        with h5File("test.h5dc") as fp:
            self.assertEqual(
                fp["data/test_npy"][()].tobytes(), NpyFile(data).encode_zip()
            )

        b = Container(file="test.h5dc")
        os.remove("test.h5dc")

        self.assertTrue(np.allclose(a["data/test.npy"], b["data/test.npy"]))
