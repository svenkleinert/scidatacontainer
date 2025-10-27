import os
from unittest import TestCase

import numpy as np
from h5py import File as h5File

from scidatacontainer import Container, register
from scidatacontainer.fileimage import PngFile

from . import get_test_container


class FileImageTest(TestCase):
    def test_encode_decode_zip(self):
        a = get_test_container(fileformat="zip")
        data = np.random.randint(0, 256, (100, 100, 3))

        a["data/test.png"] = data

        a.write("test.zdc")

        b = Container(file="test.zdc")

        self.assertTrue(np.allclose(a["data/test.png"], b["data/test.png"]))

    def test_encode_decode_hdf5(self):
        a = get_test_container(fileformat="hdf5")
        data = np.random.randint(0, 256, (100, 100, 3))

        a["data/test.png"] = data

        a.write("test.h5dc")

        with h5File("test.h5dc") as fp:
            self.assertEqual(
                fp["data/test_png"][()].tobytes(),
                PngFile(a["data/test.png"]).encode_zip(),
            )

        b = Container(file="test.h5dc")
        os.remove("test.h5dc")
        self.assertTrue(np.allclose(a["data/test.png"], b["data/test.png"]))
