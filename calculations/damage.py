import json

from calculations.utils import checkox_av

def damage_all(floor_id, doc):
    f = open('coefficients.json')
    info = json.load(f)
    site = max(info[floor_id]['2'][doc['2']]['damage'], info[floor_id]['3'][doc['3']]['damage'], 1, info[floor_id]['3'][doc['3']]['damage'])
    building = (info[floor_id]['5'][doc['5']]['damage'] * info[floor_id]['6'][doc['6']]['damage'] * info[floor_id]['7'][doc['7']]['damage'])
    print("site_damage: {}".format(site))
    print("building_damage: {}".format(building))

    return site*building*clad_struct_average(floor_id, doc)


def clad_struct_average(floor_id, doc): 
    f = open('coefficients.json')
    info = json.load(f)

    if floor_id == "1":
        clad_av = (checkox_av(floor_id, doc, '16', 'damage') + checkox_av(floor_id, doc, '17', 'damage') + 3)/5
        structure_av = (checkox_av(floor_id, doc, '8', 'damage') + info[floor_id]['9'][doc['9']]['damage'] + 1 + info[floor_id]['13'][doc['13']]['damage'] + info[floor_id]['14'][doc['14']]['damage'] + info[floor_id]['15'][doc['15']]['damage'] + 12)/18
        print("clad_av: {}".format(clad_av))
        print("structure_av: {}".format(structure_av))
        return clad_av*structure_av*info[floor_id]['21'][doc['21']]['damage']

    if floor_id == "2":
        clad_av = (checkox_av(floor_id, doc, '20', 'damage') + checkox_av(floor_id, doc, '21', 'damage') + checkox_av(floor_id, doc, '22', 'damage') + 2)/5
        structure_av = (checkox_av(floor_id, doc, '8', 'damage') + info[floor_id]['9'][doc['9']]['damage'] + 1 + info[floor_id]['13'][doc['13']]['damage'] + info[floor_id]['14'][doc['14']]['damage'] + info[floor_id]['16'][doc['16']]['damage'] + info[floor_id]['17'][doc['17']]['damage'] + info[floor_id]['18'][doc['18']]['damage'] + info[floor_id]['19'][doc['19']]['damage'] + 9)/18
        print("clad_av: {}".format(clad_av))
        print("structure_av: {}".format(structure_av))
        return clad_av*structure_av*structure_av*info[floor_id]['28'][doc['28']]['damage']

    if floor_id == "3":
        clad_av = (checkox_av(floor_id, doc, '24', 'damage') + checkox_av(floor_id, doc, '25', 'damage') + checkox_av(floor_id, doc, '26', 'damage') + checkox_av(floor_id, doc, '27', 'damage') + 1)/5
        structure_av = (checkox_av(floor_id, doc, '8', 'damage') + info[floor_id]['9'][doc['9']]['damage'] + 1 + info[floor_id]['13'][doc['13']]['damage'] + info[floor_id]['14'][doc['14']]['damage'] + info[floor_id]['15'][doc['15']]['damage'] + info[floor_id]['16'][doc['16']]['damage'] + info[floor_id]['17'][doc['17']]['damage'] + info[floor_id]['18'][doc['18']]['damage'] + info[floor_id]['19'][doc['19']]['damage'] + info[floor_id]['20'][doc['20']]['damage'] + info[floor_id]['21'][doc['21']]['damage'] + info[floor_id]['22'][doc['22']]['damage'] + info[floor_id]['23'][doc['23']]['damage'] + 4)/18
        print("clad_av: {}".format(clad_av))
        print("structure_av: {}".format(structure_av))
        return clad_av*structure_av*structure_av*info[floor_id]['35'][doc['35']]['damage']

    if floor_id == "1b":
        clad_av = (checkox_av(floor_id, doc, '20', 'damage') + checkox_av(floor_id, doc, '21', 'damage') + checkox_av(floor_id, doc, '22', 'damage') + 2)/5
        structure_av = (checkox_av(floor_id, doc, '8', 'damage') + info[floor_id]['9'][doc['9']]['damage'] + info[floor_id]['13'][doc['13']]['damage'] + info[floor_id]['14'][doc['14']]['damage'] + info[floor_id]['15'][doc['15']]['damage'] + info[floor_id]['16'][doc['16']]['damage'] + info[floor_id]['17'][doc['17']]['damage'] + info[floor_id]['18'][doc['18']]['damage'] + info[floor_id]['19'][doc['19']]['damage'] + 9)/18
        print("clad_av: {}".format(clad_av))
        print("structure_av: {}".format(structure_av))
        return clad_av*structure_av*structure_av*info[floor_id]['28'][doc['28']]['damage']

    if floor_id == "2b":
        clad_av = (checkox_av(floor_id, doc, '24', 'damage') + checkox_av(floor_id, doc, '25', 'damage') + checkox_av(floor_id, doc, '26', 'damage') + checkox_av(floor_id, doc, '27', 'damage') + 1)/5
        structure_av = (checkox_av(floor_id, doc, '8', 'damage') + info[floor_id]['9'][doc['9']]['damage'] + info[floor_id]['13'][doc['13']]['damage'] + info[floor_id]['14'][doc['14']]['damage'] + info[floor_id]['15'][doc['15']]['damage'] + info[floor_id]['16'][doc['16']]['damage'] + info[floor_id]['17'][doc['17']]['damage'] + info[floor_id]['18'][doc['18']]['damage'] + info[floor_id]['19'][doc['19']]['damage'] + info[floor_id]['20'][doc['20']]['damage'] + info[floor_id]['21'][doc['21']]['damage'] + info[floor_id]['22'][doc['22']]['damage'] + info[floor_id]['23'][doc['23']]['damage'] + 5)/18
        print("clad_av: {}".format(clad_av))
        print("structure_av: {}".format(structure_av))
        return clad_av*structure_av*structure_av*info[floor_id]['35'][doc['35']]['damage']

    if floor_id == "3b":
        clad_av = (checkox_av(floor_id, doc, '28', 'damage') + checkox_av(floor_id, doc, '29', 'damage') + checkox_av(floor_id, doc, '30', 'damage') + checkox_av(floor_id, doc, '31', 'damage') + checkox_av(floor_id, doc, '32', 'damage'))/5
        structure_av = (checkox_av(floor_id, doc, '8', 'damage') + info[floor_id]['9'][doc['9']]['damage'] + info[floor_id]['13'][doc['13']]['damage'] + info[floor_id]['14'][doc['14']]['damage'] + info[floor_id]['15'][doc['15']]['damage'] + info[floor_id]['16'][doc['16']]['damage'] + info[floor_id]['17'][doc['17']]['damage'] + info[floor_id]['18'][doc['18']]['damage'] + info[floor_id]['19'][doc['19']]['damage'] + info[floor_id]['20'][doc['20']]['damage'] + info[floor_id]['21'][doc['21']]['damage'] + info[floor_id]['22'][doc['22']]['damage'] + info[floor_id]['23'][doc['23']]['damage'] + info[floor_id]['24'][doc['24']]['damage'] + info[floor_id]['25'][doc['25']]['damage'] + info[floor_id]['26'][doc['26']]['damage'] + info[floor_id]['27'][doc['27']]['damage'] + 1)/18
        print("clad_av: {}".format(clad_av))
        print("structure_av: {}".format(structure_av))
        return clad_av*structure_av*structure_av*info[floor_id]['42'][doc['42']]['damage']


