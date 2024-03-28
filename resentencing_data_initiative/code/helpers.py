# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import datetime
from tqdm import tqdm
import copy
import os
import utils


def extract_data(main_path, 
                 county_name, 
                 file_name, 
                 month = None, 
                 write_path = None, 
                 pickle = False): 
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
        Specify the full path where the pickle outputs should be written (folder level)
        If pickle = True but write_path = None, data outputs are written to the county_name + month folder by default. To avoid this behavior, pass a value to write_path
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
            # Create a write path based on the inputs
            write_path = '/'.join(l for l in [main_path, county_name, month, 'input'] if l) 
            
            # If directory does not exist, then first create it
            if not os.path.exists(write_path):
                os.makedirs(write_path)                                              
            
            # Pickle the dataframe
            df.to_pickle(write_path+'/'+file_name.split('.')[0]+'.pkl')
            print('Pickled input written to: '+write_path+'/'+file_name.split('.')[0]+'.pkl')
        
        elif write_path:
            # If directory does not exist, then first create it
            if not os.path.exists(write_path+'/'+'input'):
                os.makedirs(write_path+'/'+'input')
            
            # Pickle the dataframe
            df.to_pickle('/'.join([write_path, 'input', file_name.split('.')[0]+'.pkl']))
            print('Pickled input written to: '+ str('/'.join([write_path, 'input', file_name.split('.')[0]+'.pkl'])))
    
    return df
  

def gen_time_vars(df, 
                  id_label, 
                  merge = True):
    """

    Parameters
    ----------
    df : pandas dataframe
        Dataframe containing all of the information needed to calculate the time variables for the incarcerated population
    id_label : str
        Name of column in df with CDCR IDs
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
    # Clean all the column names
    df.columns = [utils.clean(col, remove = ['\n']) for col in df.columns]
    
    # Check if all columns needed for calcualtion are present in the dataframe
    if all(col in df.columns for col in [utils.clean(id_label), 'birthday', 'aggregate sentence in months', 'offense end date']):
        pass
    else:
        print('Variables needed for calculation are missing in demographics dataframe')
        return   
    
    # Get the present date
    present_date = datetime.datetime.now()
    # Sentence duration in years
    df['aggregate sentence in years'] = df['aggregate sentence in months']/12
    # Age of individual
    df['age in years'] = [x.days/365 for x in present_date - pd.to_datetime(df['birthday'], errors = 'coerce')]
    # Sentence served in years
    df['time served in years'] = [x.days/365 for x in present_date - pd.to_datetime(df['offense end date'], errors = 'coerce')]
    # Age at the time of offense
    df['age during offense'] = [x.days/365 for x in pd.to_datetime(df['offense end date'], errors = 'coerce') - pd.to_datetime(df['birthday'], errors = 'coerce')]
  
    # Store all the time columns calculated above
    calc_t_cols = ['aggregate sentence in years', 'age in years', 'time served in years', 'age during offense']
  
    # Return the resulting dataframe with the calculated time columns and the data with NaN/NaTs in these columns
    
    # If time variables are to be added to the input dataframe
    if merge: 
        return df, utils.incorrect_time(df = df, cols = calc_t_cols)
    # If time variables are to be stored in a separate dataframe
    else:
        return df[[id_label, 'birthday', 'aggregate sentence in months', 'offense end date']+calc_t_cols], utils.incorrect_time(df = df, cols = calc_t_cols)
        

def gen_summary(df, 
                id_label, 
                current_commits, 
                prior_commits, 
                merit_credit, 
                milestone_credit,
                rehab_credit, 
                voced_credit, 
                rv_report, 
                clean_col_names = True,
                merge = True):
    """

    Parameters
    ----------
    df : pandas dataframe
        Data with CDCR numbers to generate summaries for. This can be a single column with selected CDCR numbers or a dataframe with selected CDCR numbers including other information
    id_label : str
        Name of the column with the CDCR IDs
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
    clean_col_names : boolean, optional
        Specify whether to clean column names before running the eligibility model. Applies the helpers.clean() function on the column headers
        Default is True
    merge : boolean
        Specify whether to return input dataframe with summary columns or a separate dataframe with just the summary columns
        Default is True
        
    Returns
    -------
    df : pandas dataframe
        Data on convictions, rules violations, programming for each CDCR number passed in the input dataframe. If merge = True, this includes the input dataframe as well

    """
    # Clean the column names 
    if clean_col_names:
        for df in [current_commits, prior_commits, merit_credit, milestone_credit, rehab_credit, voced_credit, rv_report]:
            df.columns = [utils.clean(col, remove = ['\n']) for col in df.columns]
    else:
        print('Since column names are not cleaned, several required variables for summary generation cannot be found')
    
    # Initialize lists for other variables
    current_conv = []
    prior_conv = []
    programming = []
    rvr = []
    
    # Get summary variables for each CDCR number
    for cdcr_num in df[utils.clean(id_label)]:
      # Current convictions
      current_conv.append(', '.join(current_commits[current_commits[utils.clean(id_label)] == cdcr_num]['offense'].tolist()))
      # Previous convictions
      prior_conv.append(', '.join(prior_commits[prior_commits[utils.clean(id_label)] == cdcr_num]['offense'].tolist()))
      # Participation in programming
      if (cdcr_num in merit_credit[utils.clean(id_label)]) or (cdcr_num in milestone_credit[utils.clean(id_label)]) or (cdcr_num in rehab_credit[utils.clean(id_label)]) or (cdcr_num in voced_credit[utils.clean(id_label)]):
        programming.append('Yes')
      else:
        programming.append('No')
      # Rule violation reports
      ext = rv_report[rv_report[utils.clean(id_label)] == cdcr_num][['rule violation date', 'division', 'rule violation']].reset_index(drop = True).to_dict('index')
      rvr.append("\n\n".join("\n".join(k_b + ': ' + str(v_b) for k_b, v_b in v_a.items()) for k_a, v_a in ext.items()))
    
    # Store lists in dataframe
    df['current convictions'] = current_conv
    df['prior convictions'] = prior_conv
    df['programming'] = programming
    df['rules violations'] = rvr
    
    # Return the input dataframe with summary variables
    if merge: 
        return df
    # Return only the summary variables
    else:
        return df[[utils.clean(id_label), 'current convictions', 'prior convictions', 'programming', 'rules violations']]

    