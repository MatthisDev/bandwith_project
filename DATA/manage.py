import sys
import json

def fetch_data():
    with open("bandwith_project/DATA/save.json", "r") as file:
        JSON_data = json.load(file)
        list_ = JSON_data
        print("list_JSON DATA : ", list_)


def set_avarage(values_list):

    sum = 0 
    len_list = len(values_list)     
    
    # add all values
    for i in values_list :
        sum += i

    # do a division
    avarage = sum // len_list
    return avarage


def fetch_upload():
    return upload_list

def fetch_download():
    return download_list


# fait la moyenne de toute les valeurs 
def weekly_value():

    return (weekly_download_list, weekly_upload_list)