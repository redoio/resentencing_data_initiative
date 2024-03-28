# -*- coding: utf-8 -*-
from scenarios import rules
from scenarios import utils

# Adult eligibility
el_cond =  {'population': 'adult',
            'lenience': 'low',
            'offense type': 'all',
            'r_1': {'use': True, 'desc': rules.r_1, 'category': utils.dict_search(rules.cat, rules.r_1)},
            'r_2': {'use': True, 'desc': rules.r_2, 'category': utils.dict_search(rules.cat, rules.r_2)},
            'r_3': {'use': True, 'desc': rules.r_3, 'category': utils.dict_search(rules.cat, rules.r_3)},
            'r_4': {'use': True, 
                    'desc': rules.r_4, 
                    'implied ineligibility': {'all': ["/att", "(664)", "2nd"], 
                                              '459': ["/att", "(664)"]}, 
                    'perm': 2,
                    'category': utils.dict_search(rules.cat, rules.r_4)},
            'r_5': {'use': True, 
                    'desc': rules.r_5, 
                    'implied ineligibility': {'all': ["/att", "(664)", "2nd"], 
                                              '459': ["/att", "(664)"]}, 
                    'perm': 2,
                    'category': utils.dict_search(rules.cat, rules.r_5)}, 
            'r_6': {'use': False, 'desc': rules.r_6, 'category': utils.dict_search(rules.cat, rules.r_6)},
            'r_7': {'use': False, 'desc': rules.r_7, 'category': utils.dict_search(rules.cat, rules.r_7)},
            'r_8': {'use': False, 'desc': rules.r_8, 'category': utils.dict_search(rules.cat, rules.r_8)}, 
            'r_9': {'use': False, 'desc': rules.r_9, 'category': utils.dict_search(rules.cat, rules.r_9)}, 
            'r_10': {'use': False, 'desc': rules.r_10, 'category': utils.dict_search(rules.cat, rules.r_10)},
            'r_11': {'use': False, 'desc': rules.r_11, 'category': utils.dict_search(rules.cat, rules.r_11)},
            'r_12': {'use': False, 'desc': rules.r_12, 'category': utils.dict_search(rules.cat, rules.r_12)},
            'r_13': {'use': False, 'desc': rules.r_13, 'category': utils.dict_search(rules.cat, rules.r_13)}}