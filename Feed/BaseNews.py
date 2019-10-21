class BaseNews:
    def __init__(self, title: str, link: str, cover: str):
        self.title = title
        self.link = link
        self.cover = cover
        self.content = None
