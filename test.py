from flask import Flask, request, jsonify
import json
import pymongo
from bson import ObjectId

app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://admin:1234@cluster.c3vxx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
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
     
    structure_av = (info[floor_id]['8'][doc['8']]['damage'] + info[floor_id]['9'][doc['9']]['damage'] + info[floor_id]['13'][doc['13']]['damage'] + info[floor_id]['14'][doc['14']]['damage'] + info[floor_id]['15'][doc['15']]['damage'] + info[floor_id]['16'][doc['16']]['damage'] + info[floor_id]['17'][doc['17']]['damage'] + info[floor_id]['19'][doc['19']]['damage'] + info[floor_id]['20'][doc['20']]['damage'])/9

    x1 = (50/3)/((doc['29']['x'] * doc['29']['y'] * info[floor_id]['25'][doc['25']]['strength'] + ((doc['31']['x'] + doc['31']['y'])*2)*((info[floor_id]['17'][doc['17']]['strength'] + info[floor_id]['28'][doc['28']]['strength'])/2))/((info[floor_id]['23'][doc['23']]['strength'])*doc['35']['x']))
    x2 = (50/3)/((doc['29']['x'] * doc['29']['y'] * info[floor_id]['25'][doc['25']]['strength'] + ((doc['31']['x'] + doc['31']['y'])*2)*((info[floor_id]['17'][doc['17']]['strength'] + info[floor_id]['28'][doc['28']]['strength'])/2))/((info[floor_id]['24'][doc['24']]['strength'])*doc['35']['y']))
    x3 = (50/3)/((doc['29']['x'] * doc['29']['y'] * info[floor_id]['25'][doc['25']]['strength'] + ((doc['31']['x'] + doc['31']['y'])*2)*((info[floor_id]['17'][doc['17']]['strength'] + info[floor_id]['28'][doc['28']]['strength'])/2) + (doc['35']['x'] * doc['35']['x']) * info[floor_id]['16'][doc['16']]['strength'] + ((doc['30']['x'] + doc['30']['x'])*2)*info[floor_id]['15'][doc['15']]['strength'])/(doc['34']['x'] * info[floor_id]['21'][doc['21']]['strength']))
    x4 = (50/3)/((doc['29']['x'] * doc['29']['y'] * info[floor_id]['25'][doc['25']]['strength'] + ((doc['31']['x'] + doc['31']['y'])*2)*((info[floor_id]['17'][doc['17']]['strength'] + info[floor_id]['28'][doc['28']]['strength'])/2) + (doc['35']['x'] * doc['35']['x']) * info[floor_id]['16'][doc['16']]['strength'] + ((doc['30']['x'] + doc['30']['x'])*2)*info[floor_id]['15'][doc['15']]['strength'])/(doc['34']['y'] * info[floor_id]['22'][doc['22']]['strength']))
    x5 = (50/3)/((doc['29']['x'] * doc['29']['y'] * info[floor_id]['25'][doc['25']]['strength'] + ((doc['31']['x'] + doc['31']['y'])*2)*((info[floor_id]['17'][doc['17']]['strength'] + info[floor_id]['28'][doc['28']]['strength'])/2) + (doc['35']['x'] * doc['35']['x']) * info[floor_id]['16'][doc['16']]['strength'] + ((doc['30']['x'] + doc['30']['x'])*2)*info[floor_id]['15'][doc['15']]['strength'] + (doc['30']['x'] * doc['30']['y']) * info[floor_id]['16'][doc['16']]['strength'] + (((doc['29']['x'] + doc['29']['y'])*2) * ((info[floor_id]['13'][doc['13']]['strength'] + info[floor_id]['26'][doc['26']]['strength'])/2)))/(info[floor_id]['19'][doc['19']]['strength'] * doc['33']['x']))
    x6 = (50/3)/((doc['29']['x'] * doc['29']['y'] * info[floor_id]['25'][doc['25']]['strength'] + ((doc['31']['x'] + doc['31']['y'])*2)*((info[floor_id]['17'][doc['17']]['strength'] + info[floor_id]['28'][doc['28']]['strength'])/2) + (doc['35']['x'] * doc['35']['x']) * info[floor_id]['16'][doc['16']]['strength'] + ((doc['30']['x'] + doc['30']['x'])*2)*info[floor_id]['15'][doc['15']]['strength'] + (doc['30']['x'] * doc['30']['y']) * info[floor_id]['16'][doc['16']]['strength'] + (((doc['29']['x'] + doc['29']['y'])*2) * ((info[floor_id]['13'][doc['13']]['strength'] + info[floor_id]['26'][doc['26']]['strength'])/2)))/(info[floor_id]['20'][doc['20']]['strength'] * doc['33']['y']))

    print(x1,x2,x3,x4,x5,x6)
test("3", "613ab5b3344a468abecf9b98")


