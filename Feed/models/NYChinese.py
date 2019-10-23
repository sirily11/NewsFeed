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

    async def fetch(self, link: str) -> Optional[Tuple]:
        try:
            # Will return cover from this function. Markdown, pure text, cover
            session = AsyncHTMLSession()
            r = await session.get(link)
            cover = r.html.find(".article-span-photo", first=True).find("img", first=True).attrs['src']
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

    async def fetch_list(self):
        url = "https://cn.nytimes.com/"
        session = AsyncHTMLSession()
        r = await session.get(url)
        container = r.html.find("#regularHomepage", first=True)
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
        for i, title in enumerate(tqdm(n_titles, desc="NY Chinese")):
            link = n_links[i]
            content, pure_text, cover = await self.fetch(link=link)
            if content:
                news = BaseNews(title=title,
                                link=link,
                                content=content,
                                pure_text=pure_text,
                                cover=cover
                                )
                if news and news.title not in self.written_list:
                    news_list.append(news)
                    self.written_list.append(news.title)
        self.news = news_list
        with open("written.json", 'w') as f:
            json.dump(self.written_list, f, ensure_ascii=False)


async def main():
    bbc = NYChinese()
    await bbc.fetch_list()
    await bbc.upload()

