import pyrebase
from flask import *
import os

"""
filelist = [f for f in os.listdir(".") if f.endswith(".jpg")]
for f in filelist:
    os.remove(os.path.join(".",f))
"""

config = {
    "apiKey": "AIzaSyAOksU2ogxblR2vUVczwffzmv-x15v2OJI",
    "authDomain": "casptone-a2cbe.firebaseapp.com",
    "databaseURL": "https://casptone-a2cbe-default-rtdb.firebaseio.com",
    "projectId": "casptone-a2cbe",
    "storageBucket": "casptone-a2cbe.appspot.com",
    "messagingSenderId": "247150714233",
    "appId": "1:247150714233:web:31b6a3fdcc9d5138c5e3a8",
    "serviceAccount": "serviceAccountKey.json"
}

firebase = pyrebase.initialize_app(config)

storage = firebase.storage()


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        upload = request.files['upload']
        storage.child("images/new.png").put(upload)
        return 'Successful'
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)