from unittest import TestCase

from scidatacontainer import Container

from . import get_test_container


class FileIOObjectTest(TestCase):
    def test_access(self):
        a = get_test_container()

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

        b = Container(file="test.zdc", ignore_files=["data/test.exe"])

        with self.assertRaisesRegex(
            KeyError, r"Item 'data/test\.exe' was ignored while reading the file\."
        ):
            b["data/test.exe"]

    def test_release(self):
        a = get_test_container()

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
        b = Container(file="test.zdc", ignore_files=["data/test.exe"])
        with self.assertRaisesRegex(
            RuntimeError,
            r"Modifying a file that was only partially read is not supported! Make sure 'ignore_files' is empty during initialisation.",
        ):
            b.release()

    def test_load_incomplete(self):
        a = get_test_container()
        a["content.json"]["complete"] = False

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

        with self.assertRaisesRegex(
            RuntimeError,
            r"Partial loading of files only supported for immutable files!",
        ):
            b = Container(file="test.zdc", ignore_files=["data/test.exe"])
