from Parser.ParsedObject import ParsedObject, LinkObject, ListElementObject
from Parser.BaseConverter import BaseConverter
from pyquery import PyQuery


class BaseParser:
    parsed_objects: [ParsedObject]
    converter: BaseConverter

    def __init__(self, converter: BaseConverter = BaseConverter()):
        self.converter = converter
        self.parsed_objects = []

    def parse(self, content: str):
        """
        Parse html to parsed object
        :param content:
        :return:
        """
        d = PyQuery(content)
        element_list = []
        if d[0].tag != "div" or len(d.children()) == 0:
            element_list.append(self.__parse__(d[0]))
        else:
            for child in d.children():
                element_list.append(self.__parse__(child))
        self.parsed_objects = element_list
        return self

    def convert(self):
        """
        Convert objects
        :return: Converted object
        """
        return self.converter.convert(self.parsed_objects)

    def __parse__(self, child):
        """
        Parse object based on tag
        :param child: PyQuery object
        :return: ParsedObject
        """
        children = PyQuery(child).children()
        children_list = []
        for c in children:
            children_list.append(self.__parse__(c))

        if child.tag in ["div", "p", "span", "label"]:
            return self.__parse_content___(child.text, children=children_list)
        elif "h" in child.tag:
            level = child.tag.replace("h", "")
            return self.__parse_header__(content=child.text, level=level, children=children_list)
        elif child.tag == "img":
            src = PyQuery(child).attr("src")
            return self.__parse_image__(src, children=children_list)
        elif child.tag == "a":
            href = PyQuery(child).attr("href")
            return self.__parse_link__(content=child.text, link=href, children=children_list)
        elif child.tag in ['ol', 'ul', 'li']:
            return self.__parse_list___(content=child.text, children=children_list)

    @staticmethod
    def __parse_image__(content, children) -> ParsedObject:
        """
        Parse image tag. Content is image src
        :return:
        """
        return ParsedObject(tag="image", content=content, children=children)

    @staticmethod
    def __parse_content___(content, children) -> ParsedObject:
        """
        Parse content tags. <p/>, </span>, <div/>
        :return:
        """
        return ParsedObject(tag="content", content=content, children=children)

    @staticmethod
    def __parse_list___(content, children) -> ParsedObject:
        """
        Parse list.
        :return:
        """
        return ListElementObject(tag="list", content=content, children=children)

    @staticmethod
    def __parse_header__(content, level, children) -> ParsedObject:
        """
        Parse header. <h1/>, <h2/>
        @:param level: indicate the header, h1, h2, or h3
        :return:
        """
        return ParsedObject(tag=f"header-{level}", content=content, children=children)

    @staticmethod
    def __parse_link__(content, link, children) -> ParsedObject:
        return LinkObject(tag="link", content=content, link=link, children=children)
