import os
import unittest
from uuid import uuid4

from requests import HTTPError

from scidatacontainer import Container

from ._abstract_container_test import has_connection


class _TestDownload(unittest.TestCase):
    uuid = "00000000-0000-0000-0000-000000000000"
    test_server_url = os.getenv("SCIDATA_TEST_SERVER")
    api_key = os.getenv("SCIDATA_TEST_KEY")
    __test__ = False

    def run(self, result=None):
        if self.__test__:
            return super().run(result)

    def test_download(self):
        Container(
            uuid=self.uuid, config={"server": self.test_server_url, "key": self.api_key}
        )

    def test_replaced(self):
        uuid = "00000000-0000-0000-0000-000000000301"
        dc = Container(uuid=uuid, server=self.test_server_url, key=self.api_key)
        self.assertEqual(dc["content.json"]["uuid"], self.uuid)
        self.assertEqual(dc["content.json"]["replaces"], uuid)

    def test_no_url(self):
        with self.assertRaisesRegex(RuntimeError, "Server URL is missing!"):
            Container(uuid=self.uuid, config={"server": False, "key": self.api_key})

    def test_no_key(self):
        with self.assertRaisesRegex(RuntimeError, "Server API key is missing!"):
            Container(
                uuid=self.uuid, config={"server": self.test_server_url, "key": False}
            )

    def test_wrong_url(self):
        with self.assertRaisesRegex(
            ConnectionError, "Connection to server " + "http://localhost:54321 failed!"
        ):
            Container(
                uuid=self.uuid,
                config={"server": "http://localhost:54321", "key": self.api_key},
            )

    def test_deleted(self):
        with self.assertRaisesRegex(HTTPError, "204 No Content: Deleted dataset"):
            Container(
                uuid=self.uuid[:-3] + "204",
                server=self.test_server_url,
                key=self.api_key,
            )

    def test_unkown_uuid(self):
        with self.assertRaisesRegex(HTTPError, "404 Not Found: Unknown dataset"):
            Container(uuid=str(uuid4()), server=self.test_server_url, key=self.api_key)

    def test_invalid_key(self):
        with self.assertRaisesRegex(HTTPError, "403 Forbidden: Unauthorized access"):
            Container(
                uuid=self.uuid[:-3] + "403",
                server=self.test_server_url,
                key=self.api_key,
            )


@unittest.skipUnless(has_connection, "No server connection available.")
class TestDownload(_TestDownload):
    __test__ = True
