import pandas as pd
import sys
import json

class excel_data():
    def __init__(self):
        sum = 0
        total_list = []
        self.res = {}
        while(sum<=6):
            total_list.append(self.json_input(sum))
            sum += 1
        self.data_name = total_list[0]
        col_list = total_list[1:]

        list_tuple = self.list_compare(col_list)

        self.data_to_json(list_tuple)




    def data_to_json(self, tuple_list):
        temp_data = pd.read_excel(self.data_name, usecols=tuple_list[1])
        for i in range(len(tuple_list[1])):
            temp_list = temp_data.iloc[:, i].tolist()
            self.list_to_dic(tuple_list[0][i],temp_list)

        self.json_output("myjson.json", self.res)


    def list_to_dic(self,label,list):


        if(label == "Time"):
            time_list = []
            inti_time = (list[0].hour * 60 + list[0].minute) * 60 + list[0].second
            for t in list:
                time_list.append((t.hour * 60 + t.minute) * 60 + t.second - inti_time)
            self.res[label] = time_list

        else:
            self.res[label] = list




    def json_output(self,string, dic):
        out_file = open(string, "w")
        json.dump(dic, out_file, indent=2)
        out_file.close()

    def json_input(self, number):
        if(number == 0):
            print("Please input your excel data name(default.xlsx)")
            temp_name = input()
            return temp_name

        if(number == 1):
            print("Please input the col number of Time")

            try:
                temp_time = int(input())
            except:
                print("Error please input real number")
                sys.exit()
            return ("Time",temp_time-1)

        if(number == 2):
            print("Please input the col number of Latitude")
            try:
                temp_latitude = int(input())
            except:
                print("Error please input a number")
                sys.exit()
            return ("Latitude",temp_latitude-1)

        if(number == 3):
            print("Please input the col number of Longitude")
            try:
                temp_longitude = int(input())
            except:
                print("Error please input a number")
                sys.exit()
            return ("Longitude",temp_longitude-1)

        if(number == 4):
            print("Please input the col number of Altitude")
            try:
                temp_altitude = int(input())
            except:
                print("Error please input a number")
                sys.exit()
            return ("Altitude",temp_altitude-1)

        if(number == 5):

            try:
                temp_temp = int(input(
                    "Please input the col number of Temperature (press enter if don't have temperature data)\n") or -1)
            except:
                print("Error please input a number")
                sys.exit()
            return ("Temp",temp_temp-1)

        if(number == 6):

            try:
                temp_press = int(input("Please input the col number of Pressure (press enter if don't have temperature data)\n") or -1)

            except:
                print("Error please input a number")
                sys.exit()
            return ("Pressure",temp_press-1)

    def list_compare(self,lists):

        col_list = []
        string_list = []

        for i in range(len(lists)):
            if(lists[i][1]==-1):
                lists.remove(lists[i])
        for tuple in lists:
            col_list.append(tuple[1])
        mirror_list = col_list.copy()
        col_list.sort()

        for value in col_list:
            string_list.append(lists[mirror_list.index(value)][0])
        return (string_list,col_list)


excel_data()








