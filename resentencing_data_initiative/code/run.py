# -*- coding: utf-8 -*-
import helpers
import config
from scenarios import adult
from scenarios import juvenile
from scenarios import robbery
from scenarios import rules
from scenarios import utils
import extract 
import eligibility
import summary
import pandas as pd
import numpy as np
import datetime
from tqdm import tqdm
import copy
import os

print('\n######################################################################')
print('################################## START ###############################')
print('########################################################################')

# Extract all the relevant datasets from the path
sorting_criteria, demographics, merit_credit, milestone_credit, rehab_credit, voced_credit, rv_report, current_commits, prior_commits = extract.get_input(read_path = config.read_data_path, 
                                                                                                                                                          month = config.month,
                                                                                                                                                          county_name = config.county_name, 
                                                                                                                                                          pickle = True) 

print('\n######################################################################')
print('################################ COMPLETE ##############################')
print('########################################################################')

print('\n######################################################################')
print('################################## START ###############################')
print('########################################################################')

# Identify eligible CDCR numbers for adults and juveniles
errors, adult_el_cdcr_nums = eligibility.gen_eligibility(demographics = demographics, 
                                                         sorting_criteria = sorting_criteria,
                                                         current_commits = current_commits, 
                                                         prior_commits = prior_commits, 
                                                         read_path = config.read_data_path, 
                                                         county_name = config.county_name, 
                                                         month = config.month,
                                                         eligibility_conditions = adult.el_cond,
                                                         pop_label = adult.el_cond['population'],
                                                         id_label = config.id_label, 
                                                         to_excel = True)

print('\n######################################################################')
print('################################ COMPLETE ##############################')
print('########################################################################')

print('\n######################################################################')
print('################################## START ###############################')
print('########################################################################')

errors, juvenile_el_cdcr_nums = eligibility.gen_eligibility(demographics = demographics, 
                                                            sorting_criteria = sorting_criteria,
                                                            current_commits = current_commits, 
                                                            prior_commits = prior_commits, 
                                                            read_path = config.read_data_path, 
                                                            county_name = config.county_name, 
                                                            month = config.month,
                                                            eligibility_conditions = juvenile.el_cond,
                                                            pop_label = juvenile.el_cond['population'],
                                                            id_label = config.id_label, 
                                                            to_excel = True)

print('\n######################################################################')
print('################################ COMPLETE ##############################')
print('########################################################################')

print('\n######################################################################')
print('################################## START ###############################')
print('########################################################################')

errors, rob_el_cdcr_nums = eligibility.gen_eligibility(demographics = demographics, 
                                                       sorting_criteria = sorting_criteria,
                                                       current_commits = current_commits, 
                                                       prior_commits = prior_commits, 
                                                       read_path = config.read_data_path, 
                                                       county_name = config.county_name, 
                                                       month = config.month,
                                                       eligibility_conditions = robbery.el_cond,
                                                       pop_label = robbery.el_cond['offense type'],
                                                       id_label = config.id_label, 
                                                       to_excel = True)

print('\n######################################################################')
print('################################ COMPLETE ##############################')
print('########################################################################')

print('\n######################################################################')
print('################################## START ###############################')
print('########################################################################')

# Generate summaries of eligible individuals in the CDCR system
adult_summary = summary.gen_summary(cdcr_nums = adult_el_cdcr_nums, 
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
                                    pop_label = adult.el_cond['population'],
                                    id_label = config.id_label, 
                                    write_path = None,
                                    to_excel = True)

print('\n######################################################################')
print('################################ COMPLETE ##############################')
print('########################################################################')

print('\n######################################################################')
print('################################## START ###############################')
print('########################################################################')

juvenile_summary = summary.gen_summary(cdcr_nums = juvenile_el_cdcr_nums, 
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
                                       pop_label = juvenile.el_cond['population'], 
                                       write_path = None,
                                       to_excel = True)

print('\n######################################################################')
print('################################ COMPLETE ##############################')
print('########################################################################')

print('\n######################################################################')
print('################################## START ###############################')
print('########################################################################')

rob_summary = summary.gen_summary(cdcr_nums = rob_el_cdcr_nums, 
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
                                  pop_label = robbery.el_cond['offense type'], 
                                  write_path = None,
                                  to_excel = True)

print('\n######################################################################')
print('################################ COMPLETE ##############################')
print('########################################################################')
