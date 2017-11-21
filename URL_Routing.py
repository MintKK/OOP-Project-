from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)


@app.route('/')
def mainHomePage():
    return 'Insert home page'


if __name__ == '__main__':
    app.run()
