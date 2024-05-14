# -*- coding: utf-8 -*-

# Specify data connection nature
data_conn = 'aws ec2'

# File location information
if data_conn == 'google drive':
    county_name = 'Los Angeles County'
    month = '/'.join(['Rough', 'Data_05_2021', '21_05'])
    read_data_path = '/content/drive/My Drive/Redo.io/Stanford Law 3XP/Data'
    write_data_path = None
elif data_conn == 'aws ec2':
    county_name = 'los_angeles'
    month = '/'.join(['ALL LA INMATE DATA SETS-20240120T003310Z-001', 'ALL LA INMATE DATA SETS', '24_03'])
    read_data_path = "D:/Users/3xProject/Documents/Redo.io/Stanford Law 3XP/data/county"
    naming_convention = "naming_convention/file_names.txt"
    comp_path = {'adult': ["D:/Users/3xProject/Documents/Redo.io/Stanford Law 3XP/data/county/los_angeles/ALL LA INMATE DATA SETS-20240120T003310Z-001/ALL LA INMATE DATA SETS/24_03/output/date of execution/2024_5_13/adult_eligible_demographics.xlsx",
                           "D:/Users/3xProject/Documents/Redo.io/Stanford Law 3XP/data/county/los_angeles/ALL LA INMATE DATA SETS-20240120T003310Z-001/ALL LA INMATE DATA SETS/24_02/output/date of execution/2024_4_30/adult_eligible_demographics.xlsx"],
                 'juvenile': ["D:/Users/3xProject/Documents/Redo.io/Stanford Law 3XP/data/county/los_angeles/ALL LA INMATE DATA SETS-20240120T003310Z-001/ALL LA INMATE DATA SETS/24_03/output/date of execution/2024_5_13/juvenile_eligible_demographics.xlsx",
                              "D:/Users/3xProject/Documents/Redo.io/Stanford Law 3XP/data/county/los_angeles/ALL LA INMATE DATA SETS-20240120T003310Z-001/ALL LA INMATE DATA SETS/24_02/output/date of execution/2024_4_30/juvenile_eligible_demographics.xlsx"], 
                 'robbery': ["D:/Users/3xProject/Documents/Redo.io/Stanford Law 3XP/data/county/los_angeles/ALL LA INMATE DATA SETS-20240120T003310Z-001/ALL LA INMATE DATA SETS/24_03/output/date of execution/2024_5_13/robbery_eligible_demographics.xlsx",
                             "D:/Users/3xProject/Documents/Redo.io/Stanford Law 3XP/data/county/los_angeles/ALL LA INMATE DATA SETS-20240120T003310Z-001/ALL LA INMATE DATA SETS/24_02/output/date of execution/2024_4_30/robbery_eligible_demographics.xlsx"]}
    comp_info = ['2024_03 eligible cohort', '2024_02 eligible cohort']
    write_data_path = None
# Specify CDCR ID column
id_label = 'CDCNo'