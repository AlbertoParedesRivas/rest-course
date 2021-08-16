import json

default_locale = "en-us"
cache_strings = {}

def refresh():
    global cache_strings
    with open(f"strings/{default_locale}.json") as f:
        cache_strings = json.load(f)

def gettext(name):
    return cache_strings[name]

refresh()