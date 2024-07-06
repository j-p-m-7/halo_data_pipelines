import io
import os
import re
import sys
import json
import requests
import dirtyjson
import subprocess
import pandas as pd
from datetime import datetime
import xml.etree.ElementTree as ET
from mage_ai.data_preparation.variable_manager import set_global_variable


""" 
Required installation:
- npm install @xboxreplay/xboxlive-api
- Set credentials in .env
"""


headers = {
        "x-xbl-contract-version": "1"
    }

XSTS_TOKEN_URL = 'https://xsts.auth.xboxlive.com/xsts/authorize'

XBOX_RELYING_PARTIES = ['http://xboxlive.com']
HALO_RELYING_PARTIES = ['https://prod.xsts.halowaypoint.com/']

SPARTAN_TOKEN_URL = 'https://settings.svc.halowaypoint.com/spartan-token'
CLEARANCE_URL = "https://settings.svc.halowaypoint.com/oban/flight-configurations/titles/hi/audiences/RETAIL/players/xuid({})/active?sandbox=UNUSED&build=210921.22.01.10.1706-0"

HALO_INFINITE_STATS_URL = "https://halostats.svc.halowaypoint.com/hi/"
HALO_INFINITE_SKILL_URL = "https://skill.svc.halowaypoint.com/hi/"



if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test



def get_user_token():
    json_data_as_bytes = subprocess.Popen(['/usr/bin/node', 
                            '/home/src/node_js_scripts/halo_auth.js'], 
                            stdout=subprocess.PIPE)

    data_string = json_data_as_bytes.stdout.read()
    cleaned_data_as_string = data_string.decode("utf-8").strip().replace("'", '"')

    # Add double quotes around keys and string values, excluding "service" and "com"
    json_string_fixed = re.sub(r'(?<!:)(\b(?!service|com)[a-zA-Z_][a-zA-Z0-9_]*\b):', r'"\1":', cleaned_data_as_string)
    json_string_fixed = re.sub(r'(?<!:)(\b(?!service|com)[a-zA-Z_][a-zA-Z0-9_]*\b)(?=:)', r'"\1"', json_string_fixed)
    json_string_fixed = json_string_fixed.replace("[Array]", "[]")

    # Parse the fixed JSON string
    data = json.loads(json_string_fixed)
    user_token = data['user.auth.xboxlive.com']['Token']

    return user_token


def get_halo_xsts_token(user_token):

    xsts_token_json = {
    "Properties": {
        "SandboxId": "RETAIL", 
        "UserTokens": [
            user_token
        ]
    },
    "RelyingParty": HALO_RELYING_PARTIES[0],
    "TokenType": "JWT",
    }

    response = requests.post(XSTS_TOKEN_URL, json=xsts_token_json, headers=headers)

    xsts_token_info = response.json()

    if 'error' in xsts_token_info:
        return xsts_token_info

    xsts_token = xsts_token_info['Token']

    return xsts_token


def get_spartan_token(xsts_token):
    spartan_token_json = {
    "Audience": "urn:343:s3:services",
    "MinVersion": "4",
    "Proof": [
        {
            "Token": xsts_token,
            "TokenType": "Xbox_XSTSv3"
        }
    ]
    }
    
    response = requests.post(SPARTAN_TOKEN_URL, json=spartan_token_json)

    if response.status_code != 201:
        return "Error: Get Spartan Token resulted in error"

    spartan_token_raw_xml = response.content.decode('utf-8')  # Decode bytes to string
    root = ET.fromstring(spartan_token_raw_xml)

    # Convert to JSON
    spartan_token_info = json.dumps(
        {
            "ExpiresUtc": root.find('.//{http://schemas.datacontract.org/2004/07/Microsoft.Studios.StudiosNebula.Bond}ISO8601Date').text,
            "SpartanToken": root.find('.//{http://schemas.datacontract.org/2004/07/Microsoft.Halo.RegisterClient.Bond}SpartanToken').text,
            "TokenDuration": root.find('.//{http://schemas.datacontract.org/2004/07/Microsoft.Halo.RegisterClient.Bond}TokenDuration').text
        }
    )

    # Parse response for token
    spartan_token_info = json.loads(spartan_token_info)
    spartan_token = spartan_token_info['SpartanToken']

    return spartan_token


def get_clearance_value(xuid, spartan_token):

        headers = {"x-343-authorization-spartan": spartan_token}
        response = requests.get(CLEARANCE_URL.format(xuid), headers=headers)

        clearance_value = response.json()['FlightConfigurationId']
        return clearance_value


def get_spartan_and_clearance_tokens(xuid):
        # Get user_token for generating a Halo XSTS Token
        user_token = get_user_token()
        
        # Assigns Halo XSTS Token
        xsts_token = get_halo_xsts_token(user_token)

        # Assigns 343 Spartan Token
        spartan_token = get_spartan_token(xsts_token)
        #clearance_value = get_clearance_value(xuid, spartan_token)
        
        return spartan_token#, clearance_value


def get_matches_played_count(xuid, spartan_token):

        headers = {"x-343-authorization-spartan": spartan_token,
            "Accept": "application/json"
        }

        # Match Count
        response = requests.get('https://halostats.svc.halowaypoint.com/hi/players/xuid({})/matches/count'.format(xuid), headers=headers)

        matches_played = response.json()['MatchesPlayedCount']
        return matches_played




@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """

    # Sets global variables to be used downstream
    set_global_variable('get_my_matches', key='accept_header', value='application/json')
    set_global_variable('get_my_matches', key='accept_language_header', value='en-US')
    
    # Get xuid from kwargs
    # If xuid is not provided, use my xuid
    # May be used in the future if we want to get match history for a specific user
    if 'xuid' not in kwargs:
        xuid = 2533274816174040
        set_global_variable('get_my_matches', key='xuid', value=xuid)
    else:
        xuid = kwargs.get('xuid')

    # Test later to see if my xuid is needed or we can use anyones xuid
    spartan_token = get_spartan_and_clearance_tokens(xuid) #, clearance_url

    # Sets more global variables to be used downstream
    set_global_variable('get_my_matches', key='spartan_token', value=spartan_token)
    #set_global_variable('get_my_matches', key='clearance_url', value=clearance_url)

    # Get number of matches played
    matches_count = get_matches_played_count(xuid, spartan_token)
    print("Numer of matches played:\n", matches_count)

    set_global_variable('get_my_matches', key='matches_count', value=matches_count)

    return 'Loading count of all matches...'


    


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

