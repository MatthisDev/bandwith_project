from time import sleep
import speedtest
import tkinter
import datetime
import managedata

# Constante défini pour plus de simplicité de gestion :
LOOP_MAX = 1
WAITING_TIME = 1


def app_interface(server):
    texte = str(server) 
    app = tkinter.Tk()
    app.title("bandwitch project")
    app.geometry("600x400")
    lb = tkinter.Label(app, text=texte).pack()
    app.mainloop()

def get_serverlist(): 
    SPEEDTEST = speedtest.Speedtest()
    serversList = SPEEDTEST.get_servers()
    return SPEEDTEST, serversList

def get_server(serversDICT):
    countServerName = 0 # = localisation du serveur
    countServerSponsor = 0 # = nom du serveur
    distanceDICT = {}
    distance_orange_DICT = {}
    paris_avaible = False
    distance_avaible = False
    key = float(0.0)

    
    # # chaque ville contient un nombre de serveurs
    for serversList in serversDICT :
        # on accède a une ville et on cherche si c'est Paris
        for server in serversDICT[serversList]:

            # si oui on regarde s'il y a pas plusieurs serv
            if server['name'] == 'Paris':
                paris_avaible = True
                countServerName += 1
                key = float(serversList)   # on enregistre la clé du dictionnaire qui représente la ville de Paris

                # si y a 2 serv PARIS on va donc chercher un serveur ORANGE
                if countServerName > 1 :
                    # on accède a Paris pour chercher un serv ORANGE
                    for server in serversDICT[key]:

                        if server['sponsor'] == 'ORANGE FRANCE' :
                            countServerSponsor += 1
                        # si y en a plus que 2 on compare les distances
                        elif countServerSponsor > 1:
                            for server in serversDICT[key]:
                                if server['sponsor'] == 'ORANGE FRANCE' :
                                    return server['id']
                    # si y a 1 serv ORANGE on le return
                    if countServerSponsor == 1 :
                        for server in serversDICT[key]:
                            if server['sponsor'] == 'ORANGE FRANCE' :
                                return server['id']

                    # si y a 0 serv ORANGE on prend le 1er venu
                    elif countServerSponsor == 0:    
                        for server in serversDICT[key]:
                            return server['id']

            elif server['sponsor'] == 'ORANGE FRANCE':
                distance_orange_DICT[server['id']] = server['d']
                distance_avaible = False
                
        if countServerName == 1:
            return serversDICT[key][0]['id']
        
    #s'il n'y pas de serv sur Paris on regarde s'il y a des serves ORANGE
    if not paris_avaible :
        sorte = sorted(distance_orange_DICT.items(), key=lambda x: x[1])
        return sorte[0][0]

    #s'il n'y a pas de serv sur Paris ni de serve ORANGE on regarde le serve qui est le plus proche    
    if distance_avaible :
        for serversList in serversDICT :
            for server in serversDICT[serversList]:
                distanceDICT[server['id']] = server['d']
        sorte = sorted(distance_orange_DICT.items(), key=lambda x: x[1])
        return sorte[0][0]

def get_data(server, SPEEDTEST):
    SPEEDTEST.get_servers(servers= [server])

    download = SPEEDTEST.download()
    upload = SPEEDTEST.upload()
    
    return (download, upload)

def usual_checking():
    """
        * return  tuple(0, 0, (0, 0, 0, 0))
        - upload (int)
        - download (int)
        - date (tuple) {years - month - day - hour}
    """

    download_list = []
    download = 0
    upload_list = []
    upload = 0
    dates_list = 0
    time = 0

    SPEEDTEST, serversDict = get_serverlist()
    server = get_server(serversDict)
    
    # on répète l'infomation 10fois
    while LOOP_MAX > time:
        time += 1
        download, upload = get_data(server, SPEEDTEST)
        print(f"{time} : récupération data...")

        # on ajoute tout dans une liste
        download_list.append(download)
        upload_list.append(upload)

        # dernière boucle on récup info
        if LOOP_MAX == time:
            dates_list = getinfo_time()
            
            # interval de 10s
            download = set_avarage(download_list)
            upload = set_avarage(upload_list)
        sleep(WAITING_TIME)

    print(f"log : usual_check() -> download : {download} -- upload : {upload} -- dates : {dates_list}")       
    return int(download), int(upload), dates_list 

# simple calcule de moyenne
def set_avarage(list_): 
    download_avarage = 0 
    list_len = len(list_)     # longueur de la liste
    
    # add all values
    for i in list_ :
        download_avarage += i
    # do a division
    download_avarage = download_avarage // list_len
    return download_avarage

def getinfo_time(): 
    sys_time = datetime.datetime.now()

    # récupère les données sur le temps
    date = sys_time.strftime("%d")
    years = sys_time.strftime("%Y")
    month = sys_time.strftime("%m")
    month = str_modifie_month(month)
    hour = sys_time.strftime("%H")
    return (years, month, date, hour)

# return une chaine de caractère (préférable pour le stockage de donnée)
def str_modifie_month(month):
    if month == "01" : month = "january"
    elif month == "02" : month = "february"
    elif month == "03" : month = "march"
    elif month == "04" : month = "april"
    elif month == "05" : month = "may"
    elif month == "06" : month = "june"
    elif month == "07" : month = "july"
    elif month == "08" : month = "august"
    elif month == "09" : month = "september"
    elif month == "10" : month = "october"
    elif month == "11" : month = "november"
    elif month == "12" : month = "december"
    else : return 0
    return month


# le concept c'est de récupérer le fichier -> appliquer changements -> sauvegarder avec dump
# tuple(download, upload, (years, month, date, hour))
usual_data = usual_checking()
managedata.get_save_json(usual_data)