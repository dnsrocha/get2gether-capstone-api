from flask import Flask, request
from flask_cors import CORS, cross_origin
import os
from datetime import datetime
from pyrebase import pyrebase
from dotenv import load_dotenv
load_dotenv('.env')


config = {
    'apiKey': os.getenv('FLASK_APP_FIREBASE_API_KEY'),
    'authDomain': os.getenv('FLASK_APP_FIREBASE_AUTH_DOMAIN'),
    'databaseURL': os.getenv('FLASK_APP_FIREBASE_DATABASE_URL'),
    'storageBucket': os.getenv('FLASK_APP_FIREBASE_STORAGE_BUCKET'),
    'serviceAccount': os.getenv('FLASK_APP_FIREBASE_SERVICE_ACCOUNT'),
    'messagingSenderId': os.getenv('FLASK_APP_MESSAGING_SENDER_ID'),
    'appId': os.getenv('FLASK_APP_APP_ID'),
    'measurementId': os.getenv('FLASK_APP_MEASUREMENT_ID')
}


app = Flask(__name__)
firebase = pyrebase.initialize_app(config)
CORS(app)
app.debug=True


@app.route('/')
def home():
    return 'Get2Gether'

@app.route('/users', methods=['POST'])
def add_user():
    db=firebase.database()
    if request.method == 'POST':
        submitted_data = request.get_json()
        new_user = {
            'id': submitted_data['id'],
            'username': submitted_data['username'],
            'full_name': submitted_data['full_name'],
            'email': submitted_data['email'],
            'avatar_url': submitted_data['avatar_url'],
            'location_info': {  #this will bring up timezone info //
                'country': submitted_data['location_info']['country'],
                'state': submitted_data['location_info']['state'],
                'city': submitted_data['location_info']['city'],
                'time_zone': submitted_data['location_info']['time_zone'] 
            },
            #'contact_list': {},  --> check for acuracy;
            #'availability_info': {},
            'joined': str(datetime.utcnow())
        }
        db.child('users').push(new_user)
        return({'message': 'New user successfully added.'})
    else:
        return({'message': 'Error: Unable to add user.'})

@app.route('/add_contact', methods=['POST'])
def add_contact():
    db = firebase.database()
    if request.method == 'POST':
        submitted_data = request.get_json()
        new_contact = {
            # 'id': submitted_data['id'], --> should this be auto defined?
            'name': submitted_data['name'],
            'nickname': submitted_data['nickname'],
            'email': submitted_data['email'],
            'location_info': {
                'country': submitted_data['location_info']['country'],
                'state': submitted_data['location_info']['state'],
                'city': submitted_data['location_info']['city'],
                'time_zone': submitted_data['location_info']['time_zone'] 
            }
        }
        db.child('user_contacts').push(new_contact)
        return ({'message': 'New contact successfully added.'})
    else:
        return ({'message': 'Error: Unable to add user.'})


@app.route('/contacts_list', methods=['GET'])
def contacts_list():
    db = firebase.database()


    return "contact list"
    


# @app.route('/search', methods=['GET'])
# def search():
#     if request.method == 'GET':
#     email = request.form['email']
#     name = request.form['name']
#         return "search for contacts"
#     else:
#         return ({'message': 'Error. Invalid endpoint.'})



if __name__ == "__main__":
    app.run()