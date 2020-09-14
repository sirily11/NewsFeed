from Parser.ParsedObject import ParsedObject
from .ParsedObject import ParsedObject, ListElementObject, LinkObject, HeaderObject
from typing import List
from .BaseConverter import BaseConverter


class BaseConverterWithOnlyP(BaseConverter):

    def __init__(self):
        super().__init__()

    def convert(self, parse_objects: List[ParsedObject]):
        """
        Convert parsed objects to objects that can be encoded.
        :param parse_objects: parsed objects provided from parser
        :return: encodeable objects
        """
        return self.__convert__(parse_objects)

    def __convert_content__(self, parse_object: ParsedObject):
        """
        Parse content tags. <p/>, </span>, <div/>
        :return:
        """
        content = f"{parse_object.content}{self.__convert__(parse_object.children)}\n\n"
        if parse_object.newline:
            content += "\n\n"
        return content
