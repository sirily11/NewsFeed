import requests
from typing import List, Optional
from pprint import pprint

try:
    from Sentiment.key import key, endpoint
except:
    pass


class Sentiment:
    def __init__(self, content: List[str]):
        self.content = content

    def analyze(self) -> Optional[List]:
        try:
            sentiment_url = endpoint + "/text/analytics/v2.1/sentiment"
            documents = {"documents": [{"id": i, "text": t, "language": "zh"} for i, t in enumerate(self.content)]}
            headers = {"Ocp-Apim-Subscription-Key": key}
            res = requests.post(sentiment_url, headers=headers, json=documents)
            sentiments = res.json()
            pprint(sentiments)
            return sentiments['documents']
        except Exception as e:
            print(e)
            return []
