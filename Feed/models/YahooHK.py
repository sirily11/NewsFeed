from Feed.BaseFeed import BaseFeed
from Feed.BaseNews import BaseNews
from typing import List, Optional, Any, Union, Tuple
from requests_html import AsyncHTMLSession, HTMLResponse, HTMLSession
import asyncio
import json
from tqdm import tqdm
from hanziconv import HanziConv


class YahooHK(BaseFeed):
    def __init__(self):
        super().__init__()
        self.news_publisher = 6
        self.display_name = "Yahoo HK"
        self.__init_written_list__()

    async def fetch(self, link: str) -> Optional[Tuple]:
        try:
            session = AsyncHTMLSession()
            r = await session.get(link)
            body2 = r.html.find(".canvas-body", first=True)
            cover_container = r.html.find(".canvas-image", first=True)
            cover = None
            if cover_container:
                cover = cover_container.find("img", first=True)
                if cover:
                    cover = cover.attrs['src']

            eles = body2.find()
            html = f"<img src='{cover}' />"

            for e in eles:
                if e.tag == "p":
                    html += f"<p>{e.text}</p>"
            self.parser.parse(html)
            return HanziConv.toSimplified(self.parser.convert()), HanziConv.toSimplified(str(self.parser)), cover
        except Exception as e:
            print(e)
            return None, None, None

    async def fetch_list(self) -> List[Tuple[str, str, Optional[str]]]:
        try:
            session = AsyncHTMLSession()
            r: HTMLResponse = await session.get("https://hk.news.yahoo.com/")
            news_list = []
            list_elem = r.html.find(".js-stream-content")

            for ele in list_elem:
                ad = ele.find(".Feedback", first=True)
                # Only get content if it is not ad
                if not ad:
                    title = ele.find("h3", first=True).text
                    link = ele.find("a", first=True).absolute_links.pop()
                    news_list.append(
                        (HanziConv.toSimplified(title), link, None))

            return news_list
        except Exception as e:
            # print(e)
            e


async def main():
    try:
        bbc = YahooHK()
        await bbc.fetch_feed()
        await bbc.upload()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    asyncio.run(main())
