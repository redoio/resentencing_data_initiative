# -*- coding: utf-8 -*-

from .functions import *
from .config import *
from .extract import *
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
2.   Not serving current sentence for any offense listed in Table D and E; AND
3. Has served a minimum of 10 years in custody; AND
4. Does not have a prior conviction for any offense listed in Table D.

"""

# Add all of the time variables to the demographic data necessary for classification - years served, sentence length, age, etc.
demographics, errors = gen_time_vars(demographics = demographics, merge = True)
# Show CDCR numbers and data of individuals with no age or time-served information
print(errors)

""" 

Identify Candidates: Adults

Conditions to search: 1., 2. and 3. for Cohort 1

"""

# Total population count
print('Total number of CDCR#s available: ', len(demographics['CDCR #'].unique()))

# Extracting CDCR numbers with eligible ages
el_cdcr_nums_1 = demographics[demographics['Age in years'] >= 50]['CDCR #']
print('Number of CDCR#s that are older than 50 years: ', len(el_cdcr_nums_1))

# Extracting CDCR numbers that met the age criteria that also meet the time sentenced criteria
el_cdcr_nums_2 = demographics[(demographics['Aggregate sentence in years'] >= 20) & demographics['CDCR #'].isin(el_cdcr_nums_1)]['CDCR #']
print('Number of CDCR#s that are older than 50 years & sentenced to over 20 years: ', len(el_cdcr_nums_2))

# Extracting CDCR numbers that met the age criteria that also meet the time served criteria
el_cdcr_nums_3 = demographics[(demographics['Time served in years'] >= 10) & demographics['CDCR #'].isin(el_cdcr_nums_2)]['CDCR #']
print('Number of CDCR#s that are older than 50 years, sentenced to over 20 years and served over 10 years: ', len(el_cdcr_nums_3))

""" 

Identify Candidates: Adults

Conditions to search: 4. for Cohort 1

"""

# Extracting ineligible offenses from sorting criteria
inel_offenses = sorting_criteria[sorting_criteria['Table'].isin(['Table A', 'Table B', 'Table C', 'Table D'])]['Offenses'].tolist()

# Appending new offenses based on implied ineligibility for adult populations
inel_offenses = gen_inel_off(inel_offenses, clean = True, 
                             impl = {'all': ["/att", "(664)", "2nd"], '459': ["/att", "(664)"]})

# Clean offense data in current commits file
current_commits['Offense cleaned'] = clean_offense_blk(data = current_commits['Offense'])

# Extracting current commits data with eligible offenses
el_cdcr_nums_4 = []
for cdcr_num in tqdm(el_cdcr_nums_3):
  # Extract offenses of the CDCR number
  offenses = current_commits[current_commits['CDCR #'] == cdcr_num]['Offense cleaned'].unique()
  if len(det_inel_off(offenses = offenses, inel_offenses = inel_offenses, pop = 'adult')) == 0:
    el_cdcr_nums_4.append(cdcr_num)

print('Number of CDCR#s that are older than 50 years, sentenced to over 20 years, served over 10 years, and have eligible current offenses: ', len(el_cdcr_nums_4))

""" 

Identify Candidates: Adults

Conditions to search: 5. for Cohort 1

"""

# Extracting ineligible offenses from sorting criteria
inel_offenses = sorting_criteria[sorting_criteria['Table'].isin(['Table C', 'Table D'])]['Offenses'].tolist()
# Appending new offenses based on implied ineligibility for adult populations
inel_offenses = gen_inel_off(inel_offenses, clean = True, 
                             impl = {'all': ["/att", "(664)", "2nd"], '459': ["/att", "(664)"]})

# Clean offense data in prior commits file
prior_commits['Offense cleaned'] = clean_offense_blk(data = prior_commits['Offense'])

# Extracting prior commits data with eligible offenses
el_cdcr_nums_5 = []
for cdcr_num in tqdm(el_cdcr_nums_4):
  # Extract offenses of the CDCR number
  offenses = prior_commits[prior_commits['CDCR #'] == cdcr_num]['Offense cleaned'].unique()
  if len(det_inel_off(offenses = offenses, inel_offenses = inel_offenses, pop = 'adult')) == 0:
    el_cdcr_nums_5.append(cdcr_num)

# Store eligible CDCR numbers in cohort 1 or adult population
adult_el_cdcr_nums = el_cdcr_nums_5

print('Number of CDCR#s that are older than 50 years, sentenced to over 20 years, served over 10 years, have eligible current offenses and eligible prior offenses: ', len(el_cdcr_nums_5))

""" 

Identify Candidates: Adults

Write results to output file

"""

# Write data to excel files
write_path = '/'.join([data_path, county_name, month, 'adult_eligible_demographics.xlsx'])
demographics[demographics['CDCR #'].isin(adult_el_cdcr_nums)].to_excel(write_path, index = False)

# Write data to excel files
write_path = '/'.join([data_path, county_name, month, 'adult_eligible_currentcommits.xlsx'])
current_commits[current_commits['CDCR #'].isin(adult_el_cdcr_nums)].to_excel(write_path, index = False)

""" 

Exploring Cohort 1 offenses, racial makeup, penal codes

"""

print('Top 20 offenses of individuals in Cohort 1 who meet all 5 eligibility conditions (from demographics data)')
print(demographics[demographics['CDCR #'].isin(el_cdcr_nums_5)]['Description'].value_counts()[0:20])

print('Top 20 offenses of individuals in Cohort 1 who meet all 5 eligibility conditions (from demographics data)')
demographics[demographics['CDCR #'].isin(el_cdcr_nums_5)]['Controlling Offense'].value_counts()[0:20]

print('Top 20 offenses of individuals in Cohort 1 who meet all 5 eligibility conditions (from current commits data)')
current_commits[current_commits['CDCR #'].isin(el_cdcr_nums_5)]['Offense'].value_counts()[0:20]

print('Sex offenses of individuals in Cohort 1 who meet all 5 eligibility conditions')
print(demographics[demographics['CDCR #'].isin(el_cdcr_nums_5)]['Sex Registrant'].value_counts())

print('Type of offenses of individuals in Cohort 1 who meet all 5 eligibility conditions')
print(demographics[demographics['CDCR #'].isin(el_cdcr_nums_5)]['Offense Category'].value_counts())
