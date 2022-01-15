from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
import json
import pymongo
from functools import wraps
from bson import ObjectId, json_util
import datetime
from dotenv import load_dotenv, find_dotenv
import os
from flask_mail import Mail, Message
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
import jwt

from calculations.damage import damage_all
from calculations.strength import stregth_all, floor_area_wall_bracing, irregulaties
from auth.user import user_construct, set_password, check_password

app = Flask(__name__)
mail= Mail(app)
CORS(app)
load_dotenv(find_dotenv())
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MAIL_SERVER'] ='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'quakestarhousecheck@gmail.com'
app.config['MAIL_PASSWORD'] = 'assnilspekoojeaw'
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
jwt = JWTManager(app)


client = pymongo.MongoClient(os.getenv("mongo_url"))
db = client.test
collection = db['Quakestar']
issues = db['issues']
users = db['users']

@app.route("/")
def index():
    return 'welcome to quakestar api'

# Returns question
@app.route("/<floor_id>/<que_id>")
def get_question(floor_id, que_id):
    f = open('questions.json')
    info = json.load(f)
    question = info[floor_id][que_id]
    return question

#register and initalize
@app.route("/register/<floor_id>", methods=['GET','POST'])
@cross_origin()
def register(floor_id):
    json_data = request.json
    form_user = {
        "name": json_data['user']['name'],
        "email": json_data['user']['email'],
        "address": json_data['user']['address'],
        "suburb": json_data['user']['suburb'],
        "city": json_data['user']['city'],
        "postcode": json_data['user']['postcode'],
        "floor_id": json_data['user']['floor_id'],
        "last_updated": str(datetime.datetime.now())
    }
    user = user_construct(form_user, floor_id)
    inserted = collection.insert_one(user)
    return jsonify(str(inserted.inserted_id))
    
    

#submit response
@app.route('/submit/<floor_id>/<que_id>/<doc_id>', methods=['GET','POST'])
@cross_origin()
def submit(floor_id, que_id, doc_id):

    json_data = request.json
    response = json_data['post']['response']
    complete_str = "completed_{}".format(str(que_id))

    collection.update_one({"_id":ObjectId(doc_id)}, {"$set": {que_id: response, complete_str: True, "last_updated": datetime.datetime.now()}})

    return jsonify('Success')

#get strength and damage
@app.route('/sd/<floor_id>/<doc_id>', methods=['GET'])
@cross_origin()
def sd(floor_id, doc_id):
    f = open('coefficients.json')
    info = json.load(f)
    doc = collection.find_one({"_id":ObjectId(doc_id)})
    strength = round(stregth_all(floor_id, doc)*floor_area_wall_bracing(floor_id, doc), 0)
    c = (10/(1.5**(strength/100))/100)
    t = 3**((strength/50)**1.5)
    k = 9*((damage_all(floor_id, doc))**0.25)*irregulaties(floor_id, doc)* ((info[floor_id]['10'][doc['10']]['strength'] + info[floor_id]['11'][doc['11']]['strength'] + info[floor_id]['12'][doc['12']]['strength'])/3)**1/2
    damage = round(100*((0.15/t)*k + c), 0)
    res = {
        "score": strength,
        "damage": damage,
        "ireg": irregulaties(floor_id, doc)

    }

    return jsonify(res)

#results
@app.route('/results/<floor_id>/<doc_id>', methods=['GET'])
@cross_origin()
def results(floor_id, doc_id):
    f = open('init.json')
    info = json.load(f)
    doc = collection.find_one({"_id":ObjectId(doc_id)})
    res = {
        "name": doc['name'],
        "email": doc['email'],
        "address": doc['address'],
        "suburb": doc['suburb'],
        "city": doc['city'],
        "postcode": doc['postcode'],
        "last_updated": doc['last_updated'],
        "floor_id": doc['floor_id']
    }
    i = 1
    state = False
    while i < len(info[floor_id]) + 1:
        complete_str = "completed_{}".format(str(i))
        res[complete_str] = doc[complete_str]
        res[str(i)] = doc[str(i)]
        i += 1
        if i == len(info[floor_id]) + 1:
            state = True
            return res

    return jsonify(res)



def parse_json(data):
    return json.loads(json_util.dumps(data))

@app.route('/doc/<doc_id>/', methods=['GET'])
@cross_origin()
def get_doc(doc_id):
    doc = collection.find_one({"_id":ObjectId(doc_id)})
    return parse_json(doc)

#report issue
@app.route('/issue', methods=['POST'])
@cross_origin()
def report_issue():
    json_data = request.json
    issue = {
        "floor_id": json_data['issue']['floor_id'],
        "que_id": json_data['issue']['que_id'],
        "issue": json_data['issue']['issue'],
        "submitted": str(datetime.datetime.now())
    }
    issues.insert_one(issue)
    return jsonify('Success')

#send email
@app.route("/send_email", methods=['POST'])
def send_email():
    json_data = request.json
    results_link = json_data['results_url']
    user = json_data['user']
    print(user)
    print(user['email'])
    msg = Message('QuakeStar Housecheck', sender = 'QuakeStar HouseCheck', recipients = [user['email']])
    msg.html  = render_template("email.html", user = json_data['user'], results_link = results_link)
    mail.send(msg)
    return jsonify('Success')

#login
@app.route("/login", methods=['POST'])
def login():
    json_data = request.json
    email = json_data['user']['email']
    password = json_data['user']['password']
    user = users.find_one({"email": email})
    if user is None or not check_password(user['password'], password):
        return jsonify({'message':'Wrong creds'}), 400
    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0.5),
        "user": user,
    }
    jwt_token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm='HS256')
    return jsonify({'token': jwt_token})

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            jwt_token = request.headers.get("Authorization")
            payload = jwt.decode(jwt_token, os.getenv("SECRET_KEY"), algorithm='HS256')
            if payload.user.admin:
                return fn(*args, **kwargs)
            else:
                return jsonify({'message': 'Wrong creds'}), 400
        return decorator
    return wrapper

@app.route('/admin', methods=['GET'])
@admin_required
def admin():

    return jsonify('Success')


if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True, port=5000)