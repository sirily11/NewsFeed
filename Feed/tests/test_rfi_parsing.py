from Feed.models.Rfi import Rfi
import pytest


@pytest.mark.asyncio
async def test_parse_list():
    rfi = Rfi()
    news_list = await rfi.fetch_list()
    assert len(news_list) > 0


@pytest.mark.asyncio
async def test_parse_list2():
    rfi = Rfi()
    news_list = await rfi.fetch_list()
    success = False
    for news in news_list:
        title, link, cover = news
        content, pure_text, cover = await rfi.fetch(link)
        if content:
            assert pure_text != None
            success = True
            break
    assert success is True
