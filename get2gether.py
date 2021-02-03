from flask import Flask, request
import os
from pyrebase import pyrebase
from dotenv import load_dotenv
load dotenv()

config = {
    'apiKey': os.getenv('FLASK_APP_FIREBASE_API_KEY'),
    'authDomain': os.getenv('FLASK_APP_FIREBASE_AUTH_DOMAIN'),
    'databaseURL': os.getenv('FLASK_APP_FIREBASE_DATABASE_URL'),
    'storageBucket': os.getenv('FLASK_APP_FIREBASE_STORAGE_BUCKET')
}

app = Flask(__name__)
firebase = pyrebase.initialize_app(config)
app.debug=True

@app.route('/')
def home():
    return 'Get2Gether'

@app.route('/search', methods=['GET'])
def search():
    # if request.method == 'GET':
    # email = request.form['email']
    # name = request.form['name']
        return "search for contacts"
    # else:
    #     return ({'message': 'Error. Invalid endpoint.'})

@app.route('/add_contacts', methods=['POST'])
def add_contacts():
    return "add contacts"

if __name__ == "__main__":
    app.run()