from unittest import TestCase
from Parser.BaseParser import BaseParser
from Parser.BaseConverter import BaseConverter


class BaseParseTest(TestCase):
    def setUp(self):
        self.parser = BaseParser()

    def test_parse_content(self):
        html = "<p>Hello</p>"
        self.parser.parse(html)
        self.assertEqual(len(self.parser.parsed_objects), 1)
        self.assertEqual(self.parser.parsed_objects[0].tag, "content")
        self.assertEqual(self.parser.parsed_objects[0].content, "Hello")

    def test_parse_content2(self):
        html = "<div>Hello</div>"
        self.parser.parse(html)
        self.assertEqual(len(self.parser.parsed_objects), 1)
        self.assertEqual(self.parser.parsed_objects[0].tag, "content")
        self.assertEqual(self.parser.parsed_objects[0].content, "Hello")

    def test_parse_image(self):
        html = "<img src='google.com' />"
        self.parser.parse(html)
        self.assertEqual(len(self.parser.parsed_objects), 1)
        self.assertEqual(self.parser.parsed_objects[0].tag, "image")
        self.assertEqual(self.parser.parsed_objects[0].content, "google.com")

    def test_parse_link(self):
        html = "<a href='google.com'>Link</a>"
        self.parser.parse(html)
        self.assertEqual(len(self.parser.parsed_objects), 1)
        self.assertEqual(self.parser.parsed_objects[0].tag, "link")
        self.assertEqual(self.parser.parsed_objects[0].link, "google.com")
        self.assertEqual(self.parser.parsed_objects[0].content, "Link")

    def test_parse_list(self):
        html = "<ul><li>1</li><li>2</li></ul>"
        self.parser.parse(html)
        self.assertEqual(len(self.parser.parsed_objects), 1)
        self.assertEqual(self.parser.parsed_objects[0].tag, "list")
        self.assertEqual(len(self.parser.parsed_objects[0].children), 2)
        self.assertEqual(self.parser.parsed_objects[0].children[0].tag, "list")


class MultilevelParserTest(TestCase):
    def setUp(self):
        self.parser = BaseParser()

    def test_parse_content(self):
        html = "<div><p>Hello</p><p>world</p></div>"
        self.parser.parse(html)
        self.assertEqual(len(self.parser.parsed_objects), 2)
