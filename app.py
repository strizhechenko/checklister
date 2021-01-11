# coding=utf-8

import yaml
from flask import Flask, render_template, request

app = Flask(__name__)
app.templates_auto_reload = True

DATA = {}


def subsection(data, key):
    if isinstance(data, dict):
        for k, value in data.items():
            if k == key:
                return value
            if isinstance(value, (dict, list)):
                s = subsection(value, key)
                if s:
                    return s
    elif isinstance(data, list):
        for item in data:
            if not isinstance(item, str):
                s = subsection(item, key)
                if s:
                    return s


@app.route('/')
def main():
    global DATA
    if not DATA:
        loader = yaml.SafeLoader
        DATA = yaml.load(open('day.yml'), loader)
    page_name = "Расписание дня"
    data = DATA
    key = request.args.get('key')
    if key is not None:
        page_name = key
        data = subsection(DATA, key)
        if not data:
            return "error", 404
    return render_template('index.html', data=data, pagename=page_name)


if __name__ == '__main__':
    app.run()
