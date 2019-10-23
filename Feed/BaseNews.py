class BaseNews:
    def __init__(self, title: str, link: str, cover: str = None, content="", pure_text=""):
        self.title = title
        self.link = link
        self.cover = cover
        self.content = content
        self.sentiment = None
        self.pure_text = pure_text

    def to_json(self):
        return {"title": self.title, "content": self.content, "cover": self.cover, "link": self.link,
                "sentiment": self.sentiment}

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<BaseNews: {self.title}> "
