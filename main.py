import speedtest
import json

def chose_server(serversDICT):
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

def get_data():
    SPEEDTEST = speedtest.Speedtest()

    serversList = SPEEDTEST.get_servers()
    # print("servers_list : ", serversList)

    server = chose_server(serversList)
    print(server)
    
    #SPEEDTEST.get_servers(servers = [29542])
    #download = SPEEDTEST.download()
    #upload = SPEEDTEST.upload()
    # print(download)
    # print("type(r) : ", type(serversList))
    # connection_data = subprocess.run('speedtest-cli --json', shell=True, capture_output= True)

get_data()
