import pyrebase
from flask import *

config = {
    "apiKey": "AIzaSyAOksU2ogxblR2vUVczwffzmv-x15v2OJI",
    "authDomain": "casptone-a2cbe.firebaseapp.com",
    "databaseURL": "https://casptone-a2cbe-default-rtdb.firebaseio.com",
    "projectId": "casptone-a2cbe",
    "storageBucket": "casptone-a2cbe.appspot.com",
    "messagingSenderId": "247150714233",
    "appId": "1:247150714233:web:31b6a3fdcc9d5138c5e3a8",
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        name = request.form['name']
        db.child('todo').push(name)
        todo = db.child('todo').get()
        todo_list = todo.val()
        return render_template('index.html', todo=todo_list.values())
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

