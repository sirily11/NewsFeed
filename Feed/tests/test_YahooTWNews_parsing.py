from Feed.models.YahooTW import YahooTW
import pytest


@pytest.mark.asyncio
async def test_parse_list():
    yahoo_tw = YahooTW()
    news_list = await yahoo_tw.fetch_list()
    assert len(news_list) > 0


@pytest.mark.asyncio
async def test_parse_list2():
    yahoo_tw = YahooTW()
    news_list = await yahoo_tw.fetch_list()
    success = False
    for news in news_list:
        title, link, cover = news
        content, pure_text, cover = await yahoo_tw.fetch(link)
        if content:
            assert pure_text != None
            success = True
            break
    assert success is True
