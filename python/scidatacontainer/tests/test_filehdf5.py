from io import BytesIO
from unittest import TestCase
from zipfile import ZipFile

import h5py
import numpy as np

from scidatacontainer import Container

from . import get_test_container


class FileHdf5Test(TestCase):
    def test_encode_decode(self):
        a = get_test_container()

        data = np.random.randint(0, 256, (10, 10, 3))

        f = h5py.File.in_memory()
        dset = f.create_dataset("hdf5_dataset", data=data)

        moredata = {
            "data1": np.random.randint(0, 256, (10, 10, 3)),
            "data2": np.random.randint(0, 256, (10, 10, 3)),
            "data3": dset,
            "attr1": "test123",
            "attr2": 123,
            "attr3": 1.23,
        }

        a["data/test.hdf5"] = data
        a["data/test2.hdf5"] = moredata

        a.write("test.zdc")

        b = Container(file="test.zdc")
        self.assertTrue(np.allclose(a["data/test.hdf5"], b["data/test.hdf5"]))
        self.assertTrue(np.allclose(moredata["data1"], b["data/test2.hdf5"]["data1"]))
        self.assertTrue(np.allclose(moredata["data2"], b["data/test2.hdf5"]["data2"]))
        self.assertTrue(np.allclose(data, b["data/test2.hdf5"]["data3"]))
        self.assertEqual(moredata["attr1"], b["data/test2.hdf5"]["attr1"])
        self.assertEqual(moredata["attr2"], b["data/test2.hdf5"]["attr2"])
        self.assertEqual(moredata["attr3"], b["data/test2.hdf5"]["attr3"])

        a.release()
        a["data/test3.hdf5"] = [data]
        with self.assertRaisesRegex(NotImplementedError, "Unknown data type list!"):
            a.write("test.zdc")

    def test_file_content(self):
        a = get_test_container()

        data = np.random.randint(0, 256, (10, 10, 3))
        moredata = {
            "data1": np.random.randint(0, 256, (10, 10, 3)),
            "data2": np.random.randint(0, 256, (10, 10, 3)),
            "attr1": "test123",
            "attr2": 123,
            "attr3": 1.23,
        }

        a["data/test.hdf5"] = data
        a["data/test2.hdf5"] = moredata

        a.write("test.zdc")

        with ZipFile("test.zdc") as zfile:
            with BytesIO(zfile.read("data/test.hdf5")) as fp:
                with h5py.File(fp) as h5file:
                    self.assertTrue(np.allclose(a["data/test.hdf5"], h5file["dataset"]))
            with BytesIO(zfile.read("data/test2.hdf5")) as fp:
                with h5py.File(fp) as h5file:
                    self.assertTrue(np.allclose(moredata["data1"], h5file["data1"]))
                    self.assertTrue(np.allclose(moredata["data2"], h5file["data2"]))
                    self.assertEqual(moredata["attr1"], h5file.attrs["attr1"])
                    self.assertEqual(moredata["attr2"], h5file.attrs["attr2"])
                    self.assertEqual(moredata["attr3"], h5file.attrs["attr3"])

    def test_hash(self):
        a = get_test_container()
        del a["meas/image.tsv"]  # remove int array that causes float precision error
        data = np.reshape(np.arange(10 * 10 * 3), (10, 10, 3))
        moredata = {
            "data1": data + 100,
            "data2": data * 10,
            "attr1": "test123",
            "attr2": 123,
            "attr3": np.float64(1.23),
            "attr4": [123, 1.24],
            "attr5": ["123", "1.24"],
            "attr6": [[123, 12], [1234, 1234]],
        }

        a["data/test.hdf5"] = data
        a["data/test2.hdf5"] = moredata
        a.freeze()
        a.write("test.zdc")

        b = Container(file="test.zdc")
        b.hash()

        self.assertEqual(a["content.json"]["hash"], b["content.json"]["hash"])
        self.assertEqual(
            b["content.json"]["hash"],
            "357bf6e2d63861cdda9239f83b23f293b3149d4d4a5283a742965199a02a7990",
        )
