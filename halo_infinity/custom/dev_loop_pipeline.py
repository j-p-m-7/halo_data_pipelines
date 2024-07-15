import requests

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@custom
def transform_custom(*args, **kwargs):
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your custom logic here
    

    # Define the API endpoint and the trigger ID
    url = 'http://localhost:6789/api/pipeline_schedules/1/pipeline_runs/446d8c32da0049e997e7df9692f9447d'

    # Define the request payload
    payload = {}

    # Define the headers
    headers = {
        'Content-Type': 'application/json'
    }

    # Make the POST request
    response = requests.post(url, headers=headers)

    # Check the response
    if response.status_code == 200:
        print('Pipeline triggered successfully.')
    else:
        print(f'Failed to trigger pipeline. Status code: {response.status_code}')
        print(response.text)

    return 'Looping back through!'


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
