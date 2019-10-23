import asyncio

from Feed.BaseFeed import BaseFeed
from requests_html import AsyncHTMLSession
from typing import Optional, Tuple
import json
from Feed.BaseNews import BaseNews
from tqdm import tqdm, trange


class GamerSky(BaseFeed):

    def __init__(self):
        super().__init__()
        self.news_publisher = 3

    async def fetch(self, link: str) -> Optional[Tuple]:
        try:
            session = AsyncHTMLSession()
            r = await session.get(link)
            content = r.html.find(".Mid2L_con", first=True)
            content_list = content.find()

            texts = []
            images = []
            content = ""

            for c in content_list:
                image = c.find("img", first=True)
                if image:
                    if image.attrs['src'] not in images:
                        content += image.html
                        images.append(image.attrs['src'])
                else:
                    if c.text not in texts:
                        content += c.html
                        texts.append(c.text)
            self.parser.parse(content)
            return self.parser.convert(), str(self.parser)
        except Exception as e:
            # print(e)
            return None, None

    async def fetch_list(self):
        url = "https://www.gamersky.com/"
        session = AsyncHTMLSession()
        r = await session.get(url)
        display = r.html.find(".Mid1_M", first=True)
        news = display.find("li")

        titles = []
        links = []
        # Get links and title
        for n in news:
            row = n.find("a", first=True)
            if row:
                if row.text != "":
                    titles.append(row.text)
                    links.append(row.attrs['href'])
        news_list = []

        for i, t in enumerate(tqdm(titles, desc="Gamersky")):
            print(f"{i}/{len(titles)}")
            link = links[i]
            content, pure_text = await self.fetch(link=link)
            if content:
                news = BaseNews(title=t,
                                link=link,
                                content=content,
                                pure_text=pure_text,
                                )
                if news and news.title not in self.written_list:
                    news_list.append(news)
                    self.written_list.append(news.title)
        self.news = news_list
        with open("written.json", 'w') as f:
            json.dump(self.written_list, f, ensure_ascii=False)


async def main():
    gamer = GamerSky()
    await gamer.fetch_list()
    await gamer.upload()


