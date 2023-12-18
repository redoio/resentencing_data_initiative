# -*- coding: utf-8 -*-

from helpers import *
import pandas as pd
import numpy as np
import datetime
from tqdm import tqdm

def get_input(data_path, county_name, pickle):
    # Criteria for selection
    sorting_criteria = extract_data(main_path = data_path, 
                                    county_name = county_name, 
                                    file_name = 'Criteria/sorting_criteria.xlsx', 
                                    pickle = pickle) 
    
    # Demographics of individuals incarcerated
    demographics = extract_data(main_path = data_path, 
                                county_name = county_name, 
                                file_name = 'demographics.xlsx', 
                                month = month,
                                pickle = pickle)
    
    # Education merit
    merit_credit = extract_data(main_path = data_path, 
                                county_name = county_name, 
                                file_name = 'EducationMeritCredits.xlsx', 
                                month = month,
                                pickle = pickle)
    
    # Milestone credit
    milestone_credit = extract_data(main_path = data_path, 
                                    county_name = county_name, 
                                    file_name = 'MilestoneCompletionCredits.xlsx', 
                                    month = month,
                                    pickle = pickle)
    
    # Rehab credit
    rehab_credit = extract_data(main_path = data_path, 
                                county_name = county_name, 
                                file_name = 'RehabilitiveAchievementCredits.xlsx', 
                                month = month,
                                pickle = pickle)
    
    # Vocational education credit
    voced_credit = extract_data(main_path = data_path, 
                                county_name = county_name, 
                                file_name = 'VocEd_TrainingCerts.xlsx', 
                                month = month,
                                pickle = pickle)
    
    # Rule violations
    rv_report = extract_data(main_path = data_path, 
                            county_name = county_name, 
                            file_name = 'RVRs.xlsx', 
                            month = month,
                            pickle = pickle)
    
    # Current commitments
    current_commits = extract_data(main_path = data_path, 
                            county_name = county_name, 
                            file_name = 'currentcommitments.xlsx', 
                            month = month,
                            pickle = pickle)
    
    # Previous commitments
    prior_commits = extract_data(main_path = data_path, 
                            county_name = county_name, 
                            file_name = 'priorcommitments.xlsx', 
                            month = month,
                            pickle = pickle)
    
    return sorting_criteria, demographics, merit_credit, milestone_credit, rehab_credit, voced_credit, rv_report, current_commits, prior_commits 
    