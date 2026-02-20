from unittest import TestCase

from scidatacontainer import Container

from . import get_test_container


class FileBinaryTest(TestCase):
    def test_encode_decode(self):
        a = get_test_container()

        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed "
        text += "do eiusmod tempor incididunt ut labore et dolore magna "
        text += "aliqua. Varius duis at consectetur lorem donec massa. Amet "
        text += "consectetur adipiscing elit ut aliquam purus sit amet. Duis "
        text += "ultricies lacus sed turpis tincidunt id aliquet risus "
        text += "feugiat. Dui id ornare arcu odio ut sem nulla pharetra."

        btext = text.encode("utf-8")

        a["data/test.exe"] = btext
        self.assertEqual(btext, a["data/test.exe"])

        a.write("test.zdc")

        b = Container(file="test.zdc")

        self.assertEqual(a["data/test.exe"], b["data/test.exe"])

        self.assertEqual(b["data/test.exe"].decode("utf-8"), text)

    def test_hash(self):
        a = get_test_container()

        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed "
        text += "do eiusmod tempor incididunt ut labore et dolore magna "
        text += "aliqua. Varius duis at consectetur lorem donec massa. Amet "
        text += "consectetur adipiscing elit ut aliquam purus sit amet. Duis "
        text += "ultricies lacus sed turpis tincidunt id aliquet risus "
        text += "feugiat. Dui id ornare arcu odio ut sem nulla pharetra."

        btext = text.encode("utf-8")

        a["data/test.exe"] = btext

        a.freeze()
        a.write("test.zdc")

        b = Container(file="test.zdc")
        b.hash()
        self.assertEqual(a["content.json"]["hash"], b["content.json"]["hash"])
        self.assertEqual(
            b["content.json"]["hash"],
            "f66ca1f63274a613e8769902349cd6182403a45fb75df2db9afb2fe0426b9bec",
        )

    def test_legacy_hash(self):
        a = get_test_container()
        a["content.json"]["modelVersion"] = "1.0.0"

        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed "
        text += "do eiusmod tempor incididunt ut labore et dolore magna "
        text += "aliqua. Varius duis at consectetur lorem donec massa. Amet "
        text += "consectetur adipiscing elit ut aliquam purus sit amet. Duis "
        text += "ultricies lacus sed turpis tincidunt id aliquet risus "
        text += "feugiat. Dui id ornare arcu odio ut sem nulla pharetra."

        btext = text.encode("utf-8")

        a["data/test.exe"] = btext

        a.freeze()
        a.write("test.zdc")

        b = Container(file="test.zdc")
        b.hash()
        self.assertEqual(a["content.json"]["hash"], b["content.json"]["hash"])
        self.assertEqual(
            b["content.json"]["hash"],
            "dad3134b6b7dd2f50557ce5d891eb74faac9dcf28e03e51194d21ad4570be7b5",
        )
