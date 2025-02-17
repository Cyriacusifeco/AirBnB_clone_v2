#!/usr/bin/python3
"""
A module that starts a web application.
"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """
    view function for the root URL.
    """
    return('Hello HBNB!')


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    view /bbnb
    """
    return('HBNB')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
