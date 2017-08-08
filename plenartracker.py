from flask import Flask
from flask_scss import Scss
from flask import render_template

app = Flask(__name__)
Scss(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/protokolle")
def protokolle():
    return render_template("protokolle.html", selected="protokolle")

@app.route("/analyse")
def analyse():
    viz = [
        {
            "description": "Welche Themen wurden wann besprochen?",
            "categories": ["Featured", "Themen"],
            "image": "/static/img/timeline_icon.png",
            "link": "timeline"
        },
        {
            "description": "Wer sprach am häufigsten zum Thema deiner Wahl?",
            "categories": ["Featured", "Themen"],
            "image": "/static/img/victory_icon.png",
            "link": "person-amount-subject"
        },
        {
            "description": "Wieviel Zeit gab es für das Thema deiner Wahl?",
            "categories": ["Featured", "Themen"],
            "image": "/static/img/fun_ico",
            "link": "time-subject"
        },
        {
            "description": "Welches Thema wurde am häufigsten besprochen?",
            "categories": ["Featured", "Themen"],
            "image": "/static/img/fun_icon.png",
            "link": "amount-subject"
        },
        {
            "description": "Wie alt sind die Sprecher zu welchen Themen?",
            "categories": ["Featured", "Themen"],
            "image": "/static/img/group_icon.png",
            "link": "speaker-age"
        },
        {
            "description": "Wer stimmt entgegen der Parteilinie?",
            "categories": ["Featured", "Themen"],
            "image": "/static/img/fun_icon.png",
            "link": "vote"
        }
    ]
    return render_template("analyse.html", selected="analyse", viz=viz)

@app.route("/tracker")
def tracker():
    return render_template("tracker.html", selected="tracker")

@app.route("/daten-tools")
def daten_tools():
    return render_template("daten-tools.html", selected="daten-tools")


if __name__ == '__main__':
    app.run()
