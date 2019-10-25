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
        try:
            session = AsyncHTMLSession()
            r = await session.get(link)
            body = r.html.find(".story-body__inner", first=True)
            if not body:
                body = r.html.find(".story-body", first=True)
                self.parser.parse(body.html)
                return self.parser.convert(), str(self.parser), None

            texts = []
            images = []
            html = ""
            children = body.find()
            first_line = body.find(".story-body__introduction", first=True)
            cover = body.find(".js-image-replace", first=True)
            # Get html
            if cover:
                html += cover.html
            if first_line:
                html += first_line.html
                texts.append(first_line.text)

            for c in children[1:]:
                inner_text = c.text
                if c.tag == "script":
                    continue
                if inner_text not in texts:
                    if "class" in c.attrs:
                        text_class = c.attrs['class']
                        if "js-delayed-image-load" in text_class and c.attrs['data-src'] not in images:
                            images.append(c.attrs['data-src'])
                            html += f"<img src={c.attrs['data-src']} />"
                    else:
                        texts.append(inner_text)
                        html += c.html
            self.parser.parse(content=html)
            if cover:
                return self.parser.convert(), str(self.parser), cover.attrs['src']
            else:
                return self.parser.convert(), str(self.parser), None
        except Exception as e:
            print(e)
            return None, None, None

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
                content, pure_text, cover = await self.fetch(link)
                cover_2 = image.replace("/news/200/", "/news/800/")
                if not cover:
                    cover = cover_2
                news = BaseNews(title=title.text,
                                link=links[i].absolute_links.pop(),
                                content=content,
                                pure_text=pure_text,
                                cover=cover)

                if news and news.title not in self.written_list:
                    news_list.append(news)
                    self.written_list.append(news.title)
                else:
                    # print("Skip title", title.text)
                    pass
            except Exception as e:
                print(e)
        self.news = news_list
        # write news title to a local file
        with open("written.json", 'w') as f:
            json.dump(self.written_list, f, ensure_ascii=False)


async def main():
    bbc = BBCChinese()
    # await bbc.fetch("https://www.bbc.com/zhongwen/simp/world-50176209")
    await bbc.fetch_list()
    await bbc.upload()



