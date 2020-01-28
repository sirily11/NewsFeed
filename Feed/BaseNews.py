import json

class BaseNews:
    def __init__(self, title: str, link: str, cover: str = None, content="", pure_text="", data=None):
        self.title = title
        self.link = link
        self.cover = cover
        self.content = content
        self.sentiment = None
        self.pure_text = pure_text
        self.data = data

    def to_json(self):
        return {"title": self.title, "content": self.content,
                "cover": self.cover, "link": self.link,
                "data": json.dumps(self.data, ensure_ascii=False),
                "sentiment": self.sentiment}

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<BaseNews: {self.title}> "
