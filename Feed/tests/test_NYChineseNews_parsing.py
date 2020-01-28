from Feed.models import NYChinese
import pytest


@pytest.mark.asyncio
async def test_parse_list():
    ny_chinese = NYChinese()
    news_list = await ny_chinese.fetch_list()
    assert len(news_list) > 0


@pytest.mark.asyncio
async def test_parse_list():
    ny_chinese = NYChinese()
    news_list = await ny_chinese.fetch_list()
    success = False
    for news in news_list:
        title, link, cover = news
        content, pure_text, cover = await ny_chinese.fetch(link)
        if content:
            assert pure_text != None
            success = True
            break
    assert success is True
