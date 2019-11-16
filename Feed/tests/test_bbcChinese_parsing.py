from Feed.models.BBCChinese import BBCChinese
import pytest


@pytest.mark.asyncio
async def test_parse_list():
    bbc = BBCChinese()
    news_list = await bbc.fetch_list()
    assert len(news_list) > 0


@pytest.mark.asyncio
async def test_parse_list():
    bbc = BBCChinese()
    news_list = await bbc.fetch_list()
    success = False
    for news in news_list:
        title, link, cover = news
        content, pure_text, cover = await bbc.fetch(link)
        if content:
            assert pure_text != None
            assert type(title) == str

            success = True
            break
    assert success is True
