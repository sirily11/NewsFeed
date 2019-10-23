from Feed.BaseNews import BaseNews
from Parser.BaseParser import BaseParser
from typing import List
import requests
import asyncio
import json
from Sentiment.Sentiment import Sentiment
from Feed.key import username, password


class BaseFeed:
    parser: BaseParser
    """
    List of news
    """
    news: List[BaseNews]

    def __init__(self, parser=BaseParser()):
        """
        News feed object. Fetch news from internet and then post the data to database
        :param parser: HTML Parser. Default is base parser.
        """
        self.parser = parser
        self.news: list[BaseNews] = []
        self.news_publisher = None
        self.written_list = []
        try:
            with open("written.json", "r") as f:
                data = f.read()
                if data != '':
                    self.written_list = json.loads(data)
        except FileNotFoundError as e:
            print(e)

    async def fetch(self, link: str) -> str:
        """
        Fetch individual page's content.
        Override this to fetch the content of the news feed
        :return:
        """
        raise NotImplementedError

    async def fetch_list(self):
        """
        Fetch list of news.
        This will let the software to fetch list of news,
        and then this will call fetch function to fetch
        individual content
        :return:
        """
        raise NotImplementedError

    async def upload_item(self, obj: BaseNews, url: str, header):
        """
        Upload single Item
        :param obj: Upload object
        :param url: Upload URL
        :param header: Auth Header. Use this to login the system
        :return:
        """
        submit_object = obj.to_json()
        submit_object['publisher'] = self.news_publisher
        res = requests.post(url, json=submit_object, headers=header)
        if res.status_code != 201:
            print(res.json())
        await asyncio.sleep(1)

    async def upload(self):
        """"
        Upload Fetched data
        """
        # get sentiments for news
        pure_texts = [n.pure_text for n in self.news if n.pure_text != ""]
        if len(pure_texts) > 0:
            sentiments = Sentiment(pure_texts).analyze()
            for s in sentiments:
                i = int(s['id'])
                n = self.news[i]
                n.sentiment = s['score']

        url = "https://toebpt5v9j.execute-api.us-east-1.amazonaws.com/dev/news-feed/news/"
        auth = requests.post("https://toebpt5v9j.execute-api.us-east-1.amazonaws.com/dev/api/token/",
                             {"username": username, "password": password})
        await asyncio.sleep(2)
        hed = {'Authorization': 'Bearer ' + auth.json()['access']}
        res = await asyncio.gather(*(self.upload_item(obj=n, url=url, header=hed) for n in self.news))
        return res
