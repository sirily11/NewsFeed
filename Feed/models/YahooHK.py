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
            body = r.html.find(".caas-body", first=True)
            cover = body.find(".caas-img", first=True)
            cover = cover.attrs['data-src'] if cover else None
            html = body.text

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
