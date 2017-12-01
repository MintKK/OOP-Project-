from flask import Flask, redirect, url_for, request, render_template, session, send_from_directory, flash
# Import all needed modules with one statement

# For HTTP get and post methods
from flask import request

# For HTML file (template) importing(?)
from flask import render_template

# Required line, __name__ contains all the Flask module names(?)
app = Flask(__name__)


@app.route('/')
def home_main():
    return render_template("Home_Main.html")


# Note using URL strings as arguments
@app.route("/hello/<username>/")
def hello_user(username):
    return "Hello {}".format(username)

# End code to execute
if __name__ == '__main__':
    app.run()
