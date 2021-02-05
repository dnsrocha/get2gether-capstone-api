from flask import Flask, request #, redirect, url_for, abort
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
CORS(app) #,supports_credentials(True)
app.debug=True


# @app.route('/')
# def home():
#     return 'Get2Gether'

# @app.route('/test', methods=['GET', 'POST'])
# def test():
#     db = firebase.database()
#     sample_data = {
#         'user1': {
#         'name': 'jane',
#         'id': 1,
#         'color': 'green' },

#         'user2': {
#             'name': 'john',
#             'id': 2,
#             'color': 'blue'
#         }
#     }
#     if request.method == 'GET':
#         test_get = db.child('users').get()
#         return(test_get)
#     else:
#         db.child('users').push(sample_data)
#         return 'success'


@app.route('/signup', methods=['POST']) #creates a new user profile
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
            'contact_list': {},  #--> check for acuracy between POST requests;
            #'availability_info': {},
            'joined': str(datetime.utcnow())
        }
        db.child('users').push(new_user) #add set to syntax to name path key
        return({'message': 'New user successfully added.'})
    else:
        return({'message': 'Error: Unable to add user.'})

@app.route('/users/user_id', methods=['GET']) #show user profile dashboard // maybe route could be by username? 'users/<string:id>' or 'users/<string:username>'
def user_profile(user_id):
    db = firebase.database()
    # if request.method == 'GET':
        # submitted_data = request['form'] #request from form
        #user = db.session.query(User).filter(User.user_id == user_id).one()
        #total_contacts = len(get_friends(user.user_id).all())

        #check connection between user_a and user_b to show if they are friends or if requests are in pending status
        # user_a_id = session['current_user'][user_id]
        # user_b_id = user.user_id

        # friends, pending_request = is_friend_or_pending(user_a_id, user_b_id)

        # return user profile template, where: {
        #     user = user,
        #     total_friends = total_friends,
        #     friends = friends,
        #     pending_request=pending_request
        # }


@app.route('/add_contact', methods=['POST'])  #manually create new contact - user can have 
def add_contact():
    db = firebase.database()
    if request.method == 'POST':
        submitted_data = request.get_json()
        new_contact = {
            # 'id': submitted_data['id'], --> not submitted but auto defined? ++ autoincrement // fix
            'name': submitted_data['name'],
            'nickname': submitted_data['nickname'],
            'email': submitted_data['email'],
            'location_info': {
                'country': submitted_data['location_info']['country'],
                'state': submitted_data['location_info']['state'],
                'city': submitted_data['location_info']['city'],
                'time_zone': submitted_data['location_info']['time_zone']  #time zone == time info
            },
            'manually_added': True,  #will make a difference when merging added friends and manual entries; user can update manual entries info but can't update added friends (app users) info
        }
        db.child('user_contacts').push(new_contact)
        return ({'message': 'New contact successfully added.'})
    else:
        return ({'message': 'Error: Unable to add user.'})

#will app really need to display a list of contacts or just display contacts by search
# @app.route('/contacts_list', methods=['GET'])
# def contacts_list():
#     db = firebase.database()
#     if request.method == 'GET':
#         contacts_list = db.child('users').get() #how do I exclude the user making the search from showing up here?
#         return(contact list)
#     else:
#         return ({'message': 'Error: Invalid endpoint.'})


@app.route('/search', methods=['GET'])
def search():
    if request.method == 'GET':
        #if search by email:
            find_by_email = request.form['email']
            searched_contact = db.child('users').child('id').child('user_contacts').child('email').get() #where does 'find_by_email' go? //
        #elif search by name:
            find_by_name = request.form['name']
            searched_contact = db.child('user_contacts').child('id').child('user_contacts').child('email').get() #where does 'find_by_name' go?
        #elif search by nickname:
            find_by_nickname = request.form['nickname']
            searched_contact = db.child('user_contacts').child('id').child('user_contacts').child('email').get() #where does 'find_by_nickname' go?
        return "searched_contact"  #complete contact info
    else:
        return ({'message': 'Error. Invalid endpoint.'})


@app.route('/add_friend', methods=['POST']) #called by button click //PATCH?
def search():
    db = firebase.database()
    if request.method == 'POST':
        #this does not return user objects, just the query
    # friends = db.session.query(User).filter(Connection.user_a_id == user_id,
    #     Connection.status == "Accepted").join(Connection,
    #         Connection.user_b_id == User.user_id)

    # return friends
    # if pending, pending = True, if accepted, pending = False
    # db.child('user_contacts').push(add_friend) #push add friend so it 
    #how do I add and set the manually_added value to False here? Maybe I just check if user has a manually_added child field for update purposes?
    return 'add friend'

@app.route('get_friend_requests', methods=[])


if __name__ == "__main__":
    app.run()