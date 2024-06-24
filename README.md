<img src= "https://github.com/redoio/.github/assets/124313756/9f405081-081a-4716-b8a6-f90f840fa8f5" width = "25%" height = "15%">

# Table of Contents

- [Introduction](#introduction)
- [Citation](#citation)
- [License](#license)
- [Background](#background)
- [Our tool](#our-tool)
  * [Summary](#summary)
  * [Execution](#execution)
  * [Example](#example)
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
- [Opportunities](#opportunities)

# Introduction

A data science application for the Three Strikes Project at the Stanford University School of Law that proactively and automatically identifies nonviolent offenders in California's prison system who are eligible for Prosecutor Initiated Resentencing (PIR). 

# Citation 

If you make use of our dataset(s) or code, please cite our work as follows: 

APA style:<br>
"Redo.io. resentencing-data-initiative (Version 1.0.0) [Computer software]. https://github.com/redoio/resentencing_data_initiative/"

BibTex:<br>
@software{Redo_io_resentencing-data-initiative,
author = {{Redo.io}},
title = {{resentencing-data-initiative}},
url = {https://github.com/redoio/resentencing_data_initiative/},
version = {1.0.0}}

# License 
All content in this repository is licensed under GNU AGPLv3
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

You must give appropriate credit to our work. You may not use our work for commercial purposes, which means anything primarily intended for or directed toward commercial advantage or monetary compensation.

# Background

The Three Strikes Project is legal clinical seminar where law students represent individuals serving life sentences for non-violent crimes under California’s Three Strikes Law. Lawyers assist district attorney’s offices throughout the state who are seeking opportunities to safely and effectively reduce California’s prison population through Prosecutor Initiated Resentencing (PIR).

But, given that there are over 100,000 people in California's prisons, lawyers need efficient and accurate ways to identify those who are eligible for PIR instead of manually reviewing piles of paperwork. Redo.io's open-source eligibility tool helps lawyers filter their caseload and apply their expertise efficiently. We are currently under a contract with the Stanford School of Law to develop this application.

# Our tool 

## Summary 

A rules-based and deterministic model that generates cohorts of individuals eligible for PIR based on criteria established by district attorney's offices.

What it is:
- A deterministic model with a rules-based framework designed by Redo.io in conjunction with legal experts
- Easily interpretable and explainable for non-technical users and audience
- Responsive to user requests, i.e. an attorney can request changes to the eligibility criteria and see updated results

What it is not:
- A blackbox predictive model
- A decision-maker that determines the cases that are ultimately resentenced by the courts

## Execution

- Ingest the demographics, current offenses and prior offenses of individuals in California Department of Corrections and Rehabilitation (CDCR) custody
- Run the eligibility model (with selection criteria and scenarios designed by legal experts)
- Return a cohort of individuals eligible for PIR
- Provide attorneys easy-to-understand personal profiles of each candidate
- Re-run the eligibility model when new data on the prison population is available

## Example 

An example of the solution pipeline implemented for the Los Angeles County District Attorney's Office: 

<img src= "https://github.com/redoio/resentencing_data_initiative/assets/124313756/69bf0453-2a2d-4969-8bc4-f77aa5c5dcf3" width = "90%" height = "90%">

# Data 

Raw data is sourced from the Three Strikes Project and the participating district attorney's offices. We primarily utilize the following information on the prison population for eligibility determination.

## (a). Current commitments<br>
Information on the offenses an individual is currently serving time for.

### Variables<br>
`CDCR #`: Universal identification across datasets<br>
`Sentencing County`: District Attorney Office or location<br>
`Case Number`: Case identification<br>
`Offense`: Penal code number<br>
`Offense Category`: Nature of offense<br>
`Offense Begin Date`: Date when offense was committed<br>
`Enhancements`: Additional charges added to an individual's record<br>
### Note<br>
Each row will include the details on ONE offense committed by the individual, i.e. if an individual has committed 6 offenses under 2 separate case numbers, there will be 6 rows in total associated with their CDCR identification number.
### Further details<br>
`Relationship` variable specifies the nature of a sentence and takes the following values: 'Initial', 'Concurrent', 'Consecutive' or 'Stayed'<br>
`In-prison` variable specifies if an offense was committed in prison or not and takes the following values: 'Yes' or 'No'

## (b). Prior commitments<br>
Information on the offenses an individual is no longer serving time for.

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
`Relationship` variable specifies the nature of a sentence and takes the following values: 'Initial', 'Concurrent', 'Consecutive' or 'Stayed'<br>
`In-prison` variable specifies if an offense was committed in prison or not and takes the following values: 'Yes' or 'No'

## (c). Demographics<br>
Personal information on the individual. Note that we do not utilize any demographic information such as gender or race.

### Variables<br>
`CDCR #`: Universal identification across datasets<br>
`Birthday`: Individual's date of birth<br>
`Offense Begin Date`: Date when offense was committed<br>
`Aggregate Sentence in Months`: Total sentence length in months<br>

# More information

Three Strikes Law and Prosecutor Initiated Resentencing (PIR):
- https://law.stanford.edu/three-strikes-project/three-strikes-basics/ 
- https://capitalbnews.org/prosecutor-resentencing-law/

# Contact

Contact aparna.komarla@gmail.com for any questions

# Opportunities

Currently looking for interns and developers to join our team. Here is a short summary of available projects: https://github.com/redoio/resentencing_data_initiative/blob/main/opportunities.md. Reach out to Aparna Komarla (aparna.komarla@gmail.com) if you are interested!
 
