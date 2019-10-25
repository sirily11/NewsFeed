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
            return HanziConv.toSimplified(self.parser.convert()), str(self.parser), cover
        except Exception as e:
            print(e)
            return None, None, None

    async def fetch_list(self):
        try:
            session = AsyncHTMLSession()
            r: HTMLResponse = await session.get("https://hk.news.yahoo.com/")
            news_list = []
            list_elem = r.html.find(".js-stream-content")

            for ele in tqdm(list_elem, desc="Yahoo News"):
                ad = ele.find(".Feedback", first=True)
                # Only get content if it is not ad
                if not ad:
                    title = ele.find("h3", first=True).text
                    link = ele.find("a", first=True).absolute_links.pop()
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
    bbc = YahooHK()
    # markdown, _, c = await bbc.fetch(
    #     "https://hk.news.yahoo.com/%E9%99%B3%E5%90%8C%E4%BD%B3%E6%A1%88%E5%8F%B0%E6%B8%AF%E6%8B%89%E9%8B%B8-214500916.html")
    await bbc.fetch_list()
    await bbc.upload()


if __name__ == '__main__':
    asyncio.run(main())
