import firebase_admin
from firebase_admin import credentials, db
from flask import Flask,render_template
ref = db.reference('server/saving-data/fireblog')

#default_app = firebase_admin.initialize_app(cred, {
#    "databaseURL": 'https://commuhub-2017.firebaseio.com/'
#})

#root = db.reference()

app = Flask(__name__)

@app.route('/')
def test():
    return render_template

users_ref = ref.child('users')
users_ref.set({
    'alanisawesome': {
        'date_of_birth': 'June 23, 1912',
        'full_name': 'Alan Turing'
    },
    'gracehop': {
        'date_of_birth': 'December 9, 1906',
        'full_name': 'Grace Hopper'
    }
})
# code to save login data (to be changed)

hopper_ref = users_ref.child('gracehop')
hopper_ref.update({
    'nickname': 'Amazing Grace'
})
users_ref.update({
    'alanisawesome/nickname': 'Alan The Machine',
    'gracehop/nickname': 'Amazing Grace'
})
#{
#  "users": {
#    "alanisawesome": {
#      "date_of_birth": "June 23, 1912",
#      "full_name": "Alan Turing",
#      "nickname": "Alan The Machine"
#    },
#    "gracehop": {
#      "date_of_birth": "December 9, 1906",
#      "full_name": "Grace Hopper",
#      "nickname": "Amazing Grace"
#    }
#  }
#}

#code to update saved file
#This are example codes, looking for a way to use them along side event listeners in html