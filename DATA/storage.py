import json

def get_save_json(informations = tuple):

    with open("bandwith_project/DATA/save.json", "r") as file :
        JSON_data = json.load(file)
    
    # modif/add .json 
    with open("bandwith_project/DATA/save.json", "w") as file :
        month = informations[2][1]
        day = int(informations[2][2])
        avaible = False

        # moment can be morning - afternoon - night
        moment_of_day = set_day_moment(int(informations[2][3]))

        # analyse le fichier 
        JSON_data = check_days_month(month, day, JSON_data)
        JSON_data, avaible = check_day(month, day, moment_of_day, JSON_data)

        if avaible :
            JSON_data = put_data(JSON_data, informations, moment_of_day, day, month)

        json.dump(JSON_data, file)

def check_days_month(month, day, JSON_data):

    # we add day in the month if there is some missing 
    if len(JSON_data[month]) == 0 and day > 1:
        for i in range(0, day) :
            JSON_data[month].append({})
        print(f"log -> checking_month() : on ajoute {day} jours")  
    # if it is a new day we add a new day (dict)
    elif len(JSON_data[month]) == (day - 1):
        JSON_data[month].append({})
        print("log -> check_day_month() : add 1 day")
    else : 
        print("log -> check_day_month() : right number of days")
    return JSON_data

def check_day(month, day, moment_of_day, JSON_data):
    avaible = True
    day_keys = list(JSON_data[month][day - 1])
    len_keys = len(day_keys)

    # if there is values in the day
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
                print("log -> check_day() : ping have already been done or it is not the good moment of the day")
                avaible = False


    # else it's the first ping of the day
    elif len_keys == 0:
        if moment_of_day == "morning" :
            JSON_data[month][day - 1 ]["morning"] = {}
        # first ping is the afternoon
        elif moment_of_day == "afternoon" :
            JSON_data[month][day - 1]["morning"] = {}
            JSON_data[month][day - 1]["afternoon"] = {}
        # first ping is the night
        elif moment_of_day == "night" :
            JSON_data[month][day - 1]["morning"] = {}
            JSON_data[month][day - 1]["afternoon"] = {}
            JSON_data[month][day - 1]["night"] = {}
    
    # else we don't need to add day with have already 3 moments
    elif len_keys == 3 :
        print("log -> check_day() : 3 ping have already been done")
        avaible = False

    return JSON_data, avaible

def set_day_moment(hour):
    # morning 0-12h59
    if 0 <= hour <= 12 : return "morning"
    # afternoon 13-18h59
    elif 13 <= hour <= 18 : return "afternoon"
    # night 19-23h59
    else : return "night"

def put_data(JSON_data, informations, moment_of_day, day, month) :
    JSON_data[month][day - 1][moment_of_day]["download"] = informations[0]
    JSON_data[month][day - 1][moment_of_day]["upload"] = informations[1]
    return JSON_data