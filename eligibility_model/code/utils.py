# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import datetime
from tqdm import tqdm
import copy
import os

def filter_dict(dictn, txt, how = 'contains'):
    """
    
    Parameters
    ----------
    dictn : dictionary
        Input dictionary 
    txt : str
        Text to match and select keys in the input dictionary
    how : str, optional
        Accepts 'start', 'contains', 'end' for match location. Specify the location in which the text should be present in the dictionary key. The 'contains' option implies that the text can be present anywhere in the key. 
        Default is 'contains'
    
    Returns
    -------
    sel_dict : dictionary
        Subset of input dictionary in which the selected keys contain the specified text at the end, beginning or anywhere in the key

    """
    if how == 'start':
        sel_dict = {}
        for k in dictn.keys():
            if k[0:len(txt)] == txt:
                sel_dict[k] = dictn[k]
        return sel_dict
    elif how == 'contains':
        sel_dict = {}
        for k in dictn.keys():
            if k[0:len(txt)] in txt:
                sel_dict[k] = dictn[k]
        return sel_dict
    elif how == 'end':
        sel_dict = {}
        for k in dictn.keys():
            if k[len(k)-len(txt):] == txt:
                sel_dict[k] = dictn[k]
        return sel_dict
    else:
        print('Dictionary key selection method specified is not recognized')
        return
    
    
def incorrect_time(df, cols):
    """

    Parameters
    ----------
    df : pandas dataframe
        Dataframe with columns that are time-related values
    cols : list
        List of column names that contain time-related values

    Returns
    -------
    errors : pandas dataframe
        Rows of df in which ANY of the time-related columns have an error (NaN or NaT)

    """
    # Initialize a dataframe to store the errors
    errors = pd.DataFrame()
    # Loop through all time related columns 
    for col in cols:
        errors = pd.concat([errors, df[pd.isna(df[col])]])
    return errors


def clean(data, remove = ['pc', 'rape', '\n', ' ']):
    """

    Parameters
    ----------
    data : str
        A single string. Example: An offense value 'PC123 (A).(1).'
    
    remove : list, optional
        List of values to be removed from the input string. Default is ['pc', 'rape', '\n', ' ']
        
    Returns
    -------
    data : str
        Lower-case string without trailing periods and the contents specified in remove parameter
        For example, the input string 'PC123 (A).(1).' will return 'pc123(a).(1)'

    """
    # Lowercase all letters
    data = str(data).lower()
    # Remove trailing periods
    data = data.rstrip('.')
    # Remove info specified 
    for r in remove: 
        if r in data:
            data = data.replace(r, '')
    
    return data


def clean_blk(data, 
              inplace = False, 
              names = None):
    """

    Parameters
    ----------
    data : str, list, pandas dataframe or pandas series
        Bulk data with string contents to be cleaned
    names : dict, optional
        Only applicable when input data is a pandas dataframe
        Contains key:value pairs wherein keys correspond to the names of columns in the input dataframe that should be cleaned and values correspond to the new column names
        Default is None. All columns will be cleaned and the suffix ' cleaned' will be attached to the new column names
    inplace : boolean, optional
        Only applicable when input data is a pandas dataframe. Specify whether to return a new and separate dataframe or modify the existing one
        Default is False
        
    Returns
    -------
    data : str, list, pandas dataframe or pandas series (corresponding to input data)
        Applies the clean() function on each string in the input and returns the modified values with the same input type, i.e. if a pandas series is passed the result will be a pandas series with modified strings

    """
    # If input is a single string
    if isinstance(data, str):
        return clean(data)
    
    # If input is a list of strings
    elif isinstance(data, list):
        data_clean = []
        for off in data:
            data_clean.append(clean(off))
        return data_clean
    
    # If input is a column of a pandas dataframe
    elif isinstance(data, pd.Series):
        return data.apply(clean)
    
    # If input is a pandas dataframe
    elif isinstance(data, pd.DataFrame):
        # If names is not passed, function will default to cleaning all columns and adding the suffix ' cleaned' to the new columns
        if not names:
            names = {}
            for col in data.columns:
                names[col] = col+ ' cleaned'
        # Modify the existing dataframe, i.e. add new columns
        if inplace:
            # Apply the cleaning function onto each column specified
            for col in names.keys():
                data[names[col]] = data[col].apply(clean)
            return data
        # Create a separate dataframe with the modified columns and leave the existing one unchanged
        else:
            data_new = data[:]
            # Apply the cleaning function onto each column specified
            for col in names.keys():
                data_new[names[col]] = data[col].apply(clean)
            return data_new
        

def val_search(data, 
               sel, 
               how = 'exact'):
    """

    Parameters
    ----------
    data : list, pandas series
        Contains strings to be evaluated searched. Example: List of offenses to check eligibility for resentencing
    sel : list, pandas series
        Contains strings of selected values to be identified in the input data. Example: List of ineligible offenses or penal codes determined by an attorney
    how : str
        Specifies if selection is based on whether the values match exactly or if a value in data contains a value passed in sel
        Takes 'contains', 'exact' or None. Default is 'exact'
    Returns
    -------
    set
        The values in the input that match with those passed in sel

    """
    if how == 'exact':
        # Return offenses that are present in sel_offenses
        return set(data).intersection(set(sel))
    elif how == 'contains':
        match = []
        for s in sel:
            for d in data:
                if s in d:
                    match.append(d)
        return match
    
    
def get_todays_date(order = ['year', 'month', 'day'], 
                    sep = ''):
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


def df_diff(df_objs, comp_col, label_col, merge = True, direction = 'single', result = 'disagree'):
    """

    Parameters
    ----------
    df_objs : list of pandas dataframes
        Input dataframes to compare. If result = 'base differences', df_objs[0] is evaluated for differences against the remaining dataframes 
    comp_col : str
        Single column name or variable to be compared
    label_col : list of strs
        Labels or tags associated with each input dataframe. Should correspond 1:1 with the dataframes passed
    merge : boolean, optional
        Specify whether to return only the differences or the differences inner-joined with the base dataframe. 
        Default is True. 
    result : str, optional 
        Specify to return only the differences, i.e. when at least one label is False or all entries evaluated for differences. 
        Takes 'disagree' or 'all'. Default is 'disagree'
    direction : str, optional
        Specify whether to evaluate differences against the base dataframe defined as df_objs[0]: 'single' or find differences between all dataframes: 'multi'
        Default is 'single'.
    
    Returns
    -------
    df_diff : pandas dataframe
        Differences in comp_val between the dataframes passed in read_path

    """
    # Initialize dataframe to capture differences
    df_diff = pd.DataFrame()
    
    # Set up the dataframe with values to compare
    # Compare all dfs against each other
    if direction == 'multi':
        comp_list = []
        for df in df_objs: 
            comp_list.extend(list(df[comp_col]))
        df_diff[comp_col] = list(set(comp_list))
    # Compare only one df against the others
    elif direction == 'single':
        df_diff[comp_col] = df_objs[0][comp_col].unique() 
    else:
        print("Direction for evaluation is not understood. Please pass either 'single' or 'multi'")
        return
    
    # Prepare the dataframe to capture differences 
    df_diff.drop_duplicates(inplace = True)
    df_diff.reset_index(drop = True, inplace = True)
    
    # Find common values
    for i in range(0, len(df_objs)):
        comp_vec = df_objs[i][comp_col].unique()
        check = []
        for v in df_diff[comp_col]:
            if v in comp_vec:
                check.append(True)
            elif v not in comp_vec:
                check.append(False)
            else:
                check.append(np.nan)
        df_diff[label_col[i]] = check
    
    # Return entires with at least one disagreement (True and False) or everything 
    if result == 'all':
        pass
    elif result == 'disagree':
        sel = []
        for index, row in df_diff.iterrows(): 
            if not all(row[label_col]):
                sel.append(index)
        df_diff = df_diff.iloc[sel]
    else: 
        print("Result type is not understood. Please pass either 'disagree' or 'all'")
    
    # Return the base dataframe and differences or just the differences
    if merge:
        return pd.merge(df_objs[0], df_diff, on = comp_col, how = 'outer')
    else:
        return df_diff
    
    
def format_date(vec, how = '%m/%d/%Y'):
    """

    Parameters
    ----------
    vec : list, pandas series, other iterable
        Contains date or datetime values to be formatted
    how : str, optional
        Specify how to format the date-like text by month, day, year, hours, mins and seconds. The default is '%m/%d/%Y'.

    Returns
    -------
    fmt : list
        Input vec with formatted date or datetime values

    """
    # Format existing time variables 
    fmt = []
    for v in vec:
        try:
            fmt.append(v.strftime(how))
        except:
            fmt.append(v)
    return fmt


def format_date_blk(dfs, date_cols, how = '%m/%d/%Y', inplace = True, label = None):
    """

    Parameters
    ----------
    dfs : list of pandas dataframes
        Collection of dataframes to be formatted in bulk
    date_cols : list of strs
        List of column names that have date-like information (do not need to be present in all dataframes passed)
    how : str, optional
        Specify how to format the date or datetime value by month, day, year, hours, mins and seconds. The default is '%m/%d/%Y'.
    inplace : boolean, optional
        Specify whether to create a new column with the formatted date value or a separate one. The default is True.
    label : boolean, optional
        If a new column for the formatted date value is requested, specify how to name this column. The existing column name will be concatenated with the label passed. The default is None.

    Returns
    -------
    dfs : list of pandas dataframes
        Collection of dataframes passed in the input that have been formatted

    """
    # Iterate through all the dataframes
    for df in dfs:
        # Check if the specified date column is in the dataframe
        for col in date_cols:
            if col in df.columns:
                # Replace the column
                if inplace:
                    df[col] = format_date(df[col], how = how)
                else:
                    df[col+str(label)] = format_date(df[col], how = how)
    return dfs
    
                