from Feed.BaseFeed import BaseFeed
from Feed.BaseNews import BaseNews
from typing import List, Optional, Any, Union, Tuple
from requests_html import AsyncHTMLSession, HTMLResponse, HTMLSession
import asyncio
import json
from tqdm import tqdm


class BBCChinese(BaseFeed):
    def __init__(self):
        super().__init__()
        self.news_publisher = 1

    async def fetch(self, link: str) -> Optional[Tuple]:
        session = AsyncHTMLSession()
        r = await session.get(link)
        body = r.html.find(".story-body__inner", first=True)
        if body:
            self.parser.parse(content=body.html)
            return self.parser.convert(), str(self.parser)
        else:
            return None, None

    async def fetch_list(self):
        session = AsyncHTMLSession()
        r: HTMLResponse = await session.get("https://www.bbc.com/zhongwen/simp")
        images = [r.html.find(".buzzard__image", first=True).find("img", first=True)]
        # Header image
        titles = r.html.find(".title-link__title-text")
        links = r.html.find(".title-link")
        images += r.html.find(".js-delayed-image-load")
        news_list: List[BaseNews] = []

        for i, image in enumerate(tqdm(images, desc="BBC Chinese")):
            try:
                link = links[i].absolute_links.pop()
                title = titles[i]
                if i == 0:
                    image: str = image.attrs['src']
                else:
                    image = image.attrs['data-src']
                content, pure_text = await self.fetch(link)
                news = BaseNews(title=title.text,
                                link=links[i].absolute_links.pop(),
                                content=content,
                                pure_text=pure_text,
                                cover=image.replace("/news/200/", "/news/800/"))

                if news and news.title not in self.written_list:
                    news_list.append(news)
                    self.written_list.append(news.title)
                else:
                    print("Skip title", title.text)
            except Exception as e:
                print(e)
        self.news = news_list
        # write news title to a local file
        with open("written.json", 'w') as f:
            json.dump(self.written_list, f, ensure_ascii=False)


async def main():
    bbc = BBCChinese()
    await bbc.fetch_list()
    await bbc.upload()
