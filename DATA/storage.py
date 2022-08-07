import json

def get_save_json(informations = tuple):

    with open("bandwith_project/DATA/save.json", "r") as file :
        JSON_data = json.load(file)
    
    # modif/add .json 
    with open("bandwith_project/DATA/save.json", "w") as file :
        month = informations[2][1]
        day = int(informations[2][2])
        avaible = False

        # def un moment de la journée (matin - aprem - soir)
        moment_of_day = set_day_moment(int(informations[2][3]))

        # analyse le fichier 
        JSON_data = checking_days_in_month(month, day, JSON_data)
        JSON_data, avaible = checking_day(month, day, moment_of_day, JSON_data)

        if avaible :
            JSON_data = put_data(JSON_data, informations, moment_of_day, day, month)

        json.dump(JSON_data, file)

def checking_days_in_month(month, day, JSON_data):

    # on ajoute des dictionnaires aux jours qui n'en ont pas eu 
    if len(JSON_data[month]) == 0 and day > 1:
        for i in range(0, day) :
            JSON_data[month].append({})
        print(f"log -> checking_month() : on ajoute {day} jours")
            
    # si nouvelle journée alors add dico
    elif len(JSON_data[month]) == (day - 1):
        JSON_data[month].append({})
        print("log -> checking_month() : on ajoute 1 jour")
    else : 
        print("log -> checking_month() : bon nombre de jours")

    return JSON_data

def checking_day(month, day, moment_of_day, JSON_data):
    avaible = True
    day_keys = list(JSON_data[month][day - 1])
    len_keys = len(day_keys)

    # s'il y a des valeurs dans la tableau
    if 0 < len_keys < 3 :

        if day_keys[len_keys-1] == "morning" and moment_of_day == "afternoon":
            JSON_data[month][day - 1]["afternoon"] = {}

        elif day_keys[len_keys-1] == "afternoon" and moment_of_day == "night":
            JSON_data[month][day - 1]["night"] = {}

        else :
            if len_keys == 1 and day_keys[0] == "morning" and moment_of_day == "night" :
                JSON_data[month][day - 1]["afternoon"] = {}
                JSON_data[month][day - 1]["night"] = {}

            else : 
                print("log -> checking_day() : le ping est déjà fait ou c'est le mauvais moment de la journée")
                avaible = False


    # sinon ca veut dire que c'est le 1er PING
    elif len_keys == 0 and moment_of_day == "morning":
        JSON_data[month][day - 1 ]["morning"] = {}

    # cas spécifique (anti bug)
    elif len_keys == 0 and moment_of_day == "afternoon" or moment_of_day == "night" :
        if moment_of_day == "afternoon" :
            JSON_data[month][day - 1]["morning"] = {}
            JSON_data[month][day - 1]["afternoon"] = {}

        elif moment_of_day == "night" :
            JSON_data[month][day - 1]["morning"] = {}
            JSON_data[month][day - 1]["afternoon"] = {}
            JSON_data[month][day - 1]["night"] = {}
    
    # sinon ca veut dire c'est le 4ème (c'est trop !)
    elif len_keys == 3 :
        print("log -> checking_day() : 3 ping ont déjà été fait")
        avaible = False

    return JSON_data, avaible

def set_day_moment(hour):
    # matin 4h-11h
    if 0 <= hour <= 12 : return "morning"
    # après midi 11h-19h
    elif 13 <= hour <= 18 : return "afternoon"
    # sinon nuit
    else : return "night"

def put_data(JSON_data, informations, moment_of_day, day, month) :
    JSON_data[month][day - 1][moment_of_day]["download"] = informations[0]
    JSON_data[month][day - 1][moment_of_day]["upload"] = informations[1]
    return JSON_data