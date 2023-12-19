# -*- coding: utf-8 -*-

from helpers import *
import pandas as pd
import numpy as np
import datetime
from tqdm import tqdm

""" 

Conditions for Qualification

Cohort 1

Adults

1.   Age 50 and older; AND
2.   Sentenced to 20 years or more; AND
3.   Served a minimum of 10 years in custody; AND
4.   Is not serving a current sentence for any offense listed in Table A, B, C, or D, AND
5.   Does not have a prior conviction for any offense listed in Tables C & D

Cohort 2

Minors Tried as Adults

1.   Sentenced for a crime that was committed at age 14 or 15; AND
2.   Not serving current sentence for any offense listed in Table D and E; AND
3. Has served a minimum of 10 years in custody; AND
4. Does not have a prior conviction for any offense listed in Table D.

"""

def gen_adult_eligibility(demographics, 
                          sorting_criteria,
                          current_commits, 
                          prior_commits, 
                          data_path = None, 
                          county_name = None, 
                          month = None,
                          to_excel = False, 
                          write_path = None):
    """

    Parameters
    ----------
    sorting_criteria : pandas dataframe
        Data on offenses and their categories
    demographics : pandas dataframe
        Data on individuals currently incarcerated
    current_commits : pandas dataframe
        Data on current offenses of incarcerated individuals wherein each row pertains to a single offense
    prior_commits : pandas dataframe
        Data on prior offenses of incarcerated individuals wherein each row pertains to a single offense
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
        If to_excel = True but write_path = None, data outputs are written to the county_name + month folder by default. To avoid this behavior, pass a value to write_path.
 

    Returns
    -------
    errors : pandas dataframe
        Data in the demographics dataframe for which time variables could not be computed
    adult_el_cdcr_nums : list of strs
        List of CDCR numbers that are eligible for resentencing 

    """
    # Add all of the time variables to the demographic data necessary for classification - years served, sentence length, age, etc.
    demographics, errors = gen_time_vars(df = demographics, merge = True)
    
    ####
    
    # Conditions to search: 1., 2. and 3. for Cohort 1
    
    print('Checking eligibility for Cohort 1: Adults')
    print('Checking eligibility for conditions 1, 2 and 3')
    # Extracting CDCR numbers with eligible ages
    el_cdcr_nums_1 = demographics[demographics['Age in years'] >= 50]['CDCR #']
    # Extracting CDCR numbers that met the age criteria that also meet the time sentenced criteria
    el_cdcr_nums_2 = demographics[(demographics['Aggregate sentence in years'] >= 20) & demographics['CDCR #'].isin(el_cdcr_nums_1)]['CDCR #']
    # Extracting CDCR numbers that met the age criteria that also meet the time served criteria
    el_cdcr_nums_3 = demographics[(demographics['Time served in years'] >= 10) & demographics['CDCR #'].isin(el_cdcr_nums_2)]['CDCR #']
    
    ####
    
    # Conditions to search: 4. for Cohort 1
    
    print('Checking eligibility for condition 4')
    # Extracting ineligible offenses from sorting criteria
    inel_offenses = sorting_criteria[sorting_criteria['Table'].isin(['Table A', 'Table B', 'Table C', 'Table D'])]['Offenses'].tolist()
    # Appending new offenses based on implied ineligibility for adult populations
    inel_offenses = gen_inel_off(inel_offenses, clean = True, 
                                 impl = {'all': ["/att", "(664)", "2nd"], '459': ["/att", "(664)"]})
    # Clean offense data in current commits file
    current_commits['Offense cleaned'] = clean_offense_blk(data = current_commits['Offense'])
    # Extracting current commits data with eligible offenses
    el_cdcr_nums_4 = []
    for cdcr_num in tqdm(el_cdcr_nums_3):
      # Extract offenses of the CDCR number
      offenses = current_commits[current_commits['CDCR #'] == cdcr_num]['Offense cleaned'].unique()
      if len(det_inel_off(offenses = offenses, inel_offenses = inel_offenses, pop = 'adult')) == 0:
        el_cdcr_nums_4.append(cdcr_num)
        
    ####
        
    # Conditions to search: 5. for Cohort 1
    
    print('Checking eligibility for condition 5')
    # Extracting ineligible offenses from sorting criteria
    inel_offenses = sorting_criteria[sorting_criteria['Table'].isin(['Table C', 'Table D'])]['Offenses'].tolist()
    # Appending new offenses based on implied ineligibility for adult populations
    inel_offenses = gen_inel_off(inel_offenses, clean = True, 
                                 impl = {'all': ["/att", "(664)", "2nd"], '459': ["/att", "(664)"]})
    # Clean offense data in prior commits file
    prior_commits['Offense cleaned'] = clean_offense_blk(data = prior_commits['Offense'])
    # Extracting prior commits data with eligible offenses
    el_cdcr_nums_5 = []
    for cdcr_num in tqdm(el_cdcr_nums_4):
      # Extract offenses of the CDCR number
      offenses = prior_commits[prior_commits['CDCR #'] == cdcr_num]['Offense cleaned'].unique()
      if len(det_inel_off(offenses = offenses, inel_offenses = inel_offenses, pop = 'adult')) == 0:
        el_cdcr_nums_5.append(cdcr_num)
        
    # Store eligible CDCR numbers in adult population
    adult_el_cdcr_nums = el_cdcr_nums_5
    print('Number of CDCR#s that are older than 50 years, sentenced to over 20 years, served over 10 years, have eligible current offenses and eligible prior offenses: ', len(adult_el_cdcr_nums))
    
    ####
    
    # Write demophraphics and current commits of eligible individuals to Excel output
    if to_excel:
        if not write_path:
            # Write data to excel files
            write_path = '/'.join(l for l in [data_path, county_name, month] if l)
            demographics[demographics['CDCR #'].isin(adult_el_cdcr_nums)].to_excel(write_path+'/'+'adult_eligible_demographics.xlsx', index = False)
            current_commits[current_commits['CDCR #'].isin(adult_el_cdcr_nums)].to_excel(write_path+'/'+'adult_eligible_currentcommits.xlsx', index = False)
        elif write_path:
            # Write data to excel files
            demographics[demographics['CDCR #'].isin(adult_el_cdcr_nums)].to_excel(write_path+'/'+'adult_eligible_demographics.xlsx', index = False)
            current_commits[current_commits['CDCR #'].isin(adult_el_cdcr_nums)].to_excel(write_path+'/'+'adult_eligible_currentcommits.xlsx', index = False)
        
    return errors, adult_el_cdcr_nums


def gen_juvenile_eligibility(demographics, 
                             sorting_criteria,
                             current_commits, 
                             prior_commits, 
                             data_path = None, 
                             county_name = None, 
                             month = None,
                             to_excel = False, 
                             write_path = None):
    """

    Parameters
    ----------
        
    sorting_criteria : pandas dataframe
        Data on offenses and their categories
    demographics : pandas dataframe
        Data on individuals currently incarcerated
    current_commits : pandas dataframe
        Data on current offenses of incarcerated individuals wherein each row pertains to a single offense
    prior_commits : pandas dataframe
        Data on prior offenses of incarcerated individuals wherein each row pertains to a single offense
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
        If to_excel = True but write_path = None, data outputs are written to the county_name + month folder by default. To avoid this behavior, pass a value to write_path.
 
    Returns
    -------
    errors : pandas dataframe
        Data in the demographics dataframe for which time variables could not be computed
    juvenile_el_cdcr_nums : list of strs
        List of CDCR numbers that are eligible for resentencing 

    """
    # Add all of the time variables to the demographic data necessary for classification - years served, sentence length, age, etc.
    demographics, errors = gen_time_vars(df = demographics, merge = True)
    
    ####
    
    # Conditions to search: 1. for Cohort 2
    
    print('Checking eligibility for Cohort 2: Minors tried as adults')
    print('Checking eligibility for condition 1')
    # Extracting CDCR numbers that meet the age criteria
    el_cdcr_nums_1 = []
    el_cdcr_nums_1 = demographics[(demographics['Age during offense'] < 16) & (demographics['Age during offense'] >= 14)]['CDCR #'].to_list()
    
    ####
        
    # Conditions to search: 2. for Cohort 2
    
    print('Checking eligibility for condition 2')
    # Extracting ineligible offenses from sorting criteria
    inel_offenses = sorting_criteria[sorting_criteria['Table'].isin(['Table E', 'Table D'])]['Offenses'].tolist()
    inel_offenses = gen_inel_off(inel_offenses, clean = True, impl = {'187': ["2nd", "(664)"]}, perm = 2)
    # Clean offense data in current commits file
    current_commits['Offense cleaned'] = clean_offense_blk(data = current_commits['Offense'])
    # Extracting CDCR numbers that meet the age criteria and offense eligibility
    el_cdcr_nums_2 = []
    for cdcr_num in tqdm(el_cdcr_nums_1):
      # Extracting offenses of the CDCR number
      offenses = current_commits[current_commits['CDCR #'] == cdcr_num]['Offense cleaned'].unique()
      if len(det_inel_off(offenses = offenses, inel_offenses = inel_offenses, pop = 'juvenile')) == 0:
        el_cdcr_nums_2.append(cdcr_num)
    
    ####
    
    # Conditions to search: 3. for Cohort 2
    
    print('Checking eligibility for condition 3')
    # Extracting CDCR numbers that met the age and offense criteria that also meet the time served criteria
    el_cdcr_nums_3 = []
    el_cdcr_nums_3 = demographics[(demographics['Time served in years'] >= 10) & demographics['CDCR #'].isin(el_cdcr_nums_2)]['CDCR #'].to_list()
    print('Number of CDCR#s that committed offenses at age 14 and 15, have eligible current offenses and served more than 10 years: ', len(el_cdcr_nums_3))
    
    ####
    
    # Conditions to search: 4. for Cohort 2
    
    print('Checking eligibility for condition 4')
    # Extracting ineligible offenses from sorting criteria
    inel_offenses = sorting_criteria[sorting_criteria['Table'].isin(['Table D'])]['Offenses'].tolist()
    inel_offenses = gen_inel_off(inel_offenses, clean = True, impl = {'187': ["2nd", "(664)"]}, perm = 2)
    # Clean offense data in current commits file
    prior_commits['Offense cleaned'] = clean_offense_blk(data = prior_commits['Offense'])
    # Extracting CDCR numbers that met the age, time sentenced and current and prior offense eligibility criteria
    el_cdcr_nums_4 = []
    for cdcr_num in tqdm(el_cdcr_nums_3):
      offenses = prior_commits[prior_commits['CDCR #'] == cdcr_num]['Offense cleaned'].unique()
      if len(det_inel_off(offenses = offenses, inel_offenses = inel_offenses, pop = 'juvenile')) == 0:
        el_cdcr_nums_4.append(cdcr_num)
    
    # Store eligible CDCR numbers in cohort 2 or juvenile population
    juvenile_el_cdcr_nums = el_cdcr_nums_4
    print('Number of CDCR#s that committed offenses at age 14 and 15, have eligible current and prior offenses, and served more than 10 years: ', len(juvenile_el_cdcr_nums))
    
    ####
    
    # Write demographics and current commits of eligible individuals to Excel output
    if to_excel:
        if not write_path:
            # Write data to excel files
            write_path = '/'.join(l for l in [data_path, county_name, month] if l)
            demographics[demographics['CDCR #'].isin(juvenile_el_cdcr_nums)].to_excel(write_path+'/'+'juvenile_eligible_demographics.xlsx', index = False)
            current_commits[current_commits['CDCR #'].isin(juvenile_el_cdcr_nums)].to_excel(write_path+'/'+'juvenile_eligible_currentcommits.xlsx', index = False)
        elif write_path:
            # Write data to excel files
            demographics[demographics['CDCR #'].isin(juvenile_el_cdcr_nums)].to_excel(write_path+'/'+'juvenile_eligible_demographics.xlsx', index = False)
            current_commits[current_commits['CDCR #'].isin(juvenile_el_cdcr_nums)].to_excel(write_path+'/'+'juvenile_eligible_currentcommits.xlsx', index = False)
    
    return errors, juvenile_el_cdcr_nums


def viz_eligibility(adult_el_cdcr_nums, 
                    juvenile_el_cdcr_nums, 
                    demographics):
    """

    Parameters
    ----------
    adult_el_cdcr_nums : list of strs
        List of CDCR numbers in cohort 1 for adults that are eligible for resentencing
    juvenile_el_cdcr_nums : list of strs
        List of CDCR numbers in cohort 2 for juveniles sentenced as adults that are eligible for resentencing
    demographics : pandas dataframe
        Data on demographics of both juveniles and adults

    Returns
    -------
    None.

    """
    
    # Adult eligible demographics
    print('Top 20 offenses of individuals in Cohort 1 who meet all 5 eligibility conditions (from demographics data)')
    print(demographics[demographics['CDCR #'].isin(adult_el_cdcr_nums)]['Description'].value_counts()[0:20])

    print('Top 20 offenses of individuals in Cohort 1 who meet all 5 eligibility conditions (from demographics data)')
    demographics[demographics['CDCR #'].isin(adult_el_cdcr_nums)]['Controlling Offense'].value_counts()[0:20]

    print('Top 20 offenses of individuals in Cohort 1 who meet all 5 eligibility conditions (from current commits data)')
    current_commits[current_commits['CDCR #'].isin(adult_el_cdcr_nums)]['Offense'].value_counts()[0:20]

    print('Sex offenses of individuals in Cohort 1 who meet all 5 eligibility conditions')
    print(demographics[demographics['CDCR #'].isin(adult_el_cdcr_nums)]['Sex Registrant'].value_counts())

    print('Type of offenses of individuals in Cohort 1 who meet all 5 eligibility conditions')
    print(demographics[demographics['CDCR #'].isin(adult_el_cdcr_nums)]['Offense Category'].value_counts())

    ####
    
    # Juvenile eligible demographics
    print('Top 20 offenses of individuals in Cohort 2 who meet all 4 eligibility conditions (from demographics data)')
    print(demographics[demographics['CDCR #'].isin(juvenile_el_cdcr_nums)]['Description'].value_counts()[0:20])
    
    print('Top 20 offenses of individuals in Cohort 2 who meet all 4 eligibility conditions (from demographics data)')
    demographics[demographics['CDCR #'].isin(juvenile_el_cdcr_nums)]['Controlling Offense'].value_counts()[0:20]
    
    print('Sex offenses of individuals in Cohort 2 who meet all 4 eligibility conditions')
    print(demographics[demographics['CDCR #'].isin(juvenile_el_cdcr_nums)]['Sex Registrant'].value_counts())
    
    print('Type of offenses of individuals in Cohort 2 who meet all 4 eligibility conditions')
    print(demographics[demographics['CDCR #'].isin(juvenile_el_cdcr_nums)]['Offense Category'].value_counts())
    
    return


