from Feed.models import BBCChinese, \
    GamerSky, NYChinese, YahooHK, GNNNews, Theverge, Wuhan, YahooTW, Cnn
import time
import asyncio
import datetime
import sys
from pyvirtualdisplay import Display

sleep_time = 1800


async def main():
    while True:
        last_updated = 0

        if time.time() - last_updated > sleep_time:
            print("Start fetching")
            last_updated = time.time()
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


def main_sync():
    while True:
        last_updated = 0
        if time.time() - last_updated > sleep_time:
            print("Start fetching")
            last_updated = time.time()
            cnn = Cnn.main()
            print("Updated at", datetime.datetime.now())
            time.sleep(sleep_time)


if __name__ == '__main__':
    try:
        Display(visible=0, size=(1280, 720)).start()
    except Exception as e:
        print(e)
    if len(sys.argv) == 2:
        if sys.argv[1] == "sync":
            main_sync()
        elif sys.argv[1] == "async":
            asyncio.run(main())
    else:
        asyncio.run(main())
        main_sync()
