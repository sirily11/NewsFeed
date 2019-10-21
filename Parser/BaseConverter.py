from .ParsedObject import ParsedObject


class BaseConverter:
    def __init__(self):
        pass

    def convert(self, parse_objects: [ParsedObject]):
        """
        Convert parsed objects to objects that can be encoded.
        :param parse_objects: parsed objects provided from parser
        :return: encodeable objects
        """
        pass

    def __convert_image__(self, parse_object: ParsedObject):
        """
        Parse image tag
        :return:
        """
        pass

    def __convert_content__(self, parse_object: ParsedObject):
        """
        Parse content tags. <p/>, </span>, <div/>
        :return:
        """
        pass

    def __convert_list__(self, parse_object: ParsedObject):
        """
        Parse list.
        :return:
        """
        pass

    def __convert_header__(self, parse_object: ParsedObject):
        """
        Parse header. <h1/>, <h2/>
        :return:
        """
        pass
