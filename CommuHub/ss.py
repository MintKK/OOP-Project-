from flask import Flask, render_template, request,redirect,url_for
from entities import *
from wtforms import Form

app = Flask(__name__)


@app.route('/ss', methods=['GET', 'POST'])
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

if __name__ == '__main__':
    app.run()
