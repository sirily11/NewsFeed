from Feed.models.BBCChinese import BBCChinese


def test_filter():
    keywords = ["The", "You", "2019"]
    new_keywords = BBCChinese.filter_keywords(keywords)
    assert len(new_keywords) == 0
