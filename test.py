from flask import Flask, request, jsonify
import json
import pymongo
from bson import ObjectId
import ssl


app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://CharlieThomlinson:Charlie01@cluster.c3vxx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
db = client.test
collection = db['Quakestar']



    


#Register and initalize
def user_construct():
    f = open('init.json')
    info = json.load(f)
    #json_data = request.json
    firstName = "David"
    lastName = "Thomlinson"
    address = "99 portland rd, Remuera, Auckland 1050"
    email = "cmthomlinson@gmail.com"
    floor_id = "1"
    user = {
        "firstName": firstName,
        "lastName": lastName,
        "address": address,
        "email": email
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

def clad_struct_average(floor_id, doc_id): 
    f = open('coefficients.json')
    info = json.load(f)
    doc = collection.find_one({"_id":ObjectId(doc_id)})

    if floor_id == "1":
        clad_av = (info[floor_id]['16'][doc['16']]['damage'] + info[floor_id]['17'][doc['17']]['damage'])/2
        structure_av = (info[floor_id]['8'][doc['8']]['damage'] + info[floor_id]['9'][doc['9']]['damage'] + info[floor_id]['13'][doc['13']]['damage'] + info[floor_id]['14'][doc['14']]['damage'] + info[floor_id]['15'][doc['15']]['damage'] + info[floor_id]['16'][doc['16']]['damage'])/6
        return clad_av*structure_av

    if floor_id == "2":
        clad_av = (info[floor_id]['20'][doc['20']]['damage'] + info[floor_id]['21'][doc['21']]['damage'] + info[floor_id]['22'][doc['22']]['damage'])/3
        structure_av = (info[floor_id]['8'][doc['8']]['damage'] + info[floor_id]['9'][doc['9']]['damage'] + info[floor_id]['13'][doc['13']]['damage'] + info[floor_id]['14'][doc['14']]['damage'] + info[floor_id]['15'][doc['15']]['damage'] + info[floor_id]['16'][doc['16']]['damage'] + info[floor_id]['17'][doc['17']]['damage'] + info[floor_id]['19'][doc['19']]['damage'] + info[floor_id]['20'][doc['20']]['damage'])/9
        return clad_av*structure_av

    if floor_id == "3":
        clad_av = (info[floor_id]['24'][doc['24']]['damage'] + info[floor_id]['25'][doc['25']]['damage'] + info[floor_id]['26'][doc['26']]['damage'] + info[floor_id]['27'][doc['27']]['damage'])/4
        structure_av = (info[floor_id]['8'][doc['8']]['damage'] + info[floor_id]['9'][doc['9']]['damage'] + info[floor_id]['13'][doc['13']]['damage'] + info[floor_id]['14'][doc['14']]['damage'] + info[floor_id]['15'][doc['15']]['damage'] + info[floor_id]['16'][doc['16']]['damage'] + info[floor_id]['17'][doc['17']]['damage'] + info[floor_id]['19'][doc['19']]['damage'] + info[floor_id]['20'][doc['20']]['damage'] + info[floor_id]['21'][doc['21']]['damage'] + info[floor_id]['22'][doc['22']]['damage'] + info[floor_id]['23'][doc['23']]['damage'] + info[floor_id]['24'][doc['24']]['damage'])/13
        return clad_av*structure_av

    if floor_id == "1b":
        clad_av = (info[floor_id]['20'][doc['20']]['damage'] + info[floor_id]['21'][doc['21']]['damage'] + info[floor_id]['22'][doc['22']]['damage'])/3
        structure_av = (info[floor_id]['8'][doc['8']]['damage'] + info[floor_id]['9'][doc['9']]['damage'] + info[floor_id]['13'][doc['13']]['damage'] + info[floor_id]['14'][doc['14']]['damage'] + info[floor_id]['15'][doc['15']]['damage'] + info[floor_id]['16'][doc['16']]['damage'] + info[floor_id]['17'][doc['17']]['damage'] + info[floor_id]['19'][doc['19']]['damage'] + info[floor_id]['20'][doc['20']]['damage'])/9
        return clad_av*structure_av

    if floor_id == "2b":
        clad_av = (info[floor_id]['24'][doc['24']]['damage'] + info[floor_id]['25'][doc['25']]['damage'] + info[floor_id]['26'][doc['26']]['damage'] + info[floor_id]['27'][doc['27']]['damage'])/4
        structure_av = (info[floor_id]['8'][doc['8']]['damage'] + info[floor_id]['9'][doc['9']]['damage'] + info[floor_id]['13'][doc['13']]['damage'] + info[floor_id]['14'][doc['14']]['damage'] + info[floor_id]['15'][doc['15']]['damage'] + info[floor_id]['16'][doc['16']]['damage'] + info[floor_id]['17'][doc['17']]['damage'] + info[floor_id]['19'][doc['19']]['damage'] + info[floor_id]['20'][doc['20']]['damage'] + info[floor_id]['21'][doc['21']]['damage'] + info[floor_id]['22'][doc['22']]['damage'] + info[floor_id]['23'][doc['23']]['damage'] + info[floor_id]['24'][doc['24']]['damage'])/13
        return clad_av*structure_av

    if floor_id == "3b":
        clad_av = (info[floor_id]['29'][doc['29']]['damage'] + info[floor_id]['30'][doc['30']]['damage'] + info[floor_id]['31'][doc['31']]['damage'] + info[floor_id]['32'][doc['32']]['damage'] + info[floor_id]['33'][doc['33']]['damage'])/4
        structure_av = (info[floor_id]['8'][doc['8']]['damage'] + info[floor_id]['9'][doc['9']]['damage'] + info[floor_id]['13'][doc['13']]['damage'] + info[floor_id]['14'][doc['14']]['damage'] + info[floor_id]['15'][doc['15']]['damage'] + info[floor_id]['16'][doc['16']]['damage'] + info[floor_id]['17'][doc['17']]['damage'] + info[floor_id]['19'][doc['19']]['damage'] + info[floor_id]['20'][doc['20']]['damage'] + info[floor_id]['21'][doc['21']]['damage'] + info[floor_id]['22'][doc['22']]['damage'] + info[floor_id]['23'][doc['23']]['damage'] + info[floor_id]['24'][doc['24']]['damage'] + info[floor_id]['25'][doc['25']]['damage'] + info[floor_id]['26'][doc['26']]['damage'] + info[floor_id]['27'][doc['27']]['damage'] + info[floor_id]['28'][doc['28']]['damage'])/17
        return clad_av*structure_av


def test(floor_id, doc_id): 
    f = open('coefficients.json')
    info = json.load(f)
    doc = collection.find_one({"_id":ObjectId(doc_id)})

    x1 = ((doc['27']['x']*info[floor_id]['17'][doc['17']]['strength'])/(doc['28']['x']*info[floor_id]['19'][doc['19']]['strength']))*1.2
    x2 = ((doc['27']['y']*info[floor_id]['18'][doc['18']]['strength'])/(doc['28']['y']*info[floor_id]['20'][doc['20']]['strength']))*1.2
    


    

   



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



def test(floor_id, doc_id):
    f = open('coefficients.json')
    info = json.load(f)
    doc = collection.find_one({"_id":ObjectId(doc_id)})

    clad_av = (checkox_av(floor_id, doc, '16', 'damage') + checkox_av(floor_id, doc, '17', 'damage') + 3)/5
    structure_av = (checkox_av(floor_id, doc, '8', 'strength') + info[floor_id]['9'][doc['9']]['damage'] + 1 + info[floor_id]['13'][doc['13']]['damage'] + info[floor_id]['14'][doc['14']]['damage'] + info[floor_id]['15'][doc['15']]['damage'] + 12)/18
    print("clad_av: {}".format(clad_av))
    print("structure_av: {}".format(structure_av))




test("1", "61983da99c84e51ac124f539")



