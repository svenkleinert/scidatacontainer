import os
from unittest import TestCase

from h5py import File as h5File

from scidatacontainer import Container

from . import get_test_container


class FileTextTest(TestCase):
    def test_encode_decode_zip(self):
        a = get_test_container(fileformat="zip")

        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed "
        text += "do eiusmod tempor incididunt ut labore et dolore magna "
        text += "aliqua. Varius duis at consectetur lorem donec massa. Amet "
        text += "consectetur adipiscing elit ut aliquam purus sit amet. Duis "
        text += "ultricies lacus sed turpis tincidunt id aliquet risus "
        text += "feugiat. Dui id ornare arcu odio ut sem nulla pharetra."

        a["data/test.txt"] = text
        self.assertEqual(text, a["data/test.txt"])

        a.write("test.zdc")

        b = Container(file="test.zdc")
        os.remove("test.zdc")

        self.assertEqual(a["data/test.txt"], b["data/test.txt"])

    def test_encode_decode_hdf5(self):
        a = get_test_container(fileformat="hdf5")

        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed "
        text += "do eiusmod tempor incididunt ut labore et dolore magna "
        text += "aliqua. Varius duis at consectetur lorem donec massa. Amet "
        text += "consectetur adipiscing elit ut aliquam purus sit amet. Duis "
        text += "ultricies lacus sed turpis tincidunt id aliquet risus "
        text += "feugiat. Dui id ornare arcu odio ut sem nulla pharetra."

        a["data/test.txt"] = text
        self.assertEqual(text, a["data/test.txt"])

        a.write("test.h5dc")

        with h5File("test.h5dc") as fp:
            self.assertTrue(fp["data/test_txt"][()], bytes(text, "utf8"))

        b = Container(file="test.h5dc")
        os.remove("test.h5dc")

        self.assertEqual(a["data/test.txt"], b["data/test.txt"])
