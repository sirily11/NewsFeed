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

    async def fetch(self, link: str) -> Optional[Tuple]:
        try:
            session = AsyncHTMLSession()
            r = await session.get(link)
            container = r.html.find(".GN-lbox3B", first=True)
            image_container = container.find(".GN-thumbnail", first=True)
            cover = None
            if image_container:
                cover = image_container.find("img", first=True).attrs['data-src']

            html = ""
            elements = container.find("div")
            images = []

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
                    html += f"<div>{text}</div>"
            self.parser.parse(f"<div>{html}</div>")
            return HanziConv.toSimplified(self.parser.convert()), str(self.parser), cover
        except Exception as e:
            print(e)
            return None, None, None

    async def fetch_list(self):
        try:
            session = AsyncHTMLSession()
            r: HTMLResponse = await session.get("https://gnn.gamer.com.tw")
            news_list = []
            container = r.html.find(".BH-lbox", first=True)
            elements = container.find("h1")

            for e in tqdm(elements, desc="GNN News"):
                title = e.text
                link = e.absolute_links.pop()
                content, pure_text, cover = await self.fetch(link)

                news = BaseNews(title=HanziConv.toSimplified(title),
                                link=link,
                                content=content,
                                pure_text=pure_text,
                                cover=cover)
                if news and news.title not in self.written_list:
                    news_list.append(news)
                    self.written_list.append(news.title)
            self.news = news_list
            # write news title to a local file
            with open("written.json", 'w') as f:
                json.dump(self.written_list, f, ensure_ascii=False)
        except Exception as e:
            print(e)


async def main():
    gnn = GNNNews()
    # content, _, cover = await gnn.fetch("https://gnn.gamer.com.tw/detail.php?sn=188098")
    await gnn.fetch_list()
    await gnn.upload()


if __name__ == '__main__':
    asyncio.run(main())
