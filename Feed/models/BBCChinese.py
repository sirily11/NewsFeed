from Feed.BaseFeed import BaseFeed
from typing import List, Optional, Any, Union, Tuple
from requests_html import AsyncHTMLSession, HTMLResponse, HTMLSession
from tqdm import tqdm
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
            print(e)
            return None, None, None

    async def fetch_list(self) -> List[Tuple[str, str, str]]:
        session = AsyncHTMLSession()
        r: HTMLResponse = await session.get("https://www.bbc.com/zhongwen/simp")
        images = [r.html.find(".buzzard__image", first=True).find("img", first=True)]
        # Header image
        titles = r.html.find(".title-link__title-text")
        links = r.html.find(".title-link")
        images += r.html.find(".js-delayed-image-load")
        return_list: List[Tuple[str, str, str]] = []

        for i, image in enumerate(images):
            link = links[i].absolute_links.pop()
            title = titles[i]
            if i == 0:
                image: str = image.attrs['src']
            else:
                image = image.attrs['data-src']
            cover = image.replace("/news/200/", "/news/800/")
            return_list.append((title.text, link, cover))

        return return_list


async def main():
    bbc = BBCChinese()
    await bbc.fetch_feed()
    print(bbc.news[0])
    # await bbc.upload()


if __name__ == '__main__':
    asyncio.run(main())
