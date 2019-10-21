from unittest import TestCase
from Parser.BaseConverter import BaseConverter
from Parser.ParsedObject import ParsedObject, ListElementObject, LinkObject, HeaderObject


class BaseConvertTest(TestCase):
    def setUp(self):
        self.converter = BaseConverter()

    def test_convert_content(self):
        objects = [ParsedObject(tag="content", content="Hello")]
        ret = self.converter.convert(objects)
        self.assertEqual(ret, "Hello")

    def test_convert_header(self):
        objects = [HeaderObject(content="Header2", level=2)]
        ret = self.converter.convert(objects)
        self.assertEqual(ret, "\n##Header2\n")

    def test_convert_header2(self):
        objects = [HeaderObject(content="Header5", level=5)]
        ret = self.converter.convert(objects)
        self.assertEqual(ret, "\n#####Header5\n")

    def test_convert_link(self):
        objects = [LinkObject(content="Link", link="google.com")]
        ret = self.converter.convert(objects)
        self.assertEqual(ret, "[Link](google.com)")

    def test_convert_image(self):
        objects = [ParsedObject(content="abc", tag="image")]
        ret = self.converter.convert(objects)
        self.assertEqual(ret, "![](abc)")

    def test_convert_list(self):
        objects = [ListElementObject(content="", children=[ListElementObject(content="Hello"),
                                                           ListElementObject(content="Hello2")])]
        ret = self.converter.convert(objects)
        self.assertEqual(ret, "\n- Hello\n- Hello2")


class MultiConvertTest(TestCase):
    def setUp(self):
        self.converter = BaseConverter()

    def test_convert_content(self):
        objects = [
            ParsedObject(tag="content", content="Hello world",
                         children=[LinkObject(content="world", link="google.com")])]
        ret = self.converter.convert(objects)
        self.assertEqual(ret, "Hello [world](google.com)")

    def test_convert_content2(self):
        objects = [
            ParsedObject(tag="content", content="Hello world",
                         children=[ParsedObject(content="world", tag="image")])]
        ret = self.converter.convert(objects)
        self.assertEqual(ret, "Hello ![](world)")

    def test_convert_header(self):
        objects = [
            HeaderObject(content="Hello world", level=3,
                         children=[ParsedObject(content="world", tag="image")])]
        ret = self.converter.convert(objects)
        self.assertEqual(ret, "\n###Hello ![](world)\n")
