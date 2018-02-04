from flask import *
from flask_mail import Mail, Message
from jinja2 import Template
import json
from datetime import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import select
from models import *
from flask_bootstrap import Bootstrap

from Custom_Classes import *
from CommuHub_Forms import *
import Time_Functions as timeFunctions

import firebase_admin, os
from firebase_admin import credentials, db

cred = credentials.Certificate("cred/commuhub-2017-firebase-adminsdk-mf4l3-cef43c054d.json")
default_app = firebase_admin.initialize_app(
    cred,
    {'databaseURL': 'https://commuhub-2017.firebaseio.com/',
     'storageBucket': 'gs://commuhub-2017.appspot.com/'
     })

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

# Start of Khant's codes and routes
# The route for URL navigation to all pages TODO: NOW DISABLED, route only returns the HTML without any operations - Used only early in development
@app.route('/')
@app.route('/<path:page>/')
def show_page(page=None):
    # print(page)  To test for page
    if page == "CommuHub_Home" or not page:  # Just the base host URL (no page value set) or homepage
        return render_template("CommuHub_Home.html", returnDate=timeFunctions.returnCurrentDate())
    # elif page != "favicon.ico":  # Called with a argument for page, that's not homepage or favicon
    #     return render_template("{}.html".format(page))
    # else:  # For favicon request
    #     return page

@app.route('/Donation_Projects_Main/')
def donationProjectsMain():
    DProjects = root.child("DProjects").get()
    projectsList = []
    for p_id in DProjects:
        eachProject = DProjects[p_id]
        AProject = DProject(eachProject['Title'],
                             eachProject['Creator'],
                             eachProject['Categories'],
                             eachProject['Description'],
                             eachProject['Items'],
                             eachProject['Start date'],
                             eachProject['End date'])

        AProject.set_p_id(p_id)
        print(AProject.get_p_id())
        projectsList.append(AProject)

    return render_template("Donation_Projects_Main.html", projects = projectsList)

@app.route('/Donation_Projects_Options_test/', methods=['GET', 'POST'])
def donationProjectsOptions():
    pass

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

        return redirect(url_for('donationProjectsMain'))
# End of Khant's codes and routes

# Start of Alden's codes and routes
@app.route('/jsonCalendar/')
def jsonCalendar():
    return render_template("json.html")

@app.route('/calendardata/')
def return_calendardata():
    start_date = request.args.get('start', '')
    end_date = request.args.get('end', '')

    with open("events.json", "r") as input_data:
        return input_data.read()

# End of Alden's codes and routes


# Start of Yasuba's codes and routes
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


@app.route('/md/', methods=['GET', 'POST'])
def m_d():
    ref = db.reference('contact')
    users = ref.get()
    return render_template('messagedetails.html',users=users)

@app.route('/faq/')
def faq():
    return render_template('FAQ.html')
# End of Yasuba's codes and routes

# Start of Ahmad's codes and routes
mail = Mail(app)
@app.route('/Feedback/', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        msg = Message(subject="Feedback",
                      recipients=['jonsnow3050@gmail.com'])
        msg.html = 'From: {} ({}) <br> <br> Subject: {} <br> <br> Message: {}'.format(request.form['name'],
                                                                                      request.form['email'],
                                                                                      request.form['subject'],
                                                                                      request.form['message'])
        mail.send(msg)
        return render_template('feedback.html')

    return render_template('feedback.html')

@app.route('/events_signup/', methods=['GET', 'POST'])
def events_signup():
    if request.method == 'POST':
        eventssignup = Message(subject="events_signup",
                      recipients=['jonsnow3050@gmail.com'])
        eventssignup.html = 'From: {} ({}) <br> <br> Subject: {} <br> <br> Message: {}'.format(request.form['name'],
                                                                                      request.form['event'],
                                                                                      request.form['category'],
                                                                                      request.form['explanation'])
        mail.send(eventssignup)
        return render_template('events_signup.html')

    return render_template('events_signup.html')

@app.route('/organisations/')
def organisations():
    all_org = Organisations.query.all()
    return render_template('organisations.html', all_org = all_org)

@app.route('/organisations/add/', methods=['GET', 'POST'])
def add_organisations():
    if request.method == 'POST':
        new_entry = Organisations(name=request.form['name'], email=request.form['email'], address=request.form['address'], phone=request.form['phone'])
        sqldb.session.add(new_entry)
        sqldb.session.commit()
        return redirect(url_for('organisations'))

    return redirect(url_for('organisations'))

@app.route('/organisations/delete/<id>/', methods=['GET', 'POST'])
def delete_organisations(id):
    selected_org = Organisations.query.filter_by(id=id).first()
    sqldb.session.delete(selected_org)
    sqldb.session.commit()
    return redirect(url_for('organisations'))

@app.route('/organisations/edit/<id>/', methods=['GET', 'POST'])
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

@app.route('/employees/')
def employees():
    all_emp = Employees.query.all()
    return render_template('employee.html', all_emp=all_emp)

@app.route('/employees/add/', methods=['GET', 'POST'])
def add_employees():
    if request.method == 'POST':
        new_entry = Employees(name=request.form['name'], email=request.form['email'], position=request.form['position'], \
                              phone=request.form['phone'])
        sqldb.session.add(new_entry)
        sqldb.session.commit()
        return redirect(url_for('employees'))

    return redirect(url_for('employees'))

@app.route('/employees/delete/<id>/', methods=['GET', 'POST'])
def delete_employees(id):
    selected_emp = Employees.query.filter_by(id=id).first()
    sqldb.session.delete(selected_emp)
    sqldb.session.commit()
    return redirect(url_for('employees'))

@app.route('/employees/edit/<id>/', methods=['GET', 'POST'])
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

@app.route('/events/')
def events():
    all_events = Events.query.all()
    return render_template('events.html', all_events=all_events)


@app.route('/events/add/', methods=['GET', 'POST'])
def add_events():
    if request.method == 'POST':
        new_entry = Events(name=request.form['name'], organisations=request.form['organisations'],
                           things=request.form['things'], \
                           date=request.form['date'], website=request.form['website'])
        sqldb.session.add(new_entry)
        sqldb.session.commit()
        return redirect(url_for('events'))

    return redirect(url_for('events'))


@app.route('/events/delete/<id>/', methods=['GET', 'POST'])
def delete_events(id):
    selected_events = Events.query.filter_by(id=id).first()
    sqldb.session.delete(selected_events)
    sqldb.session.commit()
    return redirect(url_for('events'))


@app.route('/events/edit/<id>/', methods=['GET', 'POST'])
def edit_events(id):
    selected_events = Events.query.filter_by(id=id).first()
    if request.method == 'POST':
        selected_events.name = request.form['name']
        selected_events.organisations = request.form['organisations']
        selected_events.things = request.form['things']
        selected_events.date = request.form['date']
        selected_events.website = request.form['website']
        sqldb.session.commit()
        return redirect(url_for('events'))

    return redirect(url_for('events'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data): #SHA256 hashed 50,000 times
                login_user(user)
                return redirect(url_for('employees'))
        else:
            flash('Invalid username or password!')
            return redirect(url_for('login'))

    return render_template('Login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if current_user.is_authenticated == True:
        return redirect(url_for('employees'))

    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password = form.password.data)

        try:
            sqldb.session.add(new_user)
            sqldb.session.commit()

        except IntegrityError: #because of db's unique constraint
            flash('Email or Username has already been taken!')
            return redirect(url_for('signup'))

        return redirect(url_for('employees'))

    return render_template('signup.html', form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('employees'))

# End of Ahmad's codes and routes

# Start of reference codes for testing only
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

# End of reference codes

# App execution
if __name__ == '__main__':
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    app.secret_key = "e7AdCq7iwNN0RO9YixqraD6l4TuiwCyZh0yd9Yfp"
    app.run(port=80, debug=True)

