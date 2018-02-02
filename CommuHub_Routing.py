from flask import *
from flask_mail import Mail, Message
from jinja2 import Template
import json
from Custom_Classes import *
from CommuHub_Forms import *
import Time_Functions as timeFunctions
from datetime import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import select
#from models import *
from flask_bootstrap import Bootstrap


# Ahmad's calendar
import calendar
from entities import *

import firebase_admin, os
from firebase_admin import credentials, db

cred = credentials.Certificate("cred/commuhub-2017-firebase-adminsdk-mf4l3-cef43c054d.json")
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
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/database.db'
# sqldb.init_app(app)

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
Bootstrap(app)

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
def donationProjectsMain():
    DProjects = root.child("DProjects").get()
    projectsList = []
    for p_id in DProjects:
        eachProject = DProjects[p_id]
        NewProject = DProject(eachProject['Title'],
                             eachProject['Creator'],
                             eachProject['Categories'],
                             eachProject['Description'],
                             eachProject['Items'],
                             eachProject['Start date'],
                             eachProject['End date'])

        NewProject.set_p_id(p_id)
        print(NewProject.get_p_id())
        projectsList.append(NewProject)

    return render_template("Donation_Projects_Main.html", projects = projectsList)

@app.route('/Donation_Projects_Options_test/', methods=['GET', 'POST'])
def donationProjectsOptions():
    form = NewProjectForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        creator = form.creator.data
        itemCategories = form.itemCategories.data
        description = form.description.data
        items = form.items.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        # frequency = form.frequency.data
        # publisher = form.publisher.data
        # created_by = "U0001"  # hardcoded value

        project = DProject(title, creator, itemCategories, description, items, start_date, end_date)

        projects_db = root.child('DProjects')
        projects_db.push({
            'ID': "Test",
            'Title': project.get_title(),
            'Creator': project.get_creator(),
            'Categories': project.get_categories(),
            'Status': project.get_description(),
            'Items': project.get_items(),
            'Start date': project.get_start_date(),
            'End date': project.get_end_date(),
        })

        flash('Project added.', 'success')

        return render_template("Donation_Projects_Main.html")
        #return redirect(url_for('viewpublications'))

    return render_template("Donation_Projects_Options_test.html", form=form)
    #else ?
    # return render_template("Donation_Projects_Options_test.html", form=form)

@app.route('/Donation_Projects_Options_New/', methods=['GET','POST'])
def donationProjectsOptionsNew():
    if request.method == 'GET':
        return render_template("Donation_Projects_Options_New.html", form=form)
    elif request.method == 'POST': #and form.validate():
        title = request.form['title']
        print(title)
        creator = request.form['creator']
        print(creator)
        itemCategories = []
        allItemCategories = ("CMoney", "CBooks", "CClothes", "CFood", "CAmenities", "COthers")
        for category in allItemCategories:
            if request.form.get(category) is not None:
                print(request.form[category])
                itemCategories.append(category)
        print(itemCategories)
        description = request.form['description']
        print(description)
        #items = form.items.data
        start_date = request.form['start_date']
        print(start_date)
        end_date = request.form['end_date']
        print(end_date)
        # frequency = form.frequency.data
        # publisher = form.publisher.data
        # created_by = "U0001"  # hardcoded value

        project = DProject(title, creator, itemCategories, description, "Items placeholder", start_date, end_date)

        projects_db = root.child('DProjects')
        projects_db.push({
            'ID': "Test",
            'Title': project.get_title(),
            'Creator': project.get_creator(),
            'Categories': project.get_categories(),
            'Description': project.get_description(),
            'Items': project.get_items(),
            'Start date': project.get_start_date(),
            'End date': project.get_end_date(),
        })


        #flash('Project added.', 'success')

        return render_template("Donation_Projects_Main.html")

@app.route('/calendardata/')
def return_calendardata():
    start_date = request.args.get('start', '')
    end_date = request.args.get('end', '')

    with open("events.json", "r") as input_data:
        return input_data.read()


def add_contact(name, email, phone, message):
    root = db.reference('/contact')
    dict = {'name':name, 'email':email, 'phone':phone, 'message':message}
    root.push(dict)

@app.route('/ss/', methods=['GET', 'POST'])
def support_system():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        add_contact(name, email, phone, message)
        return redirect(url_for('m_d'))              #redirects the user to another page
    return render_template('Support_System.html')
        #return render_template('messagedetails.html')


@app.route('/md', methods=['GET', 'POST'])
def m_d():
    ref = db.reference('contact')
    users = ref.get()
    return render_template('messagedetails.html',users=users)

@app.route('/faq')
def faq():
    return render_template('FAQ.html')

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
            'full_name': 'New'
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
    app.run(port=80, debug=True)
    # app.run(debug=True)  optimisation
