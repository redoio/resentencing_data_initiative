# -*- coding: utf-8 -*-

# Specify data connection nature
data_conn = 'aws ec2'

# File location information
if data_conn == 'google drive':
    county_name = 'Los Angeles'
    month = '/'.join(['Rough', 'Data_05_2021', '21_05'])
    read_data_path = '/content/drive/My Drive/Redo.io/Stanford Law 3XP/Data'
    write_data_path = None
elif data_conn == 'aws ec2':
    county_name = 'Los Angeles'
    month = '/'.join(['ALL LA INMATE DATA SETS-20240120T003310Z-001', 'ALL LA INMATE DATA SETS', '23_12'])
    read_data_path = "D:/Users/3xProject/Documents/Redo.io/Stanford Law 3XP/Data"
    write_data_path = None

# Specify CDCR ID column
id_label = 'CDCNo'