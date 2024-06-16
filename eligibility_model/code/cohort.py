# -*- coding: utf-8 -*-

import helpers
import utils
import impl
from scenarios import rules
import pandas as pd
import numpy as np
import datetime
from tqdm import tqdm
import copy
import os
import multiprocessing
import itertools
import eligibility 

def gen_eligible_cohort(demographics, 
                        sorting_criteria,
                        current_commits, 
                        prior_commits, 
                        eligibility_conditions,
                        pop_label,
                        id_label,
                        comp_int,
                        clean_col_names = True,
                        read_path = None, 
                        county_name = None, 
                        month = None,
                        to_excel = False, 
                        write_path = None, 
                        parallel = True):
    """
    Parameters
    ----------
    sorting_criteria : pandas dataframe
        Data on offenses and their categories or tables
    demographics : pandas dataframe
        Data on individuals currently incarcerated
    current_commits : pandas dataframe
        Data on current offenses of incarcerated individuals wherein each row pertains to a single offense
    prior_commits : pandas dataframe
        Data on prior offenses of incarcerated individuals wherein each row pertains to a single offense
    eligibility_conditions : dict
        Data on all the rules, whether they should be applied or not and other specifications
    pop_label : str
        Label to add to file outputs
    id_label : str
        Name of the column with the CDCR IDs in the input data
    comp_int : list
        List with strings of the rule numbers in ascending order of computational intensity or demand
    clean_col_names : boolean, optional
        Specify whether to clean column names before running the eligibility model. Applies the utils.clean() function on the column headers
        Default is True
    data_path : str, optional
        Full path where output data should be written (all parent folders)
        Default is None.
    county_name : str, optional
        Name of the county for which eligibility was evaluated, ex: 'Los Angeles County'
        Default is None.
    month : str, optional
        Year and month for which eligibility was evaluated, ex: '2023_06'
        Default is None.
    to_excel : boolean, optional
        Specify whether to write current commitments and demographics of eligible individuals to Excel files.
        If True, specify the path information to write the output
        Default is False.
    write_path : str, optional 
        Specify the full path where the Excel outputs should be written. 
        If to_excel = True but write_path = None, data outputs are written to the 'county_name/month/output/date folder' by default. To avoid this behavior, pass a value to write_path.
    parallel : boolean, optional 
        Specify whether to perform the eligibility determination process using Python parallelization or not.
        Default is True.        

    Returns
    -------
    errors : pandas dataframe
        Data in the demographics dataframe for which time variables could not be computed
    el_cdcr_nums : list of strs
        List of CDCR numbers that are eligible for resentencing 
    """
    print('Starting data preparation steps for resentencing eligibility determination\n')
    
    # Clean the column names 
    if clean_col_names:
        for df in [demographics, current_commits, prior_commits]:
            df.columns = [utils.clean(col, remove = ['\n']) for col in df.columns]
        # Clean the CDCR ID label
        id_label = utils.clean(id_label)
    else:
        print('Since column names are not cleaned, the required variables for the eligibility model cannot be found\n')
        return
    
    print('Calculating necessary input time variables')
    # Add all of the time variables to the demographic data necessary for classification - years served, sentence length, age, etc.
    demographics, errors = helpers.gen_time_vars(df = demographics, 
                                                 id_label = id_label, 
                                                 merge = True, 
                                                 use_t_cols = ['birthday', 'aggregate sentence in months', 'offense end date'])    
    
    # Initialize list of CDCR numbers to be evaluated
    el_cdcr_nums = demographics[id_label].unique().tolist()
    
    print('\nCleaning offenses in enhancements of the current commits')
    # Clean offense data and enhancements data in current commits   
    utils.clean_blk(data = current_commits, 
                    names = {'offense': 'offense cleaned',
                             'off_enh1': 'off_enh1 cleaned',
                             'off_enh2': 'off_enh2 cleaned',
                             'off_enh3': 'off_enh3 cleaned',
                             'off_enh4': 'off_enh4 cleaned'}, 
                    inplace = True)
    print('Cleaning offenses in current, prior and controlling offense lists')
    # Clean offense data in prior commits
    utils.clean_blk(data = prior_commits, 
                    names = {'offense': 'offense cleaned'}, 
                    inplace = True)
    # Clean offense data in demographics
    utils.clean_blk(data = demographics, 
                    names = {'controlling offense': 'controlling offense cleaned'}, 
                    inplace = True)
    
    print('\nIdentifying individuals eligible for resentencing')
    print('This scenario is tagged with ', eligibility_conditions['lenience'], ' degree of leniency in the eligibility determination')
    print('The population in consideration belongs to the', pop_label, 'category\n')
    
    # Execute eligibility determination using parallelization
    if parallel: 
        partitions = multiprocessing.cpu_count()
        demographics_split = np.array_split(demographics, partitions)
        pool = multiprocessing.Pool(processes = partitions)
        results = [pool.apply_async(eligibility.apply_conditions, args = (ds, sorting_criteria, current_commits, prior_commits, eligibility_conditions, id_label)) for ds in demographics_split]
        pool.close()
        pool.join()
        el_cdcr_nums = [res.get() for res in results]
        #el_cdcr_nums = list(itertools.chain(*results))
    
    # Without parallelization
    else: 
        el_cdcr_nums = eligibility.apply_conditions(demographics = demographics, 
                                                    sorting_criteria = sorting_criteria,
                                                    current_commits = current_commits, 
                                                    prior_commits = prior_commits, 
                                                    eligibility_conditions = eligibility_conditions,
                                                    id_label = id_label)
    
    # Format date columns 
    _ = utils.format_date_blk(dfs = [demographics, current_commits, prior_commits], 
                              date_cols = ['birthday', 'offense end date', 'offense begin date', 'eprd/mepd', 'expected release date', 'release date'], 
                              how = '%m/%d/%Y', 
                              inplace = True, 
                              label = None)
    
    # Write demophraphics and current commits of eligible individuals to Excel output
    if to_excel:
        # If write path is specified in input
        if write_path:
            pass
        # Generate the write path based on the input path
        else:
            write_path = '/'.join(l for l in [read_path, county_name, month, 'output', 'date of execution', utils.get_todays_date(sep = '_')] if l)
        
        # If directory does not exist, then first create it
        if not os.path.exists(write_path):
            os.makedirs(write_path)
            
        # Write demographics data to excel file
        with pd.ExcelWriter(write_path+'/'+pop_label+'_eligible_demographics.xlsx') as writer:
            demographics[demographics[id_label].isin(el_cdcr_nums)].to_excel(writer, sheet_name = 'Cohort', index = False)
            pd.DataFrame.from_dict(utils.filter_dict(eligibility_conditions, 'r_'), orient='index').to_excel(writer, sheet_name = 'Conditions', index = True)
            pd.DataFrame.from_dict({'input': read_path, 'county name': county_name, 'month': month}, orient='index').to_excel(writer, sheet_name = 'Input', index = True)
        print('Demographics of eligible individuals written to: ', write_path+'/'+pop_label+'_eligible_demographics.xlsx\n')
        
        # Write current commits data to excel file
        with pd.ExcelWriter(write_path+'/'+pop_label+'_eligible_currentcommits.xlsx') as writer:
            current_commits[current_commits[id_label].isin(el_cdcr_nums)].to_excel(writer, sheet_name = 'Cohort', index = False)
            pd.DataFrame.from_dict(utils.filter_dict(eligibility_conditions, 'r_'), orient='index').to_excel(writer, sheet_name = 'Conditions', index = True)
            pd.DataFrame.from_dict({'input': read_path, 'county name': county_name, 'month': month}, orient='index').to_excel(writer, sheet_name = 'Input', index = True)
        print('Current commits of eligible individuals written to: ', write_path+'/'+pop_label+'_eligible_currentcommits.xlsx\n')
       
        # Write prior commits data to excel file
        with pd.ExcelWriter(write_path+'/'+pop_label+'_eligible_priorcommits.xlsx') as writer:
            prior_commits[prior_commits[id_label].isin(el_cdcr_nums)].to_excel(writer, sheet_name = 'Cohort', index = False)
            pd.DataFrame.from_dict(utils.filter_dict(eligibility_conditions, 'r_'), orient='index').to_excel(writer, sheet_name = 'Conditions', index = True)
            pd.DataFrame.from_dict({'input': read_path, 'county name': county_name, 'month': month}, orient='index').to_excel(writer, sheet_name = 'Input', index = True)
        print('Prior commits of eligible individuals written to: ', write_path+'/'+pop_label+'_eligible_priorcommits.xlsx\n')
    
    return errors, el_cdcr_nums