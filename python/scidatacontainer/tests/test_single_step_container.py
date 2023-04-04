import copy
import os


from scidatacontainer import Container

from ._abstract_container_test import AbstractContainerTest


class TestSingleStepContainer(AbstractContainerTest):
    def _compare_with_items(self, dc):
        super()._compare_with_items(dc)
        self.assertFalse(dc["content.json"]["static"])
        self.assertEqual(self.timestamp,
                         dc["content.json"]["created"])

        self.assertEqual(self.timestamp,
                         dc["content.json"]["modified"])
        self.assertTrue(dc["content.json"]["complete"])

    def _compare_with_minimal_items(self, dc):
        super()._compare_with_minimal_items(dc)
        self.assertFalse(dc["content.json"]["static"])
        self.assertEqual(self.timestamp,
                         dc["content.json"]["created"])

        self.assertEqual(self.timestamp,
                         dc["content.json"]["modified"])
        self.assertTrue(dc["content.json"]["complete"])

    def test_container_creation(self):
        items = self.items
        with self.assertRaisesRegex(RuntimeError, "No data!"):
            dc = Container()

        dc = Container(items=items)

        self._compare_with_items(dc)

        self.assertIsNone(dc["content.json"]["hash"])
        dc.hash()
        self.assertIsNotNone(dc["content.json"]["hash"])

        self.dc = dc

    def test_container_creation_minimal(self):
        items = self.items_minimal
        dc = Container(items=items)

        self._compare_with_minimal_items(dc)

        self.dc = dc

    def test_write(self, clean=True):
        self.test_container_creation()
        self.dc.write(self.export_filename)
        if clean:
            os.remove(self.export_filename)

    def test_read(self):
        self.test_write(clean=False)
        dc = Container(file=self.export_filename)

        self._compare_with_items(dc)

        old_hash = dc["content.json"]["hash"]
        self.assertIsNotNone(dc["content.json"]["hash"])

        dc.hash()
        self.assertIsNotNone(dc["content.json"]["hash"])
        # new hash is equal with the old one
        self.assertEqual(old_hash, dc["content.json"]["hash"])

    def test_content_validation(self):
        items = copy.deepcopy(self.items)
        del items["content.json"]
        with self.assertRaisesRegex(RuntimeError,
                                    "Item 'content.json' is missing!"):
            Container(items=items)

        items = copy.deepcopy(self.items)
        del items["content.json"]["containerType"]

        with self.assertRaisesRegex(RuntimeError,
                                    "Attribute 'containerType' is missing!"):
            Container(items=items)

        items = copy.deepcopy(self.items)
        items["content.json"]["containerType"] = ["name", "test"]

        with self.assertRaisesRegex(RuntimeError,
                                    "Attribute containerType is no " +
                                    "dictionary!"):
            Container(items=items)

        items = copy.deepcopy(self.items)
        del items["content.json"]["containerType"]["name"]
        with self.assertRaisesRegex(RuntimeError,
                                    "Name of containerType is missing!"):
            Container(items=items)

        items = copy.deepcopy(self.items)
        del items["content.json"]["containerType"]["version"]
        with self.assertRaisesRegex(RuntimeError,
                                    "Version of containerType is missing!"):
            Container(items=items)

        items = copy.deepcopy(self.items)
        del items["content.json"]["usedSoftware"][0]["name"]
        with self.assertRaisesRegex(RuntimeError,
                                    "Software name is missing!"):
            Container(items=items)

        items = copy.deepcopy(self.items)
        del items["content.json"]["usedSoftware"][0]["version"]
        with self.assertRaisesRegex(RuntimeError,
                                    "Software version is missing!"):
            Container(items=items)

        items = copy.deepcopy(self.items)
        del items["content.json"]["usedSoftware"][1]["idType"]
        with self.assertRaisesRegex(RuntimeError,
                                    "Type of software reference id is " +
                                    "missing!"):
            Container(items=items)

    def test_meta_validation(self):
        items = copy.deepcopy(self.items)
        del items["meta.json"]
        with self.assertRaisesRegex(RuntimeError,
                                    "Item 'meta.json' is missing!"):
            Container(items=items)

        items = copy.deepcopy(self.items)
        del items["meta.json"]["title"]
        with self.assertRaisesRegex(RuntimeError, "Data title is missing!"):
            Container(items=items)

    def test_mutability(self):
        self.test_container_creation()
        self.assertFalse(self.dc.mutable)
        self.dc.release()
        self.assertTrue(self.dc.mutable)
        self.dc.release()
        self.assertTrue(self.dc.mutable)

    def test_print(self):
        self.test_container_creation()
        s = self.dc.__str__()

        self.assertIn("Single-Step Container", s)
        ct = self.items["content.json"]["containerType"]
        self.assertIn("type:     " + ct["name"] + " " + ct["version"]
                      + " (" + ct["id"] + ")", s)
        self.assertIn("uuid:     " + self.dc["content.json"]["uuid"], s)
        self.assertIn("replaces: " + self.dc["content.json"]["replaces"], s)
        self.assertIn("created:  " + self.dc["content.json"]["created"], s)
        self.assertIn("author:   " + self.dc["meta.json"]["author"], s)

    def test_setitem(self):
        self.test_container_creation()

        with self.assertRaisesRegex(RuntimeError, "Immutable container!"):
            self.dc["data/test.txt"] = "Test123"

        self.dc.release()
        self.dc["data/test.txt"] = "Test123"
        self.dc["data/test.bin"] = b"Test123"
        self.dc["data/test.abc"] = b"Test123"

        self.dc["data/test.abc"] = self.img

        with self.assertRaisesRegex(RuntimeError,
                                    "No matching file format found for item " +
                                    "'data/test.list'!"):
            self.dc["data/test.list"] = ["Test123", "Test456"]

    def test_delitem(self):
        self.test_container_creation()
        with self.assertRaisesRegex(RuntimeError, "Immutable container!"):
            del self.dc["data/parameter.json"]

        self.dc.release()
        del self.dc["data/parameter.json"]

    def test_getitem(self):
        self.test_container_creation()
        self.assertEqual(self.timestamp,
                         self.dc["content.json"]["created"])

        with self.assertRaisesRegex(KeyError, "Unknown item 'data/test.abc'!"):
            self.dc["data/test.abc"]

    def test_values(self):
        self.test_container_creation()
        self.assertEqual(self.dc.values(), [self.dc["content.json"],
                                            self.parameter,
                                            self.img,
                                            self.dc["meta.json"]])