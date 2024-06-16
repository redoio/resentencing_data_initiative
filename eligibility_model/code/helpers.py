# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta
from tqdm import tqdm
import copy
import os
import utils

def verify_naming_convention(main_path, 
                             file_convention,
                             ext = '.xlsx',
                             county_name = None, 
                             month = None):
    """

    Parameters
    ----------
    main_path : str
        Folder path of the file to extract data from (all parent folders without file name)
    county_name : str
        Name of the county folder to extract data from, ex: 'Los Angeles County'
    file_convention : str
        Name of the .txt file from which the naming conventions should be extracted. Must be formatted as a numerical list with file names enclosed in single quotes, ex: "1. 'commitments.xlsx'"
        File extension of .txt should be included
    ext : str
        File extension of the file names to be checked, ex: '.xlsx', '.csv' etc. 
        Default is '.xlsx'
    month : str, optional
        Year and month for which data should be extracted, ex: '2023_06'. Default is None
    
    Returns 
    -------
    target_file_name : list of strs
        List of the targeted file names (read from the naming conventions file)
    true_file_name : list of strs
        List of the true file names (files existing in the directory)
    error : int
        Number of file names in the true_file_name list that are not present in the target_file_name list
        
    """
    # Get the target file names from the text file
    read_path = '/'.join(l for l in [main_path, county_name, file_convention] if l)
    f = open(read_path, "r")
    target_file_name = []
    for n in f.read().split("'"):
        if ext in n:
            target_file_name.append(n)
    
    # Get the true file names from the directory with the Excel data
    read_path = '/'.join(l for l in [main_path, county_name, month] if l)
    true_file_name = []
    error = 0
    for n in os.listdir(read_path):
        if ext in n:
            if n in target_file_name:
                pass
            else:
                print(f'{n} file name is missing or incorrect based on the target naming convention')
                error += 1
            true_file_name.append(n)
        
    return target_file_name, true_file_name, error
        

def extract_data(main_path, 
                 county_name, 
                 file_name = None, 
                 month = None, 
                 write_path = None, 
                 pickle = False): 
    """

    Parameters
    ----------
    main_path : str
        Folder path of the file to extract data from (all parent folders without file name)
    county_name : str
        Name of the county folder to extract data from, ex: 'Los Angeles County'
    file_name : str
        Name of the .xlsx or .csv file to extract, ex: 'sorting_criteria.xlsx'
        File extension should be included. Default is None
    month : str, optional
        Year and month for which data should be extracted, ex: '2023_06'. Default is None
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
                  use_t_cols, 
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
    use_t_cols : list of strs
        List of columns in input dataframe needed for time variable calculation
        
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
        print('Since column names are not cleaned, several required variables for time calculations cannot be found')
        return 
    
    # Add id to the columns needed for calculation 
    use_t_cols.append(id_label)
    # Check if all columns needed for calcualtion are present in the dataframe
    if all(col in df.columns for col in use_t_cols):
        print('Variables needed for time calculation are present in demographics dataframe')
        pass
    else:
        print('Variables needed for time calculation are missing in demographics dataframe. Calculation will continue for available variables')
        pass   
    
    # Get the present date
    present_date = datetime.datetime.now()
    
    # Sentence duration in years
    asy = []
    for i in range(0, len(df)):
        try:
            asy.append(round(df['aggregate sentence in months'][i]/12, 1))
        except:
            asy.append(None)
    df['aggregate sentence in years'] = asy
    print(" Calculation complete for: 'aggregate sentence in years'")
    
    # Age of individual
    ay = []
    for i in range(0, len(df)):
        try:
            x = (present_date - pd.to_datetime(df['birthday'][i])).days/365
            ay.append(round(x,1))
        except:
            ay.append(None)
    df['age in years'] = ay
    print(" Calculation complete for: 'age in years'")
    
    # Sentence served in years
    tsy = []
    for i in range(0, len(df)):
        try:
            x = (present_date - pd.to_datetime(df['offense end date'][i])).days/365
            tsy.append(round(x,1))
        except:
            tsy.append(None)
    df['time served in years'] = tsy
    print(" Calculation complete for: 'time served in years'")
    
    # Age at the time of offense
    ao = []
    for i in range(0, len(df)):
        try:
            x = (pd.to_datetime(df['offense end date'][i]) - pd.to_datetime(df['birthday'][i])).days/365
            ao.append(round(x,1))
        except:
            ao.append(None)
    df['age during offense'] = ao
    print(" Calculation complete for: 'age during offense'")
    
    # Expected release date
    est = []
    for i in range(0, len(df)):
        try:
            est.append(pd.to_datetime(df['offense end date'][i]) + relativedelta(months = df['aggregate sentence in months'][i]))
        except:
            est.append(None)
    df['expected release date'] = est
    print(" Calculation complete for: 'expected release date'")
        
    # Store all the time columns calculated above
    calc_t_cols = ['aggregate sentence in years', 'age in years', 'time served in years', 'age during offense', 'expected release date']
    
    # Return the resulting dataframe with the calculated time columns and the data with NaN/NaTs in these columns
    # If time variables are to be added to the entire input dataframe
    if merge: 
        return df, utils.incorrect_time(df = df, cols = calc_t_cols)
    # If time variables are to be stored in a separate dataframe
    else:
        return df[use_t_cols+calc_t_cols], utils.incorrect_time(df = df, cols = calc_t_cols)
        
    
def compare_output(read_path, comp_val, label, merge = True, clean_col_names = True, pop_label = None, to_excel = True, write_path = None):
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
    print('Comparing data in ', read_path[0], ' with data in : {}'.format(read_path[1:]), '\n')
    
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
        base_diff = df_objs[0][df_objs[0][comp_val].isin(diff[comp_val])]
    else: 
        base_diff = None
    
    # Generate write paths if excel output is requested
    if to_excel:
        if not write_path:
            write_path = "/".join(read_path[0].split("/")[0:-1])
    
        # If directory does not exist, then first create it
        if not os.path.exists(write_path):
            os.makedirs(write_path)
            
    # Write demographics data to excel file
    with pd.ExcelWriter(write_path+'/'+pop_label+'_differences.xlsx') as writer:
        diff.to_excel(writer, sheet_name = 'Differences', index = False)
        pd.DataFrame(read_path, columns = ['comparison']).to_excel(writer, sheet_name = 'Input', index = True)
        print('Data differences written to: ', write_path+'/'+pop_label+'_differences.xlsx\n')
   
    return diff, base_diff
    