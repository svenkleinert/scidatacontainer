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
