from Parser.ParsedObject import ParsedObject, LinkObject, ListElementObject, HeaderObject
from Parser.BaseConverter import BaseConverter, PureTextConverter
from pyquery import PyQuery
from typing import List


class BaseParser:
    parsed_objects: List[ParsedObject]
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
        if len(d.children()) == 0:
            element_list.append(self.__parse__(d[0]))
        else:
            children = d.children()
            for child in children:
                parsed = self.__parse__(child)
                if parsed:
                    element_list.append(parsed)
        self.parsed_objects = element_list
        return self

    def convert(self):
        """
        Convert objects
        :return: Converted object
        """
        return self.converter.convert(self.parsed_objects)

    def __str__(self):
        # noinspection PyCallByClass
        return PureTextConverter().convert(parse_objects=self.parsed_objects)

    def __parse__(self, child):
        """
        Parse object based on tag
        :param child: PyQuery object
        :return: ParsedObject
        """
        children = PyQuery(child).children()
        children_list = []
        for c in children:
            parsed = self.__parse__(c)
            if parsed:
                children_list.append(parsed)

        if child.tag in ["div", "p", "span", "label", "figure"]:
            return self.__parse_content___(child.text, children=children_list)
        elif child.tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = child.tag.replace("h", "")
            return self.__parse_header__(content=child.text, level=int(level), children=children_list)

        elif child.tag == "img":
            src = PyQuery(child).attr("src")
            return self.__parse_image__(src, children=children_list)
        elif child.tag == "a":
            href = PyQuery(child).attr("href")
            return self.__parse_link__(content=child.text, link=href, children=children_list)
        elif child.tag in ['ol', 'ul', 'li']:

            return self.__parse_list___(content=child.text, children=children_list)
        else:
            return

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
        return ListElementObject(content=content, children=children)

    @staticmethod
    def __parse_header__(content, level, children) -> ParsedObject:
        """
        Parse header. <h1/>, <h2/>
        @:param level: indicate the header, h1, h2, or h3
        :return:
        """
        return HeaderObject(content=content, children=children, level=level)

    @staticmethod
    def __parse_link__(content, link, children) -> ParsedObject:
        return LinkObject(content=content, link=link, children=children)
