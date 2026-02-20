from unittest import TestCase

import numpy as np

from scidatacontainer import Container, register
from scidatacontainer.fileimage import PngFile

from . import get_test_container


class FileImageTest(TestCase):
    def test_encode_decode(self):
        a = get_test_container()
        register("png", PngFile)
        data = np.random.randint(0, 256, (100, 100, 3))

        a["data/test.png"] = data

        a.write("test.zdc")

        b = Container(file="test.zdc")

        self.assertTrue(np.allclose(a["data/test.png"], b["data/test.png"]))

    def test_hash(self):
        a = get_test_container()
        register("png", PngFile)
        data = np.reshape(np.arange(100 * 100 * 3), (100, 100, 3))

        a["data/test.png"] = data
        a.freeze()

        a.write("test.zdc")

        b = Container(file="test.zdc")
        b.hash()

        self.assertEqual(
            a["content.json"]["hash"],
            b["content.json"]["hash"],
        )
        self.assertEqual(
            b["content.json"]["hash"],
            "d5dd9ea62ac5e3a6e11fa0a5efc60b86338fc27f5e9f9774adbc6b2bd9af8acf",
        )
