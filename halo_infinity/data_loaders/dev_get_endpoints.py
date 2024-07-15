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

    endpoints = [
    "https://discovery-infiniteugc.svc.halowaypoint.com/hi/engineGameVariants/b6aca0c7-8ba7-4066-bf91-693571374c3c/versions/c63ee410-784e-46ae-911e-ab7bc35933b1",
    "https://discovery-infiniteugc.svc.halowaypoint.com/hi/engineGameVariants/b6aca0c7-8ba7-4066-bf91-693571374c3c",
    "https://discovery-infiniteugc.svc.halowaypoint.com/hi/ugcGameVariants/c2d20d44-8606-4669-b894-afae15b3524f/versions/9eee25fe-39db-493f-ab0d-d95403df66b8",
    "https://discovery-infiniteugc.svc.halowaypoint.com/hi/ugcGameVariants/c2d20d44-8606-4669-b894-afae15b3524f",
    "https://discovery-infiniteugc.svc.halowaypoint.com/hi/playlists/edfef3ac-9cbe-4fa2-b949-8f29deafd483/versions/812e8daf-a564-4021-92ef-57177817eb46",
    "https://discovery-infiniteugc.svc.halowaypoint.com/hi/playlists/edfef3ac-9cbe-4fa2-b949-8f29deafd483",
    "https://discovery-infiniteugc.svc.halowaypoint.com/hi/mapModePairs/2c6df2e1-b2d0-4572-b44e-8352aa3b1d77/versions/e7eba82b-7f28-4d2f-a4c1-b5aa4af52e1c",
    "https://discovery-infiniteugc.svc.halowaypoint.com/hi/mapModePairs/2c6df2e1-b2d0-4572-b44e-8352aa3b1d77"
    ]

    #endpoint = endpoints[2]
    #endpoint = endpoints[3]
    url = endpoints[6]






    

    # match_type = "matchmade"
    # xuid_or_gamertag = "xuid(2533274848622227)"
    # _HOST = "https://halostats.svc.halowaypoint.com:443"
    
    # endpoint = f"/hi/players/{xuid_or_gamertag}/{match_type}/servicerecord"
    
    # url = f"{_HOST}{endpoint}"


    _HOST = "https://discovery-infiniteugc.svc.halowaypoint.com:443"
    
    _SortProperty = Literal[
        "name",
        "likes",
        "bookmarks",
        "plays_recent",
        "number_of_objects",
        "date_created_utc",
        "date_modified_utc",
        "date_published_utc",
        "plays_all_time",
        "parent_asset_count",
        "average_rating",
        "number_of_ratings",
    ]

    url = f"{_HOST}/hi/{asset_type}/{asset_id}/versions/{version_id}"




    #endpoints = [endpoints[i] for i in [2, 3, 6]]

    # for endpoint in endpoints:
    #     result = test_endpoint(spartan_token, endpoint)
    #     print('\n\n' + endpoint + ':')
    #     pretty_print_json(result)
    #     print('\n\n\n\n\n')

    result = test_endpoint(spartan_token, url)
    print('\n\n' + url + ':')
    pretty_print_json(result)

    # File path to save the JSON data
    file_path = 'output.json'

    # Writing JSON data to the file
    with open(file_path, 'w') as json_file:
        json.dump(result, json_file, indent=4)



    return "Success!"



@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
