from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
import json
import pymongo
from bson import ObjectId, json_util
import datetime
from dotenv import load_dotenv, find_dotenv
import os
from flask_mail import Mail, Message


app = Flask(__name__)
mail= Mail(app)
CORS(app)
load_dotenv(find_dotenv())
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['MAIL_SERVER'] ='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'cthomlinson8@gmail.com'
app.config['MAIL_PASSWORD'] = 'fntfbdpbajxzqkzz'
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

client = pymongo.MongoClient(os.getenv("mongo_url"))
db = client.test
collection = db['Quakestar']
issues = db['issues']

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


def user_construct(user, floor_id):
    f = open('init.json')
    info = json.load(f)
    #firstName = "David"
    #lastName = "Thomlinson"
    #address = "99 portland rd, Remuera, Auckland 1050"
    #email = "cmthomlinson@gmail.com"
    user = {
        "name": user['name'],
        "email": user['email'],
        "address": user['address'],
        "suburb": user['suburb'],
        "city": user['city'],
        "postcode": user['postcode'],
        "last_updated": user['last_updated'],
        "floor_id": user['floor_id'],
        "strength": 0,
        "damage": 0
    }
    i = 1
    state = False
    while i < len(info[floor_id]) + 1:
        user[str(i)] = info[floor_id][str(i)]['response']
        complete_str = "completed_{}".format(str(i))
        user[complete_str] = False
            
        i += 1
        if i == len(info[floor_id]) + 1:
            state = True
            return user


    
    return user


#Register and initalize
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
    
    

#Submit response
@app.route('/submit/<floor_id>/<que_id>/<doc_id>', methods=['GET','POST'])
@cross_origin()
def submit(floor_id, que_id, doc_id):

    json_data = request.json
    response = json_data['post']['response']
    complete_str = "completed_{}".format(str(que_id))
    collection.update_one({"_id":ObjectId(doc_id)}, {"$set": {que_id: response, complete_str: True, "last_updated": datetime.datetime.now()}})

    return jsonify('Success')

def stregth_all(floor_id, doc):
    f = open('coefficients.json')
    info = json.load(f)
    site = (info[floor_id]['2'][doc['2']]['strength'] + info[floor_id]['3'][doc['3']]['strength'] + 1 + info[floor_id]['4'][doc['4']]['strength']) / 4
    building_data1 = info[floor_id]['5'][doc['5']]['strength']
    building_data2 = (info[floor_id]['6'][doc['6']]['strength'] + info[floor_id]['7'][doc['7']]['strength'])/2
    appendages = min(irregulaties(floor_id, doc), min(info[floor_id]['10'][doc['10']]['strength'], info[floor_id]['11'][doc['11']]['strength'], info[floor_id]['12'][doc['12']]['strength']))
    seismic_coefficent = info[floor_id]['1'][doc['1']]
    foundations = checkox_av(floor_id, doc, '8', 'strength')

    print("site: {}".format(site))
    print("building_data1: {}".format(building_data1))
    print("building_data2: {}".format(building_data2))
    print("appendages: {}".format(appendages))
    print("seismic_coefficent: {}".format(seismic_coefficent))
    print("foundations: {}".format(foundations))
    print("irre: {}".format(irregulaties(floor_id, doc)))

    return site*building_data1*building_data2*appendages*(0.4/seismic_coefficent)*foundations

def checkox_av(floor_id, doc, que_id, type):
    f = open('coefficients.json')
    info = json.load(f)
    true_ = []
    sum_ = 0
    for i in doc[que_id]:
        if doc[que_id][str(i)] == True:
            sum_ += info[floor_id][que_id][i][type]
            true_.append(i)

    if sum_ == 0:
        return 1
    average = sum_/(len(true_))
    return average

def clad_struct_average(floor_id, doc): 
    f = open('coefficients.json')
    info = json.load(f)

    if floor_id == "1":
        clad_av = (checkox_av(floor_id, doc, '16', 'damage') + checkox_av(floor_id, doc, '17', 'damage') + 3)/5
        structure_av = (checkox_av(floor_id, doc, '8', 'strength') + info[floor_id]['9'][doc['9']]['damage'] + 1 + info[floor_id]['13'][doc['13']]['damage'] + info[floor_id]['14'][doc['14']]['damage'] + info[floor_id]['15'][doc['15']]['damage'] + 12)/8
        print("clad_av: {}".format(clad_av))
        print("structure_av: {}".format(structure_av))
        return clad_av*structure_av

    if floor_id == "2":
        clad_av = (checkox_av(floor_id, doc, '20', 'damage') + checkox_av(floor_id, doc, '21', 'damage') + checkox_av(floor_id, doc, '22', 'damage') + 2)/5
        structure_av = (checkox_av(floor_id, doc, '8', 'strength') + info[floor_id]['9'][doc['9']]['damage'] + 1 + info[floor_id]['13'][doc['13']]['damage'] + info[floor_id]['14'][doc['14']]['damage'] + info[floor_id]['16'][doc['16']]['damage'] + info[floor_id]['17'][doc['17']]['damage'] + info[floor_id]['18'][doc['18']]['damage'] + info[floor_id]['19'][doc['19']]['damage'] + 9)/18
        print("clad_av: {}".format(clad_av))
        print("structure_av: {}".format(structure_av))
        return clad_av*structure_av

    if floor_id == "3":
        clad_av = (checkox_av(floor_id, doc, '24', 'damage') + checkox_av(floor_id, doc, '25', 'damage') + checkox_av(floor_id, doc, '26', 'damage') + checkox_av(floor_id, doc, '27', 'damage') + 1)/5
        structure_av = (checkox_av(floor_id, doc, '8', 'strength') + info[floor_id]['9'][doc['9']]['damage'] + 1 + info[floor_id]['13'][doc['13']]['damage'] + info[floor_id]['14'][doc['14']]['damage'] + info[floor_id]['15'][doc['15']]['damage'] + info[floor_id]['16'][doc['16']]['damage'] + info[floor_id]['17'][doc['17']]['damage'] + info[floor_id]['18'][doc['18']]['damage'] + info[floor_id]['19'][doc['19']]['damage'] + info[floor_id]['20'][doc['20']]['damage'] + info[floor_id]['21'][doc['21']]['damage'] + info[floor_id]['22'][doc['22']]['damage'] + info[floor_id]['23'][doc['23']]['damage'] + 4)/18
        print("clad_av: {}".format(clad_av))
        print("structure_av: {}".format(structure_av))
        return clad_av*structure_av

    if floor_id == "1b":
        clad_av = (checkox_av(floor_id, doc, '20', 'damage') + checkox_av(floor_id, doc, '21', 'damage') + checkox_av(floor_id, doc, '22', 'damage') + 2)/5
        structure_av = (checkox_av(floor_id, doc, '8', 'strength') + info[floor_id]['9'][doc['9']]['damage'] + info[floor_id]['13'][doc['13']]['damage'] + info[floor_id]['14'][doc['14']]['damage'] + info[floor_id]['15'][doc['15']]['damage'] + info[floor_id]['16'][doc['16']]['damage'] + info[floor_id]['17'][doc['17']]['damage'] + info[floor_id]['18'][doc['18']]['damage'] + info[floor_id]['19'][doc['19']]['damage'] + 9)/18
        print("clad_av: {}".format(clad_av))
        print("structure_av: {}".format(structure_av))
        return clad_av*structure_av

    if floor_id == "2b":
        clad_av = (checkox_av(floor_id, doc, '24', 'damage') + checkox_av(floor_id, doc, '25', 'damage') + checkox_av(floor_id, doc, '26', 'damage') + checkox_av(floor_id, doc, '27', 'damage') + 1)/5
        structure_av = (checkox_av(floor_id, doc, '8', 'strength') + info[floor_id]['9'][doc['9']]['damage'] + info[floor_id]['13'][doc['13']]['damage'] + info[floor_id]['14'][doc['14']]['damage'] + info[floor_id]['15'][doc['15']]['damage'] + info[floor_id]['16'][doc['16']]['damage'] + info[floor_id]['17'][doc['17']]['damage'] + info[floor_id]['18'][doc['18']]['damage'] + info[floor_id]['19'][doc['19']]['damage'] + info[floor_id]['20'][doc['20']]['damage'] + info[floor_id]['21'][doc['21']]['damage'] + info[floor_id]['22'][doc['22']]['damage'] + info[floor_id]['23'][doc['23']]['damage'] + 5)/18
        print("clad_av: {}".format(clad_av))
        print("structure_av: {}".format(structure_av))
        return clad_av*structure_av

    if floor_id == "3b":
        clad_av = (checkox_av(floor_id, doc, '30', 'damage') + checkox_av(floor_id, doc, '31', 'damage') + checkox_av(floor_id, doc, '32', 'damage') + checkox_av(floor_id, doc, '33', 'damage') + checkox_av(floor_id, doc, '34', 'damage'))/5
        structure_av = (checkox_av(floor_id, doc, '8', 'strength') + info[floor_id]['9'][doc['9']]['damage'] + info[floor_id]['13'][doc['13']]['damage'] + info[floor_id]['14'][doc['14']]['damage'] + info[floor_id]['15'][doc['15']]['damage'] + info[floor_id]['16'][doc['16']]['damage'] + info[floor_id]['17'][doc['17']]['damage'] + info[floor_id]['18'][doc['18']]['damage'] + info[floor_id]['19'][doc['19']]['damage'] + info[floor_id]['20'][doc['20']]['damage'] + info[floor_id]['21'][doc['21']]['damage'] + info[floor_id]['22'][doc['22']]['damage'] + info[floor_id]['23'][doc['23']]['damage'] + info[floor_id]['24'][doc['24']]['damage'] + info[floor_id]['25'][doc['25']]['damage'] + info[floor_id]['26'][doc['26']]['damage'] + info[floor_id]['27'][doc['27']]['damage'] + 1)/18
        print("clad_av: {}".format(clad_av))
        print("structure_av: {}".format(structure_av))
        return clad_av*structure_av

def damage_all(floor_id, doc):
    f = open('coefficients.json')
    info = json.load(f)
    site = max(info[floor_id]['2'][doc['2']]['damage'], info[floor_id]['3'][doc['3']]['damage'], 1, info[floor_id]['3'][doc['3']]['damage'])
    building = (info[floor_id]['5'][doc['5']]['damage'] * info[floor_id]['6'][doc['6']]['damage'] * info[floor_id]['7'][doc['7']]['damage'])
    print("site_damage: {}".format(site))
    print("building_damage: {}".format(building))

    return site*building*clad_struct_average(floor_id, doc)


def get_score(floor_id, doc):
    score = round(stregth_all(floor_id, doc)*floor_area_wall_bracing(floor_id, doc), 0)

    return score

def get_damage(floor_id, doc):
    score = stregth_all(floor_id, doc)*floor_area_wall_bracing(floor_id, doc)
    damage = round((2000/score)*damage_all(floor_id, doc),0)

    return damage


@app.route('/sd/<floor_id>/<doc_id>', methods=['GET'])
@cross_origin()
def sd(floor_id, doc_id):
    f = open('coefficients.json')
    info = json.load(f)
    doc = collection.find_one({"_id":ObjectId(doc_id)})
    res = {
        "score": get_score(floor_id, doc),
        "damage": get_damage(floor_id, doc)
    }

    return jsonify(res)

def irregulaties(floor_id, doc):
    f = open('coefficients.json')
    info = json.load(f)
    if floor_id == "1":

        return 1*info[floor_id]['21'][doc['21']]['strength']

    #2   12-27 Roofcladding-20 Roofarea-25
    if floor_id == "2":
        x0 = 1
        x1 = ((doc['26']['x']*info[floor_id]['16'][doc['16']]['strength'])/(doc['27']['x']*info[floor_id]['18'][doc['18']]['strength']))*1.2
        x2 = ((doc['26']['y']*info[floor_id]['17'][doc['17']]['strength'])/(doc['27']['y']*info[floor_id]['19'][doc['19']]['strength']))*1.2
        return min(x0, x1, x2)*info[floor_id]['28'][doc['28']]['strength']

    #3   12-34 Roofcladding-24 Roofarea-31
    if floor_id == "3":
        x0 = 1
        x1 = ((info[floor_id]['20'][doc['20']]['strength']*doc['33']['x'])/(info[floor_id]['22'][doc['22']]['strength']*doc['34']['x']))*1.2
        x2 = ((info[floor_id]['21'][doc['21']]['strength']*doc['33']['y'])/(info[floor_id]['23'][doc['23']]['strength']*doc['34']['y']))*1.2
        x3 = ((info[floor_id]['18'][doc['18']]['strength']*doc['32']['x'])/(info[floor_id]['20'][doc['20']]['strength']*doc['33']['x']))*1.2
        x4 = ((info[floor_id]['19'][doc['19']]['strength']*doc['32']['y'])/(info[floor_id]['21'][doc['21']]['strength']*doc['33']['y']))*1.2
        return min(x0, x1, x2, x3, x4)*info[floor_id]['35'][doc['35']]['strength']
    #1b   12-27 Roofcladding-20 Roofarea-25
    if floor_id == "1b":
        x0 = 1
        x1 = ((info[floor_id]['18'][doc['18']]['strength']*doc['27']['x'])/(info[floor_id]['16'][doc['16']]['strength']*doc['26']['x']))*1.2
        x2 = ((info[floor_id]['19'][doc['19']]['strength']*doc['27']['y'])/(info[floor_id]['17'][doc['17']]['strength']*doc['26']['y']))*1.2
        return min(x0, x1, x2)*info[floor_id]['28'][doc['28']]['strength']

    #2b   12-34 Roofcladding-28 Roofarea-31
    if floor_id == "2b":
        x0 = 1
        x1 = ((doc['32']['x']*info[floor_id]['18'][doc['18']]['strength'])/(doc['33']['x']*info[floor_id]['20'][doc['20']]['strength']))*1.2
        x2 = ((doc['32']['y']*info[floor_id]['19'][doc['19']]['strength'])/(doc['33']['y']*info[floor_id]['21'][doc['21']]['strength']))*1.2
        x3 = ((info[floor_id]['22'][doc['22']]['strength']*doc['34']['x'])/(doc['32']['y']*info[floor_id]['19'][doc['19']]['strength']))*1.2
        x4 = ((info[floor_id]['23'][doc['23']]['strength']*doc['34']['y'])/(doc['32']['y']*info[floor_id]['19'][doc['19']]['strength']))*1.2
        return min(x0, x1, x2, x3, x4)*info[floor_id]['35'][doc['35']]['strength']

    #3b   12-41 Roofcladding-28 Roofarea-37
    if floor_id == "3b":
        x0 = 1
        x1 = ((info[floor_id]['22'][doc['22']]['strength']*doc['39']['x'])/(info[floor_id]['24'][doc['24']]['strength'] * doc['40']['x']))*1.2
        x2 = ((info[floor_id]['23'][doc['23']]['strength']*doc['39']['y'])/(info[floor_id]['25'][doc['25']]['strength'] * doc['40']['y']))*1.2
        x3 = ((info[floor_id]['20'][doc['20']]['strength']*doc['38']['x'])/(info[floor_id]['22'][doc['22']]['strength']*doc['39']['x']))*1.2
        x4 = ((info[floor_id]['21'][doc['21']]['strength']*doc['38']['y'])/(info[floor_id]['23'][doc['23']]['strength']*doc['39']['y']))*1.2
        x5 = ((info[floor_id]['26'][doc['26']]['strength'] * doc['41']['x'])/(info[floor_id]['20'][doc['20']]['strength']*doc['38']['x']))*1.2
        x6 = ((info[floor_id]['27'][doc['27']]['strength'] * doc['41']['y'])/(info[floor_id]['21'][doc['21']]['strength']*doc['38']['y']))*1.2
        return min(x0, x1, x2, x3, x4, x5, x6)*info[floor_id]['42'][doc['42']]['strength']
      

    return 'success'


def floor_area_wall_bracing(floor_id, doc):
    f = open('coefficients.json')
    info = json.load(f)

    #1   12-20 Roofcladding-16 Roofarea-19
    if floor_id == "1":
        x1 = (50/3)/(((doc['19']['x'] * doc['19']['y'] * checkox_av(floor_id, doc, '16', 'strength')) + (doc['19']['x'] + doc['19']['y'])*2*((checkox_av(floor_id, doc, '17', 'strength') + 1)/2))/(info[floor_id]['14'][doc['14']]['strength']*doc['20']['x']))
        x2 = (50/3)/(((doc['19']['x'] * doc['19']['y'] * checkox_av(floor_id, doc, '16', 'strength')) + (doc['19']['x'] + doc['19']['y'])*2*((checkox_av(floor_id, doc, '17', 'strength') + 1)/2))/(info[floor_id]['15'][doc['15']]['strength']*doc['20']['y']))
        print(min(x1, x2))
        return min(x1, x2)

    #2   12-27 Roofcladding-20 Roofarea-25
    if floor_id == "2":
        x1 = (50/3)/((doc['25']['x'] * doc['25']['y'] * checkox_av(floor_id, doc, '20', 'strength') + (doc['24']['x'] + doc['24']['y'])*2*((checkox_av(floor_id, doc, '22', 'strength') + info[floor_id]['14'][doc['14']]['strength'])/2))/(doc['27']['x']*info[floor_id]['18'][doc['18']]['strength']))
        x2 = (50/3)/((doc['25']['x'] * doc['25']['y'] * checkox_av(floor_id, doc, '20', 'strength') + (doc['24']['x'] + doc['24']['y'])*2*((checkox_av(floor_id, doc, '22', 'strength') + info[floor_id]['14'][doc['14']]['strength'])/2))/(doc['27']['y']*info[floor_id]['19'][doc['19']]['strength']))
        x3 = (50/3)/((doc['25']['x'] * doc['25']['y'] * checkox_av(floor_id, doc, '20', 'strength') + (doc['24']['x'] + doc['24']['y'])*2*((checkox_av(floor_id, doc, '22', 'strength') + info[floor_id]['14'][doc['14']]['strength'])/2) + (doc['24']['x'] * doc['24']['y'])*info[floor_id]['15'][doc['15']]['strength'] + (doc['23']['x'] + doc['23']['y'])*2*((checkox_av(floor_id, doc, '21', 'strength') + 1)/2))/(doc['26']['x']*info[floor_id]['16'][doc['16']]['strength']))
        x4 = (50/3)/((doc['25']['x'] * doc['25']['y'] * checkox_av(floor_id, doc, '20', 'strength') + (doc['24']['x'] + doc['24']['y'])*2*((checkox_av(floor_id, doc, '22', 'strength') + info[floor_id]['14'][doc['14']]['strength'])/2) + (doc['24']['x'] * doc['24']['y'])*info[floor_id]['15'][doc['15']]['strength'] + (doc['23']['x'] + doc['23']['y'])*2*((checkox_av(floor_id, doc, '21', 'strength') + 1)/2))/(doc['26']['y']*info[floor_id]['17'][doc['17']]['strength']))
        print(min(x1, x2, x3, x4))
        return min(x1, x2, x3, x4)

    #3   12-34 Roofcladding-24 Roofarea-31
    if floor_id == "3":
        x1 = (50/3)/(((doc['31']['x'] * doc['31']['y'] * checkox_av(floor_id, doc, '24', 'strength') + (doc['30']['x'] + doc['30']['y'])*2*((checkox_av(floor_id, doc, '27', 'strength') + info[floor_id]['16'][doc['16']]['strength'])/2)))/(info[floor_id]['22'][doc['22']]['strength']*doc['34']['x']))
        x2 = (50/3)/(((doc['31']['x'] * doc['31']['y'] * checkox_av(floor_id, doc, '24', 'strength') + (doc['30']['x'] + doc['30']['y'])*2*((checkox_av(floor_id, doc, '27', 'strength') + info[floor_id]['16'][doc['16']]['strength'])/2)))/(info[floor_id]['23'][doc['23']]['strength']*doc['34']['y']))
        x3 = (50/3)/(((doc['31']['x'] * doc['31']['y'] * checkox_av(floor_id, doc, '24', 'strength') + (doc['30']['x'] + doc['30']['y'])*2*((checkox_av(floor_id, doc, '27', 'strength') + info[floor_id]['16'][doc['16']]['strength'])/2) + (doc['30']['x'] * doc['30']['y'])*info[floor_id]['17'][doc['17']]['strength'] + (doc['29']['x'] + doc['29']['y'])*2*((checkox_av(floor_id, doc, '26', 'strength') + info[floor_id]['14'][doc['14']]['strength'])/2))/(info[floor_id]['20'][doc['20']]['strength']*doc['33']['x'])))
        x4 = (50/3)/(((doc['31']['x'] * doc['31']['y'] * checkox_av(floor_id, doc, '24', 'strength') + (doc['30']['x'] + doc['30']['y'])*2*((checkox_av(floor_id, doc, '27', 'strength') + info[floor_id]['16'][doc['16']]['strength'])/2) + (doc['30']['x'] * doc['30']['y'])*info[floor_id]['17'][doc['17']]['strength'] + (doc['29']['x'] + doc['29']['y'])*2*((checkox_av(floor_id, doc, '26', 'strength') + info[floor_id]['14'][doc['14']]['strength'])/2))/(info[floor_id]['21'][doc['21']]['strength']*doc['33']['y'])))
        x5 = (50/3)/((doc['31']['x'] * doc['31']['y'] * checkox_av(floor_id, doc, '24', 'strength') + (doc['30']['x'] + doc['30']['y'])*2*((checkox_av(floor_id, doc, '27', 'strength') + info[floor_id]['16'][doc['16']]['strength'])/2) + (doc['30']['x'] * doc['30']['y'])*info[floor_id]['17'][doc['17']]['strength'] + (doc['29']['x'] + doc['29']['y'])*2*((checkox_av(floor_id, doc, '26', 'strength') + info[floor_id]['14'][doc['14']]['strength'])/2) + (doc['29']['x']*doc['29']['y'])*info[floor_id]['15'][doc['15']]['strength'] + (doc['28']['x'] + doc['28']['y'])*2*((checkox_av(floor_id, doc, '25', 'strength') + 1)/2))/(info[floor_id]['18'][doc['18']]['strength']*doc['32']['x']))
        x6 = (50/3)/((doc['31']['x'] * doc['31']['y'] * checkox_av(floor_id, doc, '24', 'strength') + (doc['30']['x'] + doc['30']['y'])*2*((checkox_av(floor_id, doc, '27', 'strength') + info[floor_id]['16'][doc['16']]['strength'])/2) + (doc['30']['x'] * doc['30']['y'])*info[floor_id]['17'][doc['17']]['strength'] + (doc['29']['x'] + doc['29']['y'])*2*((checkox_av(floor_id, doc, '26', 'strength') + info[floor_id]['14'][doc['14']]['strength'])/2) + (doc['29']['x']*doc['29']['y'])*info[floor_id]['15'][doc['15']]['strength'] + (doc['28']['x'] + doc['28']['y'])*2*((checkox_av(floor_id, doc, '25', 'strength') + 1)/2))/(info[floor_id]['19'][doc['19']]['strength']*doc['32']['y']))
        print(min(x1, x2, x3, x4, x5, x6))
        return min(x1, x2, x3, x4, x5, x6)

    #1b   12-27 Roofcladding-20 Roofarea-25
    if floor_id == "1b":
        x1 = (50/3)/(((doc['25']['x'] * doc['25']['y'] * checkox_av(floor_id, doc, '20', 'strength')) + (doc['23']['x'] + doc['23']['y'])*2*((checkox_av(floor_id, doc, '21', 'strength') + info[floor_id]['13'][doc['13']]['strength'])/2))/(info[floor_id]['16'][doc['16']]['strength']*(doc['26']['x'])))
        x2 = (50/3)/(((doc['25']['x'] * doc['25']['y'] * checkox_av(floor_id, doc, '20', 'strength')) + (doc['23']['x'] + doc['23']['y'])*2*((checkox_av(floor_id, doc, '21', 'strength') + info[floor_id]['13'][doc['13']]['strength'])/2))/(info[floor_id]['17'][doc['17']]['strength']*(doc['26']['y'])))
        x3 = (50/3)/(((doc['25']['x'] * doc['25']['y'] * checkox_av(floor_id, doc, '20', 'strength')) + (doc['23']['x'] + doc['23']['y'])*2*((checkox_av(floor_id, doc, '21', 'strength') + info[floor_id]['13'][doc['13']]['strength'])/2) + (doc['23']['x'] * doc['23']['y'])*info[floor_id]['14'][doc['14']]['strength'] + (doc['24']['x'] + doc['24']['y'])*2*((checkox_av(floor_id, doc, '22', 'strength') + 1)/2))/(info[floor_id]['19'][doc['19']]['strength']*doc['27']['x']))
        x4 = (50/3)/(((doc['25']['x'] * doc['25']['y'] * checkox_av(floor_id, doc, '20', 'strength')) + (doc['23']['x'] + doc['23']['y'])*2*((checkox_av(floor_id, doc, '21', 'strength') + info[floor_id]['13'][doc['13']]['strength'])/2) + (doc['23']['x'] * doc['23']['y'])*info[floor_id]['14'][doc['14']]['strength'] + (doc['24']['x'] + doc['24']['y'])*2*((checkox_av(floor_id, doc, '22', 'strength') + 1)/2))/(info[floor_id]['19'][doc['19']]['strength']*doc['27']['y']))
        print(min(x1, x2, x3, x4))
        return min(x1, x2, x3, x4)

    #2b   12-34 Roofcladding-28 Roofarea-31
    if floor_id == "2b":
        x1 = (50/3)/((doc['31']['x'] * doc['31']['y'] * checkox_av(floor_id, doc, '24', 'strength') + (doc['29']['x'] + doc['29']['y'])*2*((checkox_av(floor_id, doc, '26', 'strength') + info[floor_id]['15'][doc['15']]['strength'])/2))/(doc['33']['x']*info[floor_id]['20'][doc['20']]['strength']))
        x2 = (50/3)/((doc['31']['x'] * doc['31']['y'] * checkox_av(floor_id, doc, '24', 'strength') + (doc['29']['x'] + doc['29']['y'])*2*((checkox_av(floor_id, doc, '26', 'strength') + info[floor_id]['15'][doc['15']]['strength'])/2))/(doc['33']['y']*info[floor_id]['21'][doc['21']]['strength']))
        x3 = (50/3)/((doc['31']['x'] * doc['31']['y'] * checkox_av(floor_id, doc, '24', 'strength') + (doc['29']['x'] + doc['29']['y'])*2*((checkox_av(floor_id, doc, '26', 'strength') + info[floor_id]['15'][doc['15']]['strength'])/2) + (doc['29']['x'] * doc['29']['y'])*info[floor_id]['16'][doc['16']]['strength'] + (doc['28']['x'] + doc['28']['y'])*2*((checkox_av(floor_id, doc, '25', 'strength') + info[floor_id]['13'][doc['13']]['strength'])/2))/(doc['32']['x']*info[floor_id]['18'][doc['18']]['strength']))
        x4 = (50/3)/((doc['31']['x'] * doc['31']['y'] * checkox_av(floor_id, doc, '24', 'strength') + (doc['29']['x'] + doc['29']['y'])*2*((checkox_av(floor_id, doc, '26', 'strength') + info[floor_id]['15'][doc['15']]['strength'])/2) + (doc['29']['x'] * doc['29']['y'])*info[floor_id]['16'][doc['16']]['strength'] + (doc['28']['x'] + doc['28']['y'])*2*((checkox_av(floor_id, doc, '25', 'strength') + info[floor_id]['13'][doc['13']]['strength'])/2))/(doc['32']['y']*info[floor_id]['19'][doc['19']]['strength']))
        x5 = (50/3)/((doc['31']['x'] * doc['31']['y'] * checkox_av(floor_id, doc, '24', 'strength') + (doc['29']['x'] + doc['29']['y'])*2*((checkox_av(floor_id, doc, '26', 'strength') + info[floor_id]['15'][doc['15']]['strength'])/2) + (doc['29']['x'] * doc['29']['y'])*info[floor_id]['16'][doc['16']]['strength'] + (doc['28']['x'] + doc['28']['y'])*2*((checkox_av(floor_id, doc, '25', 'strength') + info[floor_id]['13'][doc['13']]['strength'])/2) + (doc['28']['x']*doc['28']['y'])*info[floor_id]['14'][doc['14']]['strength'] + (doc['30']['x'] + doc['30']['y'])*2*((checkox_av(floor_id, doc, '27', 'strength') + 1)/2))/(info[floor_id]['22'][doc['22']]['strength']*doc['34']['x']))
        x6 = (50/3)/((doc['31']['x'] * doc['31']['y'] * checkox_av(floor_id, doc, '24', 'strength') + (doc['29']['x'] + doc['29']['y'])*2*((checkox_av(floor_id, doc, '26', 'strength') + info[floor_id]['15'][doc['15']]['strength'])/2) + (doc['29']['x'] * doc['29']['y'])*info[floor_id]['16'][doc['16']]['strength'] + (doc['28']['x'] + doc['28']['y'])*2*((checkox_av(floor_id, doc, '25', 'strength') + info[floor_id]['13'][doc['13']]['strength'])/2) + (doc['28']['x']*doc['28']['y'])*info[floor_id]['14'][doc['14']]['strength'] + (doc['30']['x'] + doc['30']['y'])*2*((checkox_av(floor_id, doc, '27', 'strength') + 1)/2))/(info[floor_id]['23'][doc['23']]['strength']*doc['34']['y']))
        print(min(x1, x2, x3, x4, x5, x6))
        return min(x1, x2, x3, x4, x5, x6)

    #3b   12-41 Roofcladding-28 Roofarea-37
    if floor_id == "3b":
        x1 = (50/3)/((doc['37']['x'] * doc['37']['y'] * checkox_av(floor_id, doc, '28', 'strength') + (doc['35']['x'] + doc['35']['y'])*2*((checkox_av(floor_id, doc, '31', 'strength') + info[floor_id]['17'][doc['17']]['strength'])/2))/(doc['40']['x'] * info[floor_id]['24'][doc['24']]['strength']))
        x2 = (50/3)/((doc['37']['x'] * doc['37']['y'] * checkox_av(floor_id, doc, '28', 'strength') + (doc['35']['x'] + doc['35']['y'])*2*((checkox_av(floor_id, doc, '31', 'strength') + info[floor_id]['17'][doc['17']]['strength'])/2))/(doc['40']['y'] * info[floor_id]['25'][doc['25']]['strength']))
        x3 = (50/3)/((doc['37']['x'] * doc['37']['y'] * checkox_av(floor_id, doc, '28', 'strength') + (doc['35']['x'] + doc['35']['y'])*2*((checkox_av(floor_id, doc, '31', 'strength') + info[floor_id]['17'][doc['17']]['strength'])/2) + (doc['35']['x'] * doc['35']['y'])*info[floor_id]['18'][doc['18']]['strength'] + (doc['34']['x'] + doc['34']['y'])*2*((checkox_av(floor_id, doc, '30', 'strength') + info[floor_id]['15'][doc['15']]['strength'])/2))/(doc['39']['x'] * info[floor_id]['22'][doc['22']]['strength']))
        x4 = (50/3)/((doc['37']['x'] * doc['37']['y'] * checkox_av(floor_id, doc, '28', 'strength') + (doc['35']['x'] + doc['35']['y'])*2*((checkox_av(floor_id, doc, '31', 'strength') + info[floor_id]['17'][doc['17']]['strength'])/2) + (doc['35']['x'] * doc['35']['y'])*info[floor_id]['18'][doc['18']]['strength'] + (doc['34']['x'] + doc['34']['y'])*2*((checkox_av(floor_id, doc, '30', 'strength') + info[floor_id]['15'][doc['15']]['strength'])/2))/(doc['39']['y'] * info[floor_id]['23'][doc['23']]['strength']))
        x5 = (50/3)/((doc['37']['x'] * doc['37']['y'] * checkox_av(floor_id, doc, '28', 'strength') + (doc['35']['x'] + doc['35']['y'])*2*((checkox_av(floor_id, doc, '31', 'strength') + info[floor_id]['17'][doc['17']]['strength'])/2) + (doc['35']['x'] * doc['35']['y'])*info[floor_id]['18'][doc['18']]['strength'] + (doc['34']['x'] + doc['34']['y'])*2*((checkox_av(floor_id, doc, '30', 'strength') + info[floor_id]['15'][doc['15']]['strength'])/2) + (doc['34']['x'] * doc['34']['y'])*info[floor_id]['16'][doc['16']]['strength'] + (doc['33']['x'] + doc['33']['y'])*2*((checkox_av(floor_id, doc, '29', 'strength') + info[floor_id]['13'][doc['13']]['strength'])/2))/(doc['38']['x'] * info[floor_id]['20'][doc['20']]['strength']))
        x6 = (50/3)/((doc['37']['x'] * doc['37']['y'] * checkox_av(floor_id, doc, '28', 'strength') + (doc['35']['x'] + doc['35']['y'])*2*((checkox_av(floor_id, doc, '31', 'strength') + info[floor_id]['17'][doc['17']]['strength'])/2) + (doc['35']['x'] * doc['35']['y'])*info[floor_id]['18'][doc['18']]['strength'] + (doc['34']['x'] + doc['34']['y'])*2*((checkox_av(floor_id, doc, '30', 'strength') + info[floor_id]['15'][doc['15']]['strength'])/2) + (doc['34']['x'] * doc['34']['y'])*info[floor_id]['16'][doc['16']]['strength'] + (doc['33']['x'] + doc['33']['y'])*2*((checkox_av(floor_id, doc, '29', 'strength') + info[floor_id]['13'][doc['13']]['strength'])/2))/(doc['38']['y'] * info[floor_id]['21'][doc['21']]['strength']))
        x7 = (50/3)/((doc['37']['x'] * doc['37']['y'] * checkox_av(floor_id, doc, '28', 'strength') + (doc['35']['x'] + doc['35']['y'])*2*((checkox_av(floor_id, doc, '31', 'strength') + info[floor_id]['17'][doc['17']]['strength'])/2) + (doc['35']['x'] * doc['35']['y'])*info[floor_id]['18'][doc['18']]['strength'] + (doc['34']['x'] + doc['34']['y'])*2*((checkox_av(floor_id, doc, '30', 'strength') + info[floor_id]['15'][doc['15']]['strength'])/2) + (doc['34']['x'] * doc['34']['y'])*info[floor_id]['16'][doc['16']]['strength'] + (doc['33']['x'] + doc['33']['y'])*2*((checkox_av(floor_id, doc, '29', 'strength') + info[floor_id]['13'][doc['13']]['strength'])/2) + (doc['33']['x'] * doc['33']['y'])*info[floor_id]['14'][doc['14']]['strength'] + (doc['36']['x'] + doc['36']['y'])*2*((checkox_av(floor_id, doc, '32', 'strength') + 1)/2))/(doc['41']['x']*info[floor_id]['26'][doc['26']]['strength']))
        x8 = (50/3)/((doc['37']['x'] * doc['37']['y'] * checkox_av(floor_id, doc, '28', 'strength') + (doc['35']['x'] + doc['35']['y'])*2*((checkox_av(floor_id, doc, '31', 'strength') + info[floor_id]['17'][doc['17']]['strength'])/2) + (doc['35']['x'] * doc['35']['y'])*info[floor_id]['18'][doc['18']]['strength'] + (doc['34']['x'] + doc['34']['y'])*2*((checkox_av(floor_id, doc, '30', 'strength') + info[floor_id]['15'][doc['15']]['strength'])/2) + (doc['34']['x'] * doc['34']['y'])*info[floor_id]['16'][doc['16']]['strength'] + (doc['33']['x'] + doc['33']['y'])*2*((checkox_av(floor_id, doc, '29', 'strength') + info[floor_id]['13'][doc['13']]['strength'])/2) + (doc['33']['x'] * doc['33']['y'])*info[floor_id]['14'][doc['14']]['strength'] + (doc['36']['x'] + doc['36']['y'])*2*((checkox_av(floor_id, doc, '32', 'strength') + 1)/2))/(doc['41']['y']*info[floor_id]['27'][doc['27']]['strength']))
        print(min(x1, x2, x3, x4, x5, x6, x7, x8))
        return min(x1, x2, x3, x4, x5, x6, x7, x8)
    return 'success'


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


@app.route('/admin', methods=['GET'])
def admin():
    submissions = collection.find()
    return jsonify(submissions)

def parse_json(data):
    return json.loads(json_util.dumps(data))

@app.route('/doc/<doc_id>/', methods=['GET'])
@cross_origin()
def get_doc(doc_id):
    doc = collection.find_one({"_id":ObjectId(doc_id)})
    return parse_json(doc)

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

@app.route("/get_all_docs", methods=['GET'])
def get_docs():
    all_docs = []
    docs = collection.find({})
    for doc in docs:
        submission = {
            "_id": str(doc['_id'])
        }
        all_docs.append(submission)

    return jsonify(all_docs)

if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True, port=5000)