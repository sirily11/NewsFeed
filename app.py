from _asyncio import Task
from datetime import datetime
from quart import Quart, render_template, jsonify, g, redirect, request
import time
import asyncio
from Database.database import DatabaseProvider
from Feed.models import BBCChinese, \
    GamerSky, NYChinese, YahooHK, GNNNews, Theverge, Wuhan, YahooTW, Cnn

app = Quart(__name__)

global is_start
global task

list_feed_info = [
    BBCChinese.BBCChinese().get_info(),
    GamerSky.GamerSky().get_info(),
    GNNNews.GNNNews().get_info(),
    YahooHK.YahooHK().get_info(),
    YahooTW.YahooTW().get_info(),
    NYChinese.NYChinese().get_info(),
    Theverge.TheVerge().get_info(),
    Cnn.CNN().get_info()
]


async def run():
    last_updated = 0
    sleep_time = 1800

    global is_start
    while is_start:
        if time.time() - last_updated > sleep_time and is_start:
            print("Start fetching")
            last_updated = time.time()
            await BBCChinese.main()
            await GamerSky.main()
            await NYChinese.main()
            await YahooHK.main()
            await GNNNews.main()
            await Theverge.main()
            await YahooTW.main()
            # wuhan = Wuhan.main()

            print("Updated at", datetime.now())
            await asyncio.sleep(sleep_time)


@app.route("/")
async def root_home():
    # if current status is on
    global is_start
    if is_start:
        return redirect("/home")
    return await render_template('root_home.html')


@app.route("/start/", methods=['POST'])
async def start():
    global is_start, task
    is_start = True
    task = asyncio.create_task(run())
    database = DatabaseProvider()
    database.remove_progress()
    return redirect("/home")


@app.route("/stop", methods=['GET', 'POST'])
async def stop():
    global is_start, task
    is_start = False
    if task:
        task.cancel()
    return redirect('/')


@app.route('/home')
async def home():
    global is_start
    if not is_start:
        return redirect("/")

    return await render_template('home.html', feeds=list_feed_info)


@app.route('/detail/<news_id>')
async def detail(news_id: int):
    if not is_start:
        return redirect("/")
    database_provider = DatabaseProvider(news_id)
    logs = database_provider.get_logs()
    context = [log.to_json() for log in logs]
    return await render_template('detail.html', logs=context)


@app.route('/logs')
async def logs():
    if not is_start:
        return redirect("/")
    database_logs = DatabaseProvider().get_all_logs()
    for log in database_logs:
        news_id = log['news_id']
        for l in list_feed_info:
            if l['news_id'] == news_id:
                log['name'] = l['name']
    return await render_template('logs.html', logs=database_logs)


@app.route("/update_progress", methods=["GET"])
async def update_progress():
    database_provider = DatabaseProvider()

    return jsonify(database_provider.get_all_progress())


@app.route("/update_upload_progress", methods=["GET"])
async def update_upload_progress():
    database_provider = DatabaseProvider()

    return jsonify(database_provider.get_all_upload_progress())


if __name__ == '__main__':
    global is_start
    is_start = False
    app.run("0.0.0.0", port=8000, debug=True)
