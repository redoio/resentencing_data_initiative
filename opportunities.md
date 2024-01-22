# Projects available (as of Jan 2024): 

## 1. Summary report generation
Currently, the resentencing eligibility tool reads the demographics and commitments of a cohort of incarcerated individuals and returns a .csv file with the candidates who meet all of the eligibility criteria. We want to generate an interpretable PDF file with the summary of each individual that is contained in a single row of the output .csv file. This process should be automated such that all PDFs are generated with one click and are easily accessible for the attorneys to review.<br> 
Key words: `reporting` `data processing` 

## 2. Deployment 
First, we need to build a pipeline to automatically update the code repository on the EC2 instance when changes are pushed to GitHub from other locations. This can be achieved using Docker, AWS CodeDeploy or similar tools. Then, we need to establish a task scheduler to execute the tool on EC2 whenever new data is uploaded to the raw data folder on the instance. A bonus step would be notifying the stakeholders whenever new individuals have been added to the eligibile cohort.<br> 
Key words: `data engineering` `aws ec2`

## 3. Population analytics
We want to establish some metrics mainly focused on similarity to study the nature of the population that is both eligible and ineligible for resentencing. The metrics will use categorical variables like ethnicity or sentencing county, as well as natural language modeling to identify similarities between offenses.<br> 
Key words: `natural language processing` `data science` `similarity scores` `analytics`
