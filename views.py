import json
import os

from flask import render_template, request, jsonify

from plenartracker import app, cache

from models import Utterance, Top, Speaker, MdB
from datetime import datetime
from datetime import date

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def get_mdbs():
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, 'static/js/data/matches.json')
    with open(filename) as infile:
        return json.load(infile)

@app.route("/api/tops/")
def api_tops_grouped():
    search = request.args.getlist("search")
    print(search)
    people = request.args.getlist("people")
    years = request.args.getlist("years")
    categories = request.args.getlist("categories")
    sessions = Top.get_all(search=search, people=people, years=years, categories=categories)
    return jsonify(data=sessions)

@app.route("/api/speakers")
@cache.cached(timeout=2000)
def api_speakers():
    speakers = Speaker.get_all()
    i = 0
    speakers = [
        {'speaker_cleaned': utterance.speaker_cleaned,
         'speaker_name': utterance.speaker,
         'speaker_party': utterance.speaker_party,
         'speaker_fp': utterance.speaker_fp,
         'age': calculate_age(utterance.birth_date),
         'education': utterance.education,
         'picture': utterance.picture.replace("http", "https")} for utterance in speakers
    ]
    return jsonify(data=speakers)

@app.route("/api/session/<int:session_id>")
def api_utterances(session_id):
    WAHLPERIODE=18
    utterances = Utterance.get_all(WAHLPERIODE, session_id)
    return jsonify(data=[ {
        "id": item.Utterance.id,
        "sequence": item.Utterance.sequence,
        "sitzung": item.Utterance.sitzung,
        "speaker": item.Utterance.speaker,
        "speaker_cleaned": item.Utterance.speaker_cleaned,
        "speaker_fp": item.Utterance.speaker_fp,
        "speaker_key": item.Utterance.speaker_key,
        "speaker_party": item.Utterance.speaker_party,
        "text": item.Utterance.text,
        "top": item.Utterance.top.title if item.Utterance.top else None,
        "top_id": item.Utterance.top.id if item.Utterance.top else None,
        "type": item.Utterance.type,
        "wahlperiode": item.Utterance.wahlperiode,
        "profile_url": item.MdB.profile_url

    } for item in utterances], session={'date': utterances[0].Utterance.top.held_on if utterances[0].Utterance.top else None,
                                        'number': session_id, 'wahlperiode': WAHLPERIODE})

@app.route("/api/categories")
@cache.cached(timeout=2000)
def api_categories():
    categories = Top.get_categories()
    return jsonify(data=categories)

@app.route("/api/tops/category_sum")
@cache.cached(timeout=2000)
def api_tops_sum_by_category():
    return jsonify(Top.sum_by_category())

@app.route("/api/tops/category_count")
@cache.cached(timeout=2000)
def api_tops_count_by_category():
    return jsonify(Top.count_by_category())

@app.route("/api/utterances/by_gender_category")
@cache.cached(timeout=2000)
def api_uterrances():
    result = {}
    data = Utterance.all_by_gender_category_count()
    for item in data:
        categories = item['category'].split(";")
        for category in categories:
            if category not in result.keys():
                result[category] = { 'male': 0, 'female':0 }

            result[category][item['gender']] += item['count']
    return json.dumps(result)

@app.route("/api/utterances/by_birth_date_category")
@cache.cached(timeout=2000)
def api_utterances_birth_date_category():
    data = Utterance.all_by_age_cetegory_count()
    result = {}
    for item in data:
        categories = item['category'].split(";")
        for category in categories:
            if category not in result.keys():
                result[category] = { }

            group = int((datetime.now().year - item['date']) / 10) * 10
            grouplabel = '{} - {}'.format(group, group + 9)
            if grouplabel not in result[category]:
                result[category][grouplabel] = 0
            result[category][grouplabel] += 1
    return json.dumps(result)

@app.route("/api/utterances/by_profession_category")
@cache.cached(timeout=2000)
def api_utterances_profession_category():
    result = {}
    data = Utterance.all_by_education_category_count()
    for item in data:
        categories = item['category'].split(";")
        for category in categories:
            if category not in result.keys():
                result[category] = result[category] = {}
            education = item['education']
            if education not in result[category]:
                result[category][education] = 0
            result[category][education] += item['count']
    return json.dumps(result)

@app.route("/api/utterances/by_election_list_category")
@cache.cached(timeout=2000)
def api_utterances_election_list_category():
    result = {}
    data = Utterance.all_by_election_list_category_count()
    for item in data:
        categories = item['category'].split(";")
        for category in categories:
            if category not in result.keys():
                result[category] = result[category] = {}
            election_list = item['election_list']
            if election_list not in result[category]:
                result[category][election_list] = 0
            result[category][election_list] += item['count']
    return json.dumps(result)

@app.route("/api/mdb/")
@cache.cached(timeout=2000)
def api_mdb():
    return jsonify(data=[mdb.to_json() for mdb in MdB.get_all()])

@app.route("/api/mdb/speech_by_category")
@cache.cached(timeout=2000)
def api_mdb_speech_by_category():
    data = MdB.count_speeches_by_top_category()
    return jsonify(data)

@app.route("/api/mdb/speech_sum")
@cache.cached(timeout=2000)
def api_mdb_speech_sum():
    data = MdB.count_speeches_sum()
    return jsonify(data)

@app.route("/api/mdb/aggregated")
@cache.cached(timeout=2000)
def api_mdb_aggregated():
    column = request.args.get("attribute")
    return json.dumps(MdB.get_all_by(column))

@app.route("/api/mdb/aggregated/age")
@cache.cached(timeout=2000)
def api_mdb_aggregated_age():
    data = MdB.get_all_by("birth_date")
    result = {}
    for date, count in data.items():
        group = int((datetime.now().year - date.year) / 10) * 10
        grouplabel = '{} - {}'.format(group, group + 9)
        if grouplabel not in result:
            result[grouplabel] = 0
        result[grouplabel] += count
    return json.dumps(result)

