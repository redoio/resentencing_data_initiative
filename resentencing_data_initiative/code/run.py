# -*- coding: utf-8 -*-
import helpers
import config
import extract 
import eligibility
import summary
import pandas as pd
import numpy as np
import datetime
from tqdm import tqdm
import copy
import os

print('\n#####################################################################################################')
print('################################################# START ##############################################')
print('############################################## Extraction ############################################')
print('######################################################################################################\n')

# Extract all the relevant datasets from the path
sorting_criteria, demographics, merit_credit, milestone_credit, rehab_credit, voced_credit, rv_report, current_commits, prior_commits = extract.get_input(read_path = config.read_data_path, 
                                                                                                                                                          month = config.month,
                                                                                                                                                          county_name = config.county_name, 
                                                                                                                                                          pickle = True) 

print('\n#####################################################################################################')
print('################################################ COMPLETE ############################################')
print('############################################### Extraction ###########################################')
print('######################################################################################################\n')

print('\n#####################################################################################################')
print('################################################## START #############################################')
print('########################################### Adult eligibility ########################################')
print('######################################################################################################\n')

# Identify eligible CDCR numbers for adults and juveniles
errors, adult_el_cdcr_nums = eligibility.gen_eligibility(demographics = demographics, 
                                                         sorting_criteria = sorting_criteria,
                                                         current_commits = current_commits, 
                                                         prior_commits = prior_commits, 
                                                         read_path = config.read_data_path, 
                                                         county_name = config.county_name, 
                                                         month = config.month,
                                                         eligibility_conditions = config.el_cond_adult,
                                                         pop = 'adult',
                                                         id_label = config.id_label, 
                                                         to_excel = True)

print('\n#####################################################################################################')
print('################################################ COMPLETE ############################################')
print('########################################### Adult eligibility ########################################')
print('######################################################################################################\n')

print('\n#####################################################################################################')
print('################################################## START #############################################')
print('############################################ Juvenile eligibility ####################################')
print('######################################################################################################\n')

errors, juvenile_el_cdcr_nums = eligibility.gen_eligibility(demographics = demographics, 
                                                            sorting_criteria = sorting_criteria,
                                                            current_commits = current_commits, 
                                                            prior_commits = prior_commits, 
                                                            read_path = config.read_data_path, 
                                                            county_name = config.county_name, 
                                                            month = config.month,
                                                            eligibility_conditions = config.el_cond_juv,
                                                            pop = 'juvenile',
                                                            id_label = config.id_label, 
                                                            to_excel = True)

print('\n#####################################################################################################')
print('################################################# COMPLETE ###########################################')
print('############################################ Juvenile eligibility ####################################')
print('######################################################################################################\n')

print('\n#####################################################################################################')
print('################################################## START #############################################')
print('############################################ Other eligibility #######################################')
print('######################################################################################################\n')

errors, rob_el_cdcr_nums = eligibility.gen_eligibility(demographics = demographics, 
                                                       sorting_criteria = sorting_criteria,
                                                       current_commits = current_commits, 
                                                       prior_commits = prior_commits, 
                                                       read_path = config.read_data_path, 
                                                       county_name = config.county_name, 
                                                       month = config.month,
                                                       eligibility_conditions = config.el_cond_other,
                                                       pop = 'rob',
                                                       id_label = config.id_label, 
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
adult_summary = summary.gen_eligible_summary(el_cdcr_nums = adult_el_cdcr_nums, 
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
                                             id_label = config.id_label, 
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

juvenile_summary = summary.gen_eligible_summary(el_cdcr_nums = juvenile_el_cdcr_nums, 
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
                                                id_label = config.id_label, 
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

rob_summary = summary.gen_eligible_summary(el_cdcr_nums = rob_el_cdcr_nums, 
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
                                           id_label = config.id_label,
                                           pop = 'rob', 
                                           write_path = None,
                                           to_excel = True)

print('\n#####################################################################################################')
print('################################################ COMPLETE ############################################')
print('######################################## Other eligible summaries ####################################')
print('######################################################################################################\n')

