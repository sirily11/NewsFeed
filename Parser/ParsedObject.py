from typing import List


class ParsedObject:
    """
    Basic parsed object
    """

    def __init__(self, tag: str, content, children=None, newline=False):
        self.tag = tag
        self.content = content
        self.children: List = children
        self.newline = newline


class LinkObject(ParsedObject):
    """
    Link object which represents link.
    """

    def __init__(self, content, link: str, children=None, newline=False):
        super().__init__("link", content, children=children, newline=newline)
        self.link = link


class HeaderObject(ParsedObject):
    def __init__(self, content, level, children=None, newline=False):
        super().__init__("header", content, children, newline)
        self.level = level


class ListElementObject(ParsedObject):

    def __init__(self, content="", children=None, newline=False):
        super().__init__("list", content, children, newline)
