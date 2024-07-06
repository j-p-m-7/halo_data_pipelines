import re
import pytz
import pandas as pd
from datetime import datetime


# # Parse the timestamp string into a datetime object
# timestamp = datetime.fromisoformat('2024-05-25T23:24:35.282Z'.replace('T', ' '))

# # Convert the timestamp to EST
# timestamp_est = timestamp.astimezone(pytz.timezone('US/Eastern'))

# # Print the timestamp in ISO format and EST
# print(timestamp_est.isoformat())

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


def convert_to_snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def convert_duration(duration_str):
    # Remove 'PT' and 'S'
    duration_str = duration_str.replace('PT', '').replace('S', '')

    hours, minutes, seconds = '0', '0', '0'

    # Check if 'H' is in the string
    if 'H' in duration_str:
        hours, duration_str = duration_str.split('H')

    # Check if 'M' is in the string
    if 'M' in duration_str:
        minutes, seconds = duration_str.split('M')
    else:
        # If 'M' is not in the string, assume the whole string is seconds
        seconds = duration_str

    # Convert hours, minutes and seconds to integers
    hours = int(hours)
    minutes = int(minutes)
    seconds = int(float(seconds))

    # Format as 'HH:MM:SS'
    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'


@transformer
def transform(df, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here

    # Converts the column names to snake case
    df.columns = df.columns.map(convert_to_snake_case)
   

    # Date formatting and type conversions
    # Convert the start_time and end_time columns to datetime, EST, and then removes chars
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['start_time'] = pd.to_datetime(df['start_time']).dt.tz_convert('US/Eastern')
    df['start_time'] = df['start_time'].dt.strftime('%Y-%m-%d %H:%M:%S.%f')
    df['start_time'] = pd.to_datetime(df['start_time'])

    df['end_time'] = pd.to_datetime(df['end_time'])
    df['end_time'] = pd.to_datetime(df['end_time']).dt.tz_convert('US/Eastern')
    df['end_time'] = df['end_time'].dt.strftime('%Y-%m-%d %H:%M:%S.%f')
    df['end_time'] = pd.to_datetime(df['end_time'])

    

    # Duration formatting and type conversions
    df['duration'] = df['duration'].apply(convert_duration)
    #df['duration'] = pd.to_timedelta(df['duration'])

    df['playable_duration'] = df['playable_duration'].apply(convert_duration)
    #df['playable_duration'] = pd.to_timedelta(df['playable_duration'])

    # Converts data types to the most appropriate type
    df = df.convert_dtypes()
    
    print(len(df))

    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
