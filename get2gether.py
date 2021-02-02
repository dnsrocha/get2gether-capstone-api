from flask import Flask
#from dotenv import load_dotenv
#load dotenv()


app = Flask(__name__)
app.debug=True

@app.route('/')
def home():
    return 'Get2Gether'

@app.route('/search')
def search():
    return "search for contacts"

if __name__ == "__main__":
    app.run()