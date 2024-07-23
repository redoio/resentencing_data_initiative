# -*- coding: utf-8 -*-
import helpers
import pandas as pd
import numpy as np
import datetime
from tqdm import tqdm
import copy
import os


def get_input(main_path, 
              month, 
              county_name, 
              file_convention, 
              ext = '.xlsx',
              write_path = None, 
              pickle = False):
    """

    Parameters
    ----------
    main_path : str
        Folder path of the file to extract data from (all parent folders without county name, month and file name)
    county_name : str
        Name of the county folder to extract data for, ex: 'Los Angeles County', that becomes a part of the file path
    file_convention : str
        Name of the .txt file from which the naming conventions should be extracted. Must be formatted as a numerical list with file names enclosed in single quotes, ex: "1. 'commitments.xlsx'"
        File extension of .txt should be included
    ext : str
        File extension of the file names to be checked, ex: '.xlsx', '.csv' etc. 
        Default is '.xlsx'
    month : str
        Year and month for which data should be extracted, ex: '2023_06'
    count : int
        Number of inputs to extract, i.e. number of times to call the extract_data() function
    write_path : str, optional 
        Specify the path where the pickle outputs should be written. 
        If pickle = True but write_path = None, data outputs are written to the county_name folder by default. To avoid this behavior, pass a value to write_path.
    pickle: boolean, optional
        Specify whether to store dataframe output as a pickle file or not
        Default is False.
        
    Returns
    -------
    sorting_criteria : pandas dataframe
        Data on offenses and their categories
    demographics : pandas dataframe
        Data on individuals currently incarcerated
    current_commits : pandas dataframe
        Data on current offenses of incarcerated individuals wherein each row represents a single offense
    prior_commits : pandas dataframe
        Data on prior offenses of incarcerated individuals wherein each row represents a single offense
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
    print('Executing data extraction steps\n')
    
    # Checking if all required input files are present in the read path 
    target_file_name, true_file_name, error = helpers.verify_naming_convention(main_path = main_path, 
                                                                               file_convention = file_convention,
                                                                               ext = ext,
                                                                               county_name = county_name,
                                                                               month = None)
    
    # Terminate the extraction process if there are some missing files or incorrect names
    if error != 0:
        print(f'{error} file name(s) are missing or incorrect based on the target naming convention')
        print('Please ensure that the input files match the naming convention and re-run the data extraction step.')
    
    # Count of files to read (adding 1 for selection criteria)
    count = len(target_file_name)+1
    
    # Criteria for selection
    sorting_criteria = helpers.extract_data(main_path = 'offense_classification/county', 
                                            county_name = county_name, 
                                            file_name = 'selection_criteria.xlsx', 
                                            write_path = write_path, 
                                            pickle = False) 
    print('\n Extraction 1/'+str(count)+' complete \n')
    
    # Demographics of individuals incarcerated
    demographics = helpers.extract_data(main_path = main_path, 
                                        county_name = county_name, 
                                        file_name = 'Demographics.xlsx', 
                                        month = month,
                                        write_path = write_path,
                                        pickle = pickle)
    print('\n Extraction 2/'+str(count)+' complete \n')
    
    # Education merit
    merit_credit = helpers.extract_data(main_path = main_path, 
                                        county_name = county_name, 
                                        file_name = 'EducationMeritCredits.xlsx', 
                                        month = month,
                                        write_path = write_path,
                                        pickle = pickle)
    print('\n Extraction 3/'+str(count)+' complete \n')
    
    # Milestone credit
    milestone_credit = helpers.extract_data(main_path = main_path, 
                                            county_name = county_name, 
                                            file_name = 'MilestoneCompletionCredits.xlsx', 
                                            month = month,
                                            write_path = write_path,
                                            pickle = pickle)
    print('\n Extraction 4/'+str(count)+' complete \n')
    
    # Rehab credit
    rehab_credit = helpers.extract_data(main_path = main_path, 
                                        county_name = county_name, 
                                        file_name = 'RehabilitativeAchievementCredits.xlsx', 
                                        month = month,
                                        write_path = write_path,
                                        pickle = pickle)
    print('\n Extraction 5/'+str(count)+' complete \n')
    
    # Vocational education credit
    voced_credit = helpers.extract_data(main_path = main_path, 
                                        county_name = county_name, 
                                        file_name = 'VocEd_TrainingCerts.xlsx', 
                                        month = month,
                                        write_path = write_path,
                                        pickle = pickle)
    print('\n Extraction 6/'+str(count)+' complete \n')
    
    # Rule violations
    rv_report = helpers.extract_data(main_path = main_path, 
                                     county_name = county_name, 
                                     file_name = 'RulesViolationReports.xlsx', 
                                     month = month,
                                     write_path = write_path,
                                     pickle = pickle)
    print('\n Extraction 7/'+str(count)+' complete \n')
    
    # Current commitments
    current_commits = helpers.extract_data(main_path = main_path, 
                                           county_name = county_name, 
                                           file_name = 'CurrentCommitments.xlsx', 
                                           month = month,
                                           write_path = write_path,
                                           pickle = pickle)
    print('\n Extraction 8/'+str(count)+' complete \n')
    
    # Previous commitments
    prior_commits = helpers.extract_data(main_path = main_path, 
                                         county_name = county_name, 
                                         file_name = 'PriorCommitments.xlsx', 
                                         month = month,
                                         write_path = write_path,
                                         pickle = pickle)
    print('\n Extraction 9/'+str(count)+' complete \n')
    
    return sorting_criteria, demographics, merit_credit, milestone_credit, rehab_credit, voced_credit, rv_report, current_commits, prior_commits 
    