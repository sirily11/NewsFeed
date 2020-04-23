from Feed.models import BBCChinese, \
    GamerSky, NYChinese, YahooHK, GNNNews, Theverge, Wuhan, YahooTW, Cnn, Reuters
import time
import asyncio
import datetime
import sys
from pyvirtualdisplay import Display

sleep_time = 1800


async def main():
    print("Start fetching")
    bbc = BBCChinese.main()
    gamer = GamerSky.main()
    nyc = NYChinese.main()
    yahooHK = YahooHK.main()
    gnn = GNNNews.main()
    theverge = Theverge.main()
    yahooTW = YahooTW.main()
    reuters = Reuters.main()
    # wuhan = Wuhan.main()
    await asyncio.gather(nyc, bbc, gamer, yahooHK)
    await asyncio.gather(gnn, theverge, yahooTW, reuters)

    print("Updated at", datetime.datetime.now())


def main_sync():
    print("Start fetching")
    last_updated = time.time()
    cnn = Cnn.main()
    print("Updated at", datetime.datetime.now())
    time.sleep(sleep_time)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == "sync":
            main_sync()
        elif sys.argv[1] == "async":
            asyncio.run(main())
    else:
        asyncio.run(main())
        main_sync()
