# -*- coding: utf-8 -*-

from functions import *
from config import *
from extract import *
import pandas as pd
import numpy as np
import datetime
from tqdm import tqdm


"""

Conditions for Qualification

Cohort 1

Adults

1.   Age 50 and older; AND
2.   Sentenced to 20 years or more; AND
3.   Served a minimum of 10 years in custody; AND
4.   Is not serving a current sentence for any offense listed in Table A, B, C, or D, AND
5.   Does not have a prior conviction for any offense listed in Tables C & D

Cohort 2

Minors Tried as Adults

1.   Sentenced for a crime that was committed at age 14 or 15; AND
2.   Not serving current sentence for any offense listed in Table E or D; AND
3. Has served a minimum of 10 years in custody; AND
4. Does not have a prior conviction for any offense listed in Table D.

"""

# Add all of the time variables to the demographic data necessary for classification - years served, sentence length, age, etc.
demographics, errors = gen_time_vars(demographics = demographics, merge = True)
# Show CDCR numbers and data of individuals with no age or time-served information
print(errors)

"""

Identify Candidates: Juvenile

Conditions to search: 1. Cohort 2

"""

# Extracting CDCR numbers that meet the age criteria
el_cdcr_nums_1 = []
el_cdcr_nums_1 = demographics[(demographics['Age during offense'] < 16) & (demographics['Age during offense'] >= 14)]['CDCR #'].to_list()
print('Number of CDCR#s that committed offenses at the age of 14 to 15: ', len(el_cdcr_nums_1))

"""

Identify Candidates: Juvenile

Conditions to search: 2. Cohort 2

"""

# Extracting ineligible offenses from sorting criteria
inel_offenses = sorting_criteria[sorting_criteria['Table'].isin(['Table E', 'Table D'])]['Offenses'].tolist()
inel_offenses = gen_inel_off(inel_offenses, clean = True, impl = {'187': ["2nd", "(664)"]}, perm = 2)

# Clean offense data in current commits file
current_commits['Offense cleaned'] = clean_offense_blk(data = current_commits['Offense'])

# Extracting CDCR numbers that meet the age criteria and offense eligibility
el_cdcr_nums_2 = []
for cdcr_num in tqdm(el_cdcr_nums_1):
  # Extracting offenses of the CDCR number
  offenses = current_commits[current_commits['CDCR #'] == cdcr_num]['Offense cleaned'].unique()
  if len(det_inel_off(offenses = offenses, inel_offenses = inel_offenses, pop = 'juvenile')) == 0:
    el_cdcr_nums_2.append(cdcr_num)

print('Number of CDCR#s that committed offenses at age 14 and 15 and have eligible current offenses: ', len(el_cdcr_nums_2))

""" 

Identify Candidates: Juvenile

Conditions to search: 3. for Cohort 2

"""

# Extracting CDCR numbers that met the age and offense criteria that also meet the time served criteria
el_cdcr_nums_3 = []
el_cdcr_nums_3 = demographics[(demographics['Time served in years'] >= 10) & demographics['CDCR #'].isin(el_cdcr_nums_2)]['CDCR #'].to_list()
print('Number of CDCR#s that committed offenses at age 14 and 15, have eligible current offenses and served more than 10 years: ', len(el_cdcr_nums_3))

""" 

Identify Candidates: Juvenile

Conditions to search: 4. for Cohort 2

"""

# Extracting ineligible offenses from sorting criteria
inel_offenses = sorting_criteria[sorting_criteria['Table'].isin(['Table D'])]['Offenses'].tolist()
inel_offenses = gen_inel_off(inel_offenses, clean = True, impl = {'187': ["2nd", "(664)"]}, perm = 2)

# Clean offense data in current commits file
prior_commits['Offense cleaned'] = clean_offense_blk(data = prior_commits['Offense'])

# Extracting CDCR numbers that met the age, time sentenced and current and prior offense eligibility criteria
el_cdcr_nums_4 = []
for cdcr_num in tqdm(el_cdcr_nums_3):
  offenses = prior_commits[prior_commits['CDCR #'] == cdcr_num]['Offense cleaned'].unique()
  if len(det_inel_off(offenses = offenses, inel_offenses = inel_offenses, pop = 'juvenile')) == 0:
    el_cdcr_nums_4.append(cdcr_num)

# Store eligible CDCR numbers in cohort 2 or juvenile population
juvenile_el_cdcr_nums = el_cdcr_nums_4

print('Number of CDCR#s that committed offenses at age 14 and 15, have eligible current and prior offenses, and served more than 10 years: ', len(el_cdcr_nums_4))

""" 

Identify Candidates: Juvenile

Write results to output file

"""

# Write data to excel files
write_path = '/'.join([data_path, county_name, month, 'juvenile_eligible_demographics.xlsx'])
demographics[demographics['CDCR #'].isin(juvenile_el_cdcr_nums)].to_excel(write_path, index = False)

# Write data to excel files
write_path = '/'.join([data_path, county_name, month, 'juvenile_eligible_currentcommits.xlsx'])
current_commits[current_commits['CDCR #'].isin(juvenile_el_cdcr_nums)].to_excel(write_path, index = False)

"""

Exploring Cohort 1 offenses, racial makeup, penal codes

"""

print('Top 20 offenses of individuals in Cohort 2 who meet all 4 eligibility conditions (from demographics data)')
print(demographics[demographics['CDCR #'].isin(el_cdcr_nums_4)]['Description'].value_counts()[0:20])

print('Top 20 offenses of individuals in Cohort 2 who meet all 4 eligibility conditions (from demographics data)')
demographics[demographics['CDCR #'].isin(el_cdcr_nums_4)]['Controlling Offense'].value_counts()[0:20]

print('Sex offenses of individuals in Cohort 2 who meet all 4 eligibility conditions')
print(demographics[demographics['CDCR #'].isin(el_cdcr_nums_4)]['Sex Registrant'].value_counts())

print('Type of offenses of individuals in Cohort 2 who meet all 4 eligibility conditions')
print(demographics[demographics['CDCR #'].isin(el_cdcr_nums_4)]['Offense Category'].value_counts())

