# -!- coding:utf-8 -!-
import random
import re
import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from jinja2 import evalcontextfilter, Markup, escape

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    _paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n') \
                          for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


@app.template_filter()
def prcolor(value):
    random.seed(value)
    red, green, blue = [random.randint(0, 255) for _ in range(3)]
    return "rgb({}, {}, {})".format(red, green, blue)


@app.template_filter()
@evalcontextfilter
def poiemoji(eval_ctx, text):
    result = []
    if 'Beifall' in text:
        result.append("👏")
    elif "Heiterkeit" in text:
        result.append("😂")
    elif "Unterbrechung" in text:
        result.append("⏰")
    else:
        result.append("🗯")
    result = " ".join(result)
    if eval_ctx.autoescape:
        result = Markup(result)
    return result

from views import *

if __name__ == "__main__":
    # app.debug = os.environ.get("DEBUG", False)
    # app.jinja_env.auto_reload = app.debug
    # app.config['TEMPLATES_AUTO_RELOAD'] = app.debug
    app.run()
