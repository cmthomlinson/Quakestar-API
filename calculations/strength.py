import json

from calculations.utils import checkox_av

def stregth_all(floor_id, doc):
    f = open('coefficients.json')
    info = json.load(f)
    site = (info[floor_id]['2'][doc['2']]['strength'] + info[floor_id]['3'][doc['3']]['strength'] + 1 + info[floor_id]['4'][doc['4']]['strength']) / 4
    building_data1 = info[floor_id]['5'][doc['5']]['strength']
    building_data2 = (info[floor_id]['6'][doc['6']]['strength'] + info[floor_id]['7'][doc['7']]['strength'])/2
    appendages = (irregulaties(floor_id, doc) * (info[floor_id]['10'][doc['10']]['strength'] + info[floor_id]['11'][doc['11']]['strength'] + info[floor_id]['12'][doc['12']]['strength'])/3)**1/2
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


def floor_area_wall_bracing(floor_id, doc):
    f = open('coefficients.json')
    info = json.load(f)

    #1   12-20 Roofcladding-16 Roofarea-19
    if floor_id == "1":
        x1 = (50/3)/(((doc['19']['x'] * doc['19']['y'] * checkox_av(floor_id, doc, '16', 'strength')) + (doc['18']['x'] + doc['18']['y'])*2*((checkox_av(floor_id, doc, '17', 'strength') + 1)/2))/(info[floor_id]['14'][doc['14']]['strength']*doc['20']['x']))
        x2 = (50/3)/(((doc['19']['x'] * doc['19']['y'] * checkox_av(floor_id, doc, '16', 'strength')) + (doc['18']['x'] + doc['18']['y'])*2*((checkox_av(floor_id, doc, '17', 'strength') + 1)/2))/(info[floor_id]['15'][doc['15']]['strength']*doc['20']['y']))
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