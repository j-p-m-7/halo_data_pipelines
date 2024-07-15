import json
import random
import requests
from time import sleep



if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test



def get_xuid_gamertag(authorization_token, xuid_list, max_retries=20, base_delay=1.5, max_delay=300.0):

    settings = ["Gamertag"]

    url = "https://profile.xboxlive.com/users/batch/profile/settings"

    headers = {
        "Authorization": authorization_token,
        "x-xbl-contract-version": "2",
        "Content-Type": "application/json"
    }

    payload = {
        "userIds": xuid_list,
        "settings": settings
    }

    retries = 0
    gamertags = []

    while retries <= max_retries:
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            profile_data = response.json()

            # nLoop through userrs
            for user in profile_data.get('profileUsers', []):
                xuid = user.get('id')
                gamertag = next((setting.get('value') for setting in user.get('settings', []) if setting.get('id') == 'Gamertag'), None)
                gamertags.append(gamertag)

            # Add jitter delay after a successful request
            jitter = random.uniform(0, base_delay)
            print(f"Successful request. Adding jitter delay of {jitter:.2f} seconds before next operation...")
            sleep(jitter)

            return gamertags  # Return if successful
        elif response.status_code == 400:
            print("Bad Request:", response.json())
            break

        elif response.status_code == 403:
            print("Forbidden:", response.json())
            break

        elif response.status_code == 401:
            print("Unauthorized")
            break

        elif response.status_code == 429:

            retries += 1

            # Calculate exponential backoff with jitter
            delay = min(max_delay, base_delay * (2 ** retries))
            
            # Exponential backoff with jitter
            jitter = random.uniform(0, delay)
            print(f"Rate limited. Retrying in {jitter:.2f} seconds...")
            sleep(jitter)

        else:
            print("Error:", response.status_code, response.text)
            break

    return gamertags


@data_loader
def load_data(df, *args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """

    # Specify your data loading logic here
    xbl_token = kwargs['xbl_token']
    authorization_token = xbl_token
    # xuid_list = df['xuid_numeric'].to_list()[:50]
    df = df.head(50)

    # Define the batch size
    batch_size = 50

    # Loop through the DataFrame in batches and update
    total_rows = len(df)
    print("Total rows: ", total_rows)

    for start_index in range(0, total_rows, batch_size):
        end_index = min(start_index + batch_size, total_rows)
        print("Start index: ", start_index)
        print("End index: ", end_index)
        
        # Fetch col2 values for the current batch
        xuid_list_numeric = df.loc[start_index:end_index-1, 'xuid_numeric'].tolist()
        print("xuid_numeric values: ", xuid_list_numeric)
        
        
        # Instantiate values to add within the loop for the current batch
        values_to_add = get_xuid_gamertag(authorization_token, xuid_list_numeric)
        print("Values to add: ", values_to_add)

        # Check if values_to_add is empty due to max retries reached
        if not values_to_add:
            print("Max retries reached or no gamertags returned. Stopping processing.")
            break
        
        # Update the DataFrame with the unique values for the current batch
        df.loc[start_index:end_index-1, 'gamertag'] = values_to_add
        # print("Updated DataFrame:")
        # print(df)
        #sleep(1)  # Sleep for 1 second for demonstration purposes
        # print('\n\n\n')

    print("Final DataFrame:")
    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
