# -*- coding: utf-8 -*-

from helpers import *

def gen_eligible_summary(el_cdcr_nums, 
                         demographics,
                         current_commits, 
                         prior_commits, 
                         merit_credit, 
                         milestone_credit, 
                         rehab_credit, 
                         voced_credit, 
                         rv_report, 
                         data_path,
                         county_name, 
                         month,
                         file_name,
                         to_excel):
    
    # Get demographics data of eligible individuals
    el_df = demographics.loc[demographics['CDCR #'].isin(el_cdcr_nums)][['CDCR #', 'Current Security Level', 'Controlling Offense',
                                                                         'Current Classication Score', 'Classification Score 5 Years\nAgo',
                                                                         'Mental Health Level of Care', 'DPPV Disability - Mobility']]
    
    # Remove new-line character in column names
    el_df.rename(columns = {'Classification Score 5 Years\nAgo': 'Classification Score 5 Years Ago'}, 
                 inplace = True)
    
    # Format mobility disability column in demographics
    el_df['DPPV Disability - Mobility'] = el_df['DPPV Disability - Mobility'].str.replace('Impacting Placement', '')
    
    # Generate summaries of individuals who are eligible for resentencing
    el_summary = gen_summary(df = el_df, 
                             current_commits = current_commits, 
                             prior_commits = prior_commits, 
                             merit_credit = merit_credit, 
                             milestone_credit = milestone_credit, 
                             rehab_credit = rehab_credit, 
                             voced_credit = voced_credit, 
                             rv_report = rv_report)
    
    # Write data to excel files
    write_path = '/'.join([data_path, county_name, month, file_name+'.xlsx'])
    el_summary.to_excel(write_path, index = False)
    
    return el_summary