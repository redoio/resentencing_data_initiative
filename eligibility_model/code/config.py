# -*- coding: utf-8 -*-

# Specify data connection nature
data_conn = 'aws ec2'

# File location information
if data_conn == 'google drive':
    county_name = 'Los Angeles County'
    month = '/'.join(['Rough', 'Data_05_2021', '21_05'])
    read_data_path = '/content/drive/My Drive/Redo.io/Stanford Law 3XP/Data'
    write_data_path = None
    pickle_input = False
    to_excel = True
    id_label = 'CDCNo'
    parallel = True
elif data_conn == 'aws ec2':
    county_name = 'los_angeles'
    month = '24_09'
    read_data_path = "D:/Users/3xProject/Documents/Redo.io/Stanford Law 3XP/data/county"
    naming_convention = "naming_convention/file_names.txt"
    comp_path = {'adult': ["D:/Users/3xProject/Documents/Redo.io/Stanford Law 3XP/data/county/los_angeles/24_03/output/date of execution/2024_7_16/adult_eligible_demographics.xlsx",
                           "D:/Users/3xProject/Documents/Redo.io/Stanford Law 3XP/data/county/los_angeles/24_02/output/date of execution/2024_4_30/adult_eligible_demographics.xlsx"],
                 'juvenile': ["D:/Users/3xProject/Documents/Redo.io/Stanford Law 3XP/data/county/los_angeles/24_03/output/date of execution/2024_7_16/juvenile_eligible_demographics.xlsx",
                              "D:/Users/3xProject/Documents/Redo.io/Stanford Law 3XP/data/county/los_angeles/24_02/output/date of execution/2024_4_30/juvenile_eligible_demographics.xlsx"], 
                 'robbery': ["D:/Users/3xProject/Documents/Redo.io/Stanford Law 3XP/data/county/los_angeles/24_03/output/date of execution/2024_7_16/robbery_eligible_demographics.xlsx",
                             "D:/Users/3xProject/Documents/Redo.io/Stanford Law 3XP/data/county/los_angeles/24_02/output/date of execution/2024_4_30/robbery_eligible_demographics.xlsx"]}
    comp_info = ['2024_03 eligible cohort', '2024_02 eligible cohort']
    write_data_path = None
    pickle_input = False
    to_excel = True
    id_label = 'CDCNo'
    parallel = False