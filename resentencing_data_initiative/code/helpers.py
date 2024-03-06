# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import datetime
from tqdm import tqdm
import copy
import os


def extract_data(main_path, county_name, file_name, month = None, write_path = None, pickle = False): 
    """

    Parameters
    ----------
    main_path : str
        Full path of the file to extract data from (all parent folders)
    county_name : str
        Name of the county folder to extract data from, ex: 'Los Angeles County'
    file_name : str
        Name of the .xlsx or .csv file to extract, ex: 'sorting_criteria.xlsx'
        File extension should be included 
    month : str, optional
        Year and month for which data should be extracted, ex: '2023_06'
    write_path : str, optional 
        Specify the full path where the pickle outputs should be written. 
        If pickle = True but write_path = None, data outputs are written to the county_name + month folder by default. To avoid this behavior, pass a value to write_path.
    pickle : boolean, optional
        Specify whether to store dataframe output as a pickle file or not
        Default is False.
        
    Returns
    -------
    df : pandas dataframe
        Dataframe using the file path and the pickle output if specified 

    """
    # Create the path to read data from (all inputs that are not NoneType)
    read_path = '/'.join(l for l in [main_path, county_name, month, file_name] if l)
    # Read into a dataframe
    df = pd.read_excel(read_path)
    print('Extracted data from: '+read_path)
    
    # If pickle output is specified
    if pickle:
        # If no write path is passed
        if not write_path:
            write_path = '/'.join(l for l in [main_path, county_name, month, file_name.split('.')[0]+'.pkl'] if l)
            df.to_pickle(write_path)
            print('Pickle outputs written to: '+write_path)
        elif write_path:
            df.to_pickle('/'.join([write_path, file_name.split('.')[0]+'.pkl']))
            print('Pickle outputs written to: '+ str('/'.join([write_path, file_name.split('.')[0]+'.pkl'])))
    return df


def gen_time_vars(df, merge = True):
    """

    Parameters
    ----------
    df : pandas dataframe
        Dataframe containing all of the information needed to calculate the time variables for the incarcerated population
    merge : boolean, optional
        Specify whether to concatenate the calculated time-variables in the input dataframe or store them in a separate dataframe.
        The default is True.

    Returns
    -------
    df : pandas dataframe
        Dataframe with newly calculated time-variables (including the input dataframe if merge = True)
    errors : pandas dataframe
        Rows in input dataframe with errors in the calculation process

    """
    # Check if all column variables needed for calcualtion are present in the dataframe
    if all(col in df.columns for col in ['CDCR #', 'Birthday', 'Aggregate Sentence in Months', 'Offense End Date']):
        pass
    else:
        print('Variables needed for calculation are missing in demographics dataframe')
        return   
    
    # Get the present date
    present_date = datetime.datetime.now()
    # Sentence duration in years
    df['Aggregate sentence in years'] = df['Aggregate Sentence in Months']/12
    # Age of individual
    df['Age in years'] = [x.days/365 for x in present_date - pd.to_datetime(df['Birthday'], errors = 'coerce')]
    # Sentence served in years
    df['Time served in years'] = [x.days/365 for x in present_date - pd.to_datetime(df['Offense End Date'], errors = 'coerce')]
    # Age at the time of offense
    df['Age during offense'] = [x.days/365 for x in pd.to_datetime(df['Offense End Date'], errors = 'coerce') - pd.to_datetime(df['Birthday'], errors = 'coerce')]
  
    # Store all data that have NaN/NaTs for any of the time columns calculated above
    def incorrect_time(df, 
                       cols = ['Aggregate sentence in years', 'Age in years', 'Time served in years', 'Age during offense']):
      # Initialize a dataframe to store the errors
      errors = pd.DataFrame()
      # Loop through all time columns that were calculated
      for col in cols:
        errors = pd.concat([errors, df[pd.isna(df[col])]])
      return errors
  
    # Return the resulting dataframe with the calculated time columns and the data with NaN/NaTs in these columns
    
    # If time variables are to be added to the input dataframe
    if merge: 
        return df, incorrect_time(df = df)
    # If time variables are to be stored in a separate dataframe
    else:
        return df[['CDCR #', 'Birthday', 'Aggregate Sentence in Months', 'Offense End Date',
                   'Aggregate sentence in years', 'Age in years', 'Time served in years', 'Age during offense']], incorrect_time(df = df)
     

def clean_offense(off):
    """

    Parameters
    ----------
    off : str
        A single offense value, ex: 'PC123 (a).(1).'

    Returns
    -------
    clean_off : str
        Lower-case string without trailing periods, spaces, 'PC' and 'Rape' text
        For example, the input string 'PC123 (a).(1).' will return '123(a).(1)'

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


def clean_offense_blk(data, inplace = None, names = None):
    """

    Parameters
    ----------
    data : str, list, pandas dataframe or pandas series
        Bulk data on offenses wherein each value is a single string
    names : dict
        Only applicable when input data is a pandas dataframe
        Contains key:value pairs wherein keys correspond to columns in the dataframe with offense data and values correspond to the modified columns
        Default is None
    inplace : boolean, optional
        Only applicable when input data is a pandas dataframe
        Specify whether to return a new dataframe or modify the existing one. 
        Default is None
        
    Returns
    -------
    data : str, list, pandas dataframe or pandas series (corresponding to input)
        Applies the clean_offense() function on each string in the input and returns the modified values with the same input type, i.e. if a pandas series is passed the result will be a pandas series with modified strings

    """
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
    
    # If input is a pandas dataframe
    elif isinstance(data, pd.DataFrame):
        # Modify the existing dataframe, i.e. add new columns
        if inplace:
            # Apply the cleaning function onto each column specified
            for col in names.keys():
                data[names[col]] = data[col].apply(clean_offense)
            return data
        # Create a separate dataframe with the modified columns and leave the existing one unchanged
        else:
            data_new = copy.deepcopy(data)
            # Apply the cleaning function onto each column specified
            for col in names.keys():
                data_new[names[col]] = data[col].apply(clean_offense)
            return data_new
        

def gen_impl_off(offenses, clean = True, 
                 impl = {'all': ["/att", "(664)", "2nd"], '459': ["/att", "(664)"]}, 
                 perm = 2):
    """

    Parameters
    ----------
    offenses : list, pandas series
        Contains strings of offenses, for example specific values from the sorting criteria Excel sheet
    clean : boolean, optional
        Specify whether to clean the offenses data first using the clean_offense() operation. 
        Default is True.
    impl : dict, optional
        Specify how the implied selections should be generated. 
        The key:value pair is set up as follows: 
        1. 'all' represents the general implied offenses. Values in offenses are concatenated with the strings corresponding to 'all' to generate the implied ones
        2. Any other key called out separately represents an exception to 'all'
        Default is {'all': ["/att", "(664)", "2nd"], '459': ["/att", "(664)"]}.
    perm : int, optional
        Specify the number of permutations in the implied offenses 
        For example, perm = 2 means that '459(664)/att', '459(664)(664)' etc. are also ineligible
        Default is 2.

    Returns
    -------
    offenses : list
        List of offenses including both the intial offenses passed in the input (with or without cleaning) and the implied offenses

    """
    # Clean the offense data if specified
    if clean:
        offenses = clean_offense_blk(offenses)
    
    # For a single permutation or round of implied offenses
    def impl_off():
      # Generate new list of offenses based on the implied criteria
      add = []
      # Loop through all offenses in the input offenses list
      for off in offenses:
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
      # Combine newly generated offenses to the list of existing offenses and return result
      return list(set.union(set(offenses), set(add)))
    
    # Generate permutations of the implied offenses
    i = 1
    while i <= perm:
      # Run the function to generate implied offenses
      offenses = impl_off()
      i = i + 1
    
    # Return the final results after all permutations
    return offenses


def det_sel_off(offenses, 
                sel_offenses, 
                how = 'exact'):
    """

    Parameters
    ----------
    offenses : list, pandas series
        Contains strings of offenses to be evaluated (i.e. whether they are ineligible for resentencing or not)
    sel_offenses : list, pandas series
        Contains strings of selected offenses we want to identify in the offenses data
    how : str
        Specifies if selection is based whether offenses exactly match or contains a value(s) in the sel_offenses
        Takes 'contains', 'exact' or None. Default is 'exact'
    Returns
    -------
    set
        The offenses in the input that match with the sel_offenses

    """
    if how == 'exact':
        # Return offenses that are present in sel_offenses
        return set(offenses).intersection(set(sel_offenses))
    elif how == 'contains':
        match = []
        for s in sel_offenses:
            for off in offenses:
                if s in off:
                    match.append(off)
        return match
        
      

def gen_summary(df, current_commits, prior_commits, merit_credit, 
                milestone_credit, rehab_credit, voced_credit, rv_report, merge = True):
    """

    Parameters
    ----------
    df : pandas dataframe
        Data with CDCR numbers to generate summaries for. This can be a dataframe of a single column with selected CDCR numbers or a dataframe with selected CDCR numbers including their demographics
    current_commits : pandas dataframe
        Data on current offenses of the incarcerated population
    prior_commits : pandas dataframe
        Data on prior offenses of the incarcerated population
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
    merge : boolean
        Specify whether to return input dataframe with summary columns or a separate dataframe with just the summary columns
        Default is True
        
    Returns
    -------
    df : pandas dataframe
        Data on convictions, rules violations, programming for each CDCR number passed in the input dataframe. If merge = True, this includes the input dataframe as well

    """
    # Initialize lists for other variables
    current_conv = []
    prior_conv = []
    programming = []
    rvr = []
    
    # Removing newline characters in rvr dataframe column name
    rv_report.rename(columns = {'Rule\nViolation\nDate': 'Rule Violation Date'}, inplace = True)
    
    # Get summary variables for each CDCR number
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
      ext = rv_report[rv_report['CDCR\nNumber'] == cdcr_num][['Rule Violation Date', 'Division', 'Rule Violation']].reset_index(drop = True).to_dict('index')
      rvr.append("\n\n".join("\n".join(k_b + ': ' + str(v_b) for k_b, v_b in v_a.items()) for k_a, v_a in ext.items()))
    
    # Store lists in dataframe
    df['Current Convictions'] = current_conv
    df['Prior Convictions'] = prior_conv
    df['Programming'] = programming
    df['Rules Violations'] = rvr
    
    # Return the input dataframe with summary variables
    if merge: 
        return df
    # Return only the summary variables
    else:
        return df[['CDCR #', 'Current Convictions', 'Prior Convictions', 'Programming', 'Rules Violations']]


def get_todays_date(order = ['year', 'month', 'day'], sep = ''):
    """

    Parameters
    ----------
    order : list, optional
        The order in which the yyyy, mm and dd should be concatenated.
        The default is ['year', 'month', 'day'] and results in yyyy[sep]mm[sep]dd
    sep : str, optional 
        The character to use to separate the year, month and day values
        Default is an empty string or no separator
    
    Returns
    -------
    td : str
        Concatenated month, day and year values with separators and in the order specified

    """
    # Initialize today's date
    td = []
    for val in order:
        if val[0] == 'y':
            td.append(str(datetime.date.today().year))
        if val[0] == 'm':
            td.append(str(datetime.date.today().month))
        # Better to use d in case user passes 'date' instead of 'day' in the order variable
        if val[0] == 'd':
            td.append(str(datetime.date.today().day))
    return sep.join(td)
    