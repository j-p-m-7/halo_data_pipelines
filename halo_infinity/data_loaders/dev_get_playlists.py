import json
import requests
import pandas as pd



if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test



def get_map_mode_pair(spartan_token, asset_id, version_id, accept='application/json'):
    
    asset_type = "playlists"
    _HOST = "https://discovery-infiniteugc.svc.halowaypoint.com:443"
    url = f"{_HOST}/hi/{asset_type}/{asset_id}/versions/{version_id}"
    
    headers = {
        "x-343-authorization-spartan": spartan_token,
        "Accept": accept
    }

    response = requests.get(url, headers=headers)
    
    if accept == 'application/json':
        result = response.json()
    if accept == 'application/xml':
        result = response.text

    return result



# Function to print results in a pretty format
def pretty_print_json(data):
    print(json.dumps(data, indent=4))



def convert_to_df(data, asset_id, version_id):
    if "title" in data and data["title"] == 'Not Found':

        filtered_data = {
        'asset_id': asset_id,
        'version_id': version_id,
        'matchmake': 0,
        'public_name': "None - May have been deleted",
        'description': "None - May have been deleted"
        }

    else:
        asset_stats = data.get('AssetStats', {})

        filtered_data = {
        'asset_id': data.get('AssetId'),
        'version_id': data.get('VersionId'),
        'matchmake': data.get('AssetHome'),
        'public_name': data.get('PublicName'),
        'description': data.get('Description')
        }

    df = pd.DataFrame([filtered_data])

    return df


@data_loader
def load_data(df, *args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your data loading logic here
    counter = 0
    results = pd.DataFrame()

    spartan_token = kwargs['spartan_token']
    

    # Loop through each row in the DataFrame
    for index, row in df.iterrows():
        # Query the endpoint with parameters from the DataFrame
        data = get_map_mode_pair(spartan_token, row['asset_id'], row['version_id'])
        # If data is returned, append it to the result DataFrame
        if data:
            df = convert_to_df(data, row['asset_id'], row['version_id'])

            results = results.append(df, ignore_index=True)
        
        # counter += 1
        # if counter == 2:
        #     pretty_print_json(data)
        #     exit()

    return results



@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
