import json
import os

from flask import render_template, request

from plenartracker import app
from models import Utterance, Top


def get_mdbs():
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, 'static/js/data/matches.json')
    with open(filename) as infile:
        return json.load(infile)


@app.route("/protocols/session/<session>")
def protocol(session):
    data = Utterance.get_all(18, session)
    mdbs = get_mdbs()
    for utterance in data:
        utterance.agw_url = mdbs.get(utterance.speaker_fp)
    debug = request.args.get("debug")
    return render_template('protocol.html', data=data, debug=debug)


@app.route("/protocols/session/")
def protocol_overview():
    sessions = Top.get_all()
    return render_template('protocol_overview.html', sessions=sessions)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/protokolle")
def protokolle():
    return render_template("protokolle.html", title="Protokolle", selected="protokolle")

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
    return render_template("analyse.html", title="Analyse", selected="analyse", viz=viz)

@app.route("/tracker")
def tracker():
    return render_template("tracker.html", title="Tracker", selected="tracker")

@app.route("/daten-tools")
def daten_tools():
    return render_template("daten-tools.html", title="Daten & Tools", selected="daten-tools")

@app.route("/impressum")
def impressum():
    return render_template("impressum.html", title="Impressum")

@app.route("/analyse/redeanteile")
def viz_test():
    return render_template("analyse/redeanteile.html", title="Analyse")