import firebase_admin, os
from firebase_admin import credentials, db

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
FB_CRED = os.path.join(APP_ROOT, 'cred/firebase.json')

def init_firebase():
    cred = credentials.Certificate(FB_CRED)
    fb_url = {'databaseURL':'https://oopp-c6fcf.firebaseio.com'}
    default_app = firebase_admin.initialize_app(cred, fb_url)

def add_contact(name, email, phone, message):
    root = db.reference('/contact')
    dict = {'name':name, 'email':email, 'phone':phone, 'message':message}
    root.push(dict)

init_firebase()