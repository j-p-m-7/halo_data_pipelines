import json
import requests



if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test



def test_endpoint(spartan_token, endpoint, accept='application/json'):
    headers = {
        "x-343-authorization-spartan": spartan_token,
        "Accept": accept
    }

    response = requests.get(endpoint, headers=headers)
    
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
    
    asset_type = "maps"
    asset_id="37a9b5f0-6be7-4a46-8010-1fe6f7ea5611"
    version_id="e1cbf812-4f4e-44fc-9ef8-dd9ab5c4e4cf"

    url = f"{_HOST}/hi/{asset_type}/{asset_id}/versions/{version_id}"
    result = test_endpoint(spartan_token, url)
    pretty_print_json(result)

    # # Example of fetching playlist details
    # playlist_details = await service.get_playlist(
    #     asset_id="759021fe-1d82-470f-a2e6-e431300b384b",
    #     version_id="91383e7c-ba09-425a-ade0-3b42d90f75c9"
    # )

    # # Example of fetching film details by match ID
    # film_details = await service.get_film_by_match_id(
    #     match_id="006ef7e0-1821-4a79-9442-e6134853df91"
    # )

    
    return "Success!"



@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
