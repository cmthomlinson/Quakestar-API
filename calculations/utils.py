import json

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