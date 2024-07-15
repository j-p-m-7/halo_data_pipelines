import io
import os
import time
import json
import pytz
import requests
import pandas as pd
import xml.dom.minidom
from datetime import datetime, date
from urllib.parse import urlencode

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def get_match_history(xuid, spartan_token, index, accept='application/json'):
    headers = {
        "x-343-authorization-spartan": spartan_token,
        "Accept": accept
    }
    
    params = {
        "start": index
    }

    base_url = 'https://halostats.svc.halowaypoint.com/hi/players/xuid({})/matches'.format(xuid)
    response = requests.get(base_url, headers=headers, params=params)
    
    if accept == 'application/json':
        match_history = response.json()
    if accept == 'application/xml':
        match_history = response.text

    return match_history

# Generator function to fetch match history in batches with a date check
def match_history_generator(xuid, spartan_token, batch_size, cutoff_date):
    start_index = 0
    
    while True:
        start_time = time.time()
        match_history_json = get_match_history(xuid, spartan_token, start_index)
        elapsed_time = time.time() - start_time

        if match_history_json['ResultCount'] == 0:
            break

        # Check if any match date is earlier than the cutoff date
        recent_matches = match_history_json['Results']
        yield_recent_matches = True
        for match in recent_matches:
            match_start_time = datetime.strptime(match['MatchInfo']['StartTime'], '%Y-%m-%dT%H:%M:%S.%fZ').date()
            if match_start_time < cutoff_date:
                print(f"Stopping processing as match date {match_start_time} is earlier than cutoff date {cutoff_date}")
                yield_recent_matches = False
                break
        
        if yield_recent_matches:
            yield recent_matches
        else:
            yield recent_matches
            break
        start_index += batch_size

def get_full_match_history(xuid, spartan_token, cutoff_date):
    match_history = []
    total_matches = 0

    for match_batch in match_history_generator(xuid, spartan_token, batch_size=25, cutoff_date=cutoff_date):
        match_history.extend(match_batch)
        total_matches += len(match_batch)
        if total_matches % 500 == 0:
            print(f"Total matches loaded: {total_matches}")

    return match_history

@data_loader
def load_data_from_api(df, df2, *args, **kwargs):
    xuid = kwargs.get('xuid')
    spartan_token = kwargs.get('spartan_token')
    matches_count = kwargs.get('matches_count')
    cutoff_date = df2.iloc[0,0]  # Ensure cutoff_date is provided in 'YYYY-MM-DD' format
    
    print("Total matches: ", matches_count)
    
    full_match_history = get_full_match_history(xuid, spartan_token, cutoff_date)

    print("Total matches retrieved:", len(full_match_history))

    for record in full_match_history:
        print(record['MatchInfo']['StartTime'])
        print(datetime.strptime(record['MatchInfo']['StartTime'], '%Y-%m-%dT%H:%M:%S.%fZ').date())
  
    return full_match_history

@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'
