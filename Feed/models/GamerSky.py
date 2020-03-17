import asyncio
from Feed.BaseFeed import BaseFeed
from requests_html import AsyncHTMLSession
from typing import Optional, Tuple, List
import json
from Feed.BaseNews import BaseNews
from tqdm import tqdm, trange


class GamerSky(BaseFeed):

    def __init__(self):
        super().__init__()
        self.news_publisher = 3
        self.display_name = "GamerSky"
        self.__init_written_list__()

    async def fetch(self, link: str) -> Optional[Tuple]:
        try:
            session = AsyncHTMLSession()
            r = await session.get(link)
            content = r.html.find(".Mid2L_con", first=True)
            content_list = content.find()

            texts = []
            images = []
            content = ""
            cover = None

            for c in content_list:
                image = c.find("img", first=True)
                if image:
                    if image.attrs['src'] not in images:
                        content += image.html
                        images.append(image.attrs['src'])
                        if not cover:
                            cover = image.attrs['src']
                else:
                    if c.text not in texts:
                        content += c.html
                        texts.append(c.text)
            self.parser.parse(content)
            return self.parser.convert(), str(self.parser), cover
        except Exception as e:
            return None, None, None

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
        news_list: List[Tuple[str, str, Optional[str]]] = []

        for i, t in enumerate(titles):
            link: str = links[i]
            t: str
            news_list.append((t, link, None))

        return news_list


async def main():
    try:
        gamer = GamerSky()
        await gamer.fetch_feed()
        await gamer.upload()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    asyncio.run(main())
