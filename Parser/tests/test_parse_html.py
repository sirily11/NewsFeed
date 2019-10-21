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

    def test_parse_content3(self):
        html = "<div></div>"
        self.parser.parse(html)
        self.assertEqual(len(self.parser.parsed_objects), 1)
        self.assertEqual(self.parser.parsed_objects[0].tag, "content")
        self.assertEqual(self.parser.parsed_objects[0].content, None)

    def test_parse_header(self):
        html = "<h2>Hello</h2>"
        self.parser.parse(html)
        self.assertEqual(len(self.parser.parsed_objects), 1)
        self.assertEqual(self.parser.parsed_objects[0].tag, "header")
        self.assertEqual(self.parser.parsed_objects[0].content, "Hello")
        self.assertEqual(self.parser.parsed_objects[0].level, 2)

    def test_parse_image(self):
        html = "<img src='google.com' />"
        self.parser.parse(html)
        self.assertEqual(len(self.parser.parsed_objects), 1)
        self.assertEqual(self.parser.parsed_objects[0].tag, "image")
        self.assertEqual(self.parser.parsed_objects[0].content, "google.com")

    def test_parse_image2(self):
        html = "<img />"
        self.parser.parse(html)
        self.assertEqual(len(self.parser.parsed_objects), 1)
        self.assertEqual(self.parser.parsed_objects[0].tag, "image")

    def test_parse_link(self):
        html = "<a href='google.com'>Link</a>"
        self.parser.parse(html)
        self.assertEqual(len(self.parser.parsed_objects), 1)
        self.assertEqual(self.parser.parsed_objects[0].tag, "link")
        self.assertEqual(self.parser.parsed_objects[0].link, "google.com")
        self.assertEqual(self.parser.parsed_objects[0].content, "Link")

    def test_parse_list(self):
        html = "<div><ul><li>1</li><li>2</li></ul></div>"
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
        self.assertEqual(self.parser.parsed_objects[0].content, "Hello")

    def test_parse_mix(self):
        html = "<div><img src='google'/><p>Hello world</p></div>"
        self.parser.parse(html)
        self.assertEqual(len(self.parser.parsed_objects), 2)
        self.assertEqual(self.parser.parsed_objects[0].content, "google")
        self.assertEqual(self.parser.parsed_objects[1].content, "Hello world")

    def test_parse_mix2(self):
        html = "<p><img src='google'/><p>Hello world</p></p>"
        self.parser.parse(html)
        self.assertEqual(len(self.parser.parsed_objects), 2)
        self.assertEqual(self.parser.parsed_objects[0].content, "google")
        self.assertEqual(self.parser.parsed_objects[1].content, "Hello world")

    def test_inline_link(self):
        html = "<div><p>Hello <a>link</a></p></div>"
        self.parser.parse(html)
        self.assertEqual(len(self.parser.parsed_objects), 1)
        self.assertEqual(len(self.parser.parsed_objects[0].children), 1)
        self.assertEqual(self.parser.parsed_objects[0].children[0].tag, "link")

    def test_inline_link2(self):
        html = "<h2><p>Hello <a>link</a></p></h2>"
        self.parser.parse(html)
        self.assertEqual(len(self.parser.parsed_objects), 1)
        self.assertEqual(len(self.parser.parsed_objects[0].children), 1)
        self.assertEqual(self.parser.parsed_objects[0].children[0].tag, "link")

    def test_parse_complex_html(self):
        html = """
        <h2 class="story-body__crosshead">Header</h2>
        <p>content</p><p>content2</p>
        <p>content3</p>
        <p>content4</p>
        <p>content5</p>
        """
        self.parser.parse(html)
        self.assertEqual(len(self.parser.parsed_objects), 6)
        self.assertEqual(self.parser.parsed_objects[0].tag, "header")
