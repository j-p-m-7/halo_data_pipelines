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


if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test



# def titles_json_to_df(parsed_json):
    
    
#     return df



def get_titles_test(xuid, authorization_header, accept_language_header, accept_header):

    # accept_language_header = 'accept_language_header'
    # accept_header = 'accept_header'

    TITLEHUB_URL = "https://titlehub.xboxlive.com"
                  
    fields = [
        "achievement"
    ]

    # Join the fields into a single string separated by commas
    fields = ",".join(fields)

    headers = {
                "Authorization": authorization_header,
                "x-xbl-contract-version": "2",
                "x-xbl-client-name": "XboxApp",
                "Accept": accept_header,
                "x-xbl-client-type": "UWA",
                "x-xbl-client-version": "39.39.22001.0",
                "Accept-Language": accept_language_header
            }
    url = f"{TITLEHUB_URL}/users/xuid({xuid})/titles/titlehistory/decoration/{fields}"

    resp = requests.get(url, 
                        #params=params,
                        headers=headers)

    data = resp.json()
    #print("Player", xuid, "has played a total of", len(data['titles']), "title(s)")

    # Check if name == "Halo Infinite"
    at_least_one_halo_infinite = any(title["name"] == "Halo Infinite" for title in data["titles"])
    
    if at_least_one_halo_infinite:
        # Extract required fields
        # Filter out titles other than "Halo Infinite"
        filtered_titles = [title for title in data["titles"] if title["name"] == "Halo Infinite"]
        

        # Extract required fields
        parsed_data = {
            "xuid": data["xuid"],
            "titles": [
                {
                    "titleId": title["titleId"],
                    "name": title["name"],
                    "achievement": title["achievement"],
                    "titleHistory": title["titleHistory"]
                }
                for title in filtered_titles
            ]
        }
        if parsed_data:
            # Convert back to JSON
            parsed_json = json.dumps(parsed_data, indent=2)
            
            # Returns JSON and total_titles_played
            return json.loads(parsed_json), len(data['titles'])
        else:
            return {}, 0  # Return empty JSON and 0 titles played if no Halo Infinite played
    else:
        return {}, 0  # Return empty JSON and 0 titles played if no Halo Infinite played



@data_loader
def load_data(friends_df, *args, **kwargs):
    
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """

    # Initialize df for friends who play Halo Infinite
    halo_friends_df = pd.DataFrame()  

    list_of_friends_ids = friends_df['xuid'].tolist()

    authorization_header = kwargs.get('authorization_header')
    accept_language_header = kwargs.get('accept_language_header')
    accept_header = kwargs.get('accept_header')


    # Total number of values
    total_friends = len(list_of_friends_ids)

    # Loop through values
    for index, xuid in enumerate(list_of_friends_ids):
        # Calculate progress percentage
        #progress = (index / total_friends) * 100
        
        # Check if progress is at 25%, 50%, 75%, and 100%
        # if 24.5 < progress < 25.5:
        #     print("25% done")
        # elif 49.5 < progress < 51.0:
        #     print("50% done")
        # elif 74.5 < progress < 75.5:
        #     print("75% done")
            

        # Only returns value if friend plays Halo Infinite
        # parsed_json contains data related to Halo Plays (achievement, last time played, etc.)
        # total_titles_played returns sum of titles played by a friend (this will be added to the dataframe for the friend)
        parsed_json, total_titles_played = get_titles_test(xuid, 
                                                           authorization_header, 
                                                           accept_language_header,
                                                           accept_header)

        # If they do
        if parsed_json:        
            # Convert JSON to DataFrame
            df = pd.json_normalize(parsed_json['titles'])
            df['xuid'] = parsed_json['xuid']  # Add xuid column
            #print("Loading", str(df['xuid'].iloc[0]), "to df...")

            # Adds total_titles_played to individual friend record
            df['total_titles_played'] = total_titles_played

            # Appends info from JSON to DataFrame (This DF contains all friends who play Halo Infinite)
            halo_friends_df = halo_friends_df._append(df, ignore_index=True)
            
    #print("100% done")

    #print("Friends who play Halo Infinite:",len(halo_friends_df))

    return halo_friends_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
