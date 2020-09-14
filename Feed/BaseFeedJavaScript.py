from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from Feed.BaseFeed import BaseFeed
from Feed.BaseNews import BaseNews
from Parser.BaseParser import BaseParser
from typing import List, Optional, Tuple
from pyvirtualdisplay import Display
import requests
import json
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


class BaseFeedJavaScript(BaseFeed):
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
        # display = Display(visible=0, size=(1024, 768))
        # display.start()
        super().__init__(parser)

    def get_browser(self):
        options = Options()
        options.headless = True
        browser = webdriver.Firefox(options=options)
        return browser
