import copy
import os

from scidatacontainer import Container

from ._abstract_container_test import AbstractContainerTest


class TestStaticContainer(AbstractContainerTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.items["content.json"]["static"] = True
        cls.items_minimal["content.json"]["static"] = True

    def _compare_with_items(self, dc, check_model_version=True):
        super()._compare_with_items(dc, check_model_version)
        self._check_timestamp(dc["content.json"]["created"])

        self._check_timestamp(dc["content.json"]["storageTime"])

        self.assertTrue(dc["content.json"]["complete"])

        self.assertTrue(dc["content.json"]["static"])

    def _compare_with_minimal_items(self, dc):
        super()._compare_with_minimal_items(dc)
        self._check_timestamp(dc["content.json"]["created"])

        self._check_timestamp(dc["content.json"]["storageTime"])

        self.assertTrue(dc["content.json"]["complete"])

        self.assertTrue(dc["content.json"]["static"])

    def test_container_creation(self):
        items = copy.deepcopy(self.items)
        items["content.json"]["static"] = True
        dc = Container(items=items)

        self._compare_with_items(dc)
        self.assertTrue(dc["content.json"]["static"])
        self.assertIsNotNone(dc["content.json"]["hash"])

        self.dc = dc

    def test_container_creation_minimal(self):
        items = copy.deepcopy(self.items_minimal)
        items["content.json"]["static"] = True
        dc = Container(items=items)

        self._compare_with_minimal_items(dc)
        self.assertTrue(dc["content.json"]["static"])
        self.assertIsNotNone(dc["content.json"]["hash"])

        self.dc = dc

    def test_freeze(self):
        items = copy.deepcopy(self.items)
        items["content.json"]["static"] = False
        dc = Container(items=items)

        super()._compare_with_items(dc)
        self.assertIsNone(dc["content.json"]["hash"])
        self.assertFalse(dc["content.json"]["static"])

        dc.freeze()

        self._compare_with_items(dc)
        self.assertTrue(dc["content.json"]["static"])
        self.assertIsNotNone(dc["content.json"]["hash"])
        self.assertEqual(
            dc["content.json"]["hash"],
            "e1260e851a77e4b2d56aab0c33037a98fbdb4684b94461a9ace914bd07220dc4",
        )

        self.dc = dc

    def test_legacy_freeze(self):
        items = copy.deepcopy(self.items)
        items["content.json"]["static"] = False
        dc = Container(items=items)
        dc["content.json"]["modelVersion"] = "1.0.0"

        super()._compare_with_items(dc, check_model_version=False)
        self.assertIsNone(dc["content.json"]["hash"])
        self.assertFalse(dc["content.json"]["static"])

        dc.freeze()

        self._compare_with_items(dc, check_model_version=False)
        self.assertTrue(dc["content.json"]["static"])
        self.assertIsNotNone(dc["content.json"]["hash"])
        self.assertEqual(
            dc["content.json"]["hash"],
            "7a836281f4631bc6d17f41bf3b03dd1de4fd7fbcec08ea588c19752ab3668905",
        )

        self.items["content.json"]["modelVersion"] = "1.0.1"

    def test_freeze_minimal(self):
        items = copy.deepcopy(self.items_minimal)
        items["content.json"]["static"] = False
        dc = Container(items=items)

        super()._compare_with_minimal_items(dc)

        self.assertIsNone(dc["content.json"]["hash"])
        self.assertFalse(dc["content.json"]["static"])

        dc.freeze()

        self._compare_with_minimal_items(dc)
        self.assertTrue(dc["content.json"]["static"])
        self.assertIsNotNone(dc["content.json"]["hash"])
        self.assertEqual(
            dc["content.json"]["hash"],
            "10908bd58e451ef5c8ad1e575128fb3444e81675c434ccaf85d60d2ec8202e65",
        )

        self.dc = dc

    def test_hash_collision(self):
        self.test_freeze()

        old_hash = self.dc["content.json"]["hash"]

        self.dc.release()

        del self.dc["meas/image.tsv"]
        self.dc["meas/image3.tsv"] = self.data

        self.dc.freeze()
        self.assertNotEqual(old_hash, self.dc["content.json"]["hash"])

    def test_write(self, clean=True):
        self.test_freeze()
        self.dc.write(self.export_filename)
        if clean:
            os.remove(self.export_filename)

    def test_read(self):
        self.test_write(clean=False)
        dc = Container(file=self.export_filename)

        self._compare_with_items(dc)

        self.assertTrue(dc["content.json"]["static"])

        old_hash = dc["content.json"]["hash"]
        self.assertIsNotNone(dc["content.json"]["hash"])

        dc.hash()
        self.assertIsNotNone(dc["content.json"]["hash"])
        # new hash is equal with the old one
        self.assertEqual(old_hash, dc["content.json"]["hash"])

    def test_read_wrong_hash(self, clean=True):
        self.test_freeze()
        self.dc.content["hash"] += "ab"
        self.dc.write(self.export_filename)

        with self.assertRaises(RuntimeError) as cm:
            Container(file=self.export_filename)

        self.assertEqual(cm.exception.args[0], "Wrong hash!")

        if clean:
            os.remove(self.export_filename)

    def test_read_wrong_legacy_hash(self, clean=True):
        self.test_freeze()
        self.dc.release()
        self.dc.content["modelVersion"] = "1.0.0"
        self.dc.hash()
        self.dc.freeze()
        self.dc.content["hash"] += "ab"
        self.dc.write(self.export_filename)

        with self.assertRaises(RuntimeError) as cm:
            Container(file=self.export_filename)

        self.assertEqual(cm.exception.args[0], "Wrong hash!")

        if clean:
            os.remove(self.export_filename)

    def test_print(self):
        self.test_freeze()
        s = self.dc.__str__()

        self.assertIn("Static Container", s)
        ct = self.items["content.json"]["containerType"]
        self.assertIn(
            "type:        " + ct["name"] + " " + ct["version"] + " (" + ct["id"] + ")",
            s,
        )
        self.assertIn("uuid:        " + self.dc["content.json"]["uuid"], s)
        self.assertIn("replaces:    " + self.dc["content.json"]["replaces"], s)
        self.assertIn("hash:        " + self.dc["content.json"]["hash"], s)
        self.assertIn("created:     " + self.dc["content.json"]["created"], s)
        self.assertIn("storageTime: " + self.dc["content.json"]["storageTime"], s)
        self.assertIn("author:      " + self.dc["meta.json"]["author"], s)

    def test_immutable(self):
        self.test_freeze()
        with self.assertRaisesRegex(RuntimeError, "Immutable container!"):
            self.dc["data/test.txt"] = "Test123"
