from pathlib import Path
from tempfile import NamedTemporaryFile
from unittest import TestCase

from scidatacontainer import Container

from . import get_test_container


class FilePathTest(TestCase):
    def test_encode(self):
        a = get_test_container()

        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed "
        text += "do eiusmod tempor incididunt ut labore et dolore magna "
        text += "aliqua. Varius duis at consectetur lorem donec massa. Amet "
        text += "consectetur adipiscing elit ut aliquam purus sit amet. Duis "
        text += "ultricies lacus sed turpis tincidunt id aliquet risus "
        text += "feugiat. Dui id ornare arcu odio ut sem nulla pharetra."

        with NamedTemporaryFile() as tfp:
            tfp.write(text.encode("utf-8"))
            tfp.seek(0)

            a["data/test.exe"] = Path(tfp.name)

            a.write("test.zdc")

        b = Container(file="test.zdc")
        self.assertEqual(b["data/test.exe"].decode("utf-8"), text)

    def test_invalid_file_path(self):
        a = get_test_container()

        a["data/test.exe"] = Path("/this/path/doesnt/exist")

        with self.assertRaisesRegex(
            FileNotFoundError,
            r"\[Errno 2\] No such file or directory: '/this/path/doesnt/exist'",
        ):
            a.write("test.zdc")

    def test_hash(self):
        a = get_test_container()

        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed "
        text += "do eiusmod tempor incididunt ut labore et dolore magna "
        text += "aliqua. Varius duis at consectetur lorem donec massa. Amet "
        text += "consectetur adipiscing elit ut aliquam purus sit amet. Duis "
        text += "ultricies lacus sed turpis tincidunt id aliquet risus "
        text += "feugiat. Dui id ornare arcu odio ut sem nulla pharetra."

        with NamedTemporaryFile() as tfp:
            tfp.write(text.encode("utf-8"))
            tfp.seek(0)

            a["data/test.exe"] = Path(tfp.name)

            a.freeze()
            a.write("test.zdc")

        b = Container(file="test.zdc")
        b.hash()
        self.assertEqual(a["content.json"]["hash"], b["content.json"]["hash"])
        self.assertEqual(
            b["content.json"]["hash"],
            "f66ca1f63274a613e8769902349cd6182403a45fb75df2db9afb2fe0426b9bec",
        )

    def test_changing_hash(self):
        """
        This test covers the case that a decode-encode cycle would change the data.
        This might be the case for example for json files that are not correctly formatted
        or have unsorted keys.
        """
        a = get_test_container()
        text = '{"a": "123", "b": true}'
        with NamedTemporaryFile() as tfp:
            tfp.write(text.encode("utf-8"))
            tfp.seek(0)

            a["data/test.json"] = Path(tfp.name)

            a.freeze()
            a.write("test.zdc")

        b = Container(file="test.zdc")
        b.hash()
        self.assertNotEqual(a["content.json"]["hash"], b["content.json"]["hash"])

    def test_legacy_hash(self):
        a = get_test_container()
        a["content.json"]["modelVersion"] = "1.0.0"

        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed "
        text += "do eiusmod tempor incididunt ut labore et dolore magna "
        text += "aliqua. Varius duis at consectetur lorem donec massa. Amet "
        text += "consectetur adipiscing elit ut aliquam purus sit amet. Duis "
        text += "ultricies lacus sed turpis tincidunt id aliquet risus "
        text += "feugiat. Dui id ornare arcu odio ut sem nulla pharetra."

        with NamedTemporaryFile() as tfp:
            tfp.write(text.encode("utf-8"))
            tfp.seek(0)

            a["data/test.exe"] = Path(tfp.name)

            with self.assertRaisesRegex(
                RuntimeError,
                "File like objects are only supported from modelVersion '1.0.1' on.",
            ):
                a.freeze()
                a.write("test.zdc")
