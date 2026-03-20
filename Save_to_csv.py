# Save data to csv Format 

import csv
import os

class csv_string:
    @staticmethod
    def validate(data):

        if not isinstance(data,list):
            return False

        if not len(data) > 0:
            return False

        valid_data = all(
            isinstance(row, list) and
            len(row) > 0 and
            all(isinstance(value, str) for value in row)
            for row in data
        )
        return valid_data

    @staticmethod
    def save(data,file_name="New_data_file.csv",update = False):
        
        valid = csv_string.validate(data)

        if valid is False or not isinstance(file_name,str):
            raise ValueError ("_Wrong formated data is not valid _Check you data format and try again")

        action = "w"
        if not file_name.endswith(".csv"):
            file_name = f"{file_name}.csv"
        if os.path.exists(file_name):
            if update is False:
                file_name = f"New_{file_name}"
            else:
                action = "a"
        
        with open(file_name,action,encoding="utf-8",newline="")as f :
            writer = csv.writer(f)
            writer.writerows(data)
        
        return f"_{file_name} successfuly saved!"

class csv_dict:
    
    @staticmethod
    def validate(data):

        if not isinstance(data,list):
            return False

        if not len(data) > 0:
            return False 

        valid_data = all(
            isinstance(d , dict) for d in data
        )
        return valid_data

    @staticmethod
    def save(data,file_name="New_data_file.csv",update=False):

        valid = csv_dict.validate(data)

        if valid is False or not isinstance(file_name,str):
            raise ValueError ("_Wrong formated data is not valid _Check you data format and try again")

        action = "w"

        if not file_name.endswith(".csv"):
            file_name = f"{file_name}.csv"

        file_exists = os.path.exists(file_name)

        if file_exists :

            if update is False:
                file_name = f"New_{file_name}"
            else:
                action = "a"

        fieldnames = data[0].keys()

        if not all(fieldnames == d.keys() for d in data):
            raise ValueError ("_Dictioray kyes is not formated same please check data agian")   
         
        with open(file_name,action,encoding="utf-8",newline="")as f:

            writer = csv.DictWriter(f,fieldnames=fieldnames)
            if action == "w":
                writer.writeheader()
            writer.writerows(data)
            return f"_{file_name} Successfuly saved!"
