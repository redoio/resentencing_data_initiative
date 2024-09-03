from bs4 import BeautifulSoup
import requests
import pandas as pd


# Get data

# get penal codes from selection_criteria
df_penal_codes = pd.read_excel(r'C:\Users\rachu\Desktop\Redo.io\resentencing_data_initiative\eligibility_model\code\offense_classification\county\los_angeles\selection_criteria.xlsx', sheet_name = 'Penal codes')

output_list =[] 

for each_code in df_penal_codes['Offenses']:
  url = 'https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=' + each_code + '.&lawCode=PEN'  
  page = requests.get(url)
  soup = BeautifulSoup(page.text, 'html')
  html_blob = soup.find_all(id = 'codeLawSectionNoHead', limit=1)
  cleaned_text = ' '.join(tag.get_text() for tag in html_blob) 
  output_list.append(cleaned_text)

extract_df = pd.DataFrame(output_list, columns=['Extract']) 

df_combined = pd.concat([df_penal_codes, extract_df], axis=1)

df_combined.to_excel(r'C:\Users\rachu\Desktop\Redo.io\resentencing_data_initiative\eligibility_model\code\offense_classification\county\los_angeles\Penal_Code_Extracts.xlsx', index = False)