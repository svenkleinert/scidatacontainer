from unittest import TestCase

import numpy as np

from scidatacontainer import AbstractFile
from scidatacontainer.filebase import (
    BinaryFile,
    JsonFile,
    TabSeparatedValuesFile,
    TextFile,
)
from scidatacontainer.fileimage import PngFile
from scidatacontainer.filenumpy import NpyFile

from . import get_test_container


class LegacyFileTest(TestCase):
    def test_deprecation_warning(self):
        with self.assertWarnsRegex(
            DeprecationWarning,
            r"Overwriting DeprecatedFile\.encode\(\) is deprecated and might be removed in future versions\. Please overwrite DeprecatedFile\.encode_zip\(\) instead.",
        ):

            class DeprecatedFile(AbstractFile):
                def encode(self):
                    return self.data

                def decode(self, data):
                    self.data = data

        with self.assertWarnsRegex(
            DeprecationWarning,
            r"Overwriting DeprecatedFile\.decode\(\) is deprecated and might be removed in future versions\. Please overwrite DeprecatedFile\.decode_zip\(\) instead.",
        ):

            class DeprecatedFile(AbstractFile):
                def encode(self):
                    return self.data

                def decode(self, data):
                    self.data = data

    def test_legacy_alias_methods(self):
        data = b"test123"
        with self.assertWarns(DeprecationWarning):

            class DeprecatedFile(AbstractFile):
                def encode(self):
                    return self.data

                def decode(self, data):
                    self.data = data

        a = DeprecatedFile(data)
        self.assertEqual(a.encode(), a.encode_zip())

        b = DeprecatedFile([])
        b.decode_zip(a.encode_zip())
        self.assertEqual(a.data, b.data)
        self.assertEqual(a.data, data)

    def test_binary_legacy_interface(self):
        data = b"test123"
        self.assertEqual(BinaryFile(data).encode(), BinaryFile(data).encode_zip())

        a = BinaryFile(b"")
        b = BinaryFile(b"")
        a.decode(BinaryFile(data).encode_zip())
        b.decode_zip(BinaryFile(data).encode_zip())
        self.assertEqual(a.data, b.data)
        self.assertEqual(a.data, data)

    def test_json_legacy_interface(self):
        content = get_test_container().content
        meta = get_test_container().meta
        self.assertEqual(JsonFile(content).encode(), JsonFile(content).encode_zip())
        self.assertEqual(JsonFile(meta).encode(), JsonFile(meta).encode_zip())

        a = JsonFile({})
        b = JsonFile({})
        a.decode(JsonFile(content).encode_zip())
        b.decode_zip(JsonFile(content).encode_zip())
        self.assertEqual(a.data, b.data)
        self.assertEqual(a.data, content)

        a.decode(JsonFile(meta).encode_zip())
        b.decode_zip(JsonFile(meta).encode_zip())
        self.assertEqual(a.data, b.data)
        self.assertEqual(a.data, meta)

    def test_tsv_legacy_interface(self):
        arr_data = np.random.rand(199, 200)
        self.assertEqual(
            TabSeparatedValuesFile(arr_data).encode(),
            TabSeparatedValuesFile(arr_data).encode_zip(),
        )

        a = TabSeparatedValuesFile([])
        b = TabSeparatedValuesFile([])
        a.decode(TabSeparatedValuesFile(arr_data).encode_zip())
        b.decode_zip(TabSeparatedValuesFile(arr_data).encode_zip())
        self.assertTrue(np.allclose(a.data, b.data))
        self.assertTrue(np.allclose(a.data, arr_data))

    def test_text_legacy_interface(self):
        data = "test123"
        self.assertEqual(TextFile(data).encode(), TextFile(data).encode_zip())

        a = TextFile("")
        b = TextFile("")
        a.decode(TextFile(data).encode_zip())
        b.decode_zip(TextFile(data).encode_zip())
        self.assertEqual(a.data, b.data)
        self.assertEqual(a.data, data)

    def test_png_legacy_interface(self):
        arr_data = np.random.rand(199, 200)
        self.assertEqual(PngFile(arr_data).encode(), PngFile(arr_data).encode_zip())

        a = PngFile([])
        b = PngFile([])
        a.decode(PngFile(arr_data).encode_zip())
        b.decode_zip(PngFile(arr_data).encode_zip())
        self.assertTrue(np.allclose(a.data, b.data))

    def test_npy_legacy_interface(self):
        arr_data = np.random.rand(199, 200)
        self.assertEqual(NpyFile(arr_data).encode(), NpyFile(arr_data).encode_zip())

        a = NpyFile([])
        b = NpyFile([])
        a.decode(NpyFile(arr_data).encode_zip())
        b.decode_zip(NpyFile(arr_data).encode_zip())
        self.assertTrue(np.allclose(a.data, b.data))
        self.assertTrue(np.allclose(a.data, arr_data))
