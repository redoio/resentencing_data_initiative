# -*- coding: utf-8 -*-
import helpers
import utils
import pandas as pd
import numpy as np
import datetime
import copy
from tqdm import tqdm
import os


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
        print('Input column names are not cleaned, so the required variables for summary generation cannot be found\n')
        return
    
    # Initialize lists for other variables
    current_conv = []
    prior_conv = []
    programming = []
    rvr = []
    
    # Formatting time column 
    rvd = []
    for i in range(0, len(rv_report['rule violation date'])):
        try:
            rvd.append(rv_report['rule violation date'][i].strftime('%m/%d/%Y'))
        except:
            rvd.append(rv_report['rule violation date'][i])
    rv_report['rule violation date'] = rvd
    
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

