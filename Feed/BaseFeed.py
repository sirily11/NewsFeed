from Publisher.BasePublisher import BasePublisher
from Parser.BaseParser import BaseParser


class BaseFeed:
    publisher: BasePublisher
    parser: BaseParser
    news: [BaseParser]

    def __init__(self, publisher=BasePublisher(), parser=BaseParser()):
        """
        News feed object. Fetch news from internet and then post the data to database
        :param publisher:
        :param parser:
        """
        self.publisher = publisher
        self.parser = parser
        self.news: list[BaseParser] = []
        pass

    pass

    async def fetch(self, link: str) -> str:
        """
        Fetch individual page's content.
        Override this to fetch the content of the news feed
        :return:
        """
        pass

    async def fetch_list(self):
        """
        Fetch list of news.
        This will let the software to fetch list of news,
        and then this will call fetch function to fetch
        individual content
        :return:
        """
        pass

    async def upload(self):
        """"
        Upload Fetched data
        """
        for news in self.news:
            news.convert()
        pass
