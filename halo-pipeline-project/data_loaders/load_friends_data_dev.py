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
from mage_ai.data_preparation.variable_manager import set_global_variable


""" 
Required installation:
- npm install @xboxreplay/xboxlive-api
- Set credentials in .env
"""

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test



def get_xbl_token():
    json_data_as_bytes = subprocess.Popen(['/usr/bin/node', 
                            '/home/src/node_js_scripts/xbox_live_auth.js'], 
                            stdout=subprocess.PIPE)

    data_string = json_data_as_bytes.stdout.read()
    cleaned_data_as_string = data_string.decode("utf-8").strip().replace("'", '"')

    # Add double quotes around keys and string values, excluding "service" and "com"
    json_string_fixed = re.sub(r'(?<!:)(\b(?!service|com)[a-zA-Z_][a-zA-Z0-9_]*\b):', r'"\1":', cleaned_data_as_string)
    json_string_fixed = re.sub(r'(?<!:)(\b(?!service|com)[a-zA-Z_][a-zA-Z0-9_]*\b)(?=:)', r'"\1"', json_string_fixed)
    json_string_fixed = json_string_fixed.replace("[Array]", "[]")

    # Parse the fixed JSON string
    data = json.loads(json_string_fixed)

    xbl_token = f"XBL3.0 x={data['user_hash']};{data['xsts_token']}"

    return xbl_token



def get_friends_profiles(authorization_header, *args, **kwargs):
    """
    Get friends profiles
    """
    
    #. Accept json formatting
    accept_language_header = kwargs.get('accept_language_header')
    accept_header = kwargs.get('accept_header')

    # Set up authentication credentials
    x_xbl_contract_version_header = "2"  # Example value: 3
    host_header = "profile.xboxlive.com"

    # Set up optional request headers
    x_requested_service_version_header = "1"  # Default value: 1

    fields = [
    # 'GameDisplayName',
    # 'AppDisplayName',
    'Gamertag',
    'Gamerscore',
    'AccountTier',
    'TenureLevel',
    'XboxOneRep',
    'Location',
    'Bio',
    'RealName',
    'RealNameOverride',
    'ModernGamertagSuffix',
    'UniqueModernGamertag',
    'IsQuarantined',
    'DisplayedLinkedAccounts'
    # 'GameDisplayPicRaw',
    # 'PreferredColor',
    # 'Watermarks',
    ]

    # Join the fields into a single string separated by commas
    fields = ",".join(fields)

    # Set up request URL
    moniker = "People"  # The only accepted moniker is "People"
    url = f"https://profile.xboxlive.com/users/me/profile/settings/people/{moniker}?settings={fields}"

    # Set up request headers
    headers = {
        "Authorization": authorization_header,
        "x-xbl-contract-version": x_xbl_contract_version_header,
        "Accept": accept_header,
        "Accept-Language": accept_language_header,
        "Host": host_header,
        "X-RequestedServiceVersion": x_requested_service_version_header
    }

    #Send GET request
    response = requests.get(url, 
                            #params=params,
                            headers=headers)

    # Check response status code
    if response.status_code == 200:

        # DataFrame containing in depth data for each friend on friends list
        data = json.loads(response.text)

        friends_df = pd.DataFrame()


        for x in range(len(data["profileUsers"])):
            # Create first dataframe with id info only
            df_1 = pd.json_normalize(data['profileUsers'][x]).drop(columns=['settings'])
            df_1['isSponsoredUser'] = df_1['isSponsoredUser'].astype(object)

            # Create second dataframe with more info in settings field
            settings = data['profileUsers'][x]['settings']

            # Convert settings to DataFrame
            df_2 = pd.DataFrame(settings)

            # Transpose the DataFrame
            df_2 = df_2.set_index('id').transpose()

            # Reset index to ensure alignment
            df_1.reset_index(drop=True, inplace=True)
            df_2.reset_index(drop=True, inplace=True)

            # Concatenate dataframes horizontally
            df = pd.concat([df_1, df_2], axis=1)

            # Append to table containing all friends data from this for loop
            friends_df = friends_df._append(df, ignore_index=True)


        friends_df = friends_df.rename(columns={'id':'xuid'})

        return friends_df
    
    else:
        
        # Error handling
        print(f"Error: {response.status_code} - {response.reason}")
        return "Error", "Error"



@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """

    # Get authorization token/code used for getting Xbox data 
    authorization_header = get_xbl_token()

    # Sets global variables to be used downstream
    set_global_variable('load_friends_info', key='authorization_header', value=authorization_header)
    set_global_variable('load_friends_info', key='accept_language_header', value='en-US')
    set_global_variable('load_friends_info', key='accept_header', value='application/json')

    # Getting ddf of friends and list of friends ids
    friends_df = get_friends_profiles(authorization_header)

    return friends_df
    



@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
    assert (output['xuid'] == output['hostId']).all(), "xuid and hostID are not the same"
    assert (output['RealName'] == output['RealNameOverride']).all(), "xuid and hostID are not the same"

    #assert (output['IsQuarantined'] == 0).all(), "Not all values in IsQuarantined are equal to 0"



