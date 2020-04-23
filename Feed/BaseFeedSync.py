from Feed.BaseFeed import BaseFeed
from Feed.BaseNews import BaseNews
from Parser.BaseParser import BaseParser
from typing import List, Optional, Tuple
import requests
import asyncio
import json
from Sentiment.Sentiment import Sentiment
from Feed.stopwords import stop_words
from tqdm import tqdm
import os
try:
    import jieba
except Exception as e:
    pass

import collections
username = os.getenv("news-feed-username")
password = os.getenv("news-feed-password")


class BaseFeedSync(BaseFeed):
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
        super().__init__(parser)

    def fetch_feed(self):
        """
        Use fetched titles, links, covers to do the
        individual page fetching.
        If cover is None, then using fetch to fetch cover.
        Call this method for fetching
        :return:
        """
        news_list = self.fetch_list()
        for news in tqdm(news_list, desc=self.display_name):
            title, link, cover = news
            if not cover:
                content, pure_text, cover = self.fetch(link=link)
            else:
                content, pure_text, _ = self.fetch(link)
            if content:
                news_feed = BaseNews(title=title, link=link, cover=cover, content=content, pure_text=pure_text)
                if news_feed and news_feed.link not in self.written_list:
                    self.news.append(news_feed)

    def upload_keyword(self, pure_text: str, obj_id: int):
        """
        Upload keyword to the server
        :param pure_text: Text
        :param obj_id: News's id
        :return:
        """
        words = jieba.lcut(pure_text)
        url = "https://qbiv28lfa0.execute-api.us-east-1.amazonaws.com/dev/news-feed/keyword/"
        keywords = []
        for w in words:
            if w in stop_words:
                continue
            if w == "" or w == " " or w == "\n":
                continue
            if len(w) > 2 and w != '”':
                keywords.append(w)

        dup = [(k, count) for k, count, in collections.Counter(keywords).items() if count > 1]
        dup.sort(key=lambda tup: tup[1], reverse=True)
        data = [{"feed": obj_id, "keyword": k} for k, c in dup]
        res = requests.post(url, json=data[:5])
        if res.status_code != 201:
            print(res.json())

    def upload_item(self, obj: BaseNews, url: str, header):
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
        self.written_list.append(obj.link)
        if res.status_code != 201:
            print(res.json())
            return
        if obj.pure_text:
            self.upload_keyword(obj.pure_text, res.json()['id'])

    def upload(self):
        """"
        Upload Fetched data
        """
        try:
            url = "https://qbiv28lfa0.execute-api.us-east-1.amazonaws.com/dev/news-feed/news/"
            auth = requests.post("https://qbiv28lfa0.execute-api.us-east-1.amazonaws.com/dev/api/token/",
                                 {"username": username, "password": password})
            hed = {'Authorization': 'Bearer ' + auth.json()['access']}
            for n in self.news:
                self.upload_item(obj=n, url=url, header=hed)
            with open(f"written-{self.news_publisher}.json", 'w') as f:
                json.dump(self.written_list, f, ensure_ascii=False)

        except Exception as e:
            print(e)
