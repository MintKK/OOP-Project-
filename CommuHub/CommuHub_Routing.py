from flask import Flask, redirect, url_for, request, render_template, session, send_from_directory, flash, escape, g, abort
from flask_mail import Mail, Message
from jinja2 import Template

import CommuHub.CommuHub_Forms as customForms
import CommuHub.Time_Functions as timeFunctions

import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("cred/commuhub-2017-firebase-adminsdk-mf4l3-5449d3e484.json")
default_app = firebase_admin.initialize_app(cred, {
    "databaseURL": 'https://commuhub-2017.firebaseio.com/'
})

root = db.reference()

# Required line, __name__ contains all the Flask module names(?)
app = Flask(__name__)

# Testing
# app.config.from_object()

# Ahmad's config update - Currently used for email
app.config.update(
	DEBUG= True,
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT= 465,
	MAIL_USE_SSL= True,
	MAIL_USERNAME = 'jonsnow3050@gmail.com',
	MAIL_PASSWORD = 'jonsnowisdead',
    MAIL_DEFAULT_SENDER = 'jonsnow3050@gmail.com'
)

@app.route('/')
def home_main():
    return render_template("CommuHub_Home.html", returnDate = timeFunctions.returnCurrentDate())

mail = Mail(app)
@app.route('/Feedback', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = Message(subject="Feedback",
                      recipients=['jonsnow3050@gmail.com'])
        msg.html = 'From: {} ({}) <br> <br> Subject: {} <br> <br> Message: {}'.format(request.form['name'],
                                                                                      request.form['email'],
                                                                                      request.form['subject'],
                                                                                      request.form['message'])
        mail.send(msg)
        return render_template('idex.html')

    return render_template('idex.html')

# Note using URL strings as arguments and "returned" strings are parsed as HTML
@app.route("/hello/<username>/")
def hello_user(username):
    return "<h1>Hello {}<h1>".format(username)

# End code to execute
if __name__ == '__main__':
    app.secret_key = "e7AdCq7iwNN0RO9YixqraD6l4TuiwCyZh0yd9Yfp"
    app.run()
    # app.run(debug=True)  optimisation?
