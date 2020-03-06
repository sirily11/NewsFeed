from Feed.models.GamerSky import GamerSky
import pytest


@pytest.mark.asyncio
async def test_parse_list():
    gamer = GamerSky()
    news_list = await gamer.fetch_list()
    assert len(news_list) > 0


@pytest.mark.asyncio
async def test_parse_list2():
    gamer = GamerSky()
    news_list = await gamer.fetch_list()
    success = False
    for news in news_list:
        title, link, cover = news
        content, pure_text, cover = await gamer.fetch(link)
        if content:
            assert pure_text != None
            success = True
            break
    assert success is True
