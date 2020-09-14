from Feed.models.Reuters import Reuters
import pytest


@pytest.mark.asyncio
async def test_parse_list():
    reuters = Reuters()
    news_list = await reuters.fetch_list()
    assert len(news_list) > 0


@pytest.mark.asyncio
async def test_parse_list2():
    reuters = Reuters()
    news_list = await reuters.fetch_list()
    success = False
    for news in news_list:
        title, link, cover = news
        content, pure_text, cover = await reuters.fetch(link)
        if content:
            assert pure_text != None
            success = True
            break
    assert success is True
