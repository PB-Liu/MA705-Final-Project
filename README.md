# MA705-Final-Project

## Philosophy Jobs Dashboard (https://philjobs.herokuapp.com/)


### Motivating question: how has the philosophy job market evolved since 2015? Specifically:

1. Which subfiled of philosophy has the most openings each year? 
2. How has the numbers of jobs in particular areas changed over the years? Is there an area that has become increasingly popular? Conversely, is there an area the demand for which is declining?
3. What is the trend of the different types of jobs (tenure-track, tenured, fixed term, etc.) on the job market? 
4. As covid-19 pandemic has hit the academic job market hard in the year of 2020, how bad is the situation for philosophy job market overall? In particular: a). Are all areas fare equally, or are areas that fare better than others? b). Does the pandemic affect not only the total amount of jobs, but also the types of jobs avaialable? 

### Source of raw data: PhilJobs (https://philjobs.org) 

### Steps of Data Analysis:

##### 0. Import raw data and packages 

##### 1. Data Cleaning:
    1.1. Drop all redundant columns/variables 
    1.2. Add a new column 'year'; filter the dateframe for years since 2015
    1.3. Simplify the "Contract Type" column for future usage 

##### 2. Data Transformation: 

    2.1. Define functions to re-classify job areas into 11 major categories of philosophy sub-fields
    2.2. Generate a new dataframe to display openings according to the AOS(are of specialization)
    2.3. Group and summarize the data 1) by years, areas, and contract types and 2) years and areas 

##### 3. Create Dashboard

### Dashboard Components: 

1. A dash table that summarizes the data.  
2. A sunburst plot that breaks down the jobs into types and areas of a particular year (year can be chosen by users).
3. A lineplot that shows the trends of available jobs from 2015 to 2020 in different areas (areas can be chosen by users) 
