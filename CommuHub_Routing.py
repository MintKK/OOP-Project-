from flask import Flask, redirect, url_for, request, render_template, session, send_from_directory, flash, escape, g, abort, jsonify
from flask_mail import Mail, Message
from jinja2 import Template
import json
from CommuHub_Forms import *
from Custom_Classes import *
import Time_Functions as timeFunctions

# Ahmad's calendar
import calendar

import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("cred/commuhub-2017-firebase-adminsdk-mf4l3-5449d3e484.json")
default_app = firebase_admin.initialize_app(
    cred,
    {"databaseURL": 'https://commuhub-2017.firebaseio.com/'}
)

root = db.reference()

# import pyrebase
# config = {
#   "apiKey": "apiKey",
#   "authDomain": "projectId.firebaseapp.com",
#   "databaseURL": "https://databaseName.firebaseio.com",
#   "storageBucket": "projectId.appspot.com",
#   "serviceAccount": "path/to/serviceAccountCredentials.json"
# }
# pyfirebase_app = pyrebase.initialize_app(config)

# Required line, __name__ contains all the Flask module names(?)
app = Flask(__name__)

# Might need later
# app.config.from_object()

# Ahmad's config update - Currently used for email(?)
app.config.update(
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT= 465,
	MAIL_USE_SSL= True,
	MAIL_USERNAME = 'jonsnow3050@gmail.com',
	MAIL_PASSWORD = 'jonsnowisdead',
    MAIL_DEFAULT_SENDER = 'jonsnow3050@gmail.com'
)

# The route for URL navigation to all pages
@app.route('/')
@app.route('/<path:page>/')
def show_page(page=None):
    # print(page)  To test for page
    if page == "CommuHub_Home" or not page:  # Just the base host URL (no page value set) or homepage
        return render_template("CommuHub_Home.html", returnDate=timeFunctions.returnCurrentDate())
    elif page != "favicon.ico":  # Called with a argument for page, that's not homepage or favicon
        return render_template("{}.html".format(page))
    else:  # For favicon request
        return page

@app.route('/Donation_Projects_Main/')
def donationMarketMain():
    '''listings = root.child("listings").get()
    listingslist = []
    for listingId in listings:
        eachListing = listings[listingId]
        #print(listingId)

        if eachListing:
            pass'''

    return render_template("Donation_Projects_Main.html")

@app.route('/Donation_Projects_Options_test/', methods=['GET', 'POST'])
def donationProjectsOptions():
    form = NewProjectForm(request.form)
    # if request.method == 'POST' and form.validate():
    #     if form.pubtype.data == 'smag':
    #         title = form.title.data
    #         type = form.pubtype.data
    #         category = form.category.data
    #         status = form.status.data
    #         frequency = form.frequency.data
    #         publisher = form.publisher.data
    #         created_by = "U0001"  # hardcoded value
    #
    #         mag = Magazine(title, publisher, status, created_by, category, type, frequency)
    #
    #         mag_db = root.child('publications')
    #         mag_db.push({
    #             'title': mag.get_title(),
    #             'type': mag.get_type(),
    #             'category': mag.get_category(),
    #             'status': mag.get_status(),
    #             'frequency': mag.get_frequency(),
    #             'publisher': mag.get_publisher(),
    #             'created_by': mag.get_created_by(),
    #             'create_date': mag.get_created_date()
    #         })
    #
    #         flash('Magazine Inserted Sucessfully.', 'success')
    #
    #     elif form.pubtype.data == 'sbook':
    #         title = form.title.data
    #         type = form.pubtype.data
    #         category = form.category.data
    #         status = form.status.data
    #         isbn = form.isbn.data
    #         author = form.author.data
    #         synopsis = form.synopsis.data
    #         publisher = form.publisher.data
    #         created_by = "U0001"  # hardcoded value
    #
    #         book = Book(title, publisher, status, created_by, category, type, synopsis, author, isbn)
    #         book_db = root.child('publications')
    #         book_db.push({
    #             'title': book.get_title(),
    #             'type': book.get_type(),
    #             'category': book.get_category(),
    #             'status': book.get_status(),
    #             'author': book.get_author(),
    #             'publisher': book.get_publisher(),
    #             'isbn': book.get_isbnno(),
    #             'synopsis': book.get_synopsis(),
    #             'created_by': book.get_created_by(),
    #             'create_date': book.get_created_date()
    #         })
    #
    #         flash('Book Inserted Sucessfully.', 'success')
    #
    #     return redirect(url_for('viewpublications'))

    return render_template("Donation_Projects_Options_test.html", form=form)

@app.route('/calendardata/')
def return_calendardata():
    start_date = request.args.get('start', '')
    end_date = request.args.get('end', '')

    with open("events.json", "r") as input_data:
        return input_data.read()


mail = Mail(app)
@app.route('/Feedback/', methods=['GET', 'POST'])
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

@app.route("/test/create/")
def am_create():
    user = root.child('Users')
    user.set({
        'alanisawesome': {
            'date_of_birth': 'June 23, 1912',
            'full_name': 'Alan Turing'
        },
        'gracehop': {
            'date_of_birth': 'December 9, 1906',
            'full_name': 'Grace Hopper'
        }
    })
    return 'success'

@app.route("/test/update/")
def am_update():
    user = root.child('Users')
    user.update({
        'alanisawesome': {
            'date_of_birth': 'June 23, 2018',
            'full_name': 'Alan D'
        },
        'gracehop': {
            'date_of_birth': 'December 9, 1906',
            'full_name': 'Grace Hopper'
        }
    })
    return 'success'

@app.route("/test/readfullname/")
def am_readfullname():
    user  = root.child('Users').get()
    user_list = []
    #print(user)
    #values=user.get()
    #return values
    for i in user:
        name = user.get(i)
        full_name = name['full_name']
        user_list.append(full_name)

    return user_list[0] + "<br />" + user_list[1]

# Note using URL strings as arguments and "returned" strings are parsed as HTML
@app.route("/hello/<username>/")
def hello_user(username):
    return "<h1>Hello {}<h1>".format(username)

# End code to execute
if __name__ == '__main__':
    app.secret_key = "e7AdCq7iwNN0RO9YixqraD6l4TuiwCyZh0yd9Yfp"
    app.run(debug=True)
    # app.run(debug=True)  optimisation
