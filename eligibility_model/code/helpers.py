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
                  merge = True,
                  clean_col_names = True):
    """

    Parameters
    ----------
    df : pandas dataframe
        Dataframe containing all of the information needed to calculate the time variables for the incarcerated population
    id_label : str
        Name of column in df with CDCR IDs
    merge : boolean, optional
        Specify whether to concatenate the calculated time-variables in the input dataframe or store them in a separate dataframe.
        Default is True
    clean_col_names : boolean, optional
        Specify whether to clean column names. Applies the utils.clean() function on the column headers
        Default is True

    Returns
    -------
    df : pandas dataframe
        Dataframe with newly calculated time-variables (including the input dataframe if merge = True)
    errors : pandas dataframe
        Rows in input dataframe with errors in the calculation process

    """
    # Clean all the column names
    if clean_col_names:
        df.columns = [utils.clean(col, remove = ['\n']) for col in df.columns]
        id_label = utils.clean(id_label)
    else:
        print('Since column names are not cleaned, several required variables for summary generation cannot be found')
        
    # Check if all columns needed for calcualtion are present in the dataframe
    if all(col in df.columns for col in [id_label, 'birthday', 'aggregate sentence in months', 'offense end date']):
        print('Variables needed for calculation are present in demographics dataframe')
        pass
    else:
        print('Variables needed for calculation are missing in demographics dataframe. Calculation will continue for available variables')
        pass   
    
    # Get the present date
    present_date = datetime.datetime.now()
    # Sentence duration in years
    try: 
        df['aggregate sentence in years'] = df['aggregate sentence in months']/12
    except:
        df['aggregate sentence in years'] = None
    # Age of individual
    try:
        df['age in years'] = [x.days/365 for x in present_date - pd.to_datetime(df['birthday'], errors = 'coerce')]
    except:
        df['age in years'] = None
    # Sentence served in years
    try:
        df['time served in years'] = [x.days/365 for x in present_date - pd.to_datetime(df['offense end date'], errors = 'coerce')]
    except:
        df['time served in years'] = None
    # Age at the time of offense
    try:
        df['age during offense'] = [x.days/365 for x in pd.to_datetime(df['offense end date'], errors = 'coerce') - pd.to_datetime(df['birthday'], errors = 'coerce')]
    except:
        df['age during offense'] = None
        
    # Store all the time columns calculated above
    calc_t_cols = ['aggregate sentence in years', 'age in years', 'time served in years', 'age during offense']
  
    # Return the resulting dataframe with the calculated time columns and the data with NaN/NaTs in these columns
    
    # If time variables are to be added to the input dataframe
    if merge: 
        return df, utils.incorrect_time(df = df, cols = calc_t_cols)
    # If time variables are to be stored in a separate dataframe
    else:
        return df[[id_label, 'birthday', 'aggregate sentence in months', 'offense end date']+calc_t_cols], utils.incorrect_time(df = df, cols = calc_t_cols)
        

def gen_summary(cdcr_nums, 
                id_label, 
                current_commits, 
                prior_commits, 
                merit_credit, 
                milestone_credit,
                rehab_credit, 
                voced_credit, 
                rv_report, 
                clean_col_names = True):
    """

    Parameters
    ----------
    cdcr_nums : list
        List of CDCR numbers to generate summaries for
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
        Specify whether to clean column names. Applies the utils.clean() function on the column headers
        Default is True
        
    Returns
    -------
    df : pandas dataframe
        Data on convictions, rules violations, programming for each CDCR number passed in the input list

    """
    # Clean the column names in all input dataframes
    if clean_col_names:
        for df in [current_commits, prior_commits, merit_credit, milestone_credit, rehab_credit, voced_credit, rv_report]:
            df.columns = [utils.clean(col, remove = ['\n']) for col in df.columns]
        # Clean the id label
        id_label = utils.clean(id_label)
    else:
        print('Input column names are not cleaned, so the required variables for summary generation cannot be found')
    
    
    # Initialize lists for other variables
    current_conv = []
    prior_conv = []
    programming = []
    rvr = []
    
    # Get summary variables for each CDCR number
    for cn in cdcr_nums:
      # Current convictions
      current_conv.append(', '.join(current_commits[current_commits[id_label] == cn]['offense'].tolist()))
      # Previous convictions
      prior_conv.append(', '.join(prior_commits[prior_commits[id_label] == cn]['offense'].tolist()))
      # Participation in programming
      if (cn in merit_credit[id_label]) or (cn in milestone_credit[id_label]) or (cn in rehab_credit[id_label]) or (cn in voced_credit[id_label]):
        programming.append('Yes')
      else:
        programming.append('No')
      # Rule violation reports
      ext = rv_report[rv_report[id_label] == cn][['rule violation date', 'division', 'rule violation']].reset_index(drop = True).to_dict('index')
      rvr.append("\n\n".join("\n".join(k_b + ': ' + str(v_b) for k_b, v_b in v_a.items()) for k_a, v_a in ext.items()))
    
    # Initialize a dataframe to store the summaries of each CDCR number
    df = pd.DataFrame()
    # Store lists in dataframe
    df[id_label] = cdcr_nums
    df['current convictions'] = current_conv
    df['prior convictions'] = prior_conv
    df['programming'] = programming
    df['rules violations'] = rvr
    
    return df


def comp_output(read_path, comp_val, label, merge = True, clean_col_names = True, pop_label = None, to_excel = True, write_path = None):
    """

    Parameters
    ----------
    read_path : list of strs
        Paths with input dataframes to compare. Dataframe in the 0th position is evaluated against the remaining dataframes 
    comp_val : str
        Column name or variable to be compared
    label : list of strs
        Labels or tags to associate with each input. Should correspond 1:1 with the dataframes passed in read_path
    merge : boolean, optional
        Specify whether to return the differences only or with the input dataframe in 0th position. The default is True.
    clean_col_names : boolean, optional
        Specify whether to clean the column name strings before any operations. The default is True.
    pop_label : str
        Label to add to file outputs
    to_excel : boolean, optional
        Specify whether to write the output to an Excel file. The default is True. If write_path is not passed but to_excel = True, output is stored in the read_path directory
    write_path : str, optional
        Specify the directory to which the output should be written. The default is None.

    Returns
    -------
    diff : pandas dataframe
        Dataframe with differences in the input

    """
    print('Comparing data in ', read_path[0], ' with data in : {}'.format(read_path[1:]))
    
    # Initialize list of dataframes to compare
    df_objs = []
    
    # Loop through input file paths to extract data
    for r in read_path:
        # Extract dataframe 
        df = pd.read_excel(r)
        # Clean all the column names
        if clean_col_names:
            df.columns = [utils.clean(col, remove = ['\n']) for col in df.columns]
            comp_val = utils.clean(comp_val)
        # Store dataframes in a list
        df_objs.append(df)
    
    # Get the missing values in comp_val
    diff = utils.df_diff(df_objs = df_objs, comp_val = comp_val, label = label)
    
    # Return the input dataframe or just the differences
    if merge:
        out = df_objs[0][df_objs[0][comp_val].isin(diff)]
    else: 
        out = diff
    
    # Generate write paths if excel output is requested
    if to_excel:
        if write_path: 
            pass
        else:
            write_path = "/".join(read_path[0].split("/")[0:-1])
    
        # If directory does not exist, then first create it
        if not os.path.exists(write_path):
            os.makedirs(write_path)
            
    # Write demographics data to excel file
    with pd.ExcelWriter(write_path+'/'+pop_label+'_differences.xlsx') as writer:
        out.to_excel(writer, sheet_name = 'Differences', index = False)
        pd.DataFrame(read_path, columns = ['comparison']).to_excel(writer, sheet_name = 'Input', index = True)
        print('Data differences written to: ', write_path+'/'+pop_label+'_differences.xlsx')
   

    