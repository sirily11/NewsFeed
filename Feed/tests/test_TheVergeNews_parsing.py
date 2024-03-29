from Feed.models.Theverge import TheVerge
import pytest


@pytest.mark.asyncio
async def test_parse_list():
    the_verge = TheVerge()
    news_list = await the_verge.fetch_list()
    assert len(news_list) > 0


@pytest.mark.asyncio
async def test_parse_list2():
    the_verge = TheVerge()
    news_list = await the_verge.fetch_list()
    success = False
    for news in news_list:
        title, link, cover = news
        content, pure_text, cover = await the_verge.fetch(link)
        if content:
            assert pure_text != None
            success = True
            break
    assert success is True
