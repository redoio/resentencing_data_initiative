# -*- coding: utf-8 -*-

from helpers import *
import pandas as pd
import numpy as np
import datetime
from tqdm import tqdm

def get_input(data_path, month, county_name, write_path = None, pickle = None):
    """

    Parameters
    ----------
    data_path : str
        Full path of the file to extract data from (all parent folders)
    county_name : str
        Name of the county folder to extract data for, ex: 'Los Angeles County'
        Becomes a part of the file path
    month : str
        Year and month for which data should be extracted, ex: '2023_06'
    write_path : str, optional 
        Specify the path where the pickle outputs should be written. 
        If pickle = True but write_path = None, data outputs are written to the county_name folder by default. To avoid this behavior, pass a value to write_path.
    pickle: boolean, optional
        Specify whether to store dataframe output as a pickle file or not
       
    Returns
    -------
    sorting_criteria : pandas dataframe
        Data on offenses and their categories
    demographics : pandas dataframe
        Data on individuals currently incarcerated
    current_commits : pandas dataframe
        Data on current offenses of incarcerated individuals wherein each row pertains to a single offense
    prior_commits : pandas dataframe
        Data on prior offenses of incarcerated individuals wherein each row pertains to a single offense
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

    """
    # Criteria for selection
    sorting_criteria = extract_data(main_path = data_path, 
                                    county_name = county_name, 
                                    file_name = 'Criteria/sorting_criteria.xlsx', 
                                    write_path = write_path, 
                                    pickle = pickle) 
    
    # Demographics of individuals incarcerated
    demographics = extract_data(main_path = data_path, 
                                county_name = county_name, 
                                file_name = 'demographics.xlsx', 
                                month = month,
                                write_path = write_path,
                                pickle = pickle)
    
    # Education merit
    merit_credit = extract_data(main_path = data_path, 
                                county_name = county_name, 
                                file_name = 'EducationMeritCredits.xlsx', 
                                month = month,
                                write_path = write_path,
                                pickle = pickle)
    
    # Milestone credit
    milestone_credit = extract_data(main_path = data_path, 
                                    county_name = county_name, 
                                    file_name = 'MilestoneCompletionCredits.xlsx', 
                                    month = month,
                                    write_path = write_path,
                                    pickle = pickle)
    
    # Rehab credit
    rehab_credit = extract_data(main_path = data_path, 
                                county_name = county_name, 
                                file_name = 'RehabilitiveAchievementCredits.xlsx', 
                                month = month,
                                write_path = write_path,
                                pickle = pickle)
    
    # Vocational education credit
    voced_credit = extract_data(main_path = data_path, 
                                county_name = county_name, 
                                file_name = 'VocEd_TrainingCerts.xlsx', 
                                month = month,
                                write_path = write_path,
                                pickle = pickle)
    
    # Rule violations
    rv_report = extract_data(main_path = data_path, 
                            county_name = county_name, 
                            file_name = 'RVRs.xlsx', 
                            month = month,
                            write_path = write_path,
                            pickle = pickle)
    
    # Current commitments
    current_commits = extract_data(main_path = data_path, 
                            county_name = county_name, 
                            file_name = 'currentcommitments.xlsx', 
                            month = month,
                            write_path = write_path,
                            pickle = pickle)
    
    # Previous commitments
    prior_commits = extract_data(main_path = data_path, 
                            county_name = county_name, 
                            file_name = 'priorcommitments.xlsx', 
                            month = month,
                            write_path = write_path,
                            pickle = pickle)
    
    return sorting_criteria, demographics, merit_credit, milestone_credit, rehab_credit, voced_credit, rv_report, current_commits, prior_commits 
    