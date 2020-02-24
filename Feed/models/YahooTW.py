from Feed.BaseFeed import BaseFeed
from Feed.BaseNews import BaseNews
from typing import List, Optional, Any, Union, Tuple
from requests_html import AsyncHTMLSession, HTMLResponse, HTMLSession
import asyncio
import json
from tqdm import tqdm
from hanziconv import HanziConv


class YahooTW(BaseFeed):
    def __init__(self):
        super().__init__()
        self.news_publisher = 11
        self.display_name = "Yahoo TW"
        self.__init_written_list__()

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

            text_eles = body2.find("p")
            image_eles = body2.find("img")
            html = f"<img src='{cover}' />"

            for ele in text_eles:
                html += f"<p>{ele.text}</p>"

            for ele in image_eles:
                attrs = ele.attrs
                if "style" in attrs:
                    style = attrs['style']
                    style = style.replace("background-image:url(", "")
                    style = style.replace(")", "")
                    html += f"<img src='{style}' />"

            self.parser.parse(html)
            return HanziConv.toSimplified(self.parser.convert()), HanziConv.toSimplified(str(self.parser)), cover
        except Exception as e:
            print(e)
            return None, None, None

    async def fetch_list(self) -> List[Tuple[str, str, Optional[str]]]:
        try:
            session = AsyncHTMLSession()
            r: HTMLResponse = await session.get("https://tw.news.yahoo.com/most-popular")
            container = r.html.find(
                "#stream-container-scroll-template", first=True)

            news_list = []
            list_eles = container.find("li")

            for ele in list_eles:
                link_ele = ele.find("a", first=True)
                link = link_ele.absolute_links.pop()
                text = link_ele.text
                # Only get content if it is not ad
                news_list.append(
                    (HanziConv.toSimplified(text), link, None))

            return news_list
        except Exception as e:
            # print(e)
            e


async def main():
    try:
        yahoo = YahooTW()
        await yahoo.fetch_feed()
        await yahoo.upload()
        # yahoo = YahooTW()
        # a, b, c = await yahoo.fetch(
        #     link="https://tw.news.yahoo.com/%E6%81%90%E6%88%90%E9%98%B2%E7%96%AB%E7%BC%BA%E5%8F%A3-%E5%AA%BD%E7%A5%96%E9%81%B6%E5%A2%83%E7%A6%81%E4%B8%8D%E7%A6%81-%E9%99%B3%E6%99%82%E4%B8%AD%E5%9B%9E%E6%87%89%E4%BA%86-101813918.html")
        # print(a)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    asyncio.run(main())
