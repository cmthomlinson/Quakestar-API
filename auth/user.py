import json
from werkzeug.security import check_password_hash, generate_password_hash

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
    
