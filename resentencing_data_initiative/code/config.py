# -*- coding: utf-8 -*-
import rules

county_name = 'Los Angeles'
month = '/'.join(['Rough', 'Data_05_2021', '21_05'])
read_data_path = '/content/drive/My Drive/Stanford Law 3XP/Data'
write_data_path = ''

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
                 'r_9': {'use': False, 'desc': rules.r_9}}

el_cond_juv = {'r_1': {'use': False, 'desc': rules.r_1},
               'r_2': {'use': False, 'desc': rules.r_2},
               'r_3': {'use': False, 'desc': rules.r_3},
               'r_4': {'use': False, 'desc': rules.r_4},
               'r_5': {'use': False, 'desc': rules.r_5},
               'r_6': {'use': True, 'desc': rules.r_6},
               'r_7': {'use': True, 
                       'desc': rules.r_7, 
                       'implied ineligibility': {'187': ["2nd", "(664)"]}, 
                       'perm': 2},
               'r_8': {'use': True, 'desc': rules.r_8},
               'r_9': {'use': True, 
                       'desc': rules.r_9,
                       'implied ineligibility': {'187': ["2nd", "(664)"]}, 
                       'perm': 2}}