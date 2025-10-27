import json
import os
from unittest import TestCase

from h5py import File as h5File

from scidatacontainer import Container
from scidatacontainer.filebase import JsonFile

from . import get_test_container


class FileJsonTest(TestCase):
    def test_encode_decode_zip(self):
        a = get_test_container(fileformat="zip")

        a.write("test.zdc")

        b = Container(file="test.zdc")
        os.remove("test.zdc")

        self.assertEqual(a["meta.json"], b["meta.json"])
        self.assertEqual(a["content.json"], b["content.json"])

    def test_encode_decode_hdf5(self):
        a = get_test_container(fileformat="hdf5")

        a.write("test.h5dc")

        with h5File("test.h5dc") as fp:
            self.assertEqual(fp["meta_json"][()], bytes(JsonFile(a.meta).encode_zip()))
            self.assertEqual(
                fp["content_json"][()], bytes(JsonFile(a.content).encode_zip())
            )
            self.assertEqual(json.loads(fp["meta_json"][()]), a.meta)
            self.assertEqual(json.loads(fp["content_json"][()]), a.content)

        b = Container(file="test.h5dc")
        os.remove("test.h5dc")

        self.assertEqual(a["meta.json"], b["meta.json"])
        self.assertEqual(a["content.json"], b["content.json"])
