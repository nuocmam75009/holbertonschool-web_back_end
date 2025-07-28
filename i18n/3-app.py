#!/usr/bin/env python3
""" Basic Babel setup """
from flask import Flask, render_template, request
from flask_babel import Babel


class Config(object):
    """ Configuration Babel """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_TIMEZONE = 'UTC'
    BABEL_DEFAULT_LOCALE = 'en'


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel()


def get_locale():
    """ Select best match for supported languages """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


# 🔧 Ici, on passe get_locale dans init_app
babel.init_app(app, locale_selector=get_locale)


@app.route('/', strict_slashes=False)
def index():
    """ Render homepage """
    return render_template('3-index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)