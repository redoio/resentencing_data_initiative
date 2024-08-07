# -*- coding: utf-8 -*-
import importlib
import helpers
import utils
from config import config, dev_config
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
import cohort

# Get eligibility scenarios for the region or county
adult = importlib.import_module('scenarios.county.'+config.county_name+'.adult')
juvenile = importlib.import_module('scenarios.county.'+config.county_name+'.juvenile')
robbery = importlib.import_module('scenarios.county.'+config.county_name+'.robbery')

if __name__ == "__main__":
    print('\n######################################################################')
    print('################################## START ###############################')
    print('########################################################################')
    
    # Extract all the relevant datasets from the path
    sorting_criteria, demographics, merit_credit, milestone_credit, rehab_credit, voced_credit, rv_report, current_commits, prior_commits = extract.get_input(main_path = config.read_data_path, 
                                                                                                                                                              month = config.month,
                                                                                                                                                              county_name = config.county_name,
                                                                                                                                                              file_convention = config.naming_convention,
                                                                                                                                                              pickle = dev_config.ENV_VARS['pickle_input'])
    
    print('\n######################################################################')
    print('################################ COMPLETE ##############################')
    print('########################################################################')
    
    print('\n######################################################################')
    print('################################## START ###############################')
    print('########################################################################')
    
    # Identify eligible CDCR numbers for adults
    errors, adult_el_cdcr_nums = cohort.gen_eligible_cohort(demographics = demographics, 
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
                                                            write_path = config.write_data_path,
                                                            to_excel = config.to_excel, 
                                                            parallel = dev_config.ENV_VARS['parallel'])
    
    print('\n######################################################################')
    print('################################ COMPLETE ##############################')
    print('########################################################################')
    
    print('\n######################################################################')
    print('################################## START ###############################')
    print('########################################################################')
    
    # Identify eligible CDCR numbers for juveniles
    errors, juvenile_el_cdcr_nums = cohort.gen_eligible_cohort(demographics = demographics, 
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
                                                               write_path = config.write_data_path,
                                                               to_excel = config.to_excel,
                                                               parallel = dev_config.ENV_VARS['parallel'])
    
    print('\n######################################################################')
    print('################################ COMPLETE ##############################')
    print('########################################################################')
    
    print('\n######################################################################')
    print('################################## START ###############################')
    print('########################################################################')
    
    # Identify eligible CDCR numbers for robbery related offenses
    errors, rob_el_cdcr_nums = cohort.gen_eligible_cohort(demographics = demographics, 
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
                                                          write_path = config.write_data_path,
                                                          to_excel = config.to_excel,
                                                          parallel = dev_config.ENV_VARS['parallel'])
    
    print('\n######################################################################')
    print('################################ COMPLETE ##############################')
    print('########################################################################')
    
    print('\n######################################################################')
    print('################################## START ###############################')
    print('########################################################################')
    
    # Generate summaries of eligible individuals in the CDCR system
    adult_summary = cohort.gen_summary_cohort(cdcr_nums = adult_el_cdcr_nums, 
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
                                              pop_label = 'adult_eligible',
                                              sel_conditions = utils.filter_dict(adult.el_cond, 'r_'),
                                              id_label = config.id_label, 
                                              write_path = config.write_data_path,
                                              to_excel = config.to_excel)
    
    print('\n######################################################################')
    print('################################ COMPLETE ##############################')
    print('########################################################################')
    
    print('\n######################################################################')
    print('################################## START ###############################')
    print('########################################################################')
    
    # Generate summaries of eligible individuals in the CDCR system
    juvenile_summary = cohort.gen_summary_cohort(cdcr_nums = juvenile_el_cdcr_nums, 
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
                                                 pop_label = 'juvenile_eligible', 
                                                 write_path = config.write_data_path,
                                                 to_excel = config.to_excel)
    
    print('\n######################################################################')
    print('################################ COMPLETE ##############################')
    print('########################################################################')
    
    print('\n######################################################################')
    print('################################## START ###############################')
    print('########################################################################')
    
    # Generate summaries of eligible individuals in the CDCR system
    rob_summary = cohort.gen_summary_cohort(cdcr_nums = rob_el_cdcr_nums, 
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
                                            pop_label = 'robbery_eligible', 
                                            write_path = config.write_data_path,
                                            to_excel = config.to_excel)
    
    print('\n######################################################################')
    print('################################ COMPLETE ##############################')
    print('########################################################################')
    
    print('\n######################################################################')
    print('################################## START ###############################')
    print('########################################################################')
    
    # Compare outputs between months
    adult_diff = helpers.compare_output(read_path = config.comp_path['adult'], 
                                         comp_col = config.id_label, 
                                         label_col = config.comp_info,  
                                         pop_label = 'adult_eligible',
                                         direction = 'multi',
                                         result = 'disagree',
                                         to_excel = config.to_excel)
    
    print('\n######################################################################')
    print('################################ COMPLETE ##############################')
    print('########################################################################')
    
    print('\n######################################################################')
    print('################################## START ###############################')
    print('########################################################################')
    
    # Compare outputs between months
    juvenile_diff = helpers.compare_output(read_path = config.comp_path['juvenile'], 
                                            comp_col = config.id_label, 
                                            label_col = config.comp_info,  
                                            pop_label = 'juvenile_eligible',
                                            merge = True,
                                            direction = 'multi',
                                            result = 'disagree',
                                            to_excel = config.to_excel)

    print('\n######################################################################')
    print('################################ COMPLETE ##############################')
    print('########################################################################')
    
    print('\n######################################################################')
    print('################################## START ###############################')
    print('########################################################################')
    
    # Compare outputs between months
    robbery_diff = helpers.compare_output(read_path = config.comp_path['robbery'], 
                                          comp_col = config.id_label, 
                                          label_col = config.comp_info,  
                                          pop_label = 'robbery_eligible',
                                          merge = True,
                                          direction = 'multi',
                                          result = 'disagree',
                                          to_excel = config.to_excel)
    
    print('\n######################################################################')
    print('################################ COMPLETE ##############################')
    print('########################################################################')