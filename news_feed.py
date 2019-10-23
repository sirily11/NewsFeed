from Feed.models import BBCChinese, GamerSky
import time
import asyncio
import datetime


async def main():
    sleep_time = 3600
    while True:
        last_updated = 0
        bbc = BBCChinese.main()
        gamer = GamerSky.main()

        if time.time() - last_updated > sleep_time:
            last_updated = time.time()
            await asyncio.gather(bbc, gamer)
            print("Updated at", datetime.datetime.now())
            time.sleep(sleep_time)


if __name__ == '__main__':
    asyncio.run(main())