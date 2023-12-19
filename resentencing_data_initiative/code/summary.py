# -*- coding: utf-8 -*-

from helpers import *
import pandas as pd
import numpy as np
import datetime
from tqdm import tqdm

def gen_eligible_summary(el_cdcr_nums, 
                         demographics,
                         current_commits, 
                         prior_commits, 
                         merit_credit, 
                         milestone_credit, 
                         rehab_credit, 
                         voced_credit, 
                         rv_report, 
                         data_path = None,
                         county_name = None, 
                         month = None,
                         file_name = None,
                         write_path = None,
                         to_excel = False):
    """

    Parameters
    ----------
    el_cdcr_nums : list of strs
        List of CDCR numbers that are eligible for resentencing
    demographics : pandas dataframe
        Data on demographics of the incarcerated population
    current_commits : pandas dataframe
        Data on current offenses of the incarcerated population wherein each row contains a single offense
    prior_commits : pandas dataframe
        Data on prior offenses of the incarcerated population wherein each row contains a single offense
    merit_credit : pandas dataframe
        Data on education credits attained during incarceration
    milestone_credit : pandas dataframe
        Data on rehabilitation milestones attained during incarceration
    rehab_credit : pandas dataframe
        Data on credits received from institution for participating in rehabilitative programs
    voced_credit : pandas dataframe
        Data on credits received from institution for participating in vocational training programs
    rv_report : pandas dataframe
        Data on rules violations during incarceration
    data_path : str, optional
        Full path where output data should be written (all parent folders)
        Default is None.
    county_name : str, optional
        Name of the county for which eligibility was evaluated, ex: 'Los Angeles County'
        Default is None.
    month : str, optional
        Year and month for which eligibility was evaluated, ex: '2023_06'
        Default is None.
   file_name : str, optional
        Name of the .xlsx or .csv file to write output to, ex: 'adult_eligible_summaries.xlsx'
        File extension should be included 
   to_excel : boolean, optional
        Specify whether to write the summaries of eligible individuals to Excel files.
        If True, specify the path information to write the output
        Default is False.
   write_path : str, optional 
        Specify the full path where the Excel outputs should be written. 
        If to_excel = True but write_path = None, data outputs are written to the county_name + month folder by default. To avoid this behavior, pass a value to write_path.
    
    Returns
    -------
    df : pandas dataframe
        Data on convictions, rules violations, programming for each CDCR number passed in the input dataframe. If merge = True, this includes the input dataframe as well

    """
    
    # Get demographics data of eligible individuals
    el_df = demographics.loc[demographics['CDCR #'].isin(el_cdcr_nums)]
    
    # Remove new-line character in demographics column name
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
                             rv_report = rv_report, 
                             merge = True)
    
    # Write data to excel files
    if to_excel:
        if not write_path:
            # Write data to excel files
            write_path = '/'.join(l for l in [data_path, county_name, month, file_name] if l)
            el_summary.to_excel(write_path, index = False)
            print('Summary of eligible individuals written to: ', write_path)
        elif write_path:
            # Write data to excel files
            el_summary.to_excel(write_path, index = False)
            print('Summary of eligible individuals written to: ', write_path)
        
    return el_summary