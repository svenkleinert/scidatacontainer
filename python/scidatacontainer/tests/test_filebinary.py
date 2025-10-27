import os
from unittest import TestCase

from h5py import File as h5File

from scidatacontainer import Container, register
from scidatacontainer.filebase import BinaryFile

from . import get_test_container


class FileBinaryTest(TestCase):
    def test_encode_decode_zip(self):
        a = get_test_container(fileformat="zip")

        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed "
        text += "do eiusmod tempor incididunt ut labore et dolore magna "
        text += "aliqua. Varius duis at consectetur lorem donec massa. Amet "
        text += "consectetur adipiscing elit ut aliquam purus sit amet. Duis "
        text += "ultricies lacus sed turpis tincidunt id aliquet risus "
        text += "feugiat. Dui id ornare arcu odio ut sem nulla pharetra."

        btext = text.encode("utf-8")

        a["data/test.exe"] = btext
        self.assertEqual(btext, a["data/test.exe"])

        a.write("test.zdc")

        b = Container(file="test.zdc")

        self.assertEqual(a["data/test.exe"], b["data/test.exe"])

        self.assertEqual(b["data/test.exe"].decode("utf-8"), text)

    def test_encode_decode_hdf5(self):
        register("exe", BinaryFile)

        a = get_test_container(fileformat="hdf5")

        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed "
        text += "do eiusmod tempor incididunt ut labore et dolore magna "
        text += "aliqua. Varius duis at consectetur lorem donec massa. Amet "
        text += "consectetur adipiscing elit ut aliquam purus sit amet. Duis "
        text += "ultricies lacus sed turpis tincidunt id aliquet risus "
        text += "feugiat. Dui id ornare arcu odio ut sem nulla pharetra."

        btext = text.encode("utf-8")

        a["data/test.exe"] = btext
        self.assertEqual(btext, a["data/test.exe"])

        a.write("test.h5dc")
        with h5File("test.h5dc") as fp:
            self.assertEqual(fp["data/test_exe"][()].tobytes(), btext)

        b = Container(file="test.h5dc")
        os.remove("test.h5dc")
        self.assertEqual(a["data/test.exe"], b["data/test.exe"])
