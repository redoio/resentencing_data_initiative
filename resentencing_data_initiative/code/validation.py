# -*- coding: utf-8 -*-

from functions import *
from config import *
from extract import *
import pandas as pd
import numpy as np
import datetime
from tqdm import tqdm

"""

Validation of Cohort 1 results with OpenLattice results

"""

# Fix path and date range
county_name = 'Los Angeles'
month = '/'.join(['Rough', 'Data_05_2021', '21_05'])
data_path = '/content/drive/My Drive/Stanford Law 3XP/Data'
code_path = '/content/drive/My Drive/Stanford Law 3XP/Code'

# CDCR numbers eligible for resentencing according to OpenLattice
ol_el_cdcr_nums = pd.read_excel('/'.join([data_path, county_name, 'Rough/LA_DA_Cohort1_Update_05_2021.xlsx']))['CDCR..'].to_list()

# CDCR numbers eligible for resentencing according to our logic
errors, adult_el_cdcr_nums = gen_adult_eligibility(demographics, 
                                                   current_commits, 
                                                   prior_commits, 
                                                   data_path = data_path, 
                                                   county_name = county_name, 
                                                   month = month,
                                                   to_excel = False)

# Find CDCR numbers eligible in OpenLattice script that are ineligible in this script
missing_nums = []
for cdcr_num in ol_el_cdcr_nums:
  if (cdcr_num in demographics['CDCR #'].tolist()) and (cdcr_num not in adult_el_cdcr_nums):
    missing_nums.append(cdcr_num)

# Missing CDCR numbers
d = {}
write_path = '/'.join([data_path, county_name, 'Rough', 'ol_validation_.xlsx'])
for cdcr_num in missing_nums:
  off = current_commits[current_commits['CDCR #'] == cdcr_num]['Offense']
  d[cdcr_num] = off.to_list()
print('These CDCR numbers are eligible according to OpenLattice script but are ineligible according to this script')

df = pd.DataFrame()
df['CDCR #'] = d.keys()
df['Offenses'] = d.values()
df.to_excel(write_path, index = False)

# Find CDCR numbers ineligible in this script that are eligible in OpenLattice script
missing_nums = []
for cdcr_num in adult_el_cdcr_nums:
  if cdcr_num not in ol_el_cdcr_nums:
    missing_nums.append(cdcr_num)

# Missing CDCR numbers
for cdcr_num in missing_nums:
  off = current_commits[current_commits['CDCR #'] == cdcr_num]['Offense']
  print(cdcr_num, ':', off.to_list(), ';')
print('These CDCR numbers are eligible according to this script but are ineligible according to OpenLattice script')
