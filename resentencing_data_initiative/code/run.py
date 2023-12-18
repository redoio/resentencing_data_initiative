# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 00:03:13 2023

@author: akomarla
"""

from functions import *
import config
from extract import *
from eligibility import *
from summary import *
import pandas as pd
import numpy as np
import datetime
from tqdm import tqdm

# Extract all the relevant datasets from the path
sorting_criteria, demographics, merit_credit, milestone_credit, rehab_credit, voced_credit, rv_report, current_commits, prior_commits = get_input(data_path = config.data_path, 
                                                                                                                                                  county_name = config.county_name, 
                                                                                                                                                  pickle = False) 

# Identify eligible CDCR numbers for adults and juveniles
errors, adult_el_cdcr_nums = gen_adult_eligibility(demographics = demographics, 
                                                   current_commits = current_commits, 
                                                   prior_commits = prior_commits, 
                                                   data_path = config.data_path, 
                                                   county_name = config.county_name, 
                                                   month = config.month,
                                                   to_excel = True)

errors, juvenile_el_cdcr_nums = gen_juvenile_eligibility(demographics = demographics, 
                                                         current_commits = current_commits, 
                                                         prior_commits = prior_commits, 
                                                         data_path = config.data_path, 
                                                         county_name = config.county_name, 
                                                         month = config.month,
                                                         to_excel = True)

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
                                     data_path = config.data_path,
                                     county_name = config.county_name, 
                                     month = config.month,
                                     file_name = 'summary_adult',
                                     to_excel = True)

juvenile_summary = gen_eligible_summary(el_cdcr_nums = juvenile_el_cdcr_nums, 
                                        demographics = demographics,
                                        current_commits = current_commits, 
                                        prior_commits = prior_commits, 
                                        merit_credit = merit_credit, 
                                        milestone_credit = milestone_credit, 
                                        rehab_credit = rehab_credit, 
                                        voced_credit = voced_credit, 
                                        rv_report = rv_report, 
                                        data_path = config.data_path,
                                        county_name = config.county_name, 
                                        month = config.month,
                                        file_name = 'summary_juvenile',
                                        to_excel = True)
