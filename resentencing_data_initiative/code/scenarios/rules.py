# -*- coding: utf-8 -*-

# Set of all possible rules
r_1 = 'Age 50 and older'
r_2 = 'Sentenced to 20 years or more'
r_3 = 'Served a minimum of 10 years in custody'
r_4 = 'Is not serving a current sentence for any offense listed in Table A, B, C, or D and their implied offenses (from sorting_criteria.xlsx)'
r_5 = 'Does not have a prior conviction for any offense listed in Tables C & D and their implied offenses (from sorting_criteria.xlsx)'
r_6 = 'Sentenced for a crime that was committed at age 14 or 15'
r_7 = 'Is not serving current sentence for any offense listed in Table D and E and their implied offenses (from sorting_criteria.xlsx)'
r_8 = 'Does not have a prior conviction for any offense listed in Table D and its implied offenses (from sorting_criteria.xlsx)'
r_9 = 'Is serving current sentence for at least one offense listed in Table F and its implied offenses (from sorting_criteria.xlsx)'
r_10 = 'Has a controlling offense that is present in Table F (from sorting_criteria.xlsx)'
r_11 = 'Does not have an enhancement that contains PC 12022'
r_12 = 'Is not serving a current sentence for any offense listed in Table A, B (minus Table F), C or D and their implied offenses (from sorting_criteria.xlsx)'
r_13 = 'Served a minimum of 15 years in custody'

# Categories of rules (one to many)
cat = {'age': [r_1, r_6],
       'sentence length': [r_2, r_3, r_13],
       'current offenses': [r_4, r_7, r_12, r_9, r_10],
       'prior offenses': [r_5, r_8],
       'controlling offense': [r_10], 
       'enhancement': [r_11]}

# Order of computational intensity or demand (ascending)
comp_int = ['r_1', 'r_6', 'r_2', 'r_3', 'r_13', 'r_4', 'r_7', 'r_12', 'r_9', 'r_10', 'r_5', 'r_8', 'r_11']
