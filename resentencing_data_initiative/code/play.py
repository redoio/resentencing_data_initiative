# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 20:39:47 2024

@author: apkom
"""
from itertools import permutations, product
import pandas as pd
import copy
from helpers import *

criteria = pd.read_excel('C:/Users/akomarla/Downloads/sorting_criteria.xlsx', dtype = {'Offenses': str})
#current_commits = pd.read_excel('C:/Users/apkom/Downloads/currentcommitments.xlsx')
#demographics = pd.read_excel('C:/Users/apkom/Downloads/demographics.xlsx')

impl_rel = {'all': ['/att', '(664)', '2nd', "(ss)"], '459': ['/att', '(664)']}
offenses = clean_offense_blk(criteria[criteria['Table'] == 'Table F']['Offenses'].to_list())


def gen_impl_off(offenses, 
                 impl_rel, 
                 perm = 3,
                 sep = '', 
                 fix_pos = {"2nd": 0, "(ss)": 0}, 
                 placeholder = {"ss": ['a', 'b', 'c']}, 
                 how = 'inclusive'):
    
    # Remove exceptions from the list of offenses
    offenses_woe = copy.deepcopy(offenses)
    for e in impl_rel.keys():
        if (e != 'all') and (e in offenses):
            offenses_woe.remove(e)
    
    if how == 'inclusive':
        # Initialize list of implied offenses - add the baseline offenses
        impl_off = offenses[:]
    else:
        impl_off = []
        
    # Add the implied offenses
    for rel in impl_rel.keys():
        # Generate list of implied values
        impl_val = gen_impl_val(impl = impl_rel[rel],  
                                sep = sep, 
                                perm = perm,
                                fix_pos = fix_pos, 
                                placeholder = placeholder)
        
        # If offense is NOT an exception
        if rel == 'all':
            # Adding implications to all offenses that do NOT have an exception
            for owe in offenses_woe:
                for iv in impl_val:
                    impl_off.append(owe+iv)
        
        # If offense is an exception
        elif (rel != 'all') and (rel in offenses):
            # Adding implications to the exception offense (always called out individually)
            for iv in impl_val:
                impl_off.append(rel+iv)
    
    return list(set(impl_off))
            
            
    
def gen_impl_val(impl,  
                 sep = '', 
                 perm = 3, 
                 fix_pos = {"2nd": 0, "(ss)": 0}, 
                 placeholder = {"ss": ['a', 'b', 'c']}):
    
    # Initialize list of permutations of implied values
    res = []
    for i in range(1, perm+1):
        # Add permutations for each count
        res.extend(list(permutations(impl, i)))
    
    # Create a new set of resultant implied values to perform manipulations if requested
    sel = copy.deepcopy(res)
    
    # If some values should have fixed positions
    if fix_pos:
        # Remove implied values that do not have ANY of the fixed values in the speciied positions
        for r in res:
            # Only select permutations that have at least one of the specified fixed values at the given position
            if (any(f in r for f in fix_pos.keys())):
                # Not ALL of the fixed values will be at the specified position. Check if ANY of the fixed values are at the specified position.
                if (any(r[fix_pos[f]] == f for f in fix_pos.keys())):
                    pass
                # Remove permutations that do not have any of the fixed values at the specified positions
                else:
                    sel.remove(r)
    
    # Combine the tuples into a single string (necessary step since no manipulations can be made on tuple values)
    sel = [sep.join(s) for s in sel]
    
    # If implied value is a placeholder for other values
    if placeholder: 
        # Replace placeholder values with actual ones 
        new = []
        for p in placeholder.keys():
            # Perform replacement for each value
            for repl in placeholder[p]:
                for s in sel:
                    new.append(s.replace(p, repl))
        # If placeholders were requested
        return list(set(new))
    
    # If there are no placeholders return the original list of strings
    return list(set(sel))
            

        
        
        
        
        