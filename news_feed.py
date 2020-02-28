from Feed.models import BBCChinese, \
    GamerSky, NYChinese, YahooHK, GNNNews, Theverge, Wuhan, YahooTW, Cnn
import time
import asyncio
import datetime

sleep_time = 1800


async def main():
    import sys

    while True:
        last_updated = 0

        if time.time() - last_updated > sleep_time:
            last_updated = time.time()
            if len(sys.argv) == 2:
                # Use browser
                if sys.argv[1] == "cnn":
                    await Cnn.main()
            else:
                bbc = BBCChinese.main()
                gamer = GamerSky.main()
                nyc = NYChinese.main()
                yahooHK = YahooHK.main()
                gnn = GNNNews.main()
                theverge = Theverge.main()
                yahooTW = YahooTW.main()
                wuhan = Wuhan.main()
                await asyncio.gather(nyc, bbc, gamer, yahooHK, gnn, theverge, wuhan, yahooTW)
                print("Updated at", datetime.datetime.now())
                time.sleep(sleep_time)


if __name__ == '__main__':
    asyncio.run(main())
