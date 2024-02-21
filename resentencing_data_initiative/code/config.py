# -*- coding: utf-8 -*-
import rules

# File location information
county_name = 'Los Angeles'
month = '/'.join(['Rough', 'Data_05_2021', '21_05'])
read_data_path = '/content/drive/My Drive/Redo.io/Stanford Law 3XP/Data'
write_data_path = ''

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
                 'r_13': {'use': False, 
                          'desc': rules.r_13,
                          'implied ineligibility': {'all': ["/att", "(664)", "2nd"], 
                                                    '459': ["/att", "(664)"]},
                          'perm': 2}}

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
               'r_13': {'use': False, 
                        'desc': rules.r_13,
                        'implied ineligibility': {'187': ["2nd", "(664)"]}, 
                        'perm': 2}}

# Both adult and juvenile eligibility (robbery related)
el_cond_other = {'r_1': {'use': False, 'desc': rules.r_1},
                 'r_2': {'use': False, 'desc': rules.r_2},
                 'r_3': {'use': True, 'desc': rules.r_3},
                 'r_4': {'use': False, 
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
                 'r_10': {'use': True, 'desc': rules.r_10},
                 'r_11': {'use': False, 'desc': rules.r_11},
                 'r_12': {'use': True, 'desc': rules.r_12},
                 'r_13': {'use': True, 
                          'desc': rules.r_13, 
                          'implied ineligibility': {'all': ["/att", "(664)", "2nd"], 
                                                    '459': ["/att", "(664)"]},
                          'perm': 2}}