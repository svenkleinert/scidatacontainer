import hashlib
import os
import zipfile
from unittest import TestCase

import numpy as np
from h5py import File as h5File

from scidatacontainer import Container
from scidatacontainer.filebase import Dataset, TabSeparatedValuesFile

from . import get_test_container


class DatasetTest(TestCase):
    def test_encode_decode_zip(self):
        a = get_test_container(fileformat="zip")

        data = np.random.rand(200, 199)
        a["data/test.dataset"] = data

        with self.assertRaisesRegex(
            NotImplementedError, "Dataset does not implement zip encoding."
        ):
            a.write("test.zdc")

        del a["data/test.dataset"]
        a.write("test.zdc")

        with zipfile.ZipFile("test.zdc", "w") as fp:
            fp.writestr("data/test.dataset", TabSeparatedValuesFile(data).encode_zip())

        with self.assertRaisesRegex(
            NotImplementedError, "Dataset does not implement zip decoding."
        ):
            _ = Container(file="test.zdc")

        os.remove("test.zdc")

    def test_encode_decode_hdf5(self):
        a = get_test_container(fileformat="hdf5")
        data = np.random.rand(200, 199)
        a["data/test.dataset"] = data
        self.assertTrue(np.allclose(data, a["data/test.dataset"]))

        a.write("test.h5dc")

        with h5File("test.h5dc") as fp:
            self.assertTrue(np.allclose(fp["data/test_dataset"], data))

        b = Container(file="test.h5dc")
        os.remove("test.h5dc")

        self.assertTrue(np.allclose(a["data/test.dataset"], b["data/test.dataset"]))
        self.assertTrue(np.allclose(data, b["data/test.dataset"]))

        self.assertEqual(Dataset(data).hash(), Dataset(a["data/test.dataset"]).hash())
        self.assertEqual(
            hashlib.sha256(data.data).hexdigest(),
            Dataset(a["data/test.dataset"]).hash(),
        )
