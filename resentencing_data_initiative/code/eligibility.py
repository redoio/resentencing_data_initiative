# -*- coding: utf-8 -*-

from helpers import *
import rules
import pandas as pd
import numpy as np
import datetime
from tqdm import tqdm
import copy
import os



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

def gen_eligibility(demographics, 
                    sorting_criteria,
                    current_commits, 
                    prior_commits, 
                    eligibility_conditions,
                    pop,
                    read_path = None, 
                    county_name = None, 
                    month = None,
                    to_excel = False, 
                    write_path = None):
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
        If to_excel = True but write_path = None, data outputs are written to the county_name/month/output/date folder by default. To avoid this behavior, pass a value to write_path.
    
    Returns
    -------
    errors : pandas dataframe
        Data in the demographics dataframe for which time variables could not be computed
    el_cdcr_nums : list of strs
        List of CDCR numbers that are eligible for resentencing 
    """
    
def eligibility_r1(demographics, 
                   sorting_criteria,
                   current_commits, 
                   prior_commits, 
                   eligibility_conditions,
                   el_cdcr_nums = None):
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
    el_cdcr_nums: list
        CDCR numbers that already meet eligibility conditions. Only these CDCR numbers will be evaluated under the current rule. 
        Default is None.
    Returns
    -------
    errors : pandas dataframe
        Data in the demographics dataframe for which time variables could not be computed
    el_cdcr_nums : list of strs
        List of CDCR numbers that are eligible for resentencing 
        
    """
    # If existing eligible CDCR numbers are passed
    if el_cdcr_nums:
        # Extracting CDCR numbers with eligible ages
        print('Finding CDCR numbers that meet rule: ', eligibility_conditions['r_1']['desc'])
        el_cdcr_nums = demographics[(demographics['Age in years'] >= 50) & (demographics['CDCR #'].isin(el_cdcr_nums))]['CDCR #'].to_list()
    # If this is the first eligibility condition being checked
    else:
        print('Finding CDCR numbers that meet rule: ', eligibility_conditions['r_1']['desc'])
        # Extracting CDCR numbers with eligible ages
        el_cdcr_nums = []
        el_cdcr_nums = demographics[(demographics['Age in years'] >= 50)]['CDCR #'].to_list()
    return el_cdcr_nums


def eligibility_r2(demographics, 
                    sorting_criteria,
                    current_commits, 
                    prior_commits, 
                    eligibility_conditions,
                    el_cdcr_nums = None):
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
    el_cdcr_nums: list
        CDCR numbers that already meet eligibility conditions. Only these CDCR numbers will be evaluated under the current rule. 
        Default is None.
    Returns
    -------
    errors : pandas dataframe
        Data in the demographics dataframe for which time variables could not be computed
    el_cdcr_nums : list of strs
        List of CDCR numbers that are eligible for resentencing 
        
    """
    # If existing eligible CDCR numbers are passed
    if el_cdcr_nums:
        # Extracting CDCR numbers that met the age criteria that also meet the time sentenced criteria
        print('Finding CDCR numbers that meet rule: ', eligibility_conditions['r_2']['desc'])
        el_cdcr_nums = demographics[(demographics['Aggregate sentence in years'] >= 20) & (demographics['CDCR #'].isin(el_cdcr_nums))]['CDCR #'].to_list()
    else:
        print('Finding CDCR numbers that meet rule: ', eligibility_conditions['r_2']['desc'])
        el_cdcr_nums = []
        el_cdcr_nums = demographics[(demographics['Aggregate sentence in years'] >= 20)]['CDCR #'].to_list()

    return el_cdcr_nums


def eligibility_r3(demographics, 
                   sorting_criteria,
                   current_commits, 
                   prior_commits, 
                   eligibility_conditions,
                   el_cdcr_nums = None):
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
    el_cdcr_nums: list
        CDCR numbers that already meet eligibility conditions. Only these CDCR numbers will be evaluated under the current rule. 
        Default is None.
    Returns
    -------
    errors : pandas dataframe
        Data in the demographics dataframe for which time variables could not be computed
    el_cdcr_nums : list of strs
        List of CDCR numbers that are eligible for resentencing 
        
    """
    print('Finding CDCR numbers that meet rule: ', eligibility_conditions['r_3']['desc'])
    # If existing eligible CDCR numbers are passed
    if el_cdcr_nums:
        # Extracting CDCR numbers that met the age criteria that also meet the time served criteria
        el_cdcr_nums = demographics[(demographics['Time served in years'] >= 10) & demographics['CDCR #'].isin(el_cdcr_nums)]['CDCR #'].to_list() 
    else:
        el_cdcr_nums = demographics[(demographics['Time served in years'] >= 10)]['CDCR #'].to_list() 
    return el_cdcr_nums


def eligibility_r4(demographics, 
                   sorting_criteria,
                   current_commits, 
                   prior_commits, 
                   eligibility_conditions,
                   el_cdcr_nums = None):
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
    el_cdcr_nums: list
        CDCR numbers that already meet eligibility conditions. Only these CDCR numbers will be evaluated under the current rule. 
        Default is None.
    
    Returns
    -------
    errors : pandas dataframe
        Data in the demographics dataframe for which time variables could not be computed
    el_cdcr_nums : list of strs
        List of CDCR numbers that are eligible for resentencing 
        
    """
    print('Finding CDCR numbers that meet rule: ', eligibility_conditions['r_4']['desc'])
    # Extracting ineligible offenses from sorting criteria
    inel_offenses = sorting_criteria[sorting_criteria['Table'].isin(['Table A', 'Table B', 'Table C', 'Table D'])]['Offenses'].tolist()
    # Appending new offenses based on implied ineligibility
    inel_offenses = gen_inel_off(inel_offenses, 
                                 clean = True, 
                                 impl = eligibility_conditions['r_4']['implied ineligibility'], 
                                 perm = eligibility_conditions['r_4']['perm'])
    
    # If existing eligible CDCR numbers are passed
    if el_cdcr_nums:
        eval_cdcr_nums = el_cdcr_nums
    else:
        eval_cdcr_nums = demographics['CDCR #'].unqiue()
    
    # Initialize list to capture eligible CDCR numbers
    el_cdcr_nums_4 = []
    # Loop through all the CDCR numbers to evaluate eligibility
    for cdcr_num in tqdm(eval_cdcr_nums):
        # Extract offenses of the CDCR number
        offenses = current_commits[current_commits['CDCR #'] == cdcr_num]['Offense cleaned']
        if len(det_inel_off(offenses = offenses, inel_offenses = inel_offenses)) == 0:
            el_cdcr_nums_4.append(cdcr_num)
    # Store eligible CDCR numbers
    el_cdcr_nums = el_cdcr_nums_4
    
    return el_cdcr_nums
    

def eligibility_r5(demographics, 
                    sorting_criteria,
                    current_commits, 
                    prior_commits, 
                    eligibility_conditions,
                    el_cdcr_nums = None):
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
    el_cdcr_nums: list
        CDCR numbers that already meet eligibility conditions. Only these CDCR numbers will be evaluated under the current rule. 
        Default is None.
    
    Returns
    -------
    errors : pandas dataframe
        Data in the demographics dataframe for which time variables could not be computed
    el_cdcr_nums : list of strs
        List of CDCR numbers that are eligible for resentencing 
        
    """
    print('Finding CDCR numbers that meet rule: ', eligibility_conditions['r_5']['desc'])
    # Extracting ineligible offenses from sorting criteria
    inel_offenses = sorting_criteria[sorting_criteria['Table'].isin(['Table C', 'Table D'])]['Offenses'].tolist()
    # Appending new offenses based on implied ineligibility
    inel_offenses = gen_inel_off(inel_offenses, 
                                 clean = True, 
                                 impl = eligibility_conditions['r_5']['implied ineligibility'], 
                                 perm = eligibility_conditions['r_5']['perm'])
    
    # If existing eligible CDCR numbers are passed
    if el_cdcr_nums:
        eval_cdcr_nums = el_cdcr_nums
    else:
        eval_cdcr_nums = demographics['CDCR #'].unqiue()
    
    # Initialize list to capture eligible CDCR numbers
    el_cdcr_nums_5 = []
    for cdcr_num in tqdm(eval_cdcr_nums):
        # Extract offenses of the CDCR number
        offenses = prior_commits[prior_commits['CDCR #'] == cdcr_num]['Offense cleaned']
        if len(det_inel_off(offenses = offenses, inel_offenses = inel_offenses)) == 0:
            el_cdcr_nums_5.append(cdcr_num)
    # Store eligible CDCR numbers
    el_cdcr_nums = el_cdcr_nums_5
    
    return el_cdcr_nums


def eligibility_r6(demographics, 
                    sorting_criteria,
                    current_commits, 
                    prior_commits, 
                    eligibility_conditions,
                    el_cdcr_nums = None):
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
    el_cdcr_nums: list
        CDCR numbers that already meet eligibility conditions. Only these CDCR numbers will be evaluated under the current rule. 
        Default is None.
    
    Returns
    -------
    errors : pandas dataframe
        Data in the demographics dataframe for which time variables could not be computed
    el_cdcr_nums : list of strs
        List of CDCR numbers that are eligible for resentencing 
        
    """        
    # If existing eligible CDCR numbers are passed
    if el_cdcr_nums:
        print('Finding CDCR numbers that meet rule: ', eligibility_conditions['r_6']['desc'])
        # Extracting CDCR numbers that meet the age criteria
        el_cdcr_nums = demographics[(demographics['Age during offense'] < 16) & (demographics['Age during offense'] >= 14) & (demographics['CDCR #'].isin(el_cdcr_nums))]['CDCR #'].to_list()
    else:
        el_cdcr_nums = demographics[(demographics['Age during offense'] < 16) & (demographics['Age during offense'] >= 14)]['CDCR #'].to_list()

    return el_cdcr_nums


def eligibility_r7(demographics, 
                    sorting_criteria,
                    current_commits, 
                    prior_commits, 
                    eligibility_conditions,
                    el_cdcr_nums = None):
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
    el_cdcr_nums: list
        CDCR numbers that already meet eligibility conditions. Only these CDCR numbers will be evaluated under the current rule. 
        Default is None.
    
    Returns
    -------
    errors : pandas dataframe
        Data in the demographics dataframe for which time variables could not be computed
    el_cdcr_nums : list of strs
        List of CDCR numbers that are eligible for resentencing 
        
    """        
    print('Finding CDCR numbers that meet rule: ', eligibility_conditions['r_7']['desc'])
    # Extracting ineligible offenses from sorting criteria
    inel_offenses = sorting_criteria[sorting_criteria['Table'].isin(['Table E', 'Table D'])]['Offenses'].tolist()
    inel_offenses = gen_inel_off(inel_offenses, 
                                 clean = True, 
                                 impl = eligibility_conditions['r_7']['implied ineligibility'], 
                                 perm = eligibility_conditions['r_7']['perm'])
    
    # If existing eligible CDCR numbers are passed
    if el_cdcr_nums:
        eval_cdcr_nums = el_cdcr_nums
    else:
        eval_cdcr_nums = demographics['CDCR #'].unqiue()
        
    # Extracting CDCR numbers that meet the age criteria and offense eligibility
    el_cdcr_nums_7 = []
    for cdcr_num in tqdm(eval_cdcr_nums):
        # Extracting offenses of the CDCR number
        offenses = current_commits[current_commits['CDCR #'] == cdcr_num]['Offense cleaned']
        if len(det_inel_off(offenses = offenses, inel_offenses = inel_offenses)) == 0:
            el_cdcr_nums_7.append(cdcr_num)
    
    # Store eligible CDCR numbers
    el_cdcr_nums = el_cdcr_nums_7
    
    return el_cdcr_nums


def eligibility_r8(demographics, 
                   sorting_criteria,
                   current_commits, 
                   prior_commits, 
                   eligibility_conditions,
                   el_cdcr_nums = None):
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
    el_cdcr_nums: list
        CDCR numbers that already meet eligibility conditions. Only these CDCR numbers will be evaluated under the current rule. 
        Default is None.
    
    Returns
    -------
    errors : pandas dataframe
        Data in the demographics dataframe for which time variables could not be computed
    el_cdcr_nums : list of strs
        List of CDCR numbers that are eligible for resentencing 
        
    """
    print('Finding CDCR numbers that meet rule: ', eligibility_conditions['r_9']['desc'])
    # Extracting ineligible offenses from sorting criteria
    inel_offenses = sorting_criteria[sorting_criteria['Table'].isin(['Table D'])]['Offenses'].tolist()
    inel_offenses = gen_inel_off(inel_offenses, 
                                 clean = True, 
                                 impl = eligibility_conditions['r_9']['implied ineligibility'], 
                                 perm = eligibility_conditions['r_9']['perm'])
    
    # If existing eligible CDCR numbers are passed
    if el_cdcr_nums:
        eval_cdcr_nums = el_cdcr_nums
    else:
        eval_cdcr_nums = demographics['CDCR #'].unqiue()
        
    # Extracting CDCR numbers that met the age, time sentenced and current and prior offense eligibility criteria
    el_cdcr_nums_9 = []
    for cdcr_num in tqdm(eval_cdcr_nums):
       offenses = prior_commits[prior_commits['CDCR #'] == cdcr_num]['Offense cleaned']
       if len(det_inel_off(offenses = offenses, inel_offenses = inel_offenses)) == 0:
           el_cdcr_nums_9.append(cdcr_num)
    # Store eligible CDCR numbers in cohort 2 or juvenile population
    el_cdcr_nums = el_cdcr_nums_9
    
    return el_cdcr_nums


def eligibility_r9(demographics, 
                   sorting_criteria,
                   current_commits, 
                   prior_commits, 
                   eligibility_conditions,
                   el_cdcr_nums = None):
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
    el_cdcr_nums: list
        CDCR numbers that already meet eligibility conditions. Only these CDCR numbers will be evaluated under the current rule. 
        Default is None.
    
    Returns
    -------
    errors : pandas dataframe
        Data in the demographics dataframe for which time variables could not be computed
    el_cdcr_nums : list of strs
        List of CDCR numbers that are eligible for resentencing 
        
    """
    print('Finding CDCR numbers that meet rule: ', eligibility_conditions['r_10']['desc'])
    # Extracting specified offenses from sorting criteria
    sel_offenses = sorting_criteria[sorting_criteria['Table'].isin(['Table F'])]['Offenses'].tolist()
    sel_offenses = clean_offense_blk(data = sel_offenses)
    
    # If existing eligible CDCR numbers are passed
    if el_cdcr_nums:
        eval_cdcr_nums = el_cdcr_nums
    else:
        eval_cdcr_nums = demographics['CDCR #'].unqiue()
        
    # Extracting CDCR numbers that meet the age criteria and offense eligibility
    el_cdcr_nums_10 = []
    for cdcr_num in tqdm(eval_cdcr_nums):
        # Extracting offenses of the CDCR number
        offenses = current_commits[current_commits['CDCR #'] == cdcr_num]['Offense cleaned']
        if len(set(offenses).intersection(set(sel_offenses))) >= 1:
            el_cdcr_nums_10.append(cdcr_num)
    # Store eligible CDCR numbers
    el_cdcr_nums = el_cdcr_nums_10   
    
    return el_cdcr_nums


def eligibility_r10(demographics, 
                    sorting_criteria,
                    current_commits, 
                    prior_commits, 
                    eligibility_conditions,
                    el_cdcr_nums = None):
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
    el_cdcr_nums: list
        CDCR numbers that already meet eligibility conditions. Only these CDCR numbers will be evaluated under the current rule. 
        Default is None.
    
    Returns
    -------
    errors : pandas dataframe
        Data in the demographics dataframe for which time variables could not be computed
    el_cdcr_nums : list of strs
        List of CDCR numbers that are eligible for resentencing 
    
    """        
    print('Finding CDCR numbers that meet rule: ', eligibility_conditions['r_11']['desc'])
    
    # Extracting specified offenses from sorting criteria
    sel_offenses = sorting_criteria[sorting_criteria['Table'].isin(['Table G'])]['Offenses'].tolist()
    sel_offenses = clean_offense_blk(data = sel_offenses)
    
    # If existing eligible CDCR numbers are passed
    if el_cdcr_nums:
        eval_cdcr_nums = el_cdcr_nums
    else:
        eval_cdcr_nums = demographics['CDCR #'].unqiue()
        
    # Extracting CDCR numbers that meet the age criteria and offense eligibility
    el_cdcr_nums_11 = []
    for cdcr_num in tqdm(eval_cdcr_nums):
        # Extracting offenses of the CDCR number
        offenses = current_commits[current_commits['CDCR #'] == cdcr_num][['Offense cleaned', 'Off_Enh1 cleaned', 'Off_Enh2 cleaned', 'Off_Enh3 cleaned', 'Off_Enh4 cleaned']].values.flatten()
        if len(set(offenses).intersection(set(sel_offenses))) == 0:
            el_cdcr_nums_11.append(cdcr_num)
    # Store eligible CDCR numbers
    el_cdcr_nums = el_cdcr_nums_11 
    
    return el_cdcr_nums


def eligibility_r11(demographics, 
                    sorting_criteria,
                    current_commits, 
                    prior_commits, 
                    eligibility_conditions,
                    el_cdcr_nums = None):
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
    el_cdcr_nums: list
        CDCR numbers that already meet eligibility conditions. Only these CDCR numbers will be evaluated under the current rule. 
        Default is None.
    
    Returns
    -------
    errors : pandas dataframe
        Data in the demographics dataframe for which time variables could not be computed
    el_cdcr_nums : list of strs
        List of CDCR numbers that are eligible for resentencing 
    
    """        
    print('Finding CDCR numbers that meet rule: ', eligibility_conditions['r_12']['desc'])
    
    # Extracting specified offenses from sorting criteria
    sel_offenses = sorting_criteria[sorting_criteria['Table'].isin(['Table F'])]['Offenses'].tolist()
    sel_offenses = clean_offense_blk(data = sel_offenses)
    
    # If existing eligible CDCR numbers are passed
    if el_cdcr_nums:
        eval_cdcr_nums = el_cdcr_nums
    else:
        eval_cdcr_nums = demographics['CDCR #'].unqiue()
        
    # Extracting CDCR numbers that meet the age criteria and offense eligibility
    el_cdcr_nums_12 = []
    for cdcr_num in tqdm(eval_cdcr_nums):
        # Extracting offenses of the CDCR number
        controlling_offense = demographics[demographics['CDCR #'] == cdcr_num]['Controlling offense cleaned']
        if controlling_offense not in sel_offenses:
            el_cdcr_nums_12.append(cdcr_num)
    
    # Store eligible CDCR numbers
    el_cdcr_nums = el_cdcr_nums_12 
    
    return el_cdcr_nums
            

def gen_eligibility(demographics, 
                    sorting_criteria,
                    current_commits, 
                    prior_commits, 
                    eligibility_conditions,
                    pop,
                    read_path = None, 
                    county_name = None, 
                    month = None,
                    to_excel = False, 
                    write_path = None):
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
        If to_excel = True but write_path = None, data outputs are written to the county_name/month/output/date folder by default. To avoid this behavior, pass a value to write_path.
    
    Returns
    -------
    errors : pandas dataframe
        Data in the demographics dataframe for which time variables could not be computed
    el_cdcr_nums : list of strs
        List of CDCR numbers that are eligible for resentencing 
    """
    
    # Add all of the time variables to the demographic data necessary for classification - years served, sentence length, age, etc.
    demographics, errors = gen_time_vars(df = demographics, merge = True)
    
    # Initialize list of eligible CDCR numbers
    el_cdcr_nums = demographics['CDCR #']
    # Clean offense data and enhancements data in current commits   
    clean_offense_cols(df = current_commits, 
                       names = {'Offense': 'Offense cleaned',
                                'Off_Enh1': 'Off_Enh1 cleaned',
                                'Off_Enh2': 'Off_Enh2 cleaned',
                                'Off_Enh3': 'Off_Enh3 cleaned',
                                'Off_Enh4': 'Off_Enh4 cleaned'}, 
                       inplace = True)
    # Clean offense data and enhancements data in prior commits
    clean_offense_cols(df = prior_commits, 
                       names = {'Offense': 'Offense cleaned'}, 
                       inplace = True)
    # Clean offense data in demographics
    clean_offense_cols(df = demographics, 
                       names = {'Controlling Offense': 'Controlling offense cleaned'}, 
                       inplace = True)
    
    # Check all eligibility conditions
    if eligibility_conditions['r_1']['use']:
        # Extracting CDCR numbers with eligible ages
        el_cdcr_nums = eligibility_r1(demographics = demographics, 
                                      sorting_criteria = sorting_criteria,
                                      current_commits = current_commits, 
                                      prior_commits = prior_commits, 
                                      eligibility_conditions = eligibility_conditions,
                                      el_cdcr_nums = el_cdcr_nums)
        
    if eligibility_conditions['r_2']['use']:
        # Extracting CDCR numbers that met the age criteria that also meet the time sentenced criteria
        el_cdcr_nums = eligibility_r2(demographics = demographics, 
                                      sorting_criteria = sorting_criteria,
                                      current_commits = current_commits, 
                                      prior_commits = prior_commits, 
                                      eligibility_conditions = eligibility_conditions,
                                      el_cdcr_nums = el_cdcr_nums)
        
    if eligibility_conditions['r_3']['use']:
        # Extracting CDCR numbers that met the age criteria that also meet the time served criteria
        el_cdcr_nums = eligibility_r3(demographics = demographics, 
                                      sorting_criteria = sorting_criteria,
                                      current_commits = current_commits, 
                                      prior_commits = prior_commits, 
                                      eligibility_conditions = eligibility_conditions,
                                      el_cdcr_nums = el_cdcr_nums)
        
    if eligibility_conditions['r_4']['use']:
        el_cdcr_nums = eligibility_r4(demographics = demographics, 
                                      sorting_criteria = sorting_criteria,
                                      current_commits = current_commits, 
                                      prior_commits = prior_commits, 
                                      eligibility_conditions = eligibility_conditions,
                                      el_cdcr_nums = el_cdcr_nums)
        
    
    if eligibility_conditions['r_5']['use']:
        el_cdcr_nums = eligibility_r5(demographics = demographics, 
                                      sorting_criteria = sorting_criteria,
                                      current_commits = current_commits, 
                                      prior_commits = prior_commits, 
                                      eligibility_conditions = eligibility_conditions,
                                      el_cdcr_nums = el_cdcr_nums)
        
    if eligibility_conditions['r_6']['use']:
        el_cdcr_nums = eligibility_r6(demographics = demographics, 
                                      sorting_criteria = sorting_criteria,
                                      current_commits = current_commits, 
                                      prior_commits = prior_commits, 
                                      eligibility_conditions = eligibility_conditions,
                                      el_cdcr_nums = el_cdcr_nums)
        
    if eligibility_conditions['r_7']['use']:
        el_cdcr_nums = eligibility_r7(demographics = demographics, 
                                      sorting_criteria = sorting_criteria,
                                      current_commits = current_commits, 
                                      prior_commits = prior_commits, 
                                      eligibility_conditions = eligibility_conditions,
                                      el_cdcr_nums = el_cdcr_nums)
        
    if eligibility_conditions['r_8']['use']:
        el_cdcr_nums = eligibility_r9(demographics = demographics, 
                                      sorting_criteria = sorting_criteria,
                                      current_commits = current_commits, 
                                      prior_commits = prior_commits, 
                                      eligibility_conditions = eligibility_conditions,
                                      el_cdcr_nums = el_cdcr_nums)
        
    if eligibility_conditions['r_9']['use']:
        el_cdcr_nums = eligibility_r10(demographics = demographics, 
                                       sorting_criteria = sorting_criteria,
                                       current_commits = current_commits, 
                                       prior_commits = prior_commits, 
                                       eligibility_conditions = eligibility_conditions,
                                       el_cdcr_nums = el_cdcr_nums) 
        
    if eligibility_conditions['r_10']['use']:
        el_cdcr_nums = eligibility_r11(demographics = demographics, 
                                       sorting_criteria = sorting_criteria,
                                       current_commits = current_commits, 
                                       prior_commits = prior_commits, 
                                       eligibility_conditions = eligibility_conditions,
                                       el_cdcr_nums = el_cdcr_nums)
        
    if eligibility_conditions['r_11']['use']:
        el_cdcr_nums = eligibility_r12(demographics = demographics, 
                                       sorting_criteria = sorting_criteria,
                                       current_commits = current_commits, 
                                       prior_commits = prior_commits, 
                                       eligibility_conditions = eligibility_conditions,
                                       el_cdcr_nums = el_cdcr_nums)
    
    # Write demophraphics and current commits of eligible individuals to Excel output
    if to_excel:
        if write_path:
            pass
        else:
            write_path = '/'.join(l for l in [read_path, county_name, month, 'output', get_todays_date(sep = '_')] if l)
        
        # If directory does not exist, then first create it
        if not os.path.exists(write_path):
            os.mkdir(write_path)
            
        # Write data to excel files
        demographics[demographics['CDCR #'].isin(el_cdcr_nums)].to_excel(write_path+'/'+pop+'_eligible_demographics.xlsx', sheet_name = 'Cohort', index = False)
        current_commits[current_commits['CDCR #'].isin(el_cdcr_nums)].to_excel(write_path+'/'+pop+'_eligible_currentcommits.xlsx', sheet_name = 'Cohort', index = False)

        print('Current commits of eligible individuals written to: ', write_path+'/'+pop+'_eligible_currentcommits.xlsx')
        print('Demographics of eligible individuals written to: ', write_path+'/'+pop+'_eligible_demographics.xlsx')
    
    return errors, el_cdcr_nums
            
