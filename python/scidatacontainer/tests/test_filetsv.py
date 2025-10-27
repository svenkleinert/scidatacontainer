import os
from unittest import TestCase

import numpy as np
from h5py import File as h5File

from scidatacontainer import Container

from . import get_test_container


class FileTsvTest(TestCase):
    def test_encode_decode_zip(self):
        a = get_test_container(fileformat="zip")

        data = np.random.rand(200, 199)
        a["data/test.tsv"] = data
        self.assertTrue(np.allclose(data, a["data/test.tsv"]))

        a.write("test.zdc")

        b = Container(file="test.zdc")
        os.remove("test.zdc")

        self.assertTrue(np.allclose(a["data/test.tsv"], b["data/test.tsv"]))
        self.assertTrue(np.allclose(data, b["data/test.tsv"]))

    def test_encode_decode_hdf5(self):
        a = get_test_container(fileformat="hdf5")
        data = np.random.rand(200, 199)
        a["data/test.tsv"] = data
        self.assertTrue(np.allclose(data, a["data/test.tsv"]))

        a.write("test.h5dc")

        with h5File("test.h5dc") as fp:
            s = "\n".join(["\t".join([str(v) for v in a]) for a in data])
            self.assertTrue(fp["data/test_tsv"][()], bytes(s, "utf8"))

        b = Container(file="test.h5dc")
        os.remove("test.h5dc")

        self.assertTrue(np.allclose(a["data/test.tsv"], b["data/test.tsv"]))
        self.assertTrue(np.allclose(data, b["data/test.tsv"]))
