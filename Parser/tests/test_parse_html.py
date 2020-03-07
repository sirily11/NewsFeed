from unittest import TestCase
from ..BaseParser import BaseParser
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
        self.assertEqual(self.parser.parsed_objects[0].content, "")

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
        self.assertEqual("link", self.parser.parsed_objects[0].tag)
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
        html = "<div><p>Hello<a>link</a></p></div>"
        self.parser.parse(html)
        self.assertEqual(len(self.parser.parsed_objects), 1)
        self.assertEqual(len(self.parser.parsed_objects[0].children), 2)
        self.assertEqual(self.parser.parsed_objects[0].children[0].tag, "content")

    def test_inline_link2(self):
        html = '''<span>国集团领导人周二临时磋商结束时只是发表<a href="https://www.nytimes.com/2020/03/03/business/central-banks-coronavirus-g7.html" title="Link: https://www.nytimes.com/2020/03/03/business/central-banks-coronavirus-g7.html">泛泛的团结声明</a>，没有具体行动——没有承诺削减利率，没有承诺政府协调支出——他们</span>'''
        self.parser.parse(html)
        self.assertEqual(len(self.parser.parsed_objects), 3)
        self.assertEqual('国集团领导人周二临时磋商结束时只是发表', self.parser.parsed_objects[0].content)

    def test_inline_link3(self):
        html = "<h2><p>Hello <a>link</a></p></h2>"
        self.parser.parse(html)
        self.assertEqual(len(self.parser.parsed_objects), 1)
        self.assertEqual(len(self.parser.parsed_objects[0].children), 2)
        self.assertEqual(self.parser.parsed_objects[0].children[0].tag, "content")
        self.assertEqual(self.parser.parsed_objects[0].children[1].tag, "link")

    def test_inline_link4(self):
        html = '''<span>国集团领导人周二临时磋商结束时只是发表<a href="https://abc.com">泛泛的团结声明</a>，没有具体行动——没有承诺削减利率，<a href="https://abc.com">没有</a> 承诺政府协调支出——他们</span>'''
        self.parser.parse(html)
        self.assertEqual(len(self.parser.parsed_objects), 5)

    def test_inline_link5(self):
        html = '''<div><p id="9lzZkX">eBay is escalating its fight against online price gouging during the coronavirus outbreak with a new outright ban on all sales of face masks, hand sanitizer, and disinfectant wipes. The new policy, <a href="https://community.ebay.com/t5/Announcements/UPDATE-Important-information-about-listings-associated-with/ba-p/30734312">outlined in a notice to sellers posted Friday</a>, applies both to new listings and existing ones. eBay says it is in the process of removing current listings for these items as well as listings that mention the coronavirus, COVID-19 (the illness it causes), and other popular variations of the phrases like 2019nCoV. </p></div>'''
        self.parser.parse(html)
        self.assertEqual(len(self.parser.parsed_objects), 1)
        self.assertEqual(len(self.parser.parsed_objects[0].children), 3)

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

    def test_complex_inline_link(self):
        html = """
        <div>
            <ul class="story-body__unordered-list">
                <li class="story-body__list-item"><a href="/d" class="story-body__link">a</a></li>
                <li class="story-body__list-item"><a href="/b" class="story-body__link">b</a></li>
                <li class="story-body__list-item"><a href="a" class="story-body__link">c</a></li>
                <li class="story-body__list-item"><a href="/c" class="story-body__link">d</a></li>
            </ul>
        </div>
        """
        self.parser.parse(html)
        self.assertEqual(len(self.parser.parsed_objects), 1)
        self.assertEqual(self.parser.parsed_objects[0].tag, "list")
        self.assertEqual(len(self.parser.parsed_objects[0].children), 4)

    def test_complex_parse2(self):
        html = """
        <figure class="media-landscape no-caption full-width">
            <span class="image-and-copyright-container">
                <img src="https://ichef.bbci.co.uk/news/800/cpsprodpb/5761/production/_109296322_fe5be0ab-2efe-46a7-bca8-752af4a2a3bc.jpg" datasrc="https://ichef.bbci.co.uk/news/320/cpsprodpb/5761/production/_109296322_fe5be0ab-2efe-46a7-bca8-752af4a2a3bc.jpg" class="responsive-image__img js-image-replace" alt="约翰逊" width="1024" height="507" data-highest-encountered-width="800">
                 <span class="story-image-copyright">UK Parliament/Jessica Talyor</span>
            </span>
        </figure>"""
        self.parser.parse(html)
        self.assertEqual(len(self.parser.parsed_objects), 1)
        self.assertEqual(self.parser.parsed_objects[0].tag, "content")
        self.assertEqual(len(self.parser.parsed_objects[0].children), 2)
        self.assertEqual(
            self.parser.parsed_objects[0].children[0].tag, "image")
