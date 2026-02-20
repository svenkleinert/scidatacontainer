from unittest import TestCase

import numpy as np

from scidatacontainer import Container, register
from scidatacontainer.filenumpy import NpyFile

from . import get_test_container


class FileNumpyTest(TestCase):
    def test_encode_decode(self):
        a = get_test_container()
        register("npx", NpyFile)

        data = np.random.randint(0, 256, (100, 100, 3))

        a["data/test.npx"] = data

        a.write("test.zdc")

        b = Container(file="test.zdc")

        self.assertTrue(np.allclose(a["data/test.npx"], b["data/test.npx"]))

    def test_hash(self):
        a = get_test_container()
        register("npx", NpyFile)

        data = np.reshape(np.arange(100 * 100 * 3), (100, 100, 3))

        a["data/test.npx"] = data
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
            "04c7072b618f2704116a6fc172a1d06970b47e96b964a5998ab3e55b889eec88",
        )

    def test_legacy_hash(self):
        a = get_test_container()
        a["content.json"]["modelVersion"] = "1.0.0"

        register("npx", NpyFile)

        data = np.reshape(np.arange(100 * 100 * 3), (100, 100, 3))

        a["data/test.npx"] = data
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
            "4e4ac07beaa10c8ab87f0da907f70a34e1c89918b1278dde5b75c2e4d4fd5fb6",
        )
