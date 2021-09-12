from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
import pymongo
from bson import ObjectId
import datetime
from dotenv import load_dotenv, find_dotenv
import os


app = Flask(__name__)
CORS(app)
load_dotenv(find_dotenv())
app.config['CORS_HEADERS'] = 'Content-Type'

client = pymongo.MongoClient(os.getenv("mongo_url"))
db = client.test
collection = db['Quakestar']

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
        "last_updated": user['last_updated']
    }
    i = 1
    state = False
    while i < len(info[floor_id]) + 1:
        user[str(i)] = info[floor_id][str(i)]['response']
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
        "strength": 0,
        "damage": 0,
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

    collection.update_one({"_id":ObjectId(doc_id)}, {"$set": {que_id: response, "last_updated": datetime.datetime.now() }})

    return jsonify('Success')

def stregth_all(floor_id, doc_id):
    f = open('coefficients.json')
    info = json.load(f)
    doc = collection.find_one({"_id":ObjectId(doc_id)})
    iregularities = 1
    site = (info[floor_id]['2'][doc['2']]['strength'] + info[floor_id]['3'][doc['3']]['strength'] + 1 + info[floor_id]['4'][doc['4']]['strength']) / 4
    building_data1 = info[floor_id]['5'][doc['5']]['strength']
    building_data2 = (info[floor_id]['6'][doc['6']]['strength'] + info[floor_id]['7'][doc['7']]['strength'])/2
    appendages = min(irregulaties(floor_id, doc_id), min(info[floor_id]['10'][doc['10']]['strength'], info[floor_id]['11'][doc['11']]['strength'], info[floor_id]['12'][doc['12']]['strength']))
    seismic_coefficent = info[floor_id]['1'][doc['1']]
    foundations = info[floor_id]['8'][doc['8']]['strength']

    print("site: {}".format(site))
    print("building_data1: {}".format(building_data1))
    print("building_data2: {}".format(building_data2))
    print("appendages: {}".format(appendages))
    print("seismic_coefficent: {}".format(seismic_coefficent))
    print("foundations: {}".format(foundations))
    print("irre: {}".format(irregulaties(floor_id, doc_id)))

    return site*building_data1*building_data2*appendages*(0.4/seismic_coefficent)*foundations

def clad_struct_average(floor_id, doc_id): 
    f = open('coefficients.json')
    info = json.load(f)
    doc = collection.find_one({"_id":ObjectId(doc_id)})

    if floor_id == "1":
        clad_av = (info[floor_id]['16'][doc['16']]['damage'] + info[floor_id]['17'][doc['17']]['damage'])/2
        structure_av = (info[floor_id]['8'][doc['8']]['damage'] + info[floor_id]['9'][doc['9']]['damage'] + info[floor_id]['13'][doc['13']]['damage'] + info[floor_id]['14'][doc['14']]['damage'] + info[floor_id]['15'][doc['15']]['damage'] + info[floor_id]['16'][doc['16']]['damage'])/6
        print("clad_av: {}".format(clad_av))
        print("structure_av: {}".format(structure_av))
        return clad_av*structure_av

    if floor_id == "2":
        clad_av = (info[floor_id]['20'][doc['20']]['damage'] + info[floor_id]['21'][doc['21']]['damage'] + info[floor_id]['22'][doc['22']]['damage'])/3
        structure_av = (info[floor_id]['8'][doc['8']]['damage'] + info[floor_id]['9'][doc['9']]['damage'] + info[floor_id]['13'][doc['13']]['damage'] + info[floor_id]['14'][doc['14']]['damage'] + info[floor_id]['15'][doc['15']]['damage'] + info[floor_id]['17'][doc['17']]['damage'] + info[floor_id]['19'][doc['19']]['damage'] + info[floor_id]['20'][doc['20']]['damage'])/8
        print("clad_av: {}".format(clad_av))
        print("structure_av: {}".format(structure_av))
        return clad_av*structure_av

    if floor_id == "3":
        clad_av = (info[floor_id]['24'][doc['24']]['damage'] + info[floor_id]['25'][doc['25']]['damage'] + info[floor_id]['26'][doc['26']]['damage'] + info[floor_id]['27'][doc['27']]['damage'])/4
        structure_av = (info[floor_id]['8'][doc['8']]['damage'] + info[floor_id]['9'][doc['9']]['damage'] + info[floor_id]['13'][doc['13']]['damage'] + info[floor_id]['14'][doc['14']]['damage'] + info[floor_id]['15'][doc['15']]['damage'] + info[floor_id]['16'][doc['16']]['damage'] + info[floor_id]['17'][doc['17']]['damage'] + info[floor_id]['19'][doc['19']]['damage'] + info[floor_id]['20'][doc['20']]['damage'] + info[floor_id]['21'][doc['21']]['damage'] + info[floor_id]['22'][doc['22']]['damage'] + info[floor_id]['23'][doc['23']]['damage'] + info[floor_id]['24'][doc['24']]['damage'])/13
        print("clad_av: {}".format(clad_av))
        print("structure_av: {}".format(structure_av))
        return clad_av*structure_av

    if floor_id == "1b":
        clad_av = (info[floor_id]['20'][doc['20']]['damage'] + info[floor_id]['21'][doc['21']]['damage'] + info[floor_id]['22'][doc['22']]['damage'])/3
        structure_av = (info[floor_id]['8'][doc['8']]['damage'] + info[floor_id]['9'][doc['9']]['damage'] + info[floor_id]['13'][doc['13']]['damage'] + info[floor_id]['14'][doc['14']]['damage'] + info[floor_id]['15'][doc['15']]['damage'] + info[floor_id]['16'][doc['16']]['damage'] + info[floor_id]['17'][doc['17']]['damage'] + info[floor_id]['19'][doc['19']]['damage'] + info[floor_id]['20'][doc['20']]['damage'])/9
        print("clad_av: {}".format(clad_av))
        print("structure_av: {}".format(structure_av))
        return clad_av*structure_av

    if floor_id == "2b":
        clad_av = (info[floor_id]['24'][doc['24']]['damage'] + info[floor_id]['25'][doc['25']]['damage'] + info[floor_id]['26'][doc['26']]['damage'] + info[floor_id]['27'][doc['27']]['damage'])/4
        structure_av = (info[floor_id]['8'][doc['8']]['damage'] + info[floor_id]['9'][doc['9']]['damage'] + info[floor_id]['13'][doc['13']]['damage'] + info[floor_id]['14'][doc['14']]['damage'] + info[floor_id]['15'][doc['15']]['damage'] + info[floor_id]['16'][doc['16']]['damage'] + info[floor_id]['17'][doc['17']]['damage'] + info[floor_id]['19'][doc['19']]['damage'] + info[floor_id]['20'][doc['20']]['damage'] + info[floor_id]['21'][doc['21']]['damage'] + info[floor_id]['22'][doc['22']]['damage'] + info[floor_id]['23'][doc['23']]['damage'] + info[floor_id]['24'][doc['24']]['damage'])/13
        print("clad_av: {}".format(clad_av))
        print("structure_av: {}".format(structure_av))
        return clad_av*structure_av

    if floor_id == "3b":
        clad_av = (info[floor_id]['29'][doc['29']]['damage'] + info[floor_id]['30'][doc['30']]['damage'] + info[floor_id]['31'][doc['31']]['damage'] + info[floor_id]['32'][doc['32']]['damage'] + info[floor_id]['33'][doc['33']]['damage'])/4
        structure_av = (info[floor_id]['8'][doc['8']]['damage'] + info[floor_id]['9'][doc['9']]['damage'] + info[floor_id]['13'][doc['13']]['damage'] + info[floor_id]['14'][doc['14']]['damage'] + info[floor_id]['15'][doc['15']]['damage'] + info[floor_id]['17'][doc['17']]['damage'] + info[floor_id]['19'][doc['19']]['damage'] + info[floor_id]['20'][doc['20']]['damage'] + info[floor_id]['21'][doc['21']]['damage'] + info[floor_id]['22'][doc['22']]['damage'] + info[floor_id]['23'][doc['23']]['damage'] + info[floor_id]['24'][doc['24']]['damage'] + info[floor_id]['25'][doc['25']]['damage'] + info[floor_id]['26'][doc['26']]['damage'] + info[floor_id]['27'][doc['27']]['damage'] + info[floor_id]['28'][doc['28']]['damage'])/16
        print("clad_av: {}".format(clad_av))
        print("structure_av: {}".format(structure_av))
        return clad_av*structure_av

def damage_all(floor_id, doc_id):
    f = open('coefficients.json')
    info = json.load(f)
    doc = collection.find_one({"_id":ObjectId(doc_id)})
     

    site = max(info[floor_id]['2'][doc['2']]['damage'], info[floor_id]['3'][doc['3']]['damage'], 1, info[floor_id]['3'][doc['3']]['damage'])
    building = (info[floor_id]['5'][doc['5']]['damage'] * info[floor_id]['6'][doc['6']]['damage'] * info[floor_id]['7'][doc['7']]['damage'])

    return site*building*clad_struct_average(floor_id, doc_id)


def get_score(floor_id, doc_id):
    f = open('coefficients.json')
    info = json.load(f)
    doc = collection.find_one({"_id":ObjectId(doc_id)})
    score = round(stregth_all(floor_id, doc_id)*floor_area_wall_bracing(floor_id, doc_id), 0)

    return score

def get_damage(floor_id, doc_id):
    f = open('coefficients.json')
    info = json.load(f)
    doc = collection.find_one({"_id":ObjectId(doc_id)})
    score = round(stregth_all(floor_id, doc_id)*floor_area_wall_bracing(floor_id, doc_id), 0)
    damage = round((2000/score)*damage_all(floor_id, doc_id),0)

    return damage


@app.route('/sd/<floor_id>/<doc_id>', methods=['GET'])
@cross_origin()
def sd(floor_id, doc_id):
    f = open('coefficients.json')
    info = json.load(f)
    doc = collection.find_one({"_id":ObjectId(doc_id)})
    res = {
        "score": get_score(floor_id, doc_id),
        "damage": get_damage(floor_id, doc_id)
    }

    return jsonify(res)

def irregulaties(floor_id, doc_id):
    f = open('coefficients.json')
    info = json.load(f)
    doc = collection.find_one({"_id":ObjectId(doc_id)})
    if floor_id == "1":

        return 1

    #2   12-27 Roofcladding-20 Roofarea-25
    if floor_id == "2":
        x0 = 1
        x1 = ((doc['27']['x']*info[floor_id]['17'][doc['17']]['strength'])/(doc['28']['x']*info[floor_id]['19'][doc['19']]['strength']))*1.2
        x2 = ((doc['27']['y']*info[floor_id]['18'][doc['18']]['strength'])/(doc['28']['y']*info[floor_id]['20'][doc['20']]['strength']))*1.2
        return min(x0, x1, x2)

    #3   12-34 Roofcladding-24 Roofarea-31
    if floor_id == "3":
        x0 = 1
        x1 = ((info[floor_id]['21'][doc['21']]['strength']*doc['34']['x'])/(info[floor_id]['23'][doc['23']]['strength']*doc['35']['x']))*1.2
        x2 = ((info[floor_id]['22'][doc['22']]['strength']*doc['34']['y'])/(info[floor_id]['24'][doc['24']]['strength']*doc['35']['y']))*1.2
        x3 = ((info[floor_id]['19'][doc['19']]['strength']*doc['33']['x'])/(info[floor_id]['21'][doc['21']]['strength']*doc['34']['x']))*1.2
        x4 = ((info[floor_id]['20'][doc['20']]['strength']*doc['33']['y'])/(info[floor_id]['22'][doc['22']]['strength']*doc['34']['y']))*1.2
        return min(x0, x1, x2, x3, x4)
    #1b   12-27 Roofcladding-20 Roofarea-25
    if floor_id == "1b":
        x0 = 1
        x1 = ((info[floor_id]['19'][doc['19']]['strength']*doc['28']['x'])/(info[floor_id]['17'][doc['17']]['strength']*doc['27']['x']))*1.2
        x2 = ((info[floor_id]['20'][doc['20']]['strength']*doc['28']['y'])/(info[floor_id]['18'][doc['18']]['strength']*doc['27']['y']))*1.2
        return min(x0, x1, x2)

    #2b   12-34 Roofcladding-28 Roofarea-31
    if floor_id == "2b":
        x0 = 1
        x1 = ((doc['33']['x']*info[floor_id]['19'][doc['19']]['strength'])/(doc['34']['x']*info[floor_id]['21'][doc['21']]['strength']))*1.2
        x2 = ((doc['33']['y']*info[floor_id]['20'][doc['20']]['strength'])/(doc['34']['y']*info[floor_id]['22'][doc['22']]['strength']))*1.2
        x3 = ((info[floor_id]['23'][doc['23']]['strength']*doc['35']['x'])/(doc['33']['y']*info[floor_id]['20'][doc['20']]['strength']))*1.2
        x4 = ((info[floor_id]['24'][doc['24']]['strength']*doc['35']['y'])/(doc['33']['y']*info[floor_id]['20'][doc['20']]['strength']))*1.2
        return min(x0, x1, x2, x3, x4)

    #3b   12-41 Roofcladding-28 Roofarea-37
    if floor_id == "3b":
        x0 = 1
        x1 = ((info[floor_id]['23'][doc['23']]['strength']*doc['40']['x'])/(info[floor_id]['25'][doc['25']]['strength'] * doc['41']['x']))*1.2
        x2 = ((info[floor_id]['24'][doc['24']]['strength']*doc['40']['y'])/(info[floor_id]['26'][doc['26']]['strength'] * doc['41']['y']))*1.2
        x3 = ((info[floor_id]['21'][doc['21']]['strength']*doc['39']['x'])/(info[floor_id]['23'][doc['23']]['strength']*doc['40']['x']))*1.2
        x4 = ((info[floor_id]['22'][doc['22']]['strength']*doc['39']['y'])/(info[floor_id]['24'][doc['24']]['strength']*doc['40']['y']))*1.2
        x5 = ((info[floor_id]['27'][doc['27']]['strength'] * doc['42']['x'])/(info[floor_id]['21'][doc['21']]['strength']*doc['39']['x']))*1.2
        x6 = ((info[floor_id]['28'][doc['28']]['strength'] * doc['42']['y'])/(info[floor_id]['22'][doc['22']]['strength']*doc['39']['y']))*1.2
        return min(x0, x1, x2, x3, x4, x5, x6)
      

    return 'success'


def floor_area_wall_bracing(floor_id, doc_id):
    f = open('coefficients.json')
    info = json.load(f)
    doc = collection.find_one({"_id":ObjectId(doc_id)})

    #1   12-20 Roofcladding-16 Roofarea-19
    if floor_id == "1":
        x1 = (50/3)/(((doc['20']['x'] * doc['20']['y'] * info[floor_id]['17'][doc['17']]['strength']) + (doc['20']['x'] + doc['20']['y'])*2*((info[floor_id]['18'][doc['18']]['strength'] + info[floor_id]['13'][doc['13']]['strength'])/2))/(info[floor_id]['15'][doc['15']]['strength']*doc['21']['x']))
        x2 = (50/3)/(((doc['20']['x'] * doc['20']['y'] * info[floor_id]['17'][doc['17']]['strength']) + (doc['20']['x'] + doc['20']['y'])*2*((info[floor_id]['18'][doc['18']]['strength'] + info[floor_id]['13'][doc['13']]['strength'])/2))/(info[floor_id]['16'][doc['16']]['strength']*doc['21']['y']))
        print(min(x1, x2))
        return min(x1, x2)

    #2   12-27 Roofcladding-20 Roofarea-25
    if floor_id == "2":
        x1 = (50/3)/((doc['26']['x'] * doc['26']['y'] * info[floor_id]['21'][doc['21']]['strength'] + (doc['25']['x'] + doc['25']['y'])*2*((info[floor_id]['23'][doc['23']]['strength'] + info[floor_id]['15'][doc['15']]['strength'])/2))/(doc['28']['x']*info[floor_id]['19'][doc['19']]['strength']))
        x2 = (50/3)/((doc['26']['x'] * doc['26']['y'] * info[floor_id]['21'][doc['21']]['strength'] + (doc['25']['x'] + doc['25']['y'])*2*((info[floor_id]['23'][doc['23']]['strength'] + info[floor_id]['15'][doc['15']]['strength'])/2))/(doc['28']['y']*info[floor_id]['20'][doc['20']]['strength']))
        x3 = (50/3)/((doc['26']['x'] * doc['26']['y'] * info[floor_id]['21'][doc['21']]['strength'] + (doc['25']['x'] + doc['25']['y'])*2*((info[floor_id]['23'][doc['23']]['strength'] + info[floor_id]['15'][doc['15']]['strength'])/2) + (doc['25']['x'] * doc['25']['y'])*info[floor_id]['16'][doc['16']]['strength'] + (doc['24']['x'] + doc['24']['y'])*2*((info[floor_id]['22'][doc['22']]['strength'] + info[floor_id]['13'][doc['13']]['strength'])/2))/(doc['27']['x']*info[floor_id]['17'][doc['17']]['strength']))
        x4 = (50/3)/((doc['26']['x'] * doc['26']['y'] * info[floor_id]['21'][doc['21']]['strength'] + (doc['25']['x'] + doc['25']['y'])*2*((info[floor_id]['23'][doc['23']]['strength'] + info[floor_id]['15'][doc['15']]['strength'])/2) + (doc['25']['x'] * doc['25']['y'])*info[floor_id]['16'][doc['16']]['strength'] + (doc['24']['x'] + doc['24']['y'])*2*((info[floor_id]['22'][doc['22']]['strength'] + info[floor_id]['13'][doc['13']]['strength'])/2))/(doc['27']['y']*info[floor_id]['18'][doc['18']]['strength']))
        print(min(x1, x2, x3, x4))
        return min(x1, x2, x3, x4)

    #3   12-34 Roofcladding-24 Roofarea-31
    if floor_id == "3":
        x1 = (50/3)/(((doc['32']['x'] * doc['32']['y'] * info[floor_id]['25'][doc['25']]['strength'] + (doc['31']['x'] + doc['31']['y'])*2*((info[floor_id]['28'][doc['28']]['strength'] + info[floor_id]['17'][doc['17']]['strength'])/2)))/(info[floor_id]['23'][doc['23']]['strength']*doc['35']['x']))
        x2 = (50/3)/(((doc['32']['x'] * doc['32']['y'] * info[floor_id]['25'][doc['25']]['strength'] + (doc['31']['x'] + doc['31']['y'])*2*((info[floor_id]['28'][doc['28']]['strength'] + info[floor_id]['17'][doc['17']]['strength'])/2)))/(info[floor_id]['24'][doc['24']]['strength']*doc['35']['y']))
        x3 = (50/3)/(((doc['32']['x'] * doc['32']['y'] * info[floor_id]['25'][doc['25']]['strength'] + (doc['31']['x'] + doc['31']['y'])*2*((info[floor_id]['28'][doc['28']]['strength'] + info[floor_id]['17'][doc['17']]['strength'])/2) + (doc['31']['x'] * doc['31']['y'])*info[floor_id]['18'][doc['18']]['strength'] + (doc['30']['x'] + doc['30']['y'])*2*((info[floor_id]['27'][doc['27']]['strength']+info[floor_id]['15'][doc['15']]['strength'])/2))/(info[floor_id]['21'][doc['21']]['strength']*doc['34']['x'])))
        x4 = (50/3)/(((doc['32']['x'] * doc['32']['y'] * info[floor_id]['25'][doc['25']]['strength'] + (doc['31']['x'] + doc['31']['y'])*2*((info[floor_id]['28'][doc['28']]['strength'] + info[floor_id]['17'][doc['17']]['strength'])/2) + (doc['31']['x'] * doc['31']['y'])*info[floor_id]['18'][doc['18']]['strength'] + (doc['30']['x'] + doc['30']['y'])*2*((info[floor_id]['27'][doc['27']]['strength']+info[floor_id]['15'][doc['15']]['strength'])/2))/(info[floor_id]['22'][doc['22']]['strength']*doc['34']['y'])))
        x5 = (50/3)/((doc['32']['x'] * doc['32']['y'] * info[floor_id]['25'][doc['25']]['strength'] + (doc['31']['x'] + doc['31']['y'])*2*((info[floor_id]['28'][doc['28']]['strength'] + info[floor_id]['17'][doc['17']]['strength'])/2) + (doc['31']['x'] * doc['31']['y'])*info[floor_id]['18'][doc['18']]['strength'] + (doc['30']['x'] + doc['30']['y'])*2*((info[floor_id]['27'][doc['27']]['strength']+info[floor_id]['15'][doc['15']]['strength'])/2) + (doc['30']['x']*doc['30']['y'])*info[floor_id]['16'][doc['16']]['strength'] + (doc['29']['x'] + doc['29']['y'])*2*((info[floor_id]['26'][doc['26']]['strength'] + info[floor_id]['13'][doc['13']]['strength'])/2))/(info[floor_id]['19'][doc['19']]['strength']*doc['33']['x']))
        x6 = (50/3)/((doc['32']['x'] * doc['32']['y'] * info[floor_id]['25'][doc['25']]['strength'] + (doc['31']['x'] + doc['31']['y'])*2*((info[floor_id]['28'][doc['28']]['strength'] + info[floor_id]['17'][doc['17']]['strength'])/2) + (doc['31']['x'] * doc['31']['y'])*info[floor_id]['18'][doc['18']]['strength'] + (doc['30']['x'] + doc['30']['y'])*2*((info[floor_id]['27'][doc['27']]['strength']+info[floor_id]['15'][doc['15']]['strength'])/2) + (doc['30']['x']*doc['30']['y'])*info[floor_id]['16'][doc['16']]['strength'] + (doc['29']['x'] + doc['29']['y'])*2*((info[floor_id]['26'][doc['26']]['strength'] + info[floor_id]['13'][doc['13']]['strength'])/2))/(info[floor_id]['20'][doc['20']]['strength']*doc['33']['y']))
        print(min(x1, x2, x3, x4, x5, x6))
        return min(x1, x2, x3, x4, x5, x6)

    #1b   12-27 Roofcladding-20 Roofarea-25
    if floor_id == "1b":
        x1 = (50/3)/(((doc['26']['x'] * doc['26']['y'] * info[floor_id]['21'][doc['21']]['strength']) + (doc['24']['x'] + doc['24']['y'])*2*((info[floor_id]['22'][doc['22']]['strength'] + info[floor_id]['13'][doc['13']]['strength'])/2))/(info[floor_id]['17'][doc['17']]['strength']*(doc['27']['x'])))
        x2 = (50/3)/(((doc['26']['x'] * doc['26']['y'] * info[floor_id]['21'][doc['21']]['strength']) + (doc['24']['x'] + doc['24']['y'])*2*((info[floor_id]['22'][doc['22']]['strength'] + info[floor_id]['13'][doc['13']]['strength'])/2))/(info[floor_id]['18'][doc['18']]['strength']*(doc['27']['y'])))
        x3 = (50/3)/(((doc['26']['x'] * doc['26']['y'] * info[floor_id]['21'][doc['21']]['strength']) + (doc['24']['x'] + doc['24']['y'])*2*((info[floor_id]['22'][doc['22']]['strength'] + info[floor_id]['13'][doc['13']]['strength'])/2) + (doc['24']['x'] * doc['24']['y'])*info[floor_id]['14'][doc['14']]['strength'] + (doc['25']['x'] + doc['25']['y'])*2*((info[floor_id]['23'][doc['23']]['strength'] + info[floor_id]['15'][doc['15']]['strength'])/2))/(info[floor_id]['19'][doc['19']]['strength']*doc['28']['x']))
        x4 = (50/3)/(((doc['26']['x'] * doc['26']['y'] * info[floor_id]['21'][doc['21']]['strength']) + (doc['24']['x'] + doc['24']['y'])*2*((info[floor_id]['22'][doc['22']]['strength'] + info[floor_id]['13'][doc['13']]['strength'])/2) + (doc['24']['x'] * doc['24']['y'])*info[floor_id]['14'][doc['14']]['strength'] + (doc['25']['x'] + doc['25']['y'])*2*((info[floor_id]['23'][doc['23']]['strength'] + info[floor_id]['15'][doc['15']]['strength'])/2))/(info[floor_id]['20'][doc['20']]['strength']*doc['28']['y']))
        print(min(x1, x2, x3, x4))
        return min(x1, x2, x3, x4)

    #2b   12-34 Roofcladding-28 Roofarea-31
    if floor_id == "2b":
        x1 = (50/3)/((doc['32']['x'] * doc['32']['y'] * info[floor_id]['25'][doc['25']]['strength'] + (doc['30']['x'] + doc['30']['y'])*2*((info[floor_id]['27'][doc['27']]['strength'] + info[floor_id]['15'][doc['15']]['strength'])/2))/(doc['34']['x']*info[floor_id]['21'][doc['21']]['strength']))
        x2 = (50/3)/((doc['32']['x'] * doc['32']['y'] * info[floor_id]['25'][doc['25']]['strength'] + (doc['30']['x'] + doc['30']['y'])*2*((info[floor_id]['27'][doc['27']]['strength'] + info[floor_id]['15'][doc['15']]['strength'])/2))/(doc['34']['y']*info[floor_id]['22'][doc['22']]['strength']))
        x3 = (50/3)/((doc['32']['x'] * doc['32']['y'] * info[floor_id]['25'][doc['25']]['strength'] + (doc['30']['x'] + doc['30']['y'])*2*((info[floor_id]['27'][doc['27']]['strength'] + info[floor_id]['15'][doc['15']]['strength'])/2) + (doc['30']['x'] * doc['30']['y'])*info[floor_id]['16'][doc['16']]['strength'] + (doc['29']['x'] + doc['29']['y'])*2*((info[floor_id]['26'][doc['26']]['strength'] + info[floor_id]['13'][doc['13']]['strength'])/2))/(doc['33']['x']*info[floor_id]['19'][doc['19']]['strength']))
        x4 = (50/3)/((doc['32']['x'] * doc['32']['y'] * info[floor_id]['25'][doc['25']]['strength'] + (doc['30']['x'] + doc['30']['y'])*2*((info[floor_id]['27'][doc['27']]['strength'] + info[floor_id]['15'][doc['15']]['strength'])/2) + (doc['30']['x'] * doc['30']['y'])*info[floor_id]['16'][doc['16']]['strength'] + (doc['29']['x'] + doc['29']['y'])*2*((info[floor_id]['26'][doc['26']]['strength'] + info[floor_id]['13'][doc['13']]['strength'])/2))/(doc['33']['y']*info[floor_id]['20'][doc['20']]['strength']))
        x5 = (50/3)/((doc['32']['x'] * doc['32']['y'] * info[floor_id]['25'][doc['25']]['strength'] + (doc['30']['x'] + doc['30']['y'])*2*((info[floor_id]['27'][doc['27']]['strength'] + info[floor_id]['15'][doc['15']]['strength'])/2) + (doc['30']['x'] * doc['30']['y'])*info[floor_id]['16'][doc['16']]['strength'] + (doc['29']['x'] + doc['29']['y'])*2*((info[floor_id]['26'][doc['26']]['strength'] + info[floor_id]['13'][doc['13']]['strength'])/2) + (doc['29']['x']*doc['29']['y'])*info[floor_id]['14'][doc['14']]['strength'] + (doc['31']['x'] + doc['31']['y'])*2*((info[floor_id]['28'][doc['28']]['strength'] + info[floor_id]['17'][doc['17']]['strength'])/2))/(info[floor_id]['23'][doc['23']]['strength']*doc['35']['x']))
        x6 = (50/3)/((doc['32']['x'] * doc['32']['y'] * info[floor_id]['25'][doc['25']]['strength'] + (doc['30']['x'] + doc['30']['y'])*2*((info[floor_id]['27'][doc['27']]['strength'] + info[floor_id]['15'][doc['15']]['strength'])/2) + (doc['30']['x'] * doc['30']['y'])*info[floor_id]['16'][doc['16']]['strength'] + (doc['29']['x'] + doc['29']['y'])*2*((info[floor_id]['26'][doc['26']]['strength'] + info[floor_id]['13'][doc['13']]['strength'])/2) + (doc['29']['x']*doc['29']['y'])*info[floor_id]['14'][doc['14']]['strength'] + (doc['31']['x'] + doc['31']['y'])*2*((info[floor_id]['28'][doc['28']]['strength'] + info[floor_id]['17'][doc['17']]['strength'])/2))/(info[floor_id]['24'][doc['24']]['strength']*doc['35']['y']))
        print(min(x1, x2, x3, x4, x5, x6))
        return min(x1, x2, x3, x4, x5, x6)

    #3b   12-41 Roofcladding-28 Roofarea-37
    if floor_id == "3b":
        x1 = (50/3)/((doc['38']['x'] * doc['38']['y'] * info[floor_id]['29'][doc['29']]['strength'] + ((doc['36']['x'] + doc['36']['y'])*2)*((info[floor_id]['32'][doc['32']]['strength'] + info[floor_id]['17'][doc['17']]['strength'])/2))/(info[floor_id]['25'][doc['25']]['strength'] * doc['41']['x']))
        x2 = (50/3)/((doc['38']['x'] * doc['38']['y'] * info[floor_id]['29'][doc['29']]['strength'] + ((doc['36']['x'] + doc['36']['y'])*2)*((info[floor_id]['32'][doc['32']]['strength'] + info[floor_id]['17'][doc['17']]['strength'])/2))/(info[floor_id]['26'][doc['26']]['strength'] * doc['41']['y']))
        x3 = (50/3)/((doc['38']['x'] * doc['38']['y'] * info[floor_id]['29'][doc['29']]['strength'] + ((doc['36']['x'] + doc['36']['y'])*2)*((info[floor_id]['32'][doc['32']]['strength'] + info[floor_id]['17'][doc['17']]['strength'])/2) + (doc['36']['x'] * doc['36']['y'])*info[floor_id]['18'][doc['18']]['strength'] + ((doc['36']['x'] + doc['36']['y'])*2)*((info[floor_id]['31'][doc['31']]['strength'] + info[floor_id]['15'][doc['15']]['strength'])/2))/(info[floor_id]['23'][doc['23']]['strength']*doc['40']['x']))
        x4 = (50/3)/((doc['38']['x'] * doc['38']['y'] * info[floor_id]['29'][doc['29']]['strength'] + ((doc['36']['x'] + doc['36']['y'])*2)*((info[floor_id]['32'][doc['32']]['strength'] + info[floor_id]['17'][doc['17']]['strength'])/2) + (doc['36']['x'] * doc['36']['y'])*info[floor_id]['18'][doc['18']]['strength'] + ((doc['36']['x'] + doc['36']['y'])*2)*((info[floor_id]['31'][doc['31']]['strength'] + info[floor_id]['15'][doc['15']]['strength'])/2))/(info[floor_id]['24'][doc['24']]['strength']*doc['40']['y']))
        x5 = (50/3)/((doc['38']['x'] * doc['38']['y'] * info[floor_id]['29'][doc['29']]['strength'] + ((doc['36']['x'] + doc['36']['y'])*2)*((info[floor_id]['32'][doc['32']]['strength'] + info[floor_id]['17'][doc['17']]['strength'])/2) + (doc['36']['x'] * doc['36']['y'])*info[floor_id]['18'][doc['18']]['strength'] + ((doc['36']['x'] + doc['36']['y'])*2)*((info[floor_id]['31'][doc['31']]['strength'] + info[floor_id]['15'][doc['15']]['strength'])/2) + (doc['36']['x'] * doc['36']['y'])*info[floor_id]['17'][doc['17']]['strength'] + (((doc['34']['x'] + doc['34']['y'])*2)*(info[floor_id]['30'][doc['30']]['strength'] + info[floor_id]['13'][doc['13']]['strength'])/2))/(info[floor_id]['21'][doc['21']]['strength']*doc['39']['x']))
        x6 = (50/3)/((doc['38']['x'] * doc['38']['y'] * info[floor_id]['29'][doc['29']]['strength'] + ((doc['36']['x'] + doc['36']['y'])*2)*((info[floor_id]['32'][doc['32']]['strength'] + info[floor_id]['17'][doc['17']]['strength'])/2) + (doc['36']['x'] * doc['36']['y'])*info[floor_id]['18'][doc['18']]['strength'] + ((doc['36']['x'] + doc['36']['y'])*2)*((info[floor_id]['31'][doc['31']]['strength'] + info[floor_id]['15'][doc['15']]['strength'])/2) + (doc['36']['x'] * doc['36']['y'])*info[floor_id]['17'][doc['17']]['strength'] + (((doc['34']['x'] + doc['34']['y'])*2)*(info[floor_id]['30'][doc['30']]['strength'] + info[floor_id]['13'][doc['13']]['strength'])/2))/(info[floor_id]['22'][doc['22']]['strength']*doc['39']['y']))
        x7 = (50/3)/((doc['38']['x'] * doc['38']['y'] * info[floor_id]['29'][doc['29']]['strength'] + ((doc['36']['x'] + doc['36']['y'])*2)*((info[floor_id]['32'][doc['32']]['strength'] + info[floor_id]['17'][doc['17']]['strength'])/2) + (doc['36']['x'] * doc['36']['y'])*info[floor_id]['18'][doc['18']]['strength'] + ((doc['36']['x'] + doc['36']['y'])*2)*((info[floor_id]['31'][doc['31']]['strength'] + info[floor_id]['15'][doc['15']]['strength'])/2) + (doc['36']['x'] * doc['36']['y'])*info[floor_id]['17'][doc['17']]['strength'] + (((doc['34']['x'] + doc['34']['y'])*2)*(info[floor_id]['30'][doc['30']]['strength'] + info[floor_id]['13'][doc['13']]['strength'])/2) + (doc['34']['x'] * doc['34']['y'])*info[floor_id]['14'][doc['14']]['strength'] + ((doc['37']['x'] + doc['37']['y'])*2)*((info[floor_id]['33'][doc['33']]['strength'] + info[floor_id]['19'][doc['19']]['strength'])/2))/(info[floor_id]['27'][doc['27']]['strength'] * doc['42']['x']))
        x8 = (50/3)/((doc['38']['x'] * doc['38']['y'] * info[floor_id]['29'][doc['29']]['strength'] + ((doc['36']['x'] + doc['36']['y'])*2)*((info[floor_id]['32'][doc['31']]['strength'] + info[floor_id]['17'][doc['17']]['strength'])/2) + (doc['36']['x'] * doc['36']['y'])*info[floor_id]['18'][doc['18']]['strength'] + ((doc['36']['x'] + doc['36']['y'])*2)*((info[floor_id]['31'][doc['31']]['strength'] + info[floor_id]['15'][doc['15']]['strength'])/2) + (doc['36']['x'] * doc['36']['y'])*info[floor_id]['17'][doc['17']]['strength'] + (((doc['34']['x'] + doc['34']['y'])*2)*(info[floor_id]['30'][doc['30']]['strength'] + info[floor_id]['13'][doc['13']]['strength'])/2) + (doc['34']['x'] * doc['34']['y'])*info[floor_id]['14'][doc['14']]['strength'] + ((doc['37']['x'] + doc['37']['y'])*2)*((info[floor_id]['33'][doc['33']]['strength'] + info[floor_id]['19'][doc['19']]['strength'])/2))/(info[floor_id]['28'][doc['28']]['strength'] * doc['42']['y']))
        print(min(x1, x2, x3, x4, x5, x6, x7, x8))
        return min(x1, x2, x3, x4, x5, x6, x7, x8)
    return 'success'


@app.route('/results/<floor_id>/<doc_id>', methods=['GET'])
@cross_origin()
def results(floor_id, doc_id):
    doc = collection.find_one({"_id":ObjectId(doc_id)})
    res = {
        "firstName": doc['firstName'],
        "lastName": doc['lastName'],
        "address": doc['address'],
        "last_updated": doc['last_updated'],
        "score": get_score(floor_id, doc_id),
        "damage": get_damage(floor_id, doc_id)
    }
    return jsonify(res)

@app.route('/admin', methods=['GET'])
def admin():
    submissions = collection.find()
    return jsonify(submissions)



@app.route('/doc/<doc_id>/<que_id>', methods=['GET'])
@cross_origin()
def get_doc(doc_id, que_id):
    doc = collection.find_one({"_id":ObjectId(doc_id)})
    return jsonify(doc[que_id])

#Admin routes
#Get all completed docs 


if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True, port=5000)