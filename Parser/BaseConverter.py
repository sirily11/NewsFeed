from Parser.ParsedObject import ParsedObject
from .ParsedObject import ParsedObject, ListElementObject, LinkObject, HeaderObject
from typing import List


class BaseConverter:

    def __init__(self):
        pass

    def convert(self, parse_objects: List[ParsedObject]):
        """
        Convert parsed objects to objects that can be encoded.
        :param parse_objects: parsed objects provided from parser
        :return: encodeable objects
        """
        return self.__convert__(parse_objects)

    def __convert__(self, parse_objects: List[ParsedObject]) -> str:
        ret_str = ""

        if not parse_objects:
            return ""

        for parse_object in parse_objects:
            if not parse_object:
                return ""
            if parse_object.children:
                for c in parse_object.children:
                    if c:
                        parse_object.content: str
                        if type(c.content) is str and type(parse_object.content) is str:
                            parse_object.content = parse_object.content.replace(c.content, "")

            if parse_object.tag == "content":
                ret_str += self.__convert_content__(parse_object)
            elif parse_object.tag in ["image"]:
                ret_str += self.__convert_image__(parse_object)
            elif parse_object.tag == "link":
                parse_object: LinkObject
                ret_str += self.__convert_link__(parse_object)
            elif parse_object.tag == "header":
                parse_object: HeaderObject
                ret_str += self.__convert_header__(parse_object)
            elif parse_object.tag == "list":
                parse_object: ListElementObject
                ret_str += self.__convert_list__(parse_object)

        return ret_str

    def __convert_image__(self, parse_object: ParsedObject):
        """
        Parse image tag
        :return:
        """
        return f"\n![]({parse_object.content}){self.__convert__(parse_object.children)}\n\n"

    def __convert_content__(self, parse_object: ParsedObject):
        """
        Parse content tags. <p/>, </span>, <div/>
        :return:
        """
        return f"{parse_object.content}{self.__convert__(parse_object.children)}\n"

    def __convert_list__(self, parse_object: ParsedObject):
        """
        Parse list.
        :return:
        """
        if parse_object.content == "":
            return f"{self.__convert__(parse_object.children)}"
        if parse_object.content is None:
            parse_object.content = ""
        return f"\n- {parse_object.content} {self.__convert__(parse_object.children)}"

    def __convert_header__(self, parse_object: HeaderObject):
        """
        Parse header. <h1/>, <h2/>
        :return:
        """
        header = ""
        for l in range(parse_object.level):
            header += "#"
        return f"\n{header} {parse_object.content}{self.__convert__(parse_object.children)}\n"

    def __convert_link__(self, parse_object: LinkObject):
        return f"[{parse_object.content}]({parse_object.link}){self.__convert__(parse_object.children)} "


class PureTextConverter(BaseConverter):

    def convert(self, parse_objects: List[ParsedObject]) -> object:
        """
        Convert parsed objects to objects that can be encoded.
        :param parse_objects: parsed objects provided from parser
        :return: encodeable objects
        """
        return self.__convert__(parse_objects)

    def __convert__(self, parse_objects: List[ParsedObject]) -> str:
        ret_str = ""

        if not parse_objects:
            return ""

        for parse_object in parse_objects:
            if not parse_object:
                return ""
            if parse_object.children:
                for c in parse_object.children:
                    if c:
                        parse_object.content: str
                        if type(c.content) is str and type(parse_object.content) is str:
                            parse_object.content = parse_object.content.replace(c.content, "")

            if parse_object.tag == "content":
                ret_str += self.__convert_content__(parse_object)
            elif parse_object.tag == "link":
                parse_object: LinkObject
                ret_str += self.__convert_link__(parse_object)
            elif parse_object.tag == "header":
                parse_object: HeaderObject
                ret_str += self.__convert_header__(parse_object)
            elif parse_object.tag == "list":
                parse_object: ListElementObject
                ret_str += self.__convert_list__(parse_object)

        return ret_str

    def __convert_content__(self, parse_object: ParsedObject):
        """
        Parse content tags. <p/>, </span>, <div/>
        :return:
        """
        return f"{parse_object.content}{self.__convert__(parse_object.children)}\n"

    def __convert_list__(self, parse_object: ParsedObject):
        """
        Parse list.
        :return:
        """
        if parse_object.content == "":
            return f"{self.__convert__(parse_object.children)}"
        if parse_object.content is None:
            parse_object.content = ""
        return f"{parse_object.content}{self.__convert__(parse_object.children)}"

    def __convert_header__(self, parse_object: HeaderObject):
        """
        Parse header. <h1/>, <h2/>
        :return:
        """
        return f"{parse_object.content}{self.__convert__(parse_object.children)}"

    def __convert_link__(self, parse_object: LinkObject):
        return f"{parse_object.content}{self.__convert__(parse_object.children)} "
