<img src= "https://github.com/redoio/three_strikes_project/assets/124313756/9f54f1f8-e1ff-4ce3-a575-807187824d76" width = "20%" height = "20%">

# Table of Contents

- [Introduction](#introduction)
- [Background](#background)
- [Our tool](#our-tool)
- [Data](#data)
  * [(a). Current commitments<br>](#-a--current-commitments-br-)
    + [Variables<br>](#variables-br-)
    + [Note<br>](#note-br-)
    + [Further details<br>](#further-details-br-)
  * [(b). Prior commitments<br>](#-b--prior-commitments-br-)
    + [Variables<br>](#variables-br--1)
    + [Note<br>](#note-br--1)
    + [Further details<br>](#further-details-br--1)
  * [(c). Demographics<br>](#-c--demographics-br-)
    + [Variables<br>](#variables-br--2)
- [More information](#more-information)
- [Contact](#contact)

# Introduction

A data analysis tool for the Three Strikes Project at the Stanford University School of Law that proactively and automatically identifies individuals who are eligible for re-sentencing in California's prison system. 

# Background

The Three Strikes Project is legal clinical seminar where law students represent individuals serving life sentences for nonviolent crimes under California’s Three Strikes Law. Lawyers assist district attorney’s offices throughout the state who are seeking opportunities to safely and effectively reduce California’s prison population through Prosecutor-Initiated Resentencing. 

But, given that there are over 100,000 incarcerated people in California, how do attorneys accurately identify the individuals who are eligible for resentencing? Redo.io is solving this problem through an open-source eligibility tool for attorneys to filter their case load and apply their expertise efficiently. 

# Our tool

A data model to determine eligibility for resentencing:
- A deterministic model with a rules-based framework established by legal experts and district attorney offices
- Interpretability and explainability is key
- Users can easily request changes to eligibility criteria and see updated results
- Not  a blackbox prediction model

Running the data model for the prison population:
- Leveraging an AWS EC2 instance on Stanford secure servers
- Ingest all of the demographics and offenses of individuals in California Department of Corrections and Rehabilitation (CDCR) custody
- Execute the model
- Provide attorneys easy-to-understand profiles of eligible individuals
- Re-run when new data on the population is available from the district attorney's office

# Data 

The raw data for the model comes from the Three Strikes Project and the participating district attorney offices. We utilize the following information on the prison population from these datasets:

## (a). Current commitments<br>
Information on an invidual's offenses that they are currently serving time for.

### Variables<br>
`CDCR #`: Universal identification across datasets<br>
`Sentencing County`: District Attorney Office or location<br>
`Case Number`: Case identification<br>
`Offense`: Penal code number<br>
`Offense Category`: Nature of offense<br>
`Offense Begin Date`: Date when offense was committed<br>
`Enhancements`: Additional charges added to individual's record<br>
### Note<br>
Each row will include the details on ONE offense committed by the individual, i.e. if an individual has committed 6 offenses under 2 separate case numbers, there will be 6 rows in total associated with their CDCR identification number.
### Further details<br>
`Relationship` variable specifies the nature of a sentence and takes the following values: 'Initial', 'Concurrent', 'Consecutive' or 'Stayed'<br>
`In-prison` variable specifies if an offense was committed in prison or not and takes the following values: 'Yes' or 'No'

## (b). Prior commitments<br>
Information on an invidual's offenses that they are no longer serving time for.

### Variables<br>
`CDCR #`: Universal identification across datasets<br>
`Sentencing County`: District Attorney Office/Location<br>
`Case Number`: Case identification<br>
`Offense`: Penal code number<br>
`Offense Category`: Nature of offense<br>
`Offense Begin Date`: Date when offense was committed<br>
### Note<br>
Each row will include the details on ONE offense committed by the individual, i.e. if an individual has committed 6 offenses under 2 separate case numbers, there will be 6 rows in total associated with their CDCR identification number.
### Further details<br>
'Relationship' variable specifies the nature of a sentence and takes the following values: 'Initial', 'Concurrent', 'Consecutive' or 'Stayed'<br>
'In-prison' variable specifies if an offense was committed in prison or not and takes the following values: 'Yes' or 'No'

## (c). Demographics<br>
Personal information on the individual.

### Variables<br>
`CDCR #`: Universal identification across datasets<br>
`Birthday`: Individual's date of birth<br>
`Offense Begin Date`: Date when offense was committed<br>
`Aggregate Sentence in Months`: Total sentence length in months<br>

# More information

Three Strikes Law and Prosecutor-Initiated Resentencing:
- https://law.stanford.edu/three-strikes-project/three-strikes-basics/ 
- https://capitalbnews.org/prosecutor-resentencing-law/

# Contact

Reach out to Aparna Komarla (aparna.komarla@gmail.com) with any questions
 
