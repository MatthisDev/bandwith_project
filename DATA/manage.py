import json
from turtle import down

# math functions
def set_avarage(values_list):

    sum = 0 
    len_list = len(values_list)     
    
    # add all values
    for i in values_list :
        sum += i

    # do a division
    avarage = sum // len_list
    return avarage

def calculate(list_):

    list_ = sorted(list_)
    len_ = len(list_) - 1
    
    # math values needed
    avarage = set_avarage(list_)
    math_range = 0

    if len_ > 0:
        math_range = list_[len_] - list_[0]
    else : math_range = list_[0]

    result = avarage / math_range
    result = round(result, 3)
    return result

def fetch_data(day, month):

    with open("bandwith_project/DATA/save.json", "r") as file:
        JSON_data = json.load(file)
        period = Best_Period(JSON_data)
        period.defind_best_period_day()
        best_day = Best_day(JSON_data)
        best_day.get_best_day()
        # find_day = Find_day(day, month, JSON_data) 


class Best_Period():    
    def __init__(self, JSON_data) -> None:
        # moment in the day [morning, afternoon, night] 
        self.download_period_list = {}
        self.upload_period_list = {}
        self.JSON_data = JSON_data
    
    def defind_best_period_day(self):

        self.sorted_values("morning")
        self.sorted_values("afternoon")
        self.sorted_values("night")

        self.download_period_list = sorted(self.download_period_list.items(), key=lambda x: x[1])
        self.upload_period_list = sorted(self.upload_period_list.items(), key=lambda x: x[1])

        print("log -> best_period_day DOWNLOAD : ", self.download_period_list)
        print("log -> best_period_day UPLOAD : ", self.upload_period_list)


    def get_period_data(self, moment):
        download_data_list = []
        upload_data_list = []
        for month_values in self.JSON_data.values():
            # there are data in the month
            if bool(month_values):
                for day in month_values:
                    # there are data in the day
                    if bool(day.get(moment)):
                        download_data_list.append(day[moment]["download"])
                        upload_data_list.append(day[moment]["upload"])
        
        # it is possible that there are not existing values if we have never ping at the "moment" of the day (like, we never ping the morning) 
        if not bool(download_data_list) or not bool(upload_data_list):
            print(f"log -> period_data : moment - {moment} - is empty, we need values")
            return (0, 0)
        else :
            return (download_data_list, upload_data_list)

    def sorted_values(self, moment):

        download_list, upload_list = self.get_period_data(moment)

        if (download_list and upload_list) != 0:
            # put in the general list value
            self.download_period_list[moment] = calculate(download_list)
            self.upload_period_list[moment] = calculate(upload_list)

class Best_day():

    def __init__(self, JSON_data) -> None:
        self.JSON_data = JSON_data

        # list[(download, upload)]
        self.monday_list = []
        self.tuesday_list = []
        self.wednesday_list = []
        self.thursday_list = []
        self.friday_list = []
        self.saturday_list = []
        self.sunday_list = []

        # {monday : values (M/E), }
        self.all_dowload_day_dict = {}
        self.all_upload_day_dict = {}
    
    def get_day_values(self):
        # list for any day        
        month = 0
        for month_values in self.JSON_data.values():
            day_x = 0
            month += 1

            for day in month_values:
                day_x += 1
                if bool(day):
                    download = []
                    upload = []
                    
                    if bool(day.get("morning")): 
                        download.append(day["morning"]["download"])
                        upload.append(day["morning"]["upload"])
                    if bool(day.get("afternoon")) :
                        download.append(day["afternoon"]["download"])
                        upload.append(day["afternoon"]["upload"])
                    if bool(day.get("night")) :
                        download.append(day["night"]["download"])
                        upload.append(day["night"]["upload"])
                    
                    self.storage_values(download, upload, day_x, month)

    def storage_values(self, download, upload, day, month):

        avarage_download = set_avarage(download)
        avarage_upload = set_avarage(upload)

        find_day = Find_day(day, month)
        the_day = find_day.calculate_day()

        self.put_day_list(the_day, avarage_download, avarage_upload)

    def put_day_list(self, the_day, avarage_download, avarage_upload):
        if the_day == "monday": 
            self.monday_list.append((avarage_download, avarage_upload))
        elif the_day == "tuesday":
            self.tuesday_list.append((avarage_download, avarage_upload))
        elif the_day == "wednesday" :
            self.wednesday_list.append((avarage_download, avarage_upload))
        elif the_day == "thursday" :
            self.thursday_list.append((avarage_download, avarage_upload))
        elif the_day == "friday" :
            self.friday_list.append((avarage_download, avarage_upload))
        elif the_day == "saturday" :
            self.saturday_list.append((avarage_download, avarage_upload))
        elif the_day == "sunday" :
            self.sunday_list.append((avarage_download, avarage_upload))
        else : print(f"log -> put_day_list : day {the_day} don't exist")
    
    def get_best_day(self):
        
        self.get_day_values()

        self.put_values_dict("monday")
        self.put_values_dict("tuesday")
        self.put_values_dict("wednesday")
        self.put_values_dict("thursday")
        self.put_values_dict("friday")
        self.put_values_dict("saturday")
        self.put_values_dict("sunday")
        
        self.all_dowload_day_dict = sorted(self.all_dowload_day_dict.items(), key=lambda x: x[1])
        self.all_upload_day_dict = sorted(self.all_upload_day_dict.items(), key=lambda x: x[1])

        print("log -> get_best_day DOWNLOAD : ", self.all_dowload_day_dict) 
        print("log -> get_best_day UPLOAD : ", self.all_upload_day_dict )


    def put_values_dict(self, day):
        download_day = 0
        upload_day = 0
        if day == "monday" :
            if bool(self.monday_list): 
                download_day, upload_day = self.calculate_day_values(self.monday_list)
        elif day == "tuesday" :
            if bool(self.tuesday_list): 
                download_day, upload_day = self.calculate_day_values(self.tuesday_list)
        elif day == "wednesday" :
            if bool(self.wednesday_list): 
                download_day, upload_day = self.calculate_day_values(self.wednesday_list)
        elif day == "thursday" :
            if bool(self.thursday_list): 
                download_day, upload_day = self.calculate_day_values(self.thursday_list)
        elif day == "friday" :
            if bool(self.friday_list): 
                download_day, upload_day = self.calculate_day_values(self.friday_list)
        elif day == "saturday" :
            if bool(self.saturday_list): 
                download_day, upload_day = self.calculate_day_values(self.saturday_list)
        elif day == "sunday" :
            if bool(self.sunday_list): 
                download_day, upload_day = self.calculate_day_values(self.sunday_list)
        
        self.all_dowload_day_dict[day] = download_day
        self.all_upload_day_dict[day] = upload_day

    def calculate_day_values(self, list_download_upload):
        download_list = []
        upload_list = []

        # split values
        for download, upload in list_download_upload: 
            download_list.append(download) 
            upload_list.append(upload)

        day_value_download = calculate(download_list)
        day_value_upload = calculate(upload_list)
        
        return (day_value_download, day_value_upload)

class Find_day():

    def __init__(self, day, month) -> None:
        self.year = 2022
        self.month = month # int (1, 2, 3...)
        self.first_two_later_year = str()

        # for result
        self.day = day
        self.soustraction_years = self.get_soustraction_of_years()
        self.leap_year = self.get_leap_year()
        self.month_indicator = self.get_indacator_month()
        self.century_indicator = self.get_indicator_century()

    def get_soustraction_of_years(self):
        x = 0
        century_year = str(self.year)
        # take 2 first number in a year (ex : 2024 -> 20)
        for i in century_year:
            self.first_two_later_year += i
            if x >= 1 : break
            x += 1

        century_year = int(self.first_two_later_year + '00')
        result = self.year - century_year
        return result

    def get_leap_year(self):
        leap_year = self.soustraction_years / 4
        if leap_year.is_integer():
            if self.month == "january" or self.month == "frebruary" :
                leap_year -= 1
        return leap_year
    
    def get_number_about_month(self):
        binary_check_month_list = []
        
        for month in self.data_dict.values():
            if bool(month):
                binary_check_month_list.append(1)

            elif not bool(month):
                binary_check_month_list.append(0)
        return len(binary_check_month_list) - binary_check_month_list[::-1].index(1)
    
    def get_indacator_month(self):
        if self.month == 1: return 0
        elif self.month == 2: return 3
        elif self.month == 3: return 3
        elif self.month == 4: return 6
        elif self.month == 5: return 1
        elif self.month == 8: return 2
        elif self.month == 6: return 4
        elif self.month == 7: return 6
        elif self.month == 9: return 5                
        elif self.month == 10: return 0
        elif self.month == 11: return 3
        elif self.month == 12: return 5
    
    # we could do a infinite system but we don't need it
    def get_indicator_century(self):
        if int(self.first_two_later_year) == 16: return 6
        elif int(self.first_two_later_year) == 17: return 4
        elif int(self.first_two_later_year) == 18: return 2
        elif int(self.first_two_later_year) == 19: return 0
        elif int(self.first_two_later_year) == 20: return 6
        elif int(self.first_two_later_year) == 21: return 4

    def calculate_day(self):
        result = (self.day + self.soustraction_years + self.leap_year + self.month_indicator + self.century_indicator) % 7
        result = int(result)
        return self.convert_number_day(result) 

    def convert_number_day(self, number):
        if number == 0: return "sunday"
        elif number == 1: return "monday"
        elif number == 2: return "tuesday"
        elif number == 3: return "wednesday"
        elif number == 4: return "thursday"
        elif number == 5: return "friday"
        elif number == 6: return "saturday"
        else : return print("ERROR -> result : ", number)
