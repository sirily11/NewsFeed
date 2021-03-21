from Feed.BaseFeed import BaseFeed
from typing import List, Optional, Any, Union, Tuple
from requests_html import AsyncHTMLSession, HTMLResponse, HTMLSession
import asyncio
from pyquery import PyQuery as pq

class BBCChinese(BaseFeed):
    def __init__(self):
        super().__init__()
        self.news_publisher = 1
        self.__init_written_list__()
        self.display_name = "BBC Chinese"

    async def fetch(self, link: str) -> Optional[Tuple]:
        try:
            session = AsyncHTMLSession()
            r = await session.get(link)
            body = r.html.find("main", first=True)
            children = body.find("div")
            texts = []
            images = []
            htmls = ""

            for c in children[1:]:
                inner_text = c.text
                if inner_text not in texts:
                    texts.append(inner_text)
                    element = pq(c.raw_html)

                    image = element.find("img")
                    content = element.find("p")
                    h1 = element.find("h1")
                    h2 = element.find("h2")
                    h3 = element.find("h3")
                    h4 = element.find("h4")
                    figcaption = element.find("figcaption")

                    if image:
                        src = pq(image).attr("src")
                        if src not in images:
                            images.append(src)
                            htmls += f"<img src='{src}'/>"
                    elif figcaption:
                        content = pq(figcaption).find("p")
                        htmls += str(content)
                    elif content:
                        htmls += str(content)

                    elif h1:
                        htmls += str(h1)
                    elif h2:
                        htmls += str(h2)

                    elif h3:
                        htmls += str(h3)

                    elif h4:
                        htmls += str(h4)

            self.parser.parse(content=htmls)

            return self.parser.convert(), str(self.parser), images[0] if len(images) > 0 else None
        except Exception as e:
            print(e)
            return None, None, None

    async def fetch_list(self) -> List[Tuple[str, str, None]]:
        session = AsyncHTMLSession()
        r: HTMLResponse = await session.get("https://www.bbc.com/zhongwen/simp")
        list_container = r.html.find("h3")
        news_list: [str, str, str] = []
        for l in list_container:
            link = l.find("a", first=True)
            if link:
                news_list.append((link.text, link.absolute_links.pop(), None))
        return news_list


async def main():
    try:
        bbc = BBCChinese()
        # content, pure, cover = await bbc.fetch("https://www.bbc.com/zhongwen/simp/56348346")
        await bbc.fetch_feed()
        await bbc.upload()
        # print(content)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    asyncio.run(main())
