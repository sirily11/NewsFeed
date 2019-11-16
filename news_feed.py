from Feed.models import BBCChinese, BBCChinese, NYChinese, YahooHK, GNNNews, Theverge
import time
import asyncio
import datetime


async def main():
    sleep_time = 1800
    while True:
        last_updated = 0
        bbc = BBCChinese.main()
        gamer = BBCChinese.main()
        nyc = NYChinese.main()
        yahooHK = YahooHK.main()
        gnn = GNNNews.main()
        theverge = Theverge.main()

        if time.time() - last_updated > sleep_time:
            last_updated = time.time()
            await asyncio.gather(nyc, bbc, gamer, yahooHK, gnn, theverge)
            print("Updated at", datetime.datetime.now())
            time.sleep(sleep_time)


if __name__ == '__main__':
    asyncio.run(main())
