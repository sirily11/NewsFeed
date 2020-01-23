from Feed.BaseFeed import BaseFeed
from Feed.BaseNews import BaseNews
from typing import List, Optional, Any, Union, Tuple
from requests_html import AsyncHTMLSession, HTMLResponse, HTMLSession
import asyncio
import json
from tqdm import tqdm
from hanziconv import HanziConv


class GNNNews(BaseFeed):
    """
    Bahamute news feed
    https://gnn.gamer.com.tw/detail.php?
    """

    def __init__(self):
        super().__init__()
        self.news_publisher = 7
        self.display_name = "GNN News"
        self.__init_written_list__()

    async def fetch(self, link: str) -> Optional[Tuple]:
        try:
            session = AsyncHTMLSession()
            r = await session.get(link)
            container = r.html.find(".GN-lbox3B", first=True)
            image_container = container.find(".GN-thumbnail", first=True)
            cover = None
            if image_container:
                cover = image_container.find(
                    "img", first=True).attrs['data-src']

            html = ""
            elements = container.find("div")
            images = []
            textStr = ""

            for element in elements:
                image = element.find(".GN-thumbnails", first=True)
                if image:
                    image = image.find("img", first=True)
                    if image:
                        src = image.attrs['data-src']
                        if src and src not in images:
                            images.append(src)
                            html += f"<img src={src} />"
                    continue
                else:
                    text = element.text
                    if text not in textStr:
                        textStr += text
                        html += f"<div>{text}</div>"
            self.parser.parse(f"<div>{html}</div>")
            return HanziConv.toSimplified(self.parser.convert()), str(self.parser), cover
        except Exception as e:
            # print(e)
            return None, None, None

    async def fetch_list(self) -> List[Tuple[str, str, Optional[str]]]:
        try:
            session = AsyncHTMLSession()
            r: HTMLResponse = await session.get("https://gnn.gamer.com.tw")
            news_list = []
            container = r.html.find(".BH-lbox", first=True)
            elements = container.find("h1")

            for e in elements:
                title = HanziConv.toSimplified(e.text)
                link = e.absolute_links.pop()
                news_list.append((title, link, None))

            return news_list

        except Exception as e:
            # print(e)
            e


async def main():
    try:
        gnn = GNNNews()
        await gnn.fetch_feed()
        await gnn.upload()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    asyncio.run(main())
