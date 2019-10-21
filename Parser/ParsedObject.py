class ParsedObject:
    """
    Basic parsed object
    """

    def __init__(self, tag: str, content, children):
        self.tag = tag
        self.content = content
        self.children = children


class LinkObject(ParsedObject):
    """
    Link object which represents link.
    """

    def __init__(self, tag: str, content, link: str, children):
        super().__init__(tag, content, children=children)
        self.link = link


class ListElementObject(ParsedObject):

    def __init__(self, tag: str, content, children=None):
        super().__init__(tag, content, children)
