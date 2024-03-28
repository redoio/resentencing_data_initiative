# -*- coding: utf-8 -*-
import helpers
import utils
import pandas as pd
import numpy as np
import datetime
import copy
from tqdm import tqdm
import os


def gen_summary(cdcr_nums, 
                demographics,
                current_commits, 
                prior_commits, 
                merit_credit, 
                milestone_credit, 
                rehab_credit, 
                voced_credit, 
                rv_report, 
                id_label,
                clean_col_names = True,
                read_path = None,
                county_name = None, 
                month = None,
                pop_label = None,
                write_path = None,
                to_excel = False):
    """

    Parameters
    ----------
    cdcr_nums : list of strs
        List of CDCR numbers to generate population summary for
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
    read_path : str, optional
        Full path from where input data is read (all parent folders)
        Default is None.
    id_label : str
        Name of CDCR ID column in the data
    clean_col_names : boolean, optional
        Specify whether to clean column names before running the eligibility model. Applies the utils.clean() function on the column headers
        Default is True
    county_name : str, optional
        Name of the county for which eligibility was evaluated, ex: 'Los Angeles County'
        Default is None.
    month : str, optional
        Year and month for which eligibility was evaluated, ex: '2023_06'
        Default is None.
    pop : str, optional
        Nature of the population being evaluated, ex: 'adult' or 'juvenile'
        Default is none
    to_excel : boolean, optional
        Specify whether to write the summaries of eligible individuals to Excel files.
        If True, specify the path information to write the output
        Default is False.
    write_path : str, optional 
        Specify the full path where the Excel outputs should be written. 
        If to_excel = True but write_path = None, data outputs are written to the county_name/month/output/date folder by default. To avoid this behavior, pass a value to write_path.
    
    Returns
    -------
    df : pandas dataframe
        Data on convictions, rules violations, programming for each CDCR number passed in the input dataframe. If merge = True, this includes the input dataframe as well

    """
    print('Generating population summaries')
    
    # Clean the column names 
    if clean_col_names:
        for df in [demographics, current_commits, prior_commits, merit_credit, milestone_credit, rehab_credit, voced_credit, rv_report]:
            df.columns = [utils.clean(col, remove = ['\n']) for col in df.columns]
    else:
        print('Since column names are not cleaned, several required variables for summary generation cannot be found')
    
    # Get demographics data of selected individuals and take a copy so the original dataframe is not modified
    df = demographics.loc[demographics[utils.clean(id_label)].isin(cdcr_nums)][:]
    
    # Remove string in disability column of demographics dataset
    df['dppv disability - mobility'] = df['dppv disability - mobility'].str.replace('Impacting Placement', '')
    
    # Generate summaries of individuals who are selected
    summary = helpers.gen_summary(df = df, 
                                  id_label = utils.clean(id_label),
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
        if write_path: 
            pass
        else: 
            write_path = '/'.join(l for l in [read_path, county_name, month, 'output', 'date of execution', utils.get_todays_date(sep = '_')] if l)
            
        # If directory does not exist, then first create it
        if not os.path.exists(write_path):
            os.makedirs(write_path)
                
        # Write data to excel files
        summary.to_excel(write_path+'/'+pop_label+'_summary.xlsx', index = False)
        print('Summary of individuals written to: ', write_path+'/'+pop_label+'_summary.xlsx')
        
    return summary