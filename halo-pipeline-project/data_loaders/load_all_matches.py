import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test



def get_match_history(xuid, spartan_token):

    headers = {
        "x-343-authorization-spartan": spartan_token,
        "Accept": "application/json"
    }
    
    params = {
        "start": 25  # Specify the match from which to start counting the results
    }

    response = requests.get('https://halostats.svc.halowaypoint.com/hi/players/xuid({})/matches'.format(xuid), headers=headers, params=params)
    match_history = response.json()

    return match_history


def flatten_match_history(match_history_json):
        """
        Flatten the nested JSON structure of match history and return a DataFrame.
        """
        results = match_history_json['Results']

        flattened_data = []
        for result in results:
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

        df = pd.DataFrame(flattened_data)

        return df


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """

    # Get match history
    match_history_json = get_match_history(xuid, spartan_token)
    print("Match history:\n")

    match_history = flatten_match_history(match_history_json)
    return match_history


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
