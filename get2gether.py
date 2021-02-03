from flask import Flask, request
import os
from pyrebase import pyrebase
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv('.env')


config = {
    'apiKey': os.getenv('FLASK_APP_FIREBASE_API_KEY'),
    'authDomain': os.getenv('FLASK_APP_FIREBASE_AUTH_DOMAIN'),
    'databaseURL': os.getenv('FLASK_APP_FIREBASE_DATABASE_URL'),
    'storageBucket': os.getenv('FLASK_APP_FIREBASE_STORAGE_BUCKET')
}


app = Flask(__name__)
firebase = pyrebase.initialize_app(config)
CORS(app)
app.debug=True

@app.route('/')
def home():
    return 'Get2Gether'

@app.route('/add_contacts', methods=['POST'])
def add_contacts():
    db = firebase.database()
    # if request.method == 'POST':
    return "add contacts"

@app.route('/search', methods=['GET'])
def search():
    # if request.method == 'GET':
    # email = request.form['email']
    # name = request.form['name']
        return "search for contacts"
    # else:
    #     return ({'message': 'Error. Invalid endpoint.'})


@app.route('/time')
def get_current_time():
    return {'time': time.time()}


if __name__ == "__main__":
    app.run()