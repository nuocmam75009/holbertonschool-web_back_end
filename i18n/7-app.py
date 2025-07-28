#!/usr/bin/env python3
""" Basic Babel setup with locale and timezone selection """
from flask import Flask, render_template, request, g
from flask_babel import Babel, _
from typing import Union
import pytz
from pytz.exceptions import UnknownTimeZoneError


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},  # invalid
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config(object):
    """ Configuration Babel """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_TIMEZONE = 'UTC'
    BABEL_DEFAULT_LOCALE = 'en'


app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)
babel = Babel()


def get_user() -> Union[dict, None]:
    """Retrieve user dict from login_as parameter."""
    try:
        user_id = int(request.args.get("login_as"))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None


@app.before_request
def before_request():
    """Attach user to global Flask context before request."""
    g.user = get_user()


def get_locale():
    """Select best locale according to URL, user or request header."""
    locale = request.args.get("locale")
    if locale in app.config["LANGUAGES"]:
        return locale

    if g.user:
        user_locale = g.user.get("locale")
        if user_locale in app.config["LANGUAGES"]:
            return user_locale

    return request.accept_languages.best_match(app.config["LANGUAGES"])


def get_timezone() -> str:
    """Select best timezone from URL, user or fallback to UTC."""
    try:
        tz_param = request.args.get("timezone")
        if tz_param:
            return pytz.timezone(tz_param).zone

        if g.user and g.user.get("timezone"):
            return pytz.timezone(g.user["timezone"]).zone
    except UnknownTimeZoneError:
        pass

    return app.config["BABEL_DEFAULT_TIMEZONE"]


# Init Babel with both locale and timezone selector
babel.init_app(app, locale_selector=get_locale, timezone_selector=get_timezone)


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    return render_template('7-index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)