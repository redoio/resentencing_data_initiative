# -*- coding: utf-8 -*-

from functions import *
from config import *
from extract import *
from eligibility_adult import adult_el_cdcr_nums
import pandas as pd
import numpy as np
import datetime
from tqdm import tqdm

# Write data to excel files
write_path = '/'.join([data_path, county_name, month, 'summary_adult.xlsx'])

# Get demographics data
adult_el_df = demographics.loc[demographics['CDCR #'].isin(adult_el_cdcr_nums)][['CDCR #', 'Current Security Level', 'Controlling Offense',
                                                                                 'Current Classication Score', 'Classification Score 5 Years\nAgo',
                                                                                 'Mental Health Level of Care', 'DPPV Disability - Mobility']]

# Remove new-line
adult_el_df.rename(columns = {'Classification Score 5 Years\nAgo': 'Classification Score 5 Years Ago'}, 
                   inplace = True)

# Format mobility disability
adult_el_df['DPPV Disability - Mobility'] = adult_el_df['DPPV Disability - Mobility'].str.replace('Impacting Placement', '')

# Generate summaries
adult_summary = gen_summary(df = adult_el_df, 
                            current_commits = current_commits, 
                            prior_commits = prior_commits, 
                            merit_credit = merit_credit, 
                            milestone_credit = milestone_credit, 
                            rehab_credit = rehab_credit, 
                            voced_credit = voced_credit, 
                            rv_report = rv_report, 
                            write_path = write_path, 
                            to_excel = True)
