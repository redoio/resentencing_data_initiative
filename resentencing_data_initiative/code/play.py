# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 20:39:47 2024

@author: apkom
"""
from itertools import permutations, product
import pandas as pd
import copy
from helpers import *

criteria = pd.read_excel('C:/Users/apkom/Downloads/sorting_criteria.xlsx', dtype = {'Offenses': str})
current_commits = pd.read_excel('C:/Users/apkom/Downloads/currentcommitments.xlsx')
demographics = pd.read_excel('C:/Users/apkom/Downloads/demographics.xlsx')

impl = {'all': ['/att', '(664)', '2nd', "(ss)"], '459': ['/att', '(664)']}
excpt = [key for key in impl.keys() if key != 'all']
offenses = clean_offense_blk(criteria[criteria['Table'] == 'Table F']['Offenses'].to_list())

# Remove exceptions
offenses_woe = copy.deepcopy(offenses)
for e in impl.keys():
    if (e != 'all') and (e in offenses):
        offenses_woe.remove(e)

def gen_impl_val(use, perm, sep = '', fix = None, pos = None):
    if fix and pos == 0:
        res = [sep.join(v) for v in list(product(use, fix, repeat=1))]
    elif fix and pos == 1:
        res = [sep.join(v) for v in list(product(fix, use, repeat=1))]
    else:
        res = []
        
    for p in range(2, perm+1):
        for v in list(permutations(res, p)):
            res.append(sep.join(v))
    res.extend(use)
    return res
        
sep = ''
perm = 2

impl_offenses = {}
for val in impl.keys():
    if val == 'all':
        # Generate implied offenses
        add = [sep.join(t) for t in list(permutations(impl[val], perm))]
        for a in add:
            impl_offenses = list(set.union(set(impl_offenses), set([off+sep+a for off in offenses_woe])))
    # If val is an exception and called out separately
    else:
        # Generate implied offenses
        add = [sep.join(t) for t in list(permutations(impl[val], perm))]
        for a in add:
            impl_offenses = list(set.union(set(impl_offenses), set([off+sep+a for off in offenses if val in off])))




res = [('')]
attach = impl['all'][:]
for i in range(1, len(attach)+1):
    res.extend(list(permutations(attach, i)))

fix_pos = {"2nd": 0,
           "(ss)": 0}

# Only select permutations that have at least one of the specified fixed values at the given position. Not ALL of the fixed values will be at the specified position.
sel = []
for r in res:
    for f in fix_pos.keys():
        try: 
            if (f in r) and (r[fix_pos[f]] == f) and (r not in sel):
                sel.append(r)
            elif (f not in r) and (r not in sel):
                sel.append(r)
        except:
            print(r, 'error')

# Combine the tuples into a single string 
sep = ''
sel = [sep.join(s) for s in sel]

# Replace placeholder values with actual ones 
placeholder = {"ss": ['a', 'b', 'c']}

for p in placeholder.keys():
    new = []
    for repl in placeholder[p]:
        for s in sel:
            new.append(s.replace(p, repl))
            

        
        
        
        
        