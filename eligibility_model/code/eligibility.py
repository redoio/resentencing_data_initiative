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

def viz(el_cdcr_nums,  
        id_label,
        demographics,
        current_commits):
    """

    Parameters
    ----------
    el_cdcr_nums : list of strs
        List of CDCR numbers that are eligible for resentencing
    demographics : pandas dataframe
        Data on demographics of both juveniles and adults
    current_commits : pandas dataframe
        Data on current offenses of incarcerated individuals wherein each row pertains to a single offense
    id_label : str
        Name of the column with the CDCR IDs    

    Returns
    -------
    None.

    """

    print('Top 20 offenses of individuals (from demographics data)')
    print(demographics[demographics[id_label].isin(el_cdcr_nums)]['Description'].value_counts()[0:20])

    print('Top 20 controlling offenses of individuals (from demographics data)')
    demographics[demographics[id_label].isin(el_cdcr_nums)]['Controlling Offense'].value_counts()[0:20]

    print('Top 20 current sentences of individuals (from current commits data)')
    current_commits[current_commits[id_label].isin(el_cdcr_nums)]['Offense'].value_counts()[0:20]

    print('Sex offenses')
    print(demographics[demographics[id_label].isin(el_cdcr_nums)]['Sex Registrant'].value_counts())

    print('Type of offenses')
    print(demographics[demographics[id_label].isin(el_cdcr_nums)]['Offense Category'].value_counts())

    return

    
def r_1(demographics, 
        sorting_criteria,
        current_commits, 
        prior_commits, 
        eligibility_conditions,
        id_label,
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
    id_label : str
        Name of the column with the CDCR IDs
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
    print('Finding CDCR numbers that meet rule: ', eligibility_conditions['r_1']['desc'])
    print('Rule category: ', eligibility_conditions['r_1']['category'])
    # If existing eligible CDCR numbers are passed
    if el_cdcr_nums:
        # Extracting CDCR numbers with eligible ages
        el_cdcr_nums = demographics[(demographics['age in years'] >= 50) & (demographics[id_label].isin(el_cdcr_nums))][id_label].to_list()
    # If this is the first eligibility condition being checked
    else:
        # Extracting CDCR numbers with eligible ages
        el_cdcr_nums = demographics[(demographics['age in years'] >= 50)][id_label].to_list()
    
    print('Count of CDCR numbers that meet rule is: ', len(el_cdcr_nums), '\n')
    
    return el_cdcr_nums


def r_2(demographics, 
        sorting_criteria,
        current_commits, 
        prior_commits, 
        eligibility_conditions,
        id_label,
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
    id_label : str
        Name of the column with the CDCR IDs
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
    print('Finding CDCR numbers that meet rule: ', eligibility_conditions['r_2']['desc'])
    print('Rule category: ', eligibility_conditions['r_2']['category'])
    
    # If existing eligible CDCR numbers are passed
    if el_cdcr_nums:
        # Extracting CDCR numbers that met the age criteria that also meet the time sentenced criteria
        el_cdcr_nums = demographics[(demographics['aggregate sentence in years'] >= 20) & (demographics[id_label].isin(el_cdcr_nums))][id_label].to_list()
    else:
        el_cdcr_nums = demographics[(demographics['aggregate sentence in years'] >= 20)][id_label].to_list()
    
    print('Count of CDCR numbers that meet rule is: ', len(el_cdcr_nums), '\n')
    
    return el_cdcr_nums


def r_3(demographics, 
        sorting_criteria,
        current_commits, 
        prior_commits, 
        eligibility_conditions,
        id_label,
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
    id_label : str
        Name of the column with the CDCR IDs    
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
    print('Rule category: ', eligibility_conditions['r_3']['category'])
    
    # If existing eligible CDCR numbers are passed
    if el_cdcr_nums:
        # Extracting CDCR numbers that met the age criteria that also meet the time served criteria
        el_cdcr_nums = demographics[(demographics['time served in years'] >= 10) & (demographics[id_label].isin(el_cdcr_nums))][id_label].to_list() 
    else:
        el_cdcr_nums = demographics[(demographics['time served in years'] >= 10)][id_label].to_list() 
    
    print('Count of CDCR numbers that meet rule is: ', len(el_cdcr_nums), '\n')
    
    return el_cdcr_nums


def r_4(demographics, 
        sorting_criteria,
        current_commits, 
        prior_commits, 
        eligibility_conditions,
        id_label,
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
    id_label : str
        Name of the column with the CDCR IDs    
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
    print('Rule category: ', eligibility_conditions['r_4']['category'])
    
    # Extracting ineligible offenses from sorting criteria
    inel_offenses = sorting_criteria[sorting_criteria['Table'].isin(['Table A', 'Table B', 'Table C', 'Table D'])]['Offenses'].tolist()
    # Appending new offenses based on implied ineligibility
    inel_offenses = impl.gen_impl_off(offenses = inel_offenses, 
                                      impl_rel = eligibility_conditions['r_4']['implied ineligibility'],
                                      perm = eligibility_conditions['r_4']['perm'], 
                                      fix_pos = None, 
                                      placeholder = None,
                                      how = 'inclusive',
                                      sep = '',
                                      clean = True)
    
    # If existing eligible CDCR numbers are passed
    if el_cdcr_nums:
        eval_cdcr_nums = el_cdcr_nums
    else:
        eval_cdcr_nums = demographics[id_label].unique()
    
    # Initialize list to capture eligible CDCR numbers
    el_cdcr_nums_4 = []
    # Loop through all the CDCR numbers to evaluate eligibility
    for cdcr_num in tqdm(eval_cdcr_nums):
        # Extract offenses of the CDCR number
        offenses = current_commits[current_commits[id_label] == cdcr_num]['offense cleaned']
        if len(utils.val_search(data = offenses, sel = inel_offenses)) == 0:
            el_cdcr_nums_4.append(cdcr_num)
    
    # Store eligible CDCR numbers
    el_cdcr_nums = el_cdcr_nums_4
    print('Count of CDCR numbers that meet rule is: ', len(el_cdcr_nums), '\n')
    
    return el_cdcr_nums
    

def r_5(demographics, 
        sorting_criteria,
        current_commits, 
        prior_commits, 
        eligibility_conditions,
        id_label,
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
    id_label : str
        Name of the column with the CDCR IDs    
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
    print('Rule category: ', eligibility_conditions['r_5']['category'])
    
    # Extracting ineligible offenses from sorting criteria
    inel_offenses = sorting_criteria[sorting_criteria['Table'].isin(['Table C', 'Table D'])]['Offenses'].tolist()
    # Appending new offenses based on implied ineligibility
    inel_offenses = impl.gen_impl_off(offenses = inel_offenses, 
                                      impl_rel = eligibility_conditions['r_5']['implied ineligibility'],
                                      perm = eligibility_conditions['r_5']['perm'], 
                                      fix_pos = None, 
                                      placeholder = None,
                                      how = 'inclusive',
                                      sep = '',
                                      clean = True)
    
    # If existing eligible CDCR numbers are passed
    if el_cdcr_nums:
        eval_cdcr_nums = el_cdcr_nums
    else:
        eval_cdcr_nums = demographics[id_label].unique()
    
    # Initialize list to capture eligible CDCR numbers
    el_cdcr_nums_5 = []
    for cdcr_num in tqdm(eval_cdcr_nums):
        # Extract offenses of the CDCR number
        offenses = prior_commits[prior_commits[id_label] == cdcr_num]['offense cleaned']
        if len(utils.val_search(data = offenses, sel = inel_offenses)) == 0:
            el_cdcr_nums_5.append(cdcr_num)
    
    # Store eligible CDCR numbers
    el_cdcr_nums = el_cdcr_nums_5
    print('Count of CDCR numbers that meet rule is: ', len(el_cdcr_nums), '\n')
    
    return el_cdcr_nums


def r_6(demographics, 
        sorting_criteria,
        current_commits, 
        prior_commits, 
        eligibility_conditions,
        id_label,
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
    id_label : str
        Name of the column with the CDCR IDs
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
    print('Finding CDCR numbers that meet rule: ', eligibility_conditions['r_6']['desc'])
    print('Rule category: ', eligibility_conditions['r_6']['category'])
    
    # If existing eligible CDCR numbers are passed
    if el_cdcr_nums:
        # Extracting CDCR numbers that meet the age criteria
        el_cdcr_nums = demographics[(demographics['age during offense'] < 16) & (demographics['age during offense'] >= 14) & (demographics[id_label].isin(el_cdcr_nums))][id_label].to_list()
    else:
        el_cdcr_nums = demographics[(demographics['age during offense'] < 16) & (demographics['age during offense'] >= 14)][id_label].to_list()
    
    print('Count of CDCR numbers that meet rule is: ', len(el_cdcr_nums), '\n')
    
    return el_cdcr_nums


def r_7(demographics, 
        sorting_criteria,
        current_commits, 
        prior_commits, 
        eligibility_conditions,
        id_label,
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
    id_label : str
        Name of the column with the CDCR IDs    
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
    print('Rule category: ', eligibility_conditions['r_7']['category'])
    
    # Extracting ineligible offenses from sorting criteria
    inel_offenses = sorting_criteria[sorting_criteria['Table'].isin(['Table E', 'Table D'])]['Offenses'].tolist()
    inel_offenses = impl.gen_impl_off(offenses = inel_offenses, 
                                      impl_rel = eligibility_conditions['r_7']['implied ineligibility'],
                                      perm = eligibility_conditions['r_7']['perm'], 
                                      fix_pos = None, 
                                      placeholder = None,
                                      how = 'inclusive',
                                      sep = '',
                                      clean = True)
    
    # If existing eligible CDCR numbers are passed
    if el_cdcr_nums:
        eval_cdcr_nums = el_cdcr_nums
    else:
        eval_cdcr_nums = demographics[id_label].unique()
        
    # Extracting CDCR numbers that meet the age criteria and offense eligibility
    el_cdcr_nums_7 = []
    for cdcr_num in tqdm(eval_cdcr_nums):
        # Extracting offenses of the CDCR number
        offenses = current_commits[current_commits[id_label] == cdcr_num]['offense cleaned']
        if len(utils.val_search(data = offenses, sel = inel_offenses)) == 0:
            el_cdcr_nums_7.append(cdcr_num)
    
    # Store eligible CDCR numbers
    el_cdcr_nums = el_cdcr_nums_7
    print('Count of CDCR numbers that meet rule is: ', len(el_cdcr_nums), '\n')
    
    return el_cdcr_nums


def r_8(demographics, 
        sorting_criteria,
        current_commits, 
        prior_commits, 
        eligibility_conditions,
        id_label,
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
    id_label : str
        Name of the column with the CDCR IDs    
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
    print('Finding CDCR numbers that meet rule: ', eligibility_conditions['r_8']['desc'])
    print('Rule category: ', eligibility_conditions['r_8']['category'])
    
    # Extracting ineligible offenses from sorting criteria
    inel_offenses = sorting_criteria[sorting_criteria['Table'].isin(['Table D'])]['Offenses'].tolist()
    inel_offenses = impl.gen_impl_off(offenses = inel_offenses, 
                                      impl_rel = eligibility_conditions['r_8']['implied ineligibility'],
                                      perm = eligibility_conditions['r_8']['perm'], 
                                      fix_pos = None, 
                                      placeholder = None,
                                      how = 'inclusive',
                                      sep = '',
                                      clean = True)
    
    # If existing eligible CDCR numbers are passed
    if el_cdcr_nums:
        eval_cdcr_nums = el_cdcr_nums
    else:
        eval_cdcr_nums = demographics[id_label].unique()
        
    # Extracting CDCR numbers that met the age, time sentenced and current and prior offense eligibility criteria
    el_cdcr_nums_8 = []
    for cdcr_num in tqdm(eval_cdcr_nums):
       offenses = prior_commits[prior_commits[id_label] == cdcr_num]['offense cleaned']
       if len(utils.val_search(data = offenses, sel = inel_offenses)) == 0:
           el_cdcr_nums_8.append(cdcr_num)
    
    # Store eligible CDCR numbers
    el_cdcr_nums = el_cdcr_nums_8
    print('Count of CDCR numbers that meet rule is: ', len(el_cdcr_nums), '\n')
    
    return el_cdcr_nums


def r_9(demographics, 
        sorting_criteria,
        current_commits, 
        prior_commits, 
        eligibility_conditions,
        id_label,
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
    id_label : str
        Name of the column with the CDCR IDs    
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
    print('Rule category: ', eligibility_conditions['r_9']['category'])
    
    # Extracting specified offenses from sorting criteria
    sel_offenses = sorting_criteria[sorting_criteria['Table'].isin(['Table F'])]['Offenses'].tolist()
    sel_offenses = impl.gen_impl_off(offenses = sel_offenses, 
                                     impl_rel = eligibility_conditions['r_9']['implied ineligibility'],
                                     perm = eligibility_conditions['r_9']['perm'], 
                                     fix_pos = eligibility_conditions['r_9']['fix positions'], 
                                     placeholder = eligibility_conditions['r_9']['placeholder'],
                                     how = 'inclusive',
                                     sep = '',
                                     clean = True)
    
    # If existing eligible CDCR numbers are passed
    if el_cdcr_nums:
        eval_cdcr_nums = el_cdcr_nums
    else:
        eval_cdcr_nums = demographics[id_label].unique()
        
    # Extracting CDCR numbers that meet the age criteria and offense eligibility
    el_cdcr_nums_9 = []
    for cdcr_num in tqdm(eval_cdcr_nums):
        # Extracting offenses of the CDCR number
        offenses = current_commits[current_commits[id_label] == cdcr_num]['offense cleaned']
        if len(utils.val_search(data = offenses, sel = sel_offenses)) >= 1:
            el_cdcr_nums_9.append(cdcr_num)
    
    # Store eligible CDCR numbers
    el_cdcr_nums = el_cdcr_nums_9   
    print('Count of CDCR numbers that meet rule is: ', len(el_cdcr_nums), '\n')
    
    return el_cdcr_nums


def r_10(demographics, 
         sorting_criteria,
         current_commits, 
         prior_commits, 
         eligibility_conditions,
         id_label,
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
    id_label : str
        Name of the column with the CDCR IDs    
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
    print('Rule category: ', eligibility_conditions['r_10']['category'])
    
    # Extracting specified offenses from sorting criteria
    sel_offenses = sorting_criteria[sorting_criteria['Table'].isin(['Table F'])]['Offenses'].tolist()
    sel_offenses = impl.gen_impl_off(offenses = sel_offenses, 
                                     impl_rel = eligibility_conditions['r_10']['implied ineligibility'],
                                     perm = eligibility_conditions['r_10']['perm'], 
                                     fix_pos = eligibility_conditions['r_10']['fix positions'], 
                                     placeholder = eligibility_conditions['r_10']['placeholder'],
                                     how = 'inclusive',
                                     sep = '',
                                     clean = True)
    
    # If existing eligible CDCR numbers are passed
    if el_cdcr_nums:
        eval_cdcr_nums = el_cdcr_nums
    else:
        eval_cdcr_nums = demographics[id_label].unique()
        
    # Extracting CDCR numbers that meet the age criteria and offense eligibility
    el_cdcr_nums_10 = []
    for cdcr_num in tqdm(eval_cdcr_nums):
        # Extracting offenses of the CDCR number
        controlling_offense = demographics[demographics[id_label] == cdcr_num]['controlling offense cleaned'].values[0]
        if controlling_offense in sel_offenses:
            el_cdcr_nums_10.append(cdcr_num)
    
    # Store eligible CDCR numbers
    el_cdcr_nums = el_cdcr_nums_10 
    print('Count of CDCR numbers that meet rule is: ', len(el_cdcr_nums), '\n')
    
    return el_cdcr_nums


def r_11(demographics, 
         sorting_criteria,
         current_commits, 
         prior_commits, 
         eligibility_conditions,
         id_label,
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
    id_label : str
        Name of the column with the CDCR IDs    
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
    print('Rule category: ', eligibility_conditions['r_11']['category'])
    
    # If existing eligible CDCR numbers are passed
    if el_cdcr_nums:
        eval_cdcr_nums = el_cdcr_nums
    else:
        eval_cdcr_nums = demographics[id_label].unique()
        
    # Extracting CDCR numbers that meet the age criteria and offense eligibility
    el_cdcr_nums_11 = []
    for cdcr_num in tqdm(eval_cdcr_nums):
        # Extracting offenses of the CDCR number
        offenses = current_commits[current_commits[id_label] == cdcr_num][['offense cleaned', 'off_enh1 cleaned', 'off_enh2 cleaned', 'off_enh3 cleaned', 'off_enh4 cleaned']].values.flatten()
        # If sel offenses is not in any of the offenses (contains and not matches exactly)
        if len(utils.val_search(data = offenses, sel = ['12022'], how = 'contains')) == 0:
            el_cdcr_nums_11.append(cdcr_num)
    
    # Store eligible CDCR numbers
    el_cdcr_nums = el_cdcr_nums_11 
    print('Count of CDCR numbers that meet rule is: ', len(el_cdcr_nums), '\n')
    
    return el_cdcr_nums


def r_12(demographics, 
         sorting_criteria,
         current_commits, 
         prior_commits, 
         eligibility_conditions,
         id_label,
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
    id_label : str
        Name of the column with the CDCR IDs    
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
    print('Rule category: ', eligibility_conditions['r_12']['category'])
    
    # Extracting ineligible offenses from sorting criteria
    inel_offenses = utils.clean_blk(sorting_criteria[sorting_criteria['Table'].isin(['Table A', 'Table B', 'Table C', 'Table D'])]['Offenses'].tolist())
    # Implied ineligible offenses for table F
    f_inel_offenses = impl.gen_impl_off(offenses = sorting_criteria[sorting_criteria['Table'] == 'Table F']['Offenses'].tolist(), 
                                        impl_rel = {'all': ['/att', '(664)', '2nd', "(ss)"]},
                                        perm = 4,                        
                                        fix_pos = {"2nd": 0, "(ss)": 0}, 
                                        placeholder = {"ss": ['a', 'b', 'c']}, 
                                        how = 'inclusive',
                                        clean = True, 
                                        sep = '')
    # Combining all ineligible offenses
    inel_offenses = list(set(inel_offenses).difference(set(f_inel_offenses)))
    
    # Generating implied offenses for baseline ineligible offenses and combining results
    inel_offenses = impl.gen_impl_off(offenses = inel_offenses, 
                                      impl_rel = eligibility_conditions['r_12']['implied ineligibility'],
                                      perm = eligibility_conditions['r_12']['perm'], 
                                      fix_pos = None, 
                                      placeholder = None,
                                      how = 'inclusive',
                                      sep = '',
                                      clean = True)
    
    # If existing eligible CDCR numbers are passed
    if el_cdcr_nums:
        eval_cdcr_nums = el_cdcr_nums
    else:
        eval_cdcr_nums = demographics[id_label].unique()
        
    # Extracting CDCR numbers that meet the age criteria and offense eligibility
    el_cdcr_nums_12 = []
    for cdcr_num in tqdm(eval_cdcr_nums):
        # Extracting offenses of the CDCR number
        offenses = current_commits[current_commits[id_label] == cdcr_num]['offense cleaned']
        if len(utils.val_search(data = offenses, sel = inel_offenses)) == 0:
            el_cdcr_nums_12.append(cdcr_num)
    
    # Store eligible CDCR numbers
    el_cdcr_nums = el_cdcr_nums_12
    print('Count of CDCR numbers that meet rule is: ', len(el_cdcr_nums), '\n')
    
    return el_cdcr_nums


def r_13(demographics, 
         sorting_criteria,
         current_commits, 
         prior_commits, 
         eligibility_conditions,
         id_label,
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
    id_label : str
        Name of the column with the CDCR IDs    
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
    print('Finding CDCR numbers that meet rule: ', eligibility_conditions['r_13']['desc'])
    print('Rule category: ', eligibility_conditions['r_13']['category'])
    
    # If existing eligible CDCR numbers are passed
    if el_cdcr_nums:
        el_cdcr_nums = demographics[(demographics['time served in years'] >= 15) & (demographics[id_label].isin(el_cdcr_nums))][id_label].to_list() 
    else:
        el_cdcr_nums = demographics[(demographics['time served in years'] >= 15)][id_label].to_list() 
    
    print('Count of CDCR numbers that meet rule is: ', len(el_cdcr_nums), '\n')
    
    return el_cdcr_nums


def apply_conditions(demographics, 
                     sorting_criteria,
                     current_commits, 
                     prior_commits, 
                     eligibility_conditions, 
                     comp_int,
                     id_label):
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
    id_label : str
        Name of the column with the CDCR IDs in the input data
    comp_int : list
        List with strings of the rule numbers in ascending order of computational intensity or demand

    Returns
    -------
    errors : pandas dataframe
        Data in the demographics dataframe for which time variables could not be computed
    """
    
    # Initialize list of CDCR numbers to be evaluated
    el_cdcr_nums = demographics[id_label].unique().tolist()
    
    # Check all eligibility conditions and execute in order of computational intensity
    for ci in comp_int:
        if eligibility_conditions[ci]['use']:
            el_cdcr_nums = globals()[ci](demographics = demographics, 
                                         sorting_criteria = sorting_criteria,
                                         current_commits = current_commits, 
                                         prior_commits = prior_commits, 
                                         eligibility_conditions = eligibility_conditions,
                                         id_label = id_label, 
                                         el_cdcr_nums = el_cdcr_nums)
    
    return el_cdcr_nums 
