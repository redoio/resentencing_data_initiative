# -*- coding: utf-8 -*-

import config
import rules
import impl
from helpers import *
from extract import *
from eligibility import *
from summary import *
import pandas as pd
import numpy as np
import datetime
from tqdm import tqdm
import copy
import os
from itertools import permutations, product



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
3.   Has served a minimum of 10 years in custody; AND
4.   Does not have a prior conviction for any offense listed in Table D.

"""

print('\n#####################################################################################################')
print('################################################# START ##############################################')
print('############################################## Extraction ############################################')
print('######################################################################################################\n')

# Extract all the relevant datasets from the path
sorting_criteria, demographics, merit_credit, milestone_credit, rehab_credit, voced_credit, rv_report, current_commits, prior_commits = get_input(read_path = config.read_data_path, 
                                                                                                                                                  month = config.month,
                                                                                                                                                  county_name = config.county_name, 
                                                                                                                                                  pickle = True) 

# sorting_criteria = pd.read_excel('C:/Users/apkom/Downloads/sorting_criteria.xlsx', dtype = {'Offenses': str})
# current_commits = pd.read_excel('C:/Users/apkom/Downloads/currentcommitments.xlsx')
# demographics = pd.read_excel('C:/Users/apkom/Downloads/demographics.xlsx')
# prior_commits = pd.read_excel('C:/Users/apkom/Downloads/priorcommitments.xlsx')

print('\n#####################################################################################################')
print('################################################ COMPLETE ############################################')
print('############################################### Extraction ###########################################')
print('######################################################################################################\n')

print('\n#####################################################################################################')
print('################################################## START #############################################')
print('########################################### Adult eligibility ########################################')
print('######################################################################################################\n')

# Identify eligible CDCR numbers for adults and juveniles
errors, adult_el_cdcr_nums = gen_eligibility(demographics = demographics, 
                                             sorting_criteria = sorting_criteria,
                                             current_commits = current_commits, 
                                             prior_commits = prior_commits, 
                                             read_path = config.read_data_path, 
                                             county_name = config.county_name, 
                                             month = config.month,
                                             eligibility_conditions = config.el_cond_adult,
                                             pop = 'adult',
                                             to_excel = True)

print('\n#####################################################################################################')
print('################################################ COMPLETE ############################################')
print('########################################### Adult eligibility ########################################')
print('######################################################################################################\n')

print('\n#####################################################################################################')
print('################################################## START #############################################')
print('############################################ Juvenile eligibility ####################################')
print('######################################################################################################\n')

errors, juvenile_el_cdcr_nums = gen_eligibility(demographics = demographics, 
                                                sorting_criteria = sorting_criteria,
                                                current_commits = current_commits, 
                                                prior_commits = prior_commits, 
                                                read_path = config.read_data_path, 
                                                county_name = config.county_name, 
                                                month = config.month,
                                                eligibility_conditions = config.el_cond_juv,
                                                pop = 'juvenile',
                                                to_excel = True)

print('\n#####################################################################################################')
print('################################################# COMPLETE ###########################################')
print('############################################ Juvenile eligibility ####################################')
print('######################################################################################################\n')

print('\n#####################################################################################################')
print('################################################## START #############################################')
print('############################################ Other eligibility #######################################')
print('######################################################################################################\n')

errors, other_el_cdcr_nums = gen_eligibility(demographics = demographics, 
                                             sorting_criteria = sorting_criteria,
                                             current_commits = current_commits, 
                                             prior_commits = prior_commits, 
                                             read_path = config.read_data_path, 
                                             county_name = config.county_name, 
                                             month = config.month,
                                             eligibility_conditions = config.el_cond_other,
                                             pop = 'other',
                                             to_excel = True)

print('\n#####################################################################################################')
print('################################################# COMPLETE ###########################################')
print('############################################ Other eligibility #######################################')
print('######################################################################################################\n')

print('\n#####################################################################################################')
print('################################################## START #############################################')
print('######################################## Adult eligible summaries ####################################')
print('######################################################################################################\n')

# Generate summaries of eligible individuals in the CDCR system
adult_summary = gen_eligible_summary(el_cdcr_nums = adult_el_cdcr_nums, 
                                     demographics = demographics,
                                     current_commits = current_commits, 
                                     prior_commits = prior_commits, 
                                     merit_credit = merit_credit, 
                                     milestone_credit = milestone_credit, 
                                     rehab_credit = rehab_credit, 
                                     voced_credit = voced_credit, 
                                     rv_report = rv_report, 
                                     read_path = config.read_data_path,
                                     county_name = config.county_name, 
                                     month = config.month,
                                     pop = 'adult',
                                     write_path = None,
                                     to_excel = True)

print('\n#####################################################################################################')
print('################################################ COMPLETE ############################################')
print('######################################## Adult eligible summaries ####################################')
print('######################################################################################################\n')


print('\n#####################################################################################################')
print('################################################ START ###############################################')
print('##################################### Juvenile eligible summaries ####################################')
print('######################################################################################################\n')

juvenile_summary = gen_eligible_summary(el_cdcr_nums = juvenile_el_cdcr_nums, 
                                        demographics = demographics,
                                        current_commits = current_commits, 
                                        prior_commits = prior_commits, 
                                        merit_credit = merit_credit, 
                                        milestone_credit = milestone_credit, 
                                        rehab_credit = rehab_credit, 
                                        voced_credit = voced_credit, 
                                        rv_report = rv_report, 
                                        read_path = config.read_data_path,
                                        county_name = config.county_name, 
                                        month = config.month,
                                        pop = 'juvenile',
                                        write_path = None,
                                        to_excel = True)

print('\n#####################################################################################################')
print('################################################ COMPLETE ############################################')
print('##################################### Juvenile eligible summaries ####################################')
print('######################################################################################################\n')

print('\n#####################################################################################################')
print('################################################ START ###############################################')
print('######################################## Other eligible summaries ####################################')
print('######################################################################################################\n')

other_summary = gen_eligible_summary(el_cdcr_nums = other_el_cdcr_nums, 
                                     demographics = demographics,
                                     current_commits = current_commits, 
                                     prior_commits = prior_commits, 
                                     merit_credit = merit_credit, 
                                     milestone_credit = milestone_credit, 
                                     rehab_credit = rehab_credit, 
                                     voced_credit = voced_credit, 
                                     rv_report = rv_report, 
                                     read_path = config.read_data_path,
                                     county_name = config.county_name, 
                                     month = config.month,
                                     pop = 'other',
                                     write_path = None,
                                     to_excel = True)

print('\n#####################################################################################################')
print('################################################ COMPLETE ############################################')
print('######################################## Other eligible summaries ####################################')
print('######################################################################################################\n')

