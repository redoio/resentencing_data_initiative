# -*- coding: utf-8 -*-
import rules

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

# Adult eligibility
el_cond_adult = {'r_1': {'use': True, 'desc': rules.r_1},
                 'r_2': {'use': True, 'desc': rules.r_2},
                 'r_3': {'use': True, 'desc': rules.r_3},
                 'r_4': {'use': True, 
                         'desc': rules.r_4, 
                         'implied ineligibility': {'all': ["/att", "(664)", "2nd"], 
                                                   '459': ["/att", "(664)"]}, 
                         'perm': 2},
                 'r_5': {'use': True, 
                         'desc': rules.r_5, 
                         'implied ineligibility': {'all': ["/att", "(664)", "2nd"], 
                                                   '459': ["/att", "(664)"]}, 
                         'perm': 2}, 
                 'r_6': {'use': False, 'desc': rules.r_6},
                 'r_7': {'use': False, 'desc': rules.r_7},
                 'r_8': {'use': False, 'desc': rules.r_8}, 
                 'r_9': {'use': False, 'desc': rules.r_9}, 
                 'r_10': {'use': False, 'desc': rules.r_10},
                 'r_11': {'use': False, 'desc': rules.r_11},
                 'r_12': {'use': False, 'desc': rules.r_12},
                 'r_13': {'use': False, 'desc': rules.r_13}}

# Juvenile eligibility
el_cond_juv = {'r_1': {'use': False, 'desc': rules.r_1},
               'r_2': {'use': False, 'desc': rules.r_2},
               'r_3': {'use': True, 'desc': rules.r_3},
               'r_4': {'use': False, 'desc': rules.r_4}, 
               'r_5': {'use': False, 'desc': rules.r_5},
               'r_6': {'use': True, 'desc': rules.r_6},
               'r_7': {'use': True, 
                       'desc': rules.r_7, 
                       'implied ineligibility': {'187': ["2nd", "(664)"]}, 
                       'perm': 2},
               'r_8': {'use': True, 
                       'desc': rules.r_8,
                       'implied ineligibility': {'187': ["2nd", "(664)"]}, 
                       'perm': 2}, 
               'r_9': {'use': False, 'desc': rules.r_9}, 
               'r_10': {'use': False, 'desc': rules.r_10},
               'r_11': {'use': False, 'desc': rules.r_11},
               'r_12': {'use': False, 'desc': rules.r_12},
               'r_13': {'use': False, 'desc': rules.r_13}}

# Both adult and juvenile eligibility (robbery related)
el_cond_rob = {'r_1': {'use': False, 'desc': rules.r_1},
                 'r_2': {'use': False, 'desc': rules.r_2},
                 'r_3': {'use': False, 'desc': rules.r_3},
                 'r_4': {'use': False, 'desc': rules.r_4},
                 'r_5': {'use': True, 
                         'desc': rules.r_5, 
                         'implied ineligibility': {'all': ["/att", "(664)", "2nd"], 
                                                   '459': ["/att", "(664)"]}, 
                         'perm': 3}, 
                 'r_6': {'use': False, 'desc': rules.r_6},
                 'r_7': {'use': False, 'desc': rules.r_7},
                 'r_8': {'use': False, 'desc': rules.r_8}, 
                 'r_9': {'use': False, 'desc': rules.r_9}, 
                 'r_10': {'use': True, 
                          'desc': rules.r_10,
                          'perm': 4,
                          'implied ineligibility': {'all': ['/att', '(664)', '2nd', "(ss)"]},
                          'fix positions': {"2nd": 0, "(ss)": 0}, 
                          'placeholder': {"ss": ['a', 'b', 'c']}}, 
                 'r_11': {'use': True, 'desc': rules.r_11},
                 'r_12': {'use': True, 
                          'desc': rules.r_12, 
                          'implied ineligibility': {'all': ["/att", "(664)", "2nd"], 
                                                    '459': ["/att", "(664)"]},
                          'perm': 3},
                 'r_13': {'use': True, 'desc': rules.r_13}}