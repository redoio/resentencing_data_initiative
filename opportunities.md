# Projects available (as of March 2024): 

## Three Strikes Project & Resentencing Data Initiative

### 1. Summary report generation
Currently, the resentencing eligibility tool reads the demographics and commitments of a cohort of incarcerated individuals and returns a .csv file with the candidates who meet all of the eligibility criteria. We want to generate an interpretable PDF file with the summary of each individual that is contained in a single row of the output .csv file. This process should be automated such that all PDFs are generated with one click and are easily accessible for the attorneys to review.<br> 
Keywords: `reporting` `data processing` 

### 2. Code improvement 
#### 2.1. Parameterize numerical conditions 
Some eligibility criteria, especially those based on age or sentence length, are currently hard coded. We need to parameterize these conditions so we have a fewer number of rules and a user can modify them easily by passing a numerical value in the parameter set. 
#### 2.2. Create buffer zones 
We need to create and incorporate a margin, say 5% or 10%, on numerical eligibility criteria. This way, we can identify individuals who are "close" to meeting the criteria but are not quite there yet. An teenager who meets all of the criteria but is 18.5 years of age may be left out of the juvenile eligible cohort, for example, unless we incorporate some buffer zones. 

### 2. Deployment 
First, we need to build a pipeline to automatically update the code repository on the EC2 instance when changes are pushed to GitHub from other locations. This can be achieved using Docker, AWS CodeDeploy or similar tools. Then, we need to establish a task scheduler to execute the tool on EC2 whenever new data is uploaded to the raw data folder on the instance. A bonus step would be notifying the stakeholders whenever new individuals have been added to the eligibile cohort.<br> 
Keywords: `data engineering` `aws ec2`

### 3. Population analytics
We want to develop metrics, primarily focused on similarity, to carve out smaller cohorts from the population that is eligible for resentencing. The metrics will utilize categorical variables like ethnicity or sentencing county as well as natural language modeling to identify similarities between offenses. We may publish this model as an open-source package to generate cohorts of similar individuals from a population dataset.<br> 
Keywords: `natural language processing` `data science` `similarity scores`

## Prison Population Research 

### 1. Exploration 
We want to apply the eligibilty model (developed for the Three Strikes Project and their partner counties) to the entire prison population in California. This will help derive a sense of the number of incarcerated individuals who may be eligible for resentencing in counties without Prosecutor Initiated Resentencing (PIR) or similar programs. 

