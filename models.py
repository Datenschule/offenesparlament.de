import itertools
from plenartracker import db
from datetime import datetime

from sqlalchemy import ForeignKey, or_, func
from sqlalchemy.orm import relationship, load_only, Load, class_mapper, subqueryload


class Speaker:
    @staticmethod
    def get_all():
        return db.session.query(Utterance.speaker, Utterance.speaker_cleaned, Utterance.speaker_fp, Utterance.speaker_party, MdB.picture) \
            .filter(Utterance.type == 'speech') \
            .filter(Utterance.speaker_key == MdB.id) \
            .distinct(Utterance.speaker,
                      Utterance.speaker_fp,
                      Utterance.speaker_cleaned) \
            .all()

class MdB(db.Model):
    __tablename__ = "mdb"

    id = db.Column(db.Integer, primary_key=True)
    agw_id = db.Column(db.String)
    profile_url = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    gender = db.Column(db.String)
    birth_date = db.Column(db.Date)
    education = db.Column(db.String)
    picture = db.Column(db.String)
    party = db.Column(db.String)
    election_list = db.Column(db.String)
    list_won = db.Column(db.String)
    top_id = db.Column(db.Integer)

    @staticmethod
    def get_all():
        return db.session.query(MdB) \
            .all()

    @staticmethod
    def get_all_by(column):
        query = db.session.query(getattr(MdB, column), func.count(getattr(MdB, column))) \
            .group_by(getattr(MdB, column)) \
            .all()
        result = {}
        for entry, count in query:
            result[entry] = count
        return result

    def __repr__(self):
        return '<MdB {}-{}-{}>'.format(self.first_name, self.last_name, self.party)

class Utterance(db.Model):
    __tablename__ = "de_bundestag_plpr"

    id = db.Column(db.Integer, primary_key=True)
    wahlperiode = db.Column(db.Integer)
    sitzung = db.Column(db.Integer)
    sequence = db.Column(db.Integer)
    speaker_cleaned = db.Column(db.String)
    speaker_party = db.Column(db.String)
    speaker = db.Column(db.String)
    speaker_fp = db.Column(db.String)
    type = db.Column(db.String)
    text = db.Column(db.String)
    top_id = db.Column(db.Integer, ForeignKey("tops.id"))
    top = relationship("Top")
    speaker_key = db.Column(db.Integer)

    @staticmethod
    def get_all(wahlperiode, session):
        return db.session.query(Utterance) \
            .filter(Utterance.sitzung == session) \
            .filter(Utterance.wahlperiode == wahlperiode) \
            .order_by(Utterance.sequence) \
            .all()

    @staticmethod
    def all_by_gender_category_count():

        subquery = db.session.query(Utterance.sitzung.label("sitzung"), Utterance.wahlperiode, Utterance.speaker_cleaned, MdB.gender, Top.category, Top.number) \
            .filter(Utterance.speaker_key == MdB.id) \
            .filter(Utterance.top_id == Top.id) \
            .filter(Utterance.type == "speech") \
            .group_by(MdB.gender, Top.category, Utterance.sitzung, Utterance.wahlperiode, Utterance.speaker_cleaned, Top.number) \
            .subquery()

        query = db.session.query(subquery.c.category, subquery.c.gender, func.count(subquery.c.category)) \
            .group_by(subquery.c.gender, subquery.c.category) \
            .all()

        result = []
        for category, gender, count in query:
            result.append({"category": category, "gender": gender, "count": count})
        return result

    @staticmethod
    def all_by_age_cetegory_count():
        from_sq = db.session.query(Utterance.sitzung, Utterance.wahlperiode, Utterance.speaker_cleaned, MdB.birth_date, Top.category, Top.number) \
            .filter(Utterance.speaker_key == MdB.id) \
            .filter(Utterance.top_id == Top.id) \
            .filter(Utterance.type == "speech") \
            .group_by(MdB.birth_date, Top.category, Utterance.sitzung, Utterance.wahlperiode, Utterance.speaker_cleaned, Top.number) \
            .subquery()

        query = db.session.query(from_sq.c.category, from_sq.c.birth_date) \
            .all()

        result = []
        for category, date in query:
            result.append({"category": category, "date": date.year})
        return result

    @staticmethod
    def all_by_education_category_count():

        subquery = db.session.query(Utterance.sitzung, Utterance.wahlperiode, Utterance.speaker_cleaned, MdB.education, Top.category, Top.number) \
            .filter(Utterance.speaker_key == MdB.id) \
            .filter(Utterance.top_id == Top.id) \
            .filter(Utterance.type == "speech") \
            .group_by(MdB.education, Top.category, Utterance.sitzung, Utterance.wahlperiode, Utterance.speaker_cleaned, Top.number) \
            .subquery()

        query = db.session.query(subquery.c.category, subquery.c.education, func.count(subquery.c.category)) \
            .group_by(subquery.c.education, subquery.c.category) \
            .all()

        result = []
        for category, education, count in query:
            result.append({"category": category, "education": education, "count": count})
        return result

    @staticmethod
    def all_by_election_list_category_count():

        subquery = db.session.query(Utterance.sitzung, Utterance.wahlperiode, Utterance.speaker_cleaned, MdB.election_list, Top.category, Top.number) \
            .filter(Utterance.speaker_key == MdB.id) \
            .filter(Utterance.top_id == Top.id) \
            .filter(Utterance.type == "speech") \
            .group_by(MdB.election_list, Top.category, Utterance.sitzung, Utterance.wahlperiode, Utterance.speaker_cleaned, Top.number) \
            .subquery()

        query = db.session.query(subquery.c.category, subquery.c.election_list, func.count(subquery.c.category)) \
            .group_by(subquery.c.election_list, subquery.c.category) \
            .all()

        result = []
        for category, election_list, count in query:
            result.append({"category": category, "election_list": election_list, "count": count})
        return result


    def to_json(self):
        d = {}
        columns = class_mapper(self.__class__).columns
        for c in columns:
            name = c.name
            d[name] = getattr(self, name)
        d['top'] = self.top.title if self.top else None
        return d

    def __repr__(self):
        return '<Utterance {}-{}-{}>'.format(self.wahlperiode, self.sitzung, self.sequence)


class Top(db.Model):
    __tablename__ = "tops"

    id = db.Column(db.Integer, primary_key=True)
    wahlperiode = db.Column(db.Integer)
    sitzung = db.Column(db.Integer)
    title = db.Column(db.String)
    title_clean = db.Column(db.String)
    description = db.Column(db.String)
    number = db.Column(db.String)
    week = db.Column(db.Integer)
    detail = db.Column(db.String)
    year = db.Column(db.Integer)
    category = db.Column(db.String)
    duration = db.Column(db.String)
    held_on = db.Column(db.Date)

    @staticmethod
    def get_all(search=None, people=None, years=None, categories=None):
        query = db.session.query(Top)
        if search or people:
            query = query.join(Utterance)

        if search:
            query = query.filter(Utterance.text.contains(search))

        if people:
            query = query.filter(Utterance.speaker_fp.in_(people))

        if years:
            years = [int(year) for year in years]
            query = query.filter(Top.year.in_(years))

        if categories:
            conditions = [Top.category.contains(category) for category in categories]
            query = query.filter(or_(*conditions))

        data = query.all()

        results = []
        for key, igroup in itertools.groupby(data, lambda x: (x.wahlperiode, x.sitzung, x.held_on, x.duration)):
            wahlperiode, sitzung, held_on, duration = key
            results.append({"session": {"wahlperiode": wahlperiode,
                                        "sitzung": sitzung, "date": held_on, "duration": duration},
                            "tops": [{"title": entry.title, "categories": entry.category.split(";")} for entry in list(igroup)]})

        return sorted(results, key=lambda entry: (entry["session"]["wahlperiode"], entry["session"]["sitzung"]))

    @staticmethod
    def get_all_plain():
        return db.session.query(Top).all()

    @staticmethod
    def get_categories():
        db_topics = db.session.query(Top) \
                .distinct(Top.category) \
                .all()
        topics = set()
        for row in db_topics:
            topics.update(row.category.split(";"))
        topics.discard("")
        return list(topics)

    @staticmethod
    def sum_by_category(sum_by=None):
        data = Top.split_by_category()
        results = {}
        for row in data:
            cat = row['category']
            if cat not in results.keys():
                results[cat] = 0
            results[cat] += row['duration'] if row['duration'] is not None else 0
        return results

    @staticmethod
    def count_by_category(sum_by=None):
        data = Top.split_by_category()
        results = {}
        for row in data:
            cat = row['category']
            if cat not in results.keys():
                results[cat] = 0
            results[cat] += 1
        return results

    @staticmethod
    def split_by_category():
        db_topics = db.session.query(Top).filter(Top.category != '').all()

        result = []

        for row in db_topics:
            categories = row.category.split(";")
            for category in categories:
                curr = Top.row2dict(row)
                curr['category'] = category
                result.append(curr)
        return result

    @staticmethod
    def row2dict(row):
        d = {}
        for column in row.__table__.columns:
            d[column.name] = getattr(row, column.name)

        return d

