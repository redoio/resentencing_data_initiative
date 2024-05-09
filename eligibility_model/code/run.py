# -*- coding: utf-8 -*-
import importlib
import helpers
import utils
import config
from scenarios import rules
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

# Get eligibility scenarios for the region or county
adult = importlib.import_module('scenarios.county.'+config.county_name+'.adult')
juvenile = importlib.import_module('scenarios.county.'+config.county_name+'.juvenile')
robbery = importlib.import_module('scenarios.county.'+config.county_name+'.robbery')

print('\n######################################################################')
print('################################ COMPLETE ##############################')
print('########################################################################')

print('\n######################################################################')
print('################################## START ###############################')
print('########################################################################')

# Extract all the relevant datasets from the path
sorting_criteria, demographics, merit_credit, milestone_credit, rehab_credit, voced_credit, rv_report, current_commits, prior_commits = extract.get_input(read_path = config.read_data_path, 
                                                                                                                                                          month = config.month,
                                                                                                                                                          county_name = config.county_name, 
                                                                                                                                                          pickle = False) 

print('\n######################################################################')
print('################################ COMPLETE ##############################')
print('########################################################################')

print('\n######################################################################')
print('################################## START ###############################')
print('########################################################################')

# Identify eligible CDCR numbers for adults
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
                                                         comp_int = rules.comp_int,
                                                         to_excel = True)

print('\n######################################################################')
print('################################ COMPLETE ##############################')
print('########################################################################')

print('\n######################################################################')
print('################################## START ###############################')
print('########################################################################')

# Identify eligible CDCR numbers for juveniles
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
                                                            comp_int = rules.comp_int,
                                                            to_excel = True)

print('\n######################################################################')
print('################################ COMPLETE ##############################')
print('########################################################################')

print('\n######################################################################')
print('################################## START ###############################')
print('########################################################################')

# Identify eligible CDCR numbers for robbery related offenses
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
                                                       comp_int = rules.comp_int,
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
                                    sel_conditions = utils.filter_dict(adult.el_cond, 'r_'),
                                    id_label = config.id_label, 
                                    write_path = None,
                                    to_excel = True)

print('\n######################################################################')
print('################################ COMPLETE ##############################')
print('########################################################################')

print('\n######################################################################')
print('################################## START ###############################')
print('########################################################################')

# Generate summaries of eligible individuals in the CDCR system
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
                                       sel_conditions = utils.filter_dict(juvenile.el_cond, 'r_'),
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

# Generate summaries of eligible individuals in the CDCR system
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
                                  sel_conditions = utils.filter_dict(robbery.el_cond, 'r_'),
                                  id_label = config.id_label,
                                  pop_label = robbery.el_cond['offense type'], 
                                  write_path = None,
                                  to_excel = True)

print('\n######################################################################')
print('################################ COMPLETE ##############################')
print('########################################################################')

print('\n######################################################################')
print('################################## START ###############################')
print('########################################################################')

# Compare outputs between months
diff = helpers.comp_output(read_path = config.comp_path, 
                           comp_val = config.id_label, 
                           label = config.comp_info,  
                           pop_label = 'adult_eligible',
                           merge = False,
                           to_excel = True)

print('\n######################################################################')
print('################################ COMPLETE ##############################')
print('########################################################################')