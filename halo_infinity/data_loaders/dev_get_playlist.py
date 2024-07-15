import json
import requests



if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test



def test_endpoint(spartan_token, url, accept='application/json'):
    headers = {
        "x-343-authorization-spartan": spartan_token,
        "Accept": accept
    }
    
    # Define the fields you want
    fields = "AssetId,VersionId,PublicName,Description,AssetStats"


    # Parameters dictionary
    params = {
        'fields': fields
    }

    response = requests.get(url, params=params, headers=headers)
    
    if accept == 'application/json':
        result = response.json()
    if accept == 'application/xml':
        result = response.text

    return result



# Function to print results in a pretty format
def pretty_print_json(data):
    print(json.dumps(data, indent=4))



@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your data loading logic here
    spartan_token = kwargs.get('spartan_token')


    _HOST = "https://discovery-infiniteugc.svc.halowaypoint.com:443"
    
    asset_type = "playlists"
    asset_id="1b1691dc-d8b9-4b1f-825d-cb1c065184c1"
    version_id="a6b78616-28bb-4be3-b010-9ffdf553a78e"

    url = f"{_HOST}/hi/{asset_type}/{asset_id}/versions/{version_id}"
    result = test_endpoint(spartan_token, url)
    #pretty_print_json(result)

    # Define the file path
    file_path = 'output.json'

    # Write JSON data to file
    with open(file_path, 'w') as json_file:
        json.dump(result, json_file, indent=4)

    print(f"Data has been written to {file_path}")

    
    return "Success!"



@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
