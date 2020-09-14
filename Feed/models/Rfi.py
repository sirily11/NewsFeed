from Feed.BaseFeed import BaseFeed
from Feed.BaseNews import BaseNews
from typing import List, Optional, Any, Union, Tuple
from requests_html import AsyncHTMLSession, HTMLResponse, HTMLSession
import asyncio
import json
from tqdm import tqdm
from hanziconv import HanziConv


class Rfi(BaseFeed):
    def __init__(self):
        super().__init__()
        self.news_publisher = 13
        self.display_name = "Rfi CN"
        self.__init_written_list__()

    async def fetch(self, link: str) -> Optional[Tuple]:
        try:
            from json import loads
            from os.path import join
            from pyquery import PyQuery as pq
            session = AsyncHTMLSession()
            url = 'https://www.rfi.fr/cn/中国/20200914-庆功表彰遗忘-北京还在封锁真相'
            content = await session.get(url)
            content.encoding = 'utf-8'
            cover = None
            cover_container = content.html.find('.m-figure__img', first=True)
            if cover_container:
                src = cover_container.attrs.get('data-image-dataset')
                if src:
                    src = loads(src)
                    url = src['url']
                    file_name = src['filename']
                    cover = join(url, file_name)

            body = content.html.find('.t-content__body', first=True)
            html = body.html
            d = pq(html)
            contents = d("p")
            new_contents = ''

            for c in contents:
                if len(c.classes) == 0:
                    new_contents += f'<p>{c.text_content()}</p>'

            self.parser.parse(new_contents)
            return self.parser.convert(), str(self.parser), cover

        except Exception as e:
            print(e)
            return None, None, None

    async def fetch_list(self) -> List[Tuple[str, str, Optional[str]]]:
        try:
            session = AsyncHTMLSession()
            news_list = []
            content = await session.get("https://www.rfi.fr/cn/")
            links = content.html.find('a')
            blocked_list = [
                'https://s1.mingjingnews.com/',
                'https://boxun.com/',
                'https://www.secretchina.com/']
            for l in links:
                title = l.find('.article__title', first=True)
                if title:
                    href = l.absolute_links.pop()
                    if href not in blocked_list and 'https' in href:
                        news_list.append((title.text, href, None))

            return news_list

        except Exception as e:
            # print(e)
            pass


async def main():
    try:
        rfi = Rfi()
        await rfi.fetch_feed()
        await rfi.upload()

    except Exception as e:
        print(e)


if __name__ == '__main__':
    asyncio.run(main())
