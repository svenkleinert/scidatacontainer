from unittest import TestCase

from scidatacontainer import register, AbstractFile


class DummyFile(AbstractFile):
    pass


class RegisterTest(TestCase):
    def test_registration(self):
        register(".test", DummyFile, str)
        with self.assertRaisesRegex(RuntimeError, "Alias .test123:.test with" +
                                    " default class!"):
            register(".test123", ".test", str)
