from flask import Flask, redirect, url_for, request, render_template, session, send_from_directory, flash, escape, g, abort
from flask_mail import Mail, Message
from jinja2 import Template

import CommuHub.CommuHub_Forms as customForms
import CommuHub.Time_Functions as timeFunctions

# Ahmad's calendar
import calendar

import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("cred/commuhub-2017-firebase-adminsdk-mf4l3-5449d3e484.json")
default_app = firebase_admin.initialize_app(cred, {
    "databaseURL": 'https://commuhub-2017.firebaseio.com/'
})

root = db.reference()

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
@app.route('/<path:page>')
def show_page(page=None):
    # print(page)  To test for page
    if page == "CommuHub_Home" or not page:  # Just the base host URL (no page value set) or homepage
        return render_template("CommuHub_Home.html", returnDate=timeFunctions.returnCurrentDate())
    #Temporary for FAQ
    elif page == "FAQ.html":
        return render_template("FAQ.html")
    elif page != "favicon.ico":  # Called with a argument for page, that's not homepage
        return render_template("{}.html".format(page))
    else:  # For favicon request
        return page

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

#Create a plain text calendar
c = calendar.TextCalendar(calendar.THURSDAY)
str = c.formatmonth(2015,1,0,0)
print(str)

#Create an HTML formatted calendar
hc = calendar.HTMLCalendar(calendar.THURSDAY)
str = hc.formatmonth(2015, 1)
print(str)
#loop over the days of a month
#zeroes indicate that the day of the week is in a next month or overlapping month
for i in c.itermonthdays(2015,4):
  print(i)

#The calendar can give info based on local such a names of days and months (full and abbreviated forms)
for name in calendar.month_name:
    print(name)
for day in calendar.day_name:
    print(day)
#calculate days based on a rule: For instance an audit day on the second Monday of every month
#Figure out what days that would be for each month, we can use the script as shown here
for month in range(1,13):
# It retrieves a list of weeks that represent the month
    mycal = calendar.monthcalendar(2020, month)
# The second MONDAY has to be within the first two weeks
    week1 = mycal[1]
    week2 = mycal[2]
    if week1[calendar.MONDAY] != 0:
        auditday = week1[calendar.MONDAY]
    else:
# if the second MONDAY isn't in the first week, it must be in the second week
        auditday = week2[calendar.MONDAY]
print("%10s %2d" % (calendar.month_name[month], auditday))


# Note using URL strings as arguments and "returned" strings are parsed as HTML
@app.route("/hello/<username>/")
def hello_user(username):
    return "<h1>Hello {}<h1>".format(username)

# End code to execute
if __name__ == '__main__':
    app.secret_key = "e7AdCq7iwNN0RO9YixqraD6l4TuiwCyZh0yd9Yfp"
    app.run()
    # app.run(debug=True)  optimisation?
