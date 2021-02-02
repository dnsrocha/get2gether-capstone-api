import time
from flask import Flask

app = Flask(__name__)
app.debug=True

@app.route('/time')
def get_current_time():
    return {'time': time.time()}