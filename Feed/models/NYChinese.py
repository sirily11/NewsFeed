from Feed.BaseFeed import BaseFeed
from Feed.BaseNews import BaseNews
from typing import List, Optional, Any, Union, Tuple
from requests_html import AsyncHTMLSession, HTMLResponse, HTMLSession
import asyncio
import json
from tqdm import tqdm


class NYChinese(BaseFeed):
    def __init__(self):
        super().__init__()
        self.news_publisher = 4
        self.display_name = "NY Chinese"
        self.__init_written_list__()

    async def fetch(self, link: str) -> Optional[Tuple]:
        try:
            # Will return cover from this function. Markdown, pure text, cover
            session = AsyncHTMLSession()
            r = await session.get(link)
            cover = r.html.find(".article-span-photo",
                                first=True)
            if cover:
                cover = cover.find("img", first=True)
                cover = cover.attrs['src']
            body = r.html.find(".article-body", first=True)
            contents = body.find(".article-paragraph")
            content = ""
            for c in contents:
                content += c.html
            self.parser.parse(content)
            return self.parser.convert(), str(self.parser), cover
        except Exception as e:
            # print(e)
            return None, None, None

    async def fetch_list(self) -> List[Tuple[str, str, Optional[str]]]:
        url = "https://cn.nytimes.com/"
        session = AsyncHTMLSession()
        r = await session.get(url)
        container = r.html.find("body", first=True)
        titles = container.find("h3")
        n_links = []
        n_titles = []
        news_list = []
        for t in titles:
            ti = t.text
            li = t.absolute_links.pop()
            if ti not in n_titles:
                n_titles.append(ti)
                n_links.append(li)

        # Parse each
        for i, title in enumerate(n_titles):
            link = n_links[i]
            news_list.append((title, link, None))

        return news_list


async def main():
    try:
        nyc = NYChinese()
        # content, pure, cover = await nyc.fetch("https://www.bbc.com/zhongwen/simp/chinese-news-49239215")
        # print(content)
        await nyc.fetch_feed()
        await nyc.upload()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    asyncio.run(main())