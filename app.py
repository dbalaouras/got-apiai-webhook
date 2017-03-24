#!/usr/bin/env python

import json
import os

from flask import Flask
from flask import request
from flask import make_response
import logging

from got import GOT

# Flask app should start in global layout
app = Flask(__name__)


@app.before_first_request
def setup_logging():
    if not app.debug:
        # In production mode, add log handler to sys.stderr.
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.INFO)


@app.route('/', methods=['GET'])
def index():
    res = "<h1>GoT Chatbot Demo</h1><p>Made by <a href='https://helvia.io' target='_blank'>helvia.io</a>.</p>"

    r = make_response(res)
    r.headers['Content-Type'] = 'text/html'
    return r


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    # TODO: Python logging here
    print("Incoming Request")
    print(json.dumps(req, indent=4))

    res = process_request(req)
    res = json.dumps(res, indent=4)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def process_request(req):
    """
    Process API.AI request
    :param req: API.AI request
    :return: API.AI webhook result
    """

    # Initialize Request
    res = {}

    action = req.get("result").get("action")

    # TODO: Python logging here
    print("Action: " + action)

    fun = globals().get(action, None)
    if fun:
        res = fun(req)

    return res


def get_character_birth_date(req):
    """
    Get character's date of birth
    :param req: API.AI request
    :return: API.AI webhook result
    """
    name = req.get("result", {}).get("parameters", {}).get("character_name", None)
    got = GOT()
    info = got.get_character_info(name)

    if info:
        text = "%s was born %s" % (name, info[0].get("born", "unknown"))
    else:
        text = "Sorry we could not find this GOT character!"

    res = make_webhook_result(text, None)
    return res


def get_character_death_date(req):
    """
    Get character's date of death
    :param req: API.AI request
    :return: API.AI webhook result
    """
    name = req.get("result", {}).get("parameters", {}).get("character_name", None)
    got = GOT()
    info = got.get_character_info(name)

    if info:
        death = info[0].get("died", None)
        if death:
            text = "%s died %s" % (name, info[0].get("died", "unknown"))
        else:
            text = "%s is not dead (yet!)" % name
    else:
        text = "Sorry we could not find this GOT character!"

    res = make_webhook_result(text, None)
    return res


def get_character_actor(req):
    """
    Get the actor/actress who played the given character
    :param req: API.AI request
    :return: API.AI webhook result
    """
    name = req.get("result", {}).get("parameters", {}).get("character_name", None)
    got = GOT()
    info = got.get_character_info(name)

    if info:
        played_by = info[0].get("playedBy", None)
        if played_by:
            text = "Character %s was played by %s." % (name, ','.join(played_by))
        else:
            text = "We don't know who played character %s" % name
    else:
        text = "Sorry we could not find this GOT character!"

    res = make_webhook_result(text, None)
    return res


def get_random_quote(req):
    """
    Get a random quote from a character
    :param req: API.AI request
    :return: API.AI webhook result
    """

    got = GOT()
    quote = got.get_random_quote()

    if quote:
        text = "%s -- %s" % (quote['quote'], quote['character'])
    else:
        text = "Sorry we could not find this GOT character!"

    res = make_webhook_result(text, None)
    return res


def get_character_titles(req):
    """
    Get a character's titles
    :param req: API.AI request
    :return: API.AI webhook result
    """
    name = req.get("result", {}).get("parameters", {}).get("character_name", None)
    got = GOT()
    info = got.get_character_info(name)

    if info:
        titles = info[0].get("titles", None)
        if titles:
            title_word = "titles are: " if len(titles) > 1 else "title is"
            text = "Character %s's %s %s" % (name, title_word, ','.join(titles))
        else:
            text = "We don't know the titles of %s" % name
    else:
        text = "Sorry we could not find this GOT character!"

    res = make_webhook_result(text, None)
    return res


def make_webhook_result(text, data):
    return {
        "speech": text,
        "displayText": text,
        "data": data,
        # "contextOut": [],
        "source": "got-apiai-webhook"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
