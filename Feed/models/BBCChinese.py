from Feed.BaseFeed import BaseFeed
from typing import List, Optional, Any, Union, Tuple
from requests_html import AsyncHTMLSession, HTMLResponse, HTMLSession
import asyncio


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
            # print(e)
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
        # content, pure, cover = await bbc.fetch("https://www.bbc.com/zhongwen/simp/chinese-news-49317370")
        await bbc.fetch_feed()
        await bbc.upload()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    asyncio.run(main())
