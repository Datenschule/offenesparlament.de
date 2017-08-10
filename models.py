import itertools
from plenartracker import db

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


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
        return db.session.query(Utterance)\
                         .filter(Utterance.sitzung == session) \
                         .filter(Utterance.wahlperiode == wahlperiode) \
                         .order_by(Utterance.sequence) \
                         .all()

    def __repr__(self):
        return '<Utterance {}-{}-{}>'.format(self.wahlperiode, self.sitzung, self.sequence)


class Top(db.Model):
    __tablename__ = "tops"

    id = db.Column(db.Integer, primary_key=True)
    wahlperiode = db.Column(db.Integer)
    sitzung = db.Column(db.Integer)
    title = db.Column(db.String)

    @staticmethod
    def get_all():
        data = db.session.query(Top).all()

        results = []
        for key, igroup in itertools.groupby(data, lambda x: (x.wahlperiode, x.sitzung)):
            wahlperiode, sitzung = key
            results.append({"session": {"wahlperiode": wahlperiode,
                                        "sitzung": sitzung},
                            "tops": [entry.title for entry in list(igroup)]})

        return sorted(results, key=lambda entry: (entry["session"]["wahlperiode"], entry["session"]["sitzung"]))
