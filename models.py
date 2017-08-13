import itertools
from plenartracker import db

from sqlalchemy import ForeignKey, or_
from sqlalchemy.orm import relationship, load_only, class_mapper


class Speaker:
    @staticmethod
    def get_all():
        return db.session.query(Utterance) \
            .options(load_only("speaker", "speaker_fp", "speaker_cleaned")) \
            .filter(Utterance.type == 'speech') \
            .distinct(Utterance.speaker,
                      Utterance.speaker_fp,
                      Utterance.speaker_cleaned) \
            .all()


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
    agw_url = None

    @staticmethod
    def get_all(wahlperiode, session):
        return db.session.query(Utterance) \
            .filter(Utterance.sitzung == session) \
            .filter(Utterance.wahlperiode == wahlperiode) \
            .order_by(Utterance.sequence) \
            .all()

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
        for key, igroup in itertools.groupby(data, lambda x: (x.wahlperiode, x.sitzung)):
            wahlperiode, sitzung = key
            results.append({"session": {"wahlperiode": wahlperiode,
                                        "sitzung": sitzung},
                            "tops": [entry.title for entry in list(igroup)]})

        return sorted(results, key=lambda entry: (entry["session"]["wahlperiode"], entry["session"]["sitzung"]))

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
