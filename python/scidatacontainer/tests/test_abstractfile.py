from unittest import TestCase

from h5py import File as h5File

from scidatacontainer import Container, register
from scidatacontainer.filebase import AbstractFile

from . import get_test_container


class ZipOnlyFile(AbstractFile):
    def encode_zip(self):
        return self.data

    def decode_zip(self, data):
        self.data = data


class AbstractFileTest(TestCase):
    def test_no_default_hdf5(self):
        register("exe", ZipOnlyFile, None)

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

        with self.assertRaisesRegex(
            NotImplementedError, r"ZipOnlyFile does not implement hdf5 encoding\."
        ):
            a.write("test.h5dc")

        del a["data/test.exe"]

        a.write("test.h5dc")
        with h5File("test.h5dc", "w") as fd:
            fd.create_dataset("data/test_exe", data=b"test123")

        with self.assertRaisesRegex(
            NotImplementedError, r"ZipOnlyFile does not implement hdf5 decoding\."
        ):
            _ = Container(file="test.h5dc")
