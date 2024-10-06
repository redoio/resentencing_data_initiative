# -*- coding: utf-8 -*-
import helpers
import utils
import pandas as pd


# Get data

# 2021 eligible data
df_2105_el_p1 = pd.read_excel(r'D:\Users\3xProject\Documents\Redo.io\Stanford Law 3XP\data\county\los_angeles\21_05\LA_DA_Cohort1_Update_05_2021.xlsx', sheet_name = 'Sheet1')
df_2105_el_p2 = pd.read_excel(r'D:\Users\3xProject\Documents\Redo.io\Stanford Law 3XP\data\county\los_angeles\21_05\LA_DA_Cohort1_Update_05_2021.xlsx', sheet_name = 'Sheet2')
# 2024 eligible and demographics data
df_2409_el_adult = pd.read_excel(r'D:\Users\3xProject\Documents\Redo.io\Stanford Law 3XP\data\county\los_angeles\24_09\output\date of execution\2024_9_30\adult_eligible_demographics.xlsx')
df_2409_el_juv = pd.read_excel(r'D:\Users\3xProject\Documents\Redo.io\Stanford Law 3XP\data\county\los_angeles\24_09\output\date of execution\2024_9_30\juvenile_eligible_demographics.xlsx')
df_2409_dem = pd.read_excel(r'D:\Users\3xProject\Documents\Redo.io\Stanford Law 3XP\data\county\los_angeles\24_09\Demographics.xlsx')

# Combine data
df_2105_el = pd.concat([df_2105_el_p1, df_2105_el_p2])
df_2409_el = pd.concat([df_2409_el_adult, df_2409_el_juv])

# Standardize column names
df_2105_el.rename(columns = {"CDCR..": "cdcno", "CDCNo": "cdcno"}, inplace = True)
df_2409_el.rename(columns = {"CDCR..": "cdcno", "CDCNo": "cdcno"}, inplace = True)
df_2409_dem.rename(columns = {"CDCR..": "cdcno", "CDCNo": "cdcno"}, inplace = True)


# Find differences 
diff = utils.df_diff(df_objs = [df_2409_dem, df_2105_el, df_2409_el], 
                     comp_col = 'cdcno', 
                     label_col = ['2024_09_demographics', '2021_05_eligible', '2024_09_eligible'], 
                     merge = True, 
                     result = 'all',
                     direction = 'multi')
# Write result to excel
diff.to_excel(r'D:\Users\3xProject\Documents\Redo.io\Stanford Law 3XP\data\county\los_angeles\analysis\comparison.xlsx', index = False)

