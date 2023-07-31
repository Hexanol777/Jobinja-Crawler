# Jobinja Job Listings Scraper

## Overview
This project is a web scraper built using Async architecture to extract job listings from the Jobinja website. It gathers job data in an asynchronous manner, fetching 20 entries with each request, making the process significantly faster. The dataset contains approximately 26,000 rows of job data.

## Contents
- `Crawler_async.py`: The Python script for asynchronous web scraping. It fetches job listings from the Jobinja website and stores the data in a CSV file.
- `Data Extraction.ipynb`: Notebook used for data extraction and initial data cleaning. Although it's functional, it's recommended to use the `Crawler_async.py` script for efficient data gathering.
- `Data Cleaning.ipynb`: covers handling missing values, removing duplicates, and performing any necessary data transformations
- `Jobinja - Async.csv`: The raw dataset containing job listings collected from the Jobinja website with no processing.

## Dataset
The dataset (`Jobinja - Processed.csv`) contains the following columns:

- `Company Name`: The name of the company offering the job.
- ~~`Date of Establishment`: The date when the company was established (if available).~~
- `Company Category`: The category of the company's business (e.g., Technology, Marketing, Healthcare).
- `Company Size`: The size of the company in terms of the number of employees (e.g., 2 - 10 employees).
- `Company Website`: The company's website URL (if available).
- `Job URL`: The URL of the job listing on Jobinja's website.
- `Job Position`: The name of the job position.
- `Job Category`: The category of the job position (e.g., Software Development, Sales, Marketing).
- `Job Location`: The location of the job position (e.g., Tehran, Isfahan).
- `Employment Type`: The type of employment for the job (e.g., Full Time, Part Time, Remote).
- `Experience`: The required experience for the job (e.g., 1-3 years, 6+ years).
- `Salary`: The pay offered for the job.
- `Skills`: The skill set required for the job.
- `Gender`: If there is a specific gender requirement for the job (e.g., Male, Female, Any).
- `Military Service`: If the employer requires a Military Service Completion Card (MSCC) for the job.
- `Education`: The minimum educational degree required for the job (e.g., Bachelor's, Master's, Ph.D.).
- `Job Description`: A raw copy/paste of everything in the job description section.


## How to Use
1. Modify the code inside `Crawler_async.py` to your liking and  run the file to fetch job listings and create the dataset (`Jobinja - Async.csv`).
2. Optionally, you can also use `Data Extraction.ipynb` to extract data from the Jobinja website.

## Kaggle
The dataset is also available on Kaggle for further inspection and an easier download.
[Kaggle](https://www.kaggle.com/datasets/maminkheneifar/jobinja-job-listings-26k)
