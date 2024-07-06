import io
import json
import pytz
import requests
import pandas as pd
import xml.dom.minidom
from datetime import datetime

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
        # Max is 25
        "start": index  # Specify the match from which to start counting the results
    }

    response = requests.get('https://halostats.svc.halowaypoint.com/hi/players/xuid({})/matches'.format(xuid), headers=headers, params=params)
    
    if accept == 'application/json':
        match_history = response.json()
    if accept == 'application/xml':
        match_history = response.text

    return match_history


def flatten_match_history(match_history_json, last_match_datetime):
        """
        Flatten the nested JSON structure of match history and return a DataFrame.
        """
        results = match_history_json['Results']
        ignore_counter = 0 

        flattened_data = []
        for result in results:

            # If the match is a custome game, ignore it
            if result['MatchInfo']['LifecycleMode'] == 1:
                #print("Custom game, ignoring...")
                ignore_counter += 1
                continue

            flattened_record = {
                'MatchId': result['MatchId'],
                'StartTime': result['MatchInfo']['StartTime'],
                'EndTime': result['MatchInfo']['EndTime'],
                'Duration': result['MatchInfo']['Duration'],
                'LifecycleMode': result['MatchInfo']['LifecycleMode'],
                'GameVariantCategory': result['MatchInfo']['GameVariantCategory'],
                'LevelId': result['MatchInfo']['LevelId'],
                'MapVariant_AssetKind': result['MatchInfo']['MapVariant']['AssetKind'],
                'MapVariant_AssetId': result['MatchInfo']['MapVariant']['AssetId'],
                'MapVariant_VersionId': result['MatchInfo']['MapVariant']['VersionId'],
                'UgcGameVariant_AssetKind': result['MatchInfo']['UgcGameVariant']['AssetKind'],
                'UgcGameVariant_AssetId': result['MatchInfo']['UgcGameVariant']['AssetId'],
                'UgcGameVariant_VersionId': result['MatchInfo']['UgcGameVariant']['VersionId'],
                'ClearanceId': result['MatchInfo']['ClearanceId'],
                'Playlist_AssetKind': result['MatchInfo']['Playlist']['AssetKind'],
                'Playlist_AssetId': result['MatchInfo']['Playlist']['AssetId'],
                'Playlist_VersionId': result['MatchInfo']['Playlist']['VersionId'],
                'PlaylistExperience': result['MatchInfo']['PlaylistExperience'],
                'PlaylistMapModePair_AssetKind': result['MatchInfo']['PlaylistMapModePair']['AssetKind'],
                'PlaylistMapModePair_AssetId': result['MatchInfo']['PlaylistMapModePair']['AssetId'],
                'PlaylistMapModePair_VersionId': result['MatchInfo']['PlaylistMapModePair']['VersionId'],
                'SeasonId': result['MatchInfo']['SeasonId'],
                'PlayableDuration': result['MatchInfo']['PlayableDuration'],
                'TeamsEnabled': result['MatchInfo']['TeamsEnabled'],
                'TeamScoringEnabled': result['MatchInfo']['TeamScoringEnabled'],
                'GameplayInteraction': result['MatchInfo']['GameplayInteraction'],
                'LastTeamId': result['LastTeamId'],
                'Outcome': result['Outcome'],
                'Rank': result['Rank'],
                'PresentAtEndOfMatch': result['PresentAtEndOfMatch']
            }

            flattened_data.append(flattened_record)
            #print(pd.to_datetime(result['MatchInfo']['StartTime']).tz_convert('US/Eastern').strftime('%Y-%m-%d %H:%M:%S'))
            # if result['MatchInfo']['StartTime'] < last_match_datetime:
            #     print("OI")
            #     #print(result['MatchInfo']['StartTime'])
            #     break
            # print(result['MatchInfo']['StartTime'])
            # print(last_match_datetime)
            # print(result['MatchInfo']['StartTime'] == last_match_datetime)
            
        df = pd.DataFrame(flattened_data)
        if ignore_counter > 0:
            print("Number of ignored records: ", ignore_counter)

        return df


def get_all_matches(xuid, spartan_token, last_match_datetime):
    """
    Get all matches for a player
    """
    
    # Create empty dataframe
    total_match_history_df = pd.DataFrame()

    # Starting index to query match history
    index = 0
    # Limit to how many records can be accessed at once
    result_count = 25

    # # For debugging purposes (break after a certain number of iterations)
    # # Iteration count
    #iteration_count = 0
    # Maximum number of iterations through while loop (for debugging purposes)
    #max_iterations = 100

    while True:
        # Get match history
        match_history = get_match_history(xuid, spartan_token, index, 'application/json')
        #print("Match history:", match_history['ResultCount'])

        # If there are matches in the match history
        if match_history['ResultCount'] != 0:

            # Flatten the match history to a dataframe
            df = flatten_match_history(match_history, last_match_datetime)

            # Append match history to total match history
            total_match_history_df = total_match_history_df.append(df)

            # Update index
            print("Currently loading at index:", index, "to", index + result_count - 1)
            index += result_count
            


            last_record = df['StartTime'].iloc[-1]
            last_record_est = pd.to_datetime(last_record).tz_convert('US/Eastern')
            last_record_datetime = last_record_est.strftime('%Y-%m-%d %H:%M:%S')
            print(last_record_datetime)
            print(last_match_datetime)
            

            if pd.Timestamp(last_record_datetime) < last_match_datetime:
                print("No more match history")
                break

            # # For debugging porposes
            # try:
            # except TypeError:
            #     print("Error in match history")
            #     print(json.dumps(match_history, indent=4))
            #     exit()

        else:
            print("No more match history")
            break
        
        # # For debugging purposes (break after a certain number of iterations)
        # iteration_count += 1
        # if iteration_count >= max_iterations:
        #     break

        # Get the next batch of match history
    
    return total_match_history_df
        

@data_loader
def load_data_from_api(text, last_match_datetime, *args, **kwargs):
    """
    Template for loading data from API
    """
    
    # Using iat
    last_match_datetime = last_match_datetime.iat[0, 0]#.strftime('%Y-%m-%d %H:%M:%S')
    print(last_match_datetime)
     # Localize the naive Timestamp to the local timezone (e.g., US/Eastern)
    # local_tz = pytz.timezone('US/Eastern')
    # local_time = last_match_datetime.tz_localize(local_tz)

    # # Convert the datetime to UTC
    # utc_time = local_time.astimezone(pytz.utc)
    # print(utc_time)

    # # Convert to the desired string format and remove the timezone info
    # last_match_datetime = utc_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-6] + last_match_datetime.strftime('%f')
    # last_match_datetime = last_match_datetime.replace(' ', 'T').replace('000','Z')
    # print(last_match_datetime)


    xuid = kwargs.get('xuid')
    spartan_token = kwargs.get('spartan_token')
    matches_count = kwargs.get('matches_count')
    print("Total matches: ", matches_count)
    
    # # Get match history
    # match_history_json = get_match_history(xuid, spartan_token)
    # print("Length of json: ", len(match_history_json['Results']))
    # print("Match history:\n")
    # match_history = flatten_match_history(match_history_json)

    # Get all match history
    total_match_history = get_all_matches(xuid, spartan_token, last_match_datetime)


    return total_match_history


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
