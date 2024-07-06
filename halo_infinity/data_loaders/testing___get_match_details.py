import io
import os
import time
import json
import requests
import pandas as pd

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test



def get_match_details(xuid, match_id, spartan_token, accept='application/json'):

    headers = {
        "x-343-authorization-spartan": spartan_token,
        "Accept": accept
    }

    base_url = 'https://halostats.svc.halowaypoint.com/hi/matches/{}/stats'.format(match_id)

    response = requests.get(base_url, headers=headers)
    if response.status_code == 401:
        print("Authentication failed. Please check your token.")
        print("Response Headers:", response.headers)
        print("Response Text:", response.text)
    
    if accept == 'application/json':
        match_history = response.json()
    if accept == 'application/xml':
        match_history = response.text

    return match_history



# Generator function to fetch match history in batches
def match_history_generator(xuid, match_ids, spartan_token):
    for match_id in match_ids:
        start_time = time.time()  # Start timing
        match_details = get_match_details(xuid, match_id, spartan_token)
        elapsed_time = time.time() - start_time  # End timing
        
        if match_details is None:
            break

        yield match_details

        #print for debugging
        print(f"Elapsed Time: {elapsed_time:.2f} seconds")

# Function to consume the generator and extend match history
def get_full_match_history(xuid, match_ids, spartan_token):
    match_history = []
    total_matches = 0

    for match_details in match_history_generator(xuid, match_ids, spartan_token):
        match_history.append(match_details)
        total_matches += 1
        # if total_matches == 10:
        #     break
        if total_matches % 50 == 0:
            print(f"Total matches loaded: {total_matches}")

    return match_history



@data_loader
def load_data_from_api(df, *args, **kwargs):
    """
    Template for loading data from API
    """

    xuid = kwargs.get('xuid')
    spartan_token = kwargs.get('spartan_token')
    matches_count = kwargs.get('matches_count')

    # Dataframe contains 1 column, convert this to a list
    match_ids = df['match_id'].tolist()

    match_details = get_full_match_history(xuid, match_ids, spartan_token)
    print(len(match_details))

    return match_details


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
