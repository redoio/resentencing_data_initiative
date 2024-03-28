# Projects available (as of March 2024): 

## Three Strikes Project & Resentencing Data Initiative

### 1. Summary report generation
Currently, the resentencing eligibility tool reads the demographics and commitments of incarcerated individuals and returns a .csv file with the candidates who meet the eligibility criteria. We want to generate interpretable PDF files with the qualitative summary of each individual (contained in a single row of the output .csv file). This process should be automated, executable with a single click, and easy for the attorneys to review.<br> 
Keywords: `reporting` `data processing` 

### 2. Code improvement 
#### 2.1. Parameterize numerical conditions 
Some eligibility criteria, especially those based on age or sentence length, are currently hard coded. We need to parameterize these conditions so we have a fewer number of rules and a user can easily modify them by passing a numerical value in the parameter set. 
#### 2.2. Create buffer zones 
We need to create and incorporate a margin, say 5% or 10%, on the numerical eligibility criteria. This way, we can identify individuals who are "close" to meeting the criteria but are not quite there yet. An teenager who meets all of the criteria but is 18.5 years of age may be left out of the juvenile eligible cohort, for example, unless we incorporate some buffer zones to keep them in. 
#### 2.3. Order eligibility conditions 
Some selection criteria are more computationally intensive to apply than others. An age or sentence length related cut-off, for example, are significantly faster to apply than a prior or current offense related condition. We want to create a system that executes the criteria in ascending order of computational intensity. This way, the most heavy criteria is applied on the smallest amount of resultant data. 
#### 2.4. Conditional logic 
Currently, the code only supports AND conditional logic for the eligibility criteria. We want to create a capability to accept OR logic as well. 

### 2. Deployment 
First, we need to build a pipeline to automatically update the code repository on the EC2 instance when changes are pushed to GitHub from other locations. This can be achieved using Docker, AWS CodeDeploy or similar tools. Then, we need to establish a task scheduler to execute the tool on EC2 whenever new data is uploaded to the raw data folder on the instance. A bonus step would be notifying the stakeholders whenever new individuals have been added to the eligibile cohort.<br> 
Keywords: `data engineering` `aws ec2`

### 3. Population analytics
We want to develop metrics, primarily focused on similarity, to carve out smaller cohorts from the population that is eligible for resentencing. The metrics will utilize categorical variables like ethnicity or sentencing county as well as natural language modeling to identify similarities between offenses. We may publish this model as an open-source package to generate cohorts of similar individuals from a population dataset.<br> 
Keywords: `natural language processing` `data science` `similarity scores`

## Prison Population Research 

### 1. Exploration 
We want to apply the eligibilty model (developed for the Three Strikes Project and their partner counties) to the entire prison population in California. This will help derive a sense of the number of incarcerated individuals who may be eligible for resentencing in counties without Prosecutor Initiated Resentencing (PIR) or similar programs. 

