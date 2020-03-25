from Feed.BaseFeed import BaseFeed
from Feed.BaseNews import BaseNews
from typing import List, Optional, Any, Union, Tuple
from requests_html import AsyncHTMLSession, HTMLResponse, HTMLSession
import asyncio
import json
from tqdm import tqdm
from hanziconv import HanziConv


class Reuters(BaseFeed):
    def __init__(self):
        super().__init__()
        self.news_publisher = 12
        self.display_name = "Reuters"
        self.__init_written_list__()

    async def fetch(self, link: str) -> Optional[Tuple]:
        try:
            session = AsyncHTMLSession()
            r = await session.get(link)
            container = r.html.find(".StandardArticleBody_body", first=True)
            children = container.find()
            text = []
            html = ""
            cover = None
            for c in children[2:]:
                if c.tag == "figure":
                    continue
                if c.tag == "img":
                    image_src = c.attrs.get("src")
                    if image_src:
                        image_src = image_src[2:]
                        image_src = image_src.replace("&w=20", "")
                        image_src = f"https://{image_src}.jpg"
                        html += f'<img src={image_src} />'
                        if not cover:
                            cover = image_src
                        continue
                else:
                    if c.tag == "div" or c.tag == "svg" or c.tag == "figcaption" or c.tag == "path":
                        continue
                    if c.attrs.get("class"):
                        classes = c.attrs.get("class")
                        if "Image_container" in classes or "Image_zoom" in classes:
                            continue

                        if "StandardArticleBody_trustBadgeContainer" in classes or "StandardArticleBody_trustBadgeTitle" in classes or "trustBadgeUrl" in classes:
                            continue
                    if c.text not in text:
                        html += c.html
                        text.append(c.text)

            self.parser.parse(html)
            return self.parser.convert(), str(self.parser), cover
        except Exception as e:
            print(e)
            return None, None, None

    async def fetch_list(self) -> List[Tuple[str, str, Optional[str]]]:
        try:
            session = AsyncHTMLSession()
            news_list = []
            content = await session.get("https://cn.reuters.com/")
            container = content.html.find("#content", first=True)
            list_con = container.find("a")
            for con in list_con:
                link = con.absolute_links.pop()
                if "article" in link:
                    news_list.append((con.text, link, None))
            return news_list
        except Exception as e:
            # print(e)
            pass


async def main():
    try:
        reuters = Reuters()
        await reuters.fetch_feed()
        await reuters.upload()

    except Exception as e:
        print(e)


if __name__ == '__main__':
    asyncio.run(main())
