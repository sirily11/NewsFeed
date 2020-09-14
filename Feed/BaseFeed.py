from Feed.BaseNews import BaseNews
from Parser.BaseParser import BaseParser
from typing import List, Optional, Tuple, Dict
import requests
import asyncio
import json
from Database.database import DatabaseProvider
from Sentiment.Sentiment import Sentiment
from Feed.stopwords import stop_words
from tqdm import tqdm
import os
import threading

try:
    import jieba
except Exception as e:
    pass

import collections

username = os.getenv("news-feed-username")
password = os.getenv("news-feed-password")


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
        self.news_publisher: int = None
        self.written_list: List = []
        self.display_name = ""

    def __init_written_list__(self):
        """
        Init the written list
        :return:
        """
        try:
            self.database_provider = DatabaseProvider(self.news_publisher)
            with open(f"written-{self.news_publisher}.json", "r") as f:
                data = f.read()
                if data != '':
                    self.written_list = json.loads(data)
        except FileNotFoundError as e:
            print(e)

    def get_info(self) -> dict:
        """
        Get info for current feed
        """
        return {"news_id": self.news_publisher, "name": self.display_name}

    async def fetch(self, link: str) -> Optional[Tuple]:
        """
        Fetch individual page's content.
        Override this to fetch the content of the news feed
        :return: News content (parsed), pure text version's content, cover
        """
        raise NotImplementedError

    async def fetch_list(self) -> List[Tuple[str, str, Optional[str]]]:
        """
        Fetch list of news.
        This will let the software to fetch list of news,
        and then this will call fetch function to fetch
        individual content
        :return: List( title, link, cover)
        """
        raise NotImplementedError

    async def fetch_feed(self):
        """
        Use fetched titles, links, covers to do the
        individual page fetching.
        If cover is None, then using fetch to fetch cover.
        Call this method for fetching
        :return:
        """
        news_list = await self.fetch_list()
        total_length = len(news_list)
        current_index = 0
        for news in tqdm(news_list, desc=self.display_name):
            title, link, cover = news
            if not cover:
                content, pure_text, cover = await self.fetch(link=link)
            else:
                content, pure_text, _ = await self.fetch(link)

            self.database_provider.update_progress(progress=(current_index / total_length) * 100, is_finished=False)
            if content:
                news_feed = BaseNews(title=title, link=link, cover=cover, content=content, pure_text=pure_text)
                if news_feed and news_feed.link not in self.written_list:
                    self.news.append(news_feed)
            current_index += 1
        self.database_provider.update_progress(progress=100, is_finished=True)
        self.database_provider.add_log("Success fetch the feed")

    def get_keywords(self, pure_text: str):
        """
        Get keywords for feed
        :param pure_text: Text
        :return:
        """
        if not pure_text:
            return []
        words = jieba.lcut(pure_text)
        new_keywords = self.filter_keywords(words)
        dup = [(k, count) for k, count, in collections.Counter(new_keywords).items() if count > 1]
        dup.sort(key=lambda tup: tup[1], reverse=True)
        return [d for d, c in dup][: 5]

    @staticmethod
    def filter_keywords(words):
        """
        Generate keyword without stop words
        :param words:
        :return:
        """
        keywords = []
        for w in words:
            if w.lower() in stop_words:
                continue
            if w == "" or w == " " or w == "\n":
                continue
            if len(w) > 2 and w != '”':
                keywords.append(w)
        return keywords

    async def perform_upload(self, objects: List[Dict], header: Dict, url: str):
        """
        Perform upload
        :param url: upload url
        :param header: upload header
        :param objects: list of news feed
        :return:
        """
        res = requests.post(url, json=objects, headers=header)
        if res.status_code != 201:
            print(res.json())

    async def upload(self):
        """"
        Upload Fetched data
        """
        # get sentiments for news
        # pure_texts = [n.pure_text for n in self.news if n.pure_text != ""]
        # if len(pure_texts) > 0:
        #     sentiments = Sentiment(pure_texts).analyze()
        #     if sentiments:
        #         for s in sentiments:
        #             i = int(s['id'])
        #             n = self.news[i]
        #             n.sentiment = s['score']
        try:
            url = "https://api.sirileepage.com/news-feed/news/?multiple"
            auth = requests.post("https://api.sirileepage.com/api/token/",
                                 {"username": username, "password": password})
            await asyncio.sleep(2)
            res = None
            # header
            hed = {'Authorization': 'Bearer ' + auth.json()['access']}
            # update database progress
            self.database_provider.update_upload_progress(progress=0, is_finished=False)
            # list of news feeds
            submit_objects = []
            for i, n in enumerate(self.news):
                # get keywords for feed
                keywords = self.get_keywords(n.pure_text)
                n.keywords = keywords
                # append feed to the submission list
                obj = n.to_json()
                obj['publisher'] = self.news_publisher
                submit_objects.append(obj)
                self.database_provider.update_upload_progress(progress=(i / len(self.news)) * 100, is_finished=False)

            await self.perform_upload(submit_objects, hed, url)
            self.database_provider.update_upload_progress(progress=100, is_finished=True)
            with open(f"written-{self.news_publisher}.json", 'w') as f:
                json.dump(self.written_list, f, ensure_ascii=False)
            self.database_provider.add_log("Successful upload the feed")
            return res
        except Exception as e:
            print(e)
            self.database_provider.add_log(f"error: {e}")
