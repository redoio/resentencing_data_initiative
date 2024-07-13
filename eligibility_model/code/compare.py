# -*- coding: utf-8 -*-
import helpers
import utils
import pandas as pd


# Get data

# 2021 eligible data
df_2105_el_p1 = pd.read_excel(r'D:\Users\3xProject\Documents\Redo.io\Stanford Law 3XP\data\county\los_angeles\ALL LA INMATE DATA SETS-20240120T003310Z-001\ALL LA INMATE DATA SETS\21_05\LA_DA_Cohort1_Update_05_2021.xlsx', sheet_name = 'Sheet1')
df_2105_el_p2 = pd.read_excel(r'D:\Users\3xProject\Documents\Redo.io\Stanford Law 3XP\data\county\los_angeles\ALL LA INMATE DATA SETS-20240120T003310Z-001\ALL LA INMATE DATA SETS\21_05\LA_DA_Cohort1_Update_05_2021.xlsx', sheet_name = 'Sheet2')
# 2024 eligible and demographics data
df_2403_el_adult = pd.read_excel(r'D:\Users\3xProject\Documents\Redo.io\Stanford Law 3XP\data\county\los_angeles\ALL LA INMATE DATA SETS-20240120T003310Z-001\ALL LA INMATE DATA SETS\24_03\output\date of execution\2024_7_11\adult_eligible_demographics.xlsx')
df_2403_el_juv = pd.read_excel(r'D:\Users\3xProject\Documents\Redo.io\Stanford Law 3XP\data\county\los_angeles\ALL LA INMATE DATA SETS-20240120T003310Z-001\ALL LA INMATE DATA SETS\24_03\output\date of execution\2024_7_11\juvenile_eligible_demographics.xlsx')
df_2403_dem = pd.read_excel(r'D:\Users\3xProject\Documents\Redo.io\Stanford Law 3XP\data\county\los_angeles\ALL LA INMATE DATA SETS-20240120T003310Z-001\ALL LA INMATE DATA SETS\24_03\Demographics.xlsx')
# 2023 eligible and demographics data
df_2312_el_adult = pd.read_excel(r'D:\Users\3xProject\Documents\Redo.io\Stanford Law 3XP\data\county\los_angeles\ALL LA INMATE DATA SETS-20240120T003310Z-001\ALL LA INMATE DATA SETS\23_12\output\date of execution\2024_4_30\adult_eligible_demographics.xlsx')
df_2312_el_juv = pd.read_excel(r'D:\Users\3xProject\Documents\Redo.io\Stanford Law 3XP\data\county\los_angeles\ALL LA INMATE DATA SETS-20240120T003310Z-001\ALL LA INMATE DATA SETS\23_12\output\date of execution\2024_4_30\juvenile_eligible_demographics.xlsx')
df_2312_dem = pd.read_excel(r'D:\Users\3xProject\Documents\Redo.io\Stanford Law 3XP\data\county\los_angeles\ALL LA INMATE DATA SETS-20240120T003310Z-001\ALL LA INMATE DATA SETS\23_12\Demographics.xlsx')

# Combine data
df_2105_el = pd.concat([df_2105_el_p1, df_2105_el_p2])
df_2403_el = pd.concat([df_2403_el_adult, df_2403_el_juv])
df_2312_el = pd.concat([df_2312_el_adult, df_2312_el_juv])

# Standardize column names
df_2105_el.rename(columns = {"CDCR..": "cdcno", "CDCNo": "cdcno"}, inplace = True)
df_2403_el.rename(columns = {"CDCR..": "cdcno", "CDCNo": "cdcno"}, inplace = True)
df_2403_dem.rename(columns = {"CDCR..": "cdcno", "CDCNo": "cdcno"}, inplace = True)
df_2312_dem.rename(columns = {"CDCR..": "cdcno", "CDCNo": "cdcno"}, inplace = True)
df_2312_el.rename(columns = {"CDCR..": "cdcno", "CDCNo": "cdcno"}, inplace = True)

# Find differences 
diff = utils.df_diff(df_objs = [df_2403_dem, df_2105_el, df_2403_el, df_2312_el, df_2312_dem], 
                     comp_col = 'cdcno', 
                     label_col = ['2024_03_demographics', '2021_05_eligible', '2024_03_eligible', '2023_12_eligible', '2023_12_demographics'], 
                     merge = True, 
                     result = 'all',
                     direction = 'multi')
# Write result to excel
diff.to_excel(r'D:\Users\3xProject\Documents\Redo.io\Stanford Law 3XP\data\county\los_angeles\ALL LA INMATE DATA SETS-20240120T003310Z-001\ALL LA INMATE DATA SETS\analysis\releases.xlsx', index = False)

