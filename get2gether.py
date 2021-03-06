from flask import Flask, request #, redirect, url_for, abort
from flask_cors import CORS, cross_origin
import os
from datetime import datetime
from pyrebase import pyrebase
from dotenv import load_dotenv
# load_dotenv('.env')
load_dotenv()


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
CORS(app, supports_credentials=True)
app.debug=True



@app.route('/users', methods=['POST']) #creates a new user profile
def add_user():
    db=firebase.database()
    if request.method == 'POST':
        submitted_data = request.get_json()
        new_user = {
            'auth_id': submitted_data['auth_id'],
            'full_name': submitted_data['full_name'],
            'location_info': {  
                'country': submitted_data['location_info']['country'],
                'state': submitted_data['location_info']['state'],
                'city': submitted_data['location_info']['city']
            },
            'availability_info': submitted_data['availability_info'],
            'joined': str(datetime.utcnow())
        }
        db.child('users').push(new_user) 


        return(new_user, 201)
    else:
        return({'message': 'Error: Unable to add user.'}, 404)



@app.route('/users/<string:id>', methods=['GET', 'PUT']) #show user profile dashboard // update user profile
def user_profile(id):
    db = firebase.database()
    if request.method == 'GET':
        user = db.child('users').child(id).get().val()
        if user:
            return(user)
        else:
            return({'message': 'ERROR: User not found'}, 404)
    else:
        submitted_data = request.get_json()
        updated_info = {
            'auth_id': id,
            'full_name': submitted_data['full_name'],
            'location_info': {  
                'country': submitted_data['location_info']['country'],
                'state': submitted_data['location_info']['state'],
                'city': submitted_data['location_info']['city']
            },
            'availability_info': submitted_data['availability_info'],
        }
        
        db.child('users').child(id).update(updated_info)
        return(updated_info, 200)



@app.route('/users/current/<string:auth_id>', methods=['GET']) #finds user by authentication ID
def search_user(auth_id):
    db = firebase.database()
    user = db.child('users').order_by_child('auth_id').equal_to(auth_id).get().val()
    if user:
        return (user, 200)
    else:
        return({'message': 'ERROR: No user found for this authentication ID'}, 404)



@app.route('/add_contact', methods=['POST'])  #manually create new contact 
def add_contact():
    db = firebase.database()
    if request.method == 'POST':
        submitted_data = request.get_json()
        added_by_user = submitted_data['auth_id']
        new_contact = {   
            'name': submitted_data['name'],
            'nickname': submitted_data['nickname'],
            'location_info': {
                'country': submitted_data['location_info']['country'],
                'state': submitted_data['location_info']['state'],
                'city': submitted_data['location_info']['city'],
            },
            'availability_info': submitted_data['availability_info'], # --> time windows where user is available
        }
        db.child("user_contacts").child(added_by_user).push(new_contact)
        return ({'message': 'New contact successfully added.'})
    else:
        return ({'message': 'Error: Unable to add contact.'})
        


# shows contact list for current user by authentication ID
@app.route('/contacts_list/<string:id>', methods=['GET'])
def contacts_list(id):
    db = firebase.database()

    all_contacts = db.child('user_contacts').child(str(id)).get().val()

    result = []
    if all_contacts:
        for key in all_contacts.keys():
            contact = all_contacts[key]
            contact['contact_id'] = key
            result.append(contact)

    return({'result': result}, 200)


@app.route('/contacts/<string:id>/update-info/<string:contact_id>', methods=['GET', 'PUT'])
def update_contact_info(id, contact_id):
    db = firebase.database()
    submitted_data = request.get_json()

    if request.method == 'GET':
        contact = db.child('user_contacts').child(str(id)).child(str(contact_id)).get().val()
        return({'contact': contact})
    else:
        updated_contact_info = {
            'name': submitted_data['name'],
            'nickname': submitted_data['nickname'],
            'location_info': {  
            'country': submitted_data['location_info']['country'],
            'state': submitted_data['location_info']['state'],
            'city': submitted_data['location_info']['city']
            },
            'availability_info': submitted_data['availability_info'], # --> time windows where user is available
            } 

        contact_to_update = db.child('user_contacts').child(str(id)).child(contact_id).update(updated_contact_info)
        return(updated_contact_info, 200)


@app.route('/contacts/<string:id>/delete-contact/<string:contact_id>', methods=['POST']) 
def delete_contact(id, contact_id):
    db = firebase.database()
    submitted_data = request.get_json()

    if request.method == 'POST':
        db.child('user_contacts').child(str(id)).child(contact_id).remove()
        return 'Contact deleted.'
    else:
        return 'ERROR: Invalid request.'






# @app.route('/contacts/<string:auth_id>/<string:contact_id>', methods=['GET']) #finds contact by authentication ID
# def search_contact(auth_id):
#     db = firebase.database()

#     contact_id = submitted_data['contact_id']
#     submitted_data = request.get_json()
#     contact = db.child('user_contacts').child(str(id)).child(str(contact_id)).get().val()
#     if contact:
#         return (contact, 200)
#     else:
#         return({'message': 'ERROR: Contact not found'}, 404)


# # @app.route('/search', methods=['GET'])
# # def search():
# #     if request.method == 'GET':
# # 
# #         #elif search by name:
# #             find_by_name = request.form['name']
# #             searched_contact = db.child('users').order_by_child('user_contacts').equal_to(find_by_name).get().val() #check for accuracy
# #         #elif search by nickname:
# #             find_by_nickname = request.form['nickname']
# #             searched_contact = db.child('users').order_by_child('user_contacts').equal_to(find_by_nickname).get().val() #check for accuracy
# #         return(searched_contact)  #complete contact info
# #     else:
# #         return ({'message': 'Error. Invalid endpoint.'})


# # @app.route('/add_friend', methods=['POST']) #called by button click //PATCH?
# # def search():
# # db = firebase.database()
# #     if request.method == 'POST':
# #         #this does not return user objects, just the query
# #     # friends = db.session.query(User).filter(Connection.user_a_id == user_id,
# #     #     Connection.status == "Accepted").join(Connection,
# #     #         Connection.user_b_id == User.user_id)

# #     # return friends
# #     # if pending, pending = True, if accepted, pending = False
# #     # db.child('user_contacts').push(add_friend) #push add friend so it 
# #     #how do I add and set the manually_added value to False here? Maybe I just check if user has a manually_added child field for update purposes?
# #     return 'add friend'

# # @app.route('get_friend_requests', methods=['GET'])
# # def get_friend_requests()
# # if request.method == 'GET':
# #     #gather pending request info
# #     #return pending request info
# # else:
# #     #return error message



if __name__ == "__main__":
    app.run()