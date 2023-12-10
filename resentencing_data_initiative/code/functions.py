# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 18:07:35 2023

@author: apkom
"""
import pandas as pd
import numpy as np
import datetime
from tqdm import tqdm

# Functions
def extract_data(main_path, county_name, file_name, month = None): 
    """

    Parameters
    ----------
    main_path : str
        Full path of the file to extract data from (all parent folders)
    county_name : str
        Name of the county folder to extract data for, ex: 'Los Angeles County'
        Becomes a part of the file path
    file_name : str
        Name of the .xlsx or .csv file to extract, ex: 'sorting_criteria.xlsx'
    month : str, optional
        Year and month for which data should be extracted, ex: '2023_06'

    Returns
    -------
    df : pandas dataframe
        Dataframe with the data from the file path

    """
    # If the month parameter is passed
    if month: 
        sheet_name = '/'.join([main_path, county_name, month, file_name])
        df = pd.read_excel(sheet_name)
    else:
        sheet_name = '/'.join([main_path, county_name, file_name])
        df = pd.read_excel(sheet_name)
        
    return df


def gen_time_vars(demographics, merge = True):
    """

    Parameters
    ----------
    demographics : pandas dataframe
        Dataframe containing all the demographic information on the incarcerated population 
        Includes the time-variables required for calculation
    merge : boolean, optional
        Specify whether to incorporate the calculated time-variables in the demographics dataframe or store them in a separate dataframe.
        The default is True.

    Returns
    -------
    df : pandas dataframe
        Dataframe with newly calculated time-variables (includes the original demographics dataframe input if merge = True)
    errors : pandas dataframe
        Errors in calculation

    """
    # Check if all column variables needed for calcualtion are present in the dataframe
    if all(col in demographics.columns for col in ['CDCR #', 'Birthday', 'Aggregate Sentence in Months', 'Offense End Date']):
        pass
    else:
        print('Variables needed for calculation are missing in demographics dataframe')
        return
    
    # If time variables are to be added to the existing demographics dataframe
    if merge: 
        df = demographics
    # If time variables are to be stored in a separate dataframe
    else:
        df = pd.DataFrame()
        df['CDCR #'] = demographics['CDCR #']
    
    # Get the present date
    present_date = datetime.datetime.now()
    # Sentence duration in years
    df['Aggregate sentence in years'] = df['Aggregate Sentence in Months']/12
    # Age of individual
    df['Age in years'] = [x.days/365 for x in present_date - pd.to_datetime(demographics['Birthday'], errors = 'coerce')]
    # Sentence served in years
    df['Time served in years'] = [x.days/365 for x in present_date - pd.to_datetime(demographics['Offense End Date'], errors = 'coerce')]
    # Age at the time of offense
    df['Age during offense'] = [x.days/365 for x in pd.to_datetime(demographics['Offense End Date'], errors = 'coerce') - pd.to_datetime(demographics['Birthday'], errors = 'coerce')]
  
    # Store all data that have NaNs for any of the time columns calculated above
    def incorrect_time(df, 
                       cols = ['Aggregate sentence in years', 'Age in years', 'Time served in years', 'Age during offense']):
      # Initialize a dataframe to store the errors
      errors = pd.DataFrame()
      # Loop through all time columns that were calculated
      for col in cols:
        errors = pd.concat([errors, df[pd.isna(df[col])]])
      return errors
  
    # Return the resulting dataframe with the calculated time columns and the data with NaN/NaTs in these columns
    return df, incorrect_time(df = df)


def clean_offense(off):
    """

    Parameters
    ----------
    off : str
        A single offense value, ex: 'PC123 (a).(1).'

    Returns
    -------
    clean_off : str
        Lower-case string without trailing periods, spaces, 'PC' and 'Rape' text, ex: input of 'PC123 (a).(1).' returns '123(a).(1)'

    """
    # Lowercase all letters
    clean_off = str(off).lower()
    # Remove trailing periods
    clean_off = clean_off.rstrip('.')
    # Remove whitespace (any location)
    clean_off = clean_off.replace(' ', '')
    # Remove "PC" or penal code abbreviation
    clean_off = clean_off.replace('pc', '')
    # Remove "rape" which shows up in some offenses
    clean_off = clean_off.replace('rape', '')
    return clean_off


def clean_offense_blk(data):
  # If input is a single string
  if isinstance(data, str):
    return clean_offense(data)
  # If input is a list of strings
  elif isinstance(data, list):
    off_clean = []
    for off in data:
      off_clean.append(clean_offense(off))
    return off_clean
  # If input is a column of a pandas dataframe
  elif isinstance(data, pd.Series):
    return data.apply(clean_offense)


def gen_inel_off(inel_offenses, clean = True, 
                 impl = {'all': ["/att", "(664)", "2nd"], '459': ["/att", "(664)"]}, 
                 perm = 2):
  # Clean the offense data if specified
  if clean:
    inel_offenses = clean_offense_blk(inel_offenses)

  def gen_impl_off():
    # Generate new list of offenses based on the implied ineligibility
    add = []
    # Loop through all offenses in the ineligible offenses list
    for off in inel_offenses:
      # Check the two conditions: generic or exception
      matching = [key for key in impl.keys() if key in off]
      # If offense is not called out separately (exception)
      if (len(matching) == 0) and ('all' in impl.keys()):
        for impl_val in impl['all']:
          # If any additions are not already in the offense, ex: PC 123(664) does not need PC 123(664)(664) to be added
          if impl_val not in off:
            add.append(off+impl_val)
      # If offense is called out separately (exception)
      elif len(matching) != 0:
        for impl_val in impl[matching[0]]:
          # If any additions are not already in the offense, ex: PC 123(664) does not need PC 123(664)(664) to be added
          if impl_val not in off:
            add.append(off+impl_val)
    # Combine newly identified ineligible offenses to the list of existing ineligible offenses and return result
    return list(set.union(set(inel_offenses), set(add)))

  # Generate permutations of the ineligible offenses
  i = 1
  while i <= perm:
    # Run the function to generate implied ineligibility
    inel_offenses = gen_impl_off()
    i = i + 1

  # Return the final results after all permutations
  return inel_offenses


def det_inel_off(offenses, 
                 inel_offenses, 
                 pop = None):
    # Return offenses that are ineligible for adults and juveniles
    if pop == 'adult' or pop == 'juvenile':
      return set(offenses).intersection(set(inel_offenses))
    # If none of the conditions are met
    else:
      print('No offenses processed. Please double check inputs and re-run')
      

def gen_summary(df, current_commits, prior_commits, merit_credit, 
                milestone_credit, rehab_credit, voced_credit, rv_report, 
                write_path, to_excel = True):
    # Initialize lists for other variables
    current_conv = []
    prior_conv = []
    programming = []
    rvr = []
    for cdcr_num in df['CDCR #']:
      # Current convictions
      current_conv.append(', '.join(current_commits[current_commits['CDCR #'] == cdcr_num]['Offense'].tolist()))
      # Previous convictions
      prior_conv.append(', '.join(prior_commits[prior_commits['CDCR #'] == cdcr_num]['Offense'].tolist()))
      # Participation in programming
      if (cdcr_num in merit_credit['Cdcno']) or (cdcr_num in milestone_credit['Cdcno']) or (cdcr_num in rehab_credit['Cdcno']) or (cdcr_num in voced_credit['Cdcno']):
        programming.append('Yes')
      else:
        programming.append('No')
      # Rule violation reports
      rv_report.rename(columns = {'Rule\nViolation\nDate': 'Rule Violation Date'}, inplace = True)
      ext = rv_report[rv_report['CDCR\nNumber'] == cdcr_num][['Rule Violation Date', 'Division', 'Rule Violation']].reset_index(drop = True).to_dict('index')
      rvr.append("\n\n".join("\n".join(k_b + ': ' + str(v_b) for k_b, v_b in v_a.items()) for k_a, v_a in ext.items()))
    
    # Store lists in dataframe
    df['Current Convictions'] = current_conv
    df['Prior Convictions'] = prior_conv
    df['Programming'] = programming
    df['Rules Violations'] = rvr
    
    if to_excel:
        # Write data to excel files
        df.to_excel(write_path, index = False)
        
    return df