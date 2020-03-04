from flask import Flask, render_template, json, g, redirect

app = Flask(__name__)


def get_status():
    """
    Get status current fetching
    :return:
    """
    if 'status' not in g:
        g.status = False

    return g.status


@app.route("/")
def root_home():
    # if current status is on
    if get_status():
        return render_template('home.html')
    return render_template('root_home.html')


@app.route("/start", methods=['POST'])
def start():
    g.status = True
    return redirect("/home")


@app.route("/stop", methods=['GET', 'POST'])
def stop():
    g.status = False
    return render_template('root_home.html')


@app.route('/home')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run("0.0.0.0", port=8000, debug=True)
