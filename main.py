from time import sleep
import speedtest
import datetime

import sys

# from DATA.storage import "objet"/"function"
import DATA.storage
import DATA.manage

# Constante défini pour plus de simplicité de gestion :
LOOP_MAX = 1
WAITING_TIME = 1

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

    # storage informations (ORANGE - distances - Paris)    
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
        else : return self.compare_distances(self.orange_servers_dict)

    def compare_distances(self, distances_dict):
        # sorte servers according to distance (<)
        if len(distances_dict) > 1 :
            servers_distance_sorted = sorted(distances_dict.items(), key=lambda x: x[1])

            # return list[(x, y), (x, y)]
            return servers_distance_sorted[0][0]
        # there is also one key
        else :
            return str(distances_dict.keys())
    
    def choose_server(self):

        self.get_informations()
 
        # if there is a server in Paris, we choose it
        if len(self.paris_servers_dict) > 0 :
            return self.check_orange_servers(True)
 
        # else we check if there is a ORANGE servers in France   
        elif len(self.orange_servers_dict) > 0:
            return self.check_orange_servers(False)
        # we take the server with the best distance
        else : 
            return self.compare_distances(self.distance_dict)

# we take data : download and upload from the server that we have chosen
def ping_server(server, SPEEDTEST):
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
    date_list = 0
    time = 0
    
    Best_Server = Server()
    server = Best_Server.choose_server()
    
    # repaet the ping as long as we want for a more precise data
    while LOOP_MAX > time:
        time += 1
        download, upload = ping_server(server, Best_Server.speedtest_)
        print(f" log -> {time} : recovery of the data...")

        # we add the ping in a list to make the avarage
        download_list.append(download)
        upload_list.append(upload)

        # last loop we take all informations ()
        if LOOP_MAX == time:
            date_list = get_info_date()
            
            download = DATA.manage.set_avarage(download_list)
            upload = DATA.manage.set_avarage(upload_list)
        # interval of x second (default : 10s)
        sleep(WAITING_TIME)
    
    # we need to convert data
    download = bits_to_megabits(int(download))
    upload = bits_to_megabits(int(upload))

    print(f"log -> usual_check() -> download : {download} -- upload : {upload} -- dates : {date_list}")       
    return download, upload, date_list 

def get_info_date(): 
    sys_time = datetime.datetime.now()

    # récupère les données sur le temps
    date = sys_time.strftime("%d")
    years = sys_time.strftime("%Y")
    month = sys_time.strftime("%m")
    month = str_modifie_month(month)
    hour = sys_time.strftime("%H")
    return (years, month, date, hour)

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
    

usual_data = usual_checking() # => (download, upload (years, month, day, hour))
# put in the data base
DATA.storage.get_save_json(usual_data)
# work with data to have result (best day, best part of the day)
DATA.manage.fetch_data(usual_data[2][2], usual_data[2][1])
