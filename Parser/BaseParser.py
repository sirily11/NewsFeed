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
        # list of children
        children = d.contents()
        # if no children, parse first one
        if len(d.children()) == 0:
            element_list.append(self.__parse__(d[0]))
        else:
            for child in children:
                try:
                    parsed = self.__parse__(child)
                    if parsed:
                        element_list.append(parsed)
                except Exception as e:
                    pass

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

    def __parse__(self, child: PyQuery):
        """
        Parse object based on tag
        :param child: PyQuery object
        :return: ParsedObject
        """
        has_child = len(PyQuery(child).children()) > 0
        children = list(PyQuery(child).contents())
        children_list = []
        if has_child:
            for c in children:
                try:
                    parsed = self.__parse__(c)
                    if parsed:
                        children_list.append(parsed)
                except Exception as e:
                    pass
        if child is not PyQuery:
            child = PyQuery(child)

        if self.__is_(child, ["p", "span", "label", "figure", "em"]):
            return self.__parse_content___(child.text(), children=children_list, newline=False)
        elif self.__is_(child, ["div"]):
            return self.__parse_content___(child.text(), children=children_list, newline=True)
        elif self.__is_(child, ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            return self.__parse_header__(content=child.text(),
                                         level=int(self.__get_level__(child)),
                                         children=children_list)

        elif self.__is_(child, ["img"]):
            src = PyQuery(child).attr("src")
            return self.__parse_image__(src, children=children_list)
        elif self.__is_(child, ["a"]):
            href = PyQuery(child).attr("href")
            return self.__parse_link__(content=child.text(), link=href, children=children_list)
        elif self.__is_(child, ['ol', 'ul', 'li']):
            return self.__parse_list___(content=child.text(), children=children_list)
        else:
            return

    @staticmethod
    def __is_(child: PyQuery, tag_list: List[str]) -> bool:
        """
        Return true if the element tag is
        :param tag_list: list of tags name
        :param child: pyquery object
        :return:
        """
        for tag in tag_list:
            if child.is_(tag):
                return True
        return False

    @staticmethod
    def __get_level__(child: PyQuery) -> int:
        if child.is_('h1'):
            return 1
        elif child.is_('h2'):
            return 2
        elif child.is_('h3'):
            return 3
        elif child.is_('h4'):
            return 4
        else:
            return 5

    @staticmethod
    def __parse_image__(content, children) -> ParsedObject:
        """
        Parse image tag. Content is image src
        :return:
        """
        return ParsedObject(tag="image", content=content, children=children)

    @staticmethod
    def __parse_content___(content, children, newline=False) -> ParsedObject:
        """
        Parse content tags. <p/>, </span>, <div/>
        :return:
        """
        return ParsedObject(tag="content", content=content, children=children, newline=newline)

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
