import json

from calculations.utils import checkox_av

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


