"""
Helper functions and classes to interact with Waterfall API.
"""
import time
from typing import List, Optional

import requests as requests
from dotenv import load_dotenv

from os import environ

from models import ProspectorLauncherRequestBody, CompanyProspects, Person, Company

load_dotenv()

WATERFALL_API_KEY = environ.get('WATERFALL_API_KEY')
MAX_RETRY_COUNT = 5


def start_prospecting_job(company_domain, title_filter):
    req_body = ProspectorLauncherRequestBody(domain=company_domain,
                                             title_filter=title_filter).as_dict()

    try:
        response = requests.post(
            headers={
                'x-waterfall-api-key': WATERFALL_API_KEY,
                'Content-Type': 'application/json'},
            url="https://api.waterfall.to/v1/prospector",
            json=req_body)
        if response.status_code == 401:
            print('API_KEY missing. Make sure API_KEY is set in your environment variables(.env file).')
            print(response.status_code)
            print(response.json())
            return None
        if response.status_code == 403:
            print('Forbidden - please check your WATERFALL_API_KEY')
            print(response.status_code)
            print(response.json())
            return None
    except Exception as e:
        print(e)
        return None

    if response.status_code == 200:
        print('Successfully launched prospecting job')
        print(response.status_code)
        print(response.json())
        job_id = response.json().get('job_id')
        return job_id

    # if we got here something undocumented has happened
    return None


def fetch_contacts_for_domain(job_id) -> Optional[CompanyProspects]:
    try:
        response = requests.get(
            headers={
                'x-waterfall-api-key': WATERFALL_API_KEY,
                'Content-Type': 'application/json'},
            url="https://api.waterfall.to/v1/prospector",
            params={'job_id': job_id})
        if response.status_code == 401:
            print('API_KEY missing. Make sure API_KEY is set in your environment variables(.env file).')
            print(response.status_code)
            print(response.json())
            return None
        if response.status_code == 403:
            print('Forbidden - please check your WATERFALL_API_KEY')
            print(response.status_code)
            print(response.json())
            return None
    except Exception as e:
        print(e)
        return None

    if response.status_code == 200:
        print('Successfully received data from job {}'.format(job_id))
        print(response.status_code)
        print(response.json())
        return handle_contacts_response(response.json())

    # if we got here something undocumented has happened
    return None


def handle_contacts_response(response) -> Optional[CompanyProspects]:
    if response.get('status', 'FAIL') == "SUCCEEDED":
        output_data = response.get('output', {})
        company = output_data.get('company', {})
        company_persons = output_data.get('persons', [])

        persons = []
        for person in company_persons:
            persons.append(Person(**person))
        return CompanyProspects(company=Company(**company), persons=persons)
    return None


def fetch_companies_data(domain_title_list: List) -> List[CompanyProspects]:
    """
    Fetch contacts from Waterfall API for a list of domains and titles.

    :param domain_title_list: list of tuples (domain, title_filter)
    :return: list of Person objects
    """
    jobs = []
    # initiate jobs for each domain-title pair
    company_prospects_list = []
    for domain, title_filter in domain_title_list:
        jobs.append(start_prospecting_job(domain, title_filter))

    # for each job try to fetch results using exponential backoff. Quit after MAX_RETRY_COUNT retries.
    for job_id in jobs:
        retry_count = 0
        received_results = False
        while retry_count < MAX_RETRY_COUNT and not received_results:
            try:
                results = fetch_contacts_for_domain(job_id)
                if results:
                    company_prospects_list.append(results)
                    received_results = True

            except Exception as e:
                print(e)
                print("Error fetching results of job {}".format(job_id))
            retry_count += 1
            time.sleep(2 ** retry_count)

    return company_prospects_list
