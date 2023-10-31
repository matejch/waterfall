# WATERFALL TASK

We'd like you to create a script using the Waterfall.to API to find contacts for a list of companies. Here's what you need to know: 

**Inputs:**

1. A CSV file with a list of companies, one of which is the domain name. 
2. A title filter expression. 

**Your script should:** 

1. Read the CSV file. 
2. Fetch the list of contacts for each company using the Waterfall.to API. 
3. Write the list of contacts to a CSV file and a PostgreSQL database. 
4. In addition, please provide the Data Definition Language (DDL) for the database table(s) where you'll store the contacts. Consider adding tests where appropriate, and use any libraries or frameworks you typically use. 

Please include a README file with instructions on how to run your script and any other pertinent information. 

You can find the Waterfall API documentation here: https://docs.waterfall.to/waterfall-v1-1/. 

# SOLUTION & INSTRUCTIONS

## Create Postgres database

> psql -U postgres -c "CREATE DATABASE waterfall;"

## Create tables

> psql -U postgres -d waterfall -f create_tables.sql

## Set up virtual environment

> python3.10 -m venv venv
 
> source venv/bin/activate

## Install requirements
> pip install -r requirements.txt

## Edit .env file

> cp .env.example .env

Edit .env file and set your database password and Waterfall API key

## Create a csv file with companies

Create a csv file with a list of domains with title filter expression.

Example:

> "domain","title_filter"

> "google.com","CEO"

> "facebook.com","Founder or CEO"

Put this file into /data folder

## Running script

> python main.py

## How does it work?

Script first launches a prospector job for each company in a given csv file(data/companies.csv).
Then it tries to fetch results for each job and exponentially backs off if they are not ready yet.

After 5 retries it gives up and returns an error.

If it is successful it save results to csv file and into a database.

## Assumptions 

I wanted to create a simple script that does what was asked without adding heavyweight libraries. 
Hence, I used aiosql and requests.

I didn't write any unit or integration tests because the code is straight forward and only initiates requests and stores data into the database.
There's no real business logic or difficult functions to test. The whole script is an end-to-end test for 2 Waterfall API endpoints.
I also didn't handle possible failure modes that could happen if I called the script with a large csv file. I think that's outside scope for this task.
I didn't create a CLI application because the only possible input and output are csv files names/locations.

I modelled the types(models.py) based on Waterfall API documents. It's a bit of an overkill for this task, but it made code easier to read and understand. It's also easy to add/change/remove fields if needed. 

## Potential improvements

This script only does what was asked. To make this a production ready application, we should:
- add logging
- create a proper CLI with click
- replace exponential backoff with a proper retrying library that handles
- add proper validation logic and typing
- add error recovery logic
- create an async version of job fetching
- batch inserts into the database after number of contacts reaches a certain threshold (1000?)



