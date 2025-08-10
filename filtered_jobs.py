import requests
import pandas as pd
import os
import json

# Sets up the API Authentication for the call
# The API for findwork.dev expects the API Key to be in the header.
# Here the header is set up with the API call expecatation
api_key = os.getenv("MY_API_KEY")
headers = {"Authorization":f"Token {api_key}"
}

# API URL from which the call will pull the data from.
# In the response, the header is called upon along wit the URL so the API knows we are authenticated
URL = "https://findwork.dev/api/jobs/?search=python&remote=true&employment_type=full+time"
response = requests.get(URL, headers=headers)

# If else statement that indicates the call is authenticated, then to dump the .json file for easier readability
# Otherwise, it will fail and provide the response code for troubleshooting
if response.status_code == 200:
    data = response.json()
    
    # Filters the .json output to only show the data from indicated fields
    filtered_jobs = [
        {
            "job": job.get("role"),
            "keywords": job.get("keywords"),
            "company_name": job.get("company_name")
        }
        for job in data.get("results",[])
    ]
    
    with open("filtered_jobs.json", "w", encoding="utf-8") as f:
        json.dump(filtered_jobs, f, indent=4, ensure_ascii=False)
        
    print(f"Saved {len(filtered_jobs)} jobs to filtered_jobs.json")
else:
    print(f"Request failed with status {response.status_code}")
    print(response.text)