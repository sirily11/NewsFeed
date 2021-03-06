from Feed.models import BBCChinese, \
    GamerSky, NYChinese, YahooHK, GNNNews, Theverge, Wuhan, YahooTW, Cnn, Reuters, Rfi
import time
import asyncio
import datetime
import sys
from pyvirtualdisplay import Display

sleep_time = 1800


async def main():
    print('Version: 1.0')
    print("Number of news providers: 10")
    bbc = BBCChinese.main()
    gamer = GamerSky.main()
    nyc = NYChinese.main()
    yahooHK = YahooHK.main()
    gnn = GNNNews.main()
    theverge = Theverge.main()
    yahooTW = YahooTW.main()
    reuters = Reuters.main()
    rfi = Rfi.main()

    # wuhan = Wuhan.main()
    await asyncio.gather(nyc, bbc, gamer, yahooHK, rfi)
    await asyncio.gather(gnn, theverge, yahooTW, reuters,)

    print("Updated at", datetime.datetime.now())


async def javascript_main():
    cnn = Cnn.main()
    await asyncio.gather(cnn)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == "javascript":
            asyncio.run(javascript_main())
        elif sys.argv[1] == "async":
            asyncio.run(main())
    else:
        asyncio.run(main())
        javascript_main()
