from tabnanny import check
from time import sleep
from unittest import result
import speedtest
import tkinter
import datetime


import sys

# from DATA.storage import "objet"/"function"
import DATA.storage
import DATA.manage


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

class Server():
    def __init__(self) -> None:
        self.speedtest_ = speedtest.Speedtest()
        self.servers_dict = self.speedtest_.get_servers()
        self.avaible_paris_server = False

        # DATA SAVING = better execution 
        # {ID : DISTANCE}
        self.distance_dict = {}
        # {ID : DISTANCE}
        self.orange_servers_dict = {}
        # {ID : SPRONSOR}
        self.paris_servers_dict = {}
    
    def choose_server(self):

        self.get_informations()

        # if there is server from Paris we choose it
        if len(self.paris_servers_dict) > 0 :
            return self.check_orange_servers(True)
 
        # we check if there is any ORANGE servers    
        elif len(self.orange_servers_dict) > 0:
            return self.check_orange_servers(False)
        # we take distance comparason
        else : 
            return self.compare_distance(self.distance_dict)


    def get_informations(self):    
        for value  in self.servers_dict :
            # go inside key 1 (access to values key 1)
            for server in self.servers_dict[value] :
                
                if not self.check_paris_servers(server):
                    # capture the distance with id
                    self.distance_dict[server['id']] = server['d']

                    if server["sponsor"] == "ORANGE" :
                        # save in a dict {ID : DISTANCE, ...}
                        self.orange_servers_dict[server["id"]] = server["d"]

    def check_paris_servers(self, server):

        if server['name'] == 'Paris':
            self.paris_servers_dict[server["id"]] = server["d"]
            return True
        # There is actualy not Paris servers
        else : return False

    def check_orange_servers(self, in_Paris):
        # in Paris we return any ORANGE servers 
        if in_Paris :
            if len(self.orange_servers_dict) > 0 :
                # return firts value
                for i in self.orange_servers_dict.keys() :
                    return str(i)
            else : 
                for i in self.paris_servers_dict.keys():
                    return str(i)
        # else we return the closest to us
        else : return self.compare_distance(self.orange_servers_dict)

    def compare_distance(self, distances_dict):
        # sorte servers according to distance (<)
        if len(distances_dict) > 1 :
            servers_distance_sorted = sorted(distances_dict.items(), key=lambda x: x[1])

            # return list[(x, y), (x, y)]
            return servers_distance_sorted[0][0]
        # there is also one key
        else :
            return str(distances_dict.keys())

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
    
    Best_Server = Server()
    server = Best_Server.choose_server()
    
    # on répète l'infomation 10fois
    while LOOP_MAX > time:
        time += 1
        download, upload = get_data(server, Best_Server.speedtest_)
        print(f"{time} : récupération data...")

        # on ajoute tout dans une liste
        download_list.append(download)
        upload_list.append(upload)

        # dernière boucle on récup info
        if LOOP_MAX == time:
            dates_list = getinfo_time()
            
            # interval de 10s
            download = DATA.manage.set_avarage(download_list)
            upload = DATA.manage.set_avarage(upload_list)
        sleep(WAITING_TIME)
    
    # convertion -> données plus comprehensible
    download = bits_to_megabits(int(download))
    upload = bits_to_megabits(int(upload))

    print(f"log : usual_check() -> download : {download} -- upload : {upload} -- dates : {dates_list}")       
    return download, upload, dates_list 

# simple calcule de moyenne
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

def bits_to_megabits(bits):
    megabits = bits // 1000000
    return megabits
    

# tuple(download, upload, (years, month, date, hour))
usual_data = usual_checking()
DATA.storage.get_save_json(usual_data)
# DATA.manage.fetch_data()