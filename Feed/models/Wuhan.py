from tqdm import tqdm

from Feed.BaseFeed import BaseFeed
from typing import List, Optional, Tuple

from Feed.BaseNews import BaseNews
from Feed.models.wuhan.crawler import Crawler
import asyncio
from datetime import date


class Wuhan(BaseFeed):
    def __init__(self):
        super().__init__()
        self.news_publisher = 10
        self.__init_written_list__()
        self.display_name = "武汉疫情"

    async def fetch_list(self) -> List[Tuple[str, str]]:
        return_list: List[Tuple[str, str]] = []
        p_markdown, a_markdown = Crawler().crawler()
        today = date.today()
        d1 = today.strftime("%Y/%m/%d")

        return [(f'全国疫情资讯 {d1}', p_markdown), (f'全球疫情资讯 {d1}', a_markdown)]

    async def fetch_feed(self):
        news_list = await self.fetch_list()
        for news in tqdm(news_list, desc=self.display_name):
            title, content = news
            news_feed = BaseNews(title=title, link="https://3g.dxy.cn/newh5/view/pneumonia", cover=None,
                                 content=content, pure_text=None)
            self.news.append(news_feed)


async def main():
    try:
        wuhan = Wuhan()
        await wuhan.fetch_feed()
        await wuhan.upload()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    asyncio.run(main())
