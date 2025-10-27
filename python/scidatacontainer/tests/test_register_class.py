from unittest import TestCase

from scidatacontainer import AbstractFile, register


class DummyFile(AbstractFile):
    pass


class EmptyFileClass:
    pass


class RegisterTest(TestCase):
    def test_registration(self):
        register(".test", DummyFile, str)
        with self.assertRaisesRegex(
            RuntimeError, "Alias .test123:.test with default class!"
        ):
            register(".test123", ".test", str)

        with self.assertRaisesRegex(
            RuntimeError,
            "Conversion class EmptyFileClass is not derived from AbstractFile!",
        ):
            register(".test", EmptyFileClass, str)
