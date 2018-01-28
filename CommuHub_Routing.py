from flask import Flask, redirect, url_for, request, render_template, session, send_from_directory, flash, escape, g, abort, jsonify
from flask_mail import Mail, Message
from jinja2 import Template
import json
from CommuHub_Forms import *
from Custom_Classes import *
import Time_Functions as timeFunctions
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import select
from models import *

# Ahmad's calendar
import calendar

import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("cred/commuhub-2017-firebase-adminsdk-mf4l3-cef43c054d.json")
default_app = firebase_admin.initialize_app(
    cred,
    {"databaseURL": 'https://commuhub-2017.firebaseio.com/'}
)

root = db.reference()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/database.db'
sqldb.init_app(app)

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
        return render_template('index.html')

    return render_template('index.html')

@app.route('/organisations')
def organisations():
    all_org = Organisations.query.all()
    return render_template('organisations.html', all_org = all_org)

@app.route('/organisations/add', methods=['GET', 'POST'])
def add_organisations():
    if request.method == 'POST':
        new_entry = Organisations(name=request.form['name'], email=request.form['email'], address=request.form['address'], \
                                phone = request.form['phone'])
        sqldb.session.add(new_entry)
        sqldb.session.commit()
        return redirect(url_for('organisations'))
    
    return redirect(url_for('organisations'))


@app.route('/organisations/delete/<id>', methods=['GET', 'POST'])
def delete_organisations(id):
    selected_org = Organisations.query.filter_by(id=id).first()
    sqldb.session.delete(selected_org)
    sqldb.session.commit()
    return redirect(url_for('organisations'))

@app.route('/organisations/edit/<id>', methods=['GET', 'POST'])
def edit_organisations(id):
    selected_org = Organisations.query.filter_by(id=id).first()
    if request.method == 'POST':
        selected_org.name = request.form['name']
        selected_org.email = request.form['email']
        selected_org.address = request.form['address']
        selected_org.phone = request.form['phone']
        sqldb.session.commit()
        return redirect(url_for('organisations'))

    return redirect(url_for('organisations'))


@app.route('/employees')
def employees():
    all_emp = Employees.query.all()
    return render_template('employee.html', all_emp = all_emp)

@app.route('/employees/add', methods=['GET', 'POST'])
def add_employees():
    if request.method == 'POST':
        new_entry = Organisations(name=request.form['name'], email=request.form['email'], position=request.form['position'], \
                                phone = request.form['phone'])
        sqldb.session.add(new_entry)
        sqldb.session.commit()
        return redirect(url_for('employees'))
    
    return redirect(url_for('employees'))


@app.route('/employees/delete/<id>', methods=['GET', 'POST'])
def delete_employees(id):
    selected_emp = Employees.query.filter_by(id=id).first()
    sqldb.session.delete(selected_emp)
    sqldb.session.commit()
    return redirect(url_for('employees'))

@app.route('/employees/edit/<id>', methods=['GET', 'POST'])
def edit_employees(id):
    selected_emp = Employees.query.filter_by(id=id).first()
    if request.method == 'POST':
        selected_emp.name = request.form['name']
        selected_emp.email = request.form['email']
        selected_emp.position = request.form['position']
        selected_emp.phone = request.form['phone']
        sqldb.session.commit()
        return redirect(url_for('employees'))

    return redirect(url_for('employees'))

# End code to execute
if __name__ == '__main__':
    app.secret_key = "e7AdCq7iwNN0RO9YixqraD6l4TuiwCyZh0yd9Yfp"
    app.run(debug=True)
