from typing import List
# import pyppdf.patch_pyppeteer

from Feed.BaseFeedSync import BaseFeedSync
from typing import List, Optional, Any, Union, Tuple
from requests_html import AsyncHTMLSession, HTMLResponse, HTMLSession, Element
import asyncio
import time


class CNN(BaseFeedSync):
    def __init__(self):
        super().__init__()
        self.news_publisher = 2
        self.display_name = "CNN"
        self.__init_written_list__()

    def fetch(self, link: str) -> Optional[Tuple]:
        session = HTMLSession()
        try:
            r = session.get(link)
            r.html.render()
            session.close()
            container = r.html.find(".zn-body-text", first=True)
            contents: List[Element] = container.find()
            html = ""
            cover = None

            for content in contents:
                element_class = content.attrs.get('class')
                if element_class:
                    if "zn-body__paragraph" in element_class:
                        html += content.html

                    if "el__embedded" in element_class:
                        img = content.find('img', first=True)
                        if img:
                            caption = img.attrs.get('alt')
                            src = img.attrs.get('data-src-large')
                            src = f"https:{src}"
                            if not cover:
                                cover = src
                            html += f'<img src="{src}" />\n'
                            html += f"<span>{caption}</span>\n"
            self.parser.parse(html)
            return self.parser.convert(), str(self.parser), cover
        except Exception as e:
            session.close()
            print(e)
            return None, None, None

    def fetch_list(self) -> List[Tuple[str, str, Optional[str]]]:
        session = HTMLSession()
        try:
            r = session.get("https://www.cnn.com/")
            r.html.render()
            session.close()
            news_list = []
            articles = r.html.find("article")
            for article in articles:
                link = article.find("a", first=True)
                if link:
                    if link.text != "":
                        news_list.append((link.text, link.absolute_links.pop(), None))
            return news_list
        except Exception as e:
            session.close()
            print(e)


def main():
    cnn = CNN()
    cnn.fetch_feed()
    cnn.upload()


if __name__ == '__main__':
    main()
