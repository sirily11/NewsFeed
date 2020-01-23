from Feed.BaseFeed import BaseFeed
from Feed.BaseNews import BaseNews
from typing import List, Optional, Any, Union, Tuple
from requests_html import AsyncHTMLSession, HTMLResponse, HTMLSession
import asyncio
import json
from tqdm import tqdm
from hanziconv import HanziConv


class TheVerge(BaseFeed):
    """
    The verge
    """

    def __init__(self):
        super().__init__()
        self.news_publisher = 8
        self.display_name = "The Verge"
        self.__init_written_list__()

    async def fetch(self, link: str) -> Optional[Tuple]:
        try:
            session = AsyncHTMLSession()
            r = await session.get(link)
            cover = r.html.find(".e-image__image",
                                first=True)  # maybe optional
            if cover:
                cover = cover.attrs['data-original']
            container = r.html.find(".c-entry-content", first=True)
            elements = container.find()

            texts = []
            images = []
            html = ""
            for element in elements:
                if element.tag == "figure":
                    src = element.find(".e-image__image ", first=True)
                    src = src.attrs['data-original']
                    if src not in images:
                        html += f"<img src={src} />\n"
                        images.append(src)
                    continue
                elif element.tag in ['h1', 'h2', 'h3'] or element.tag == "p":
                    if element.text not in texts:
                        html += element.html
                        texts.append(element.text)
                elif element.tag == "div":
                    inside = element.find("aside", first=True)
                    if inside:
                        if inside.text not in texts:
                            html += f"<h2>{inside.text}</h2>"
                        texts.append(inside.text)

            self.parser.parse(content=html)
            return self.parser.convert(), str(self.parser), cover
        except Exception as e:
            # print(e)
            return None, None, None

    async def fetch_list(self) -> List[Tuple[str, str, Optional[str]]]:
        session = AsyncHTMLSession()
        r: HTMLResponse = await session.get("https://www.theverge.com/archives")
        news_list = []
        container = r.html.find(".c-compact-river", first=True)
        elements = container.find(".c-compact-river__entry ")

        for e in elements:
            title = e.find("h2", first=True).text
            link = e.absolute_links.pop()
            news_list.append((title, link, None))

        return news_list


async def main():
    try:
        theverge = TheVerge()
        await theverge.fetch_feed()
        await theverge.upload()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    asyncio.run(main())
