from typing import List
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.firefox.webelement import FirefoxWebElement

from Feed.BaseFeedJavaScript import BaseFeedJavaScript
from typing import List, Optional, Any, Union, Tuple
from requests_html import AsyncHTMLSession, HTMLResponse, HTMLSession, Element
import asyncio
import time
from os import path


class CNN(BaseFeedJavaScript):
    def __init__(self):
        super().__init__()
        self.news_publisher = 2
        self.display_name = "CNN"
        self.__init_written_list__()

    async def fetch(self, link) -> Optional[Tuple]:
        session = AsyncHTMLSession()
        try:
            r = await session.get(link)
            container = r.html.find(".zn-body-text", first=True)
            contents: List[Element] = container.find()
            html = ""
            cover = None
            for content in contents:
                element_class = content.attrs.get('class')
                if element_class:
                    if "zn-body__paragraph" in element_class:
                        html += content.html

                    if "el__embedded" in element_class:
                        img = content.find('img', first=True)
                        if img:
                            caption = img.attrs.get('alt')
                            src = img.attrs.get('data-src-large')
                            src = f"https:{src}"
                            if not cover:
                                cover = src
                            html += f'<img src="{src}" />\n'
                            html += f"<span>{caption}</span>\n"
            self.parser.parse(html)
            return self.parser.convert(), str(self.parser), cover
        except Exception as e:
            print(e)
            return None, None, None

    async def fetch_list(self) -> List[Tuple[str, str, Optional[str]]]:
        browser = self.get_browser()
        try:
            url = "https://www.cnn.com/"
            browser.get(url)
            news_list = []
            articles = browser.find_elements_by_tag_name("article")
            for article in articles:
                article: FirefoxWebElement
                try:
                    link = article.find_element_by_tag_name("a")
                    if link:
                        if link.text != "":
                            absolute_link = link.get_attribute("href")
                            news_list.append((link.text, absolute_link, None))
                except Exception as e:
                    pass
            return news_list
        except Exception as e:
            print(e)
        finally:
            browser.close()


async def main():
    cnn = CNN()
    await cnn.fetch_feed()
    await cnn.upload()


if __name__ == '__main__':
    asyncio.run(main())
