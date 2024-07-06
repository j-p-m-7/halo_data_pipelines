import pytz
import pandas as pd
from datetime import datetime

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


# Timezone variables
utc_timezone = pytz.utc
est_timezone = pytz.timezone('US/Eastern')
date_format = "%Y-%m-%d %H:%M:%S"

# Last Time Played column name (used in case renamed later)
last_time_played = 'last_time_played'


def convert_to_est(utc_timestamp):
    # Parse the UTC timestamp string to a datetime object
    utc_dt = datetime.strptime(utc_timestamp, "%Y-%m-%d %H:%M:%S")

    # Convert the datetime object to UTC timezone
    utc_dt = utc_timezone.localize(utc_dt)

    # Convert to Eastern Time (ET)
    et_dt = utc_dt.astimezone(est_timezone)

    # Format the timestamp without timezone offset
    formatted_et_timestamp = et_dt.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_et_timestamp



@transformer
def transform(data, *args, **kwargs):
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

    # Reorder columns to have xuid as the first column
    data = data[['xuid'] + [col for col in data.columns if col != 'xuid']]

    # # Select specific columns
    columns_to_keep = ['xuid', 
                       'titleId', 
                       'name', 
                       'achievement.currentAchievements', 
                       'achievement.currentGamerscore', 
                       'achievement.totalGamerscore',
                       'achievement.progressPercentage',
                       'titleHistory.lastTimePlayed',
                       'total_titles_played']

    data = data[columns_to_keep]

    data.columns = ['player_id', 'title_id', 'game', 'game_achievements', 
                    'game_gamerscore', 'game_max_gamerscore', 'game_achievements_progress',
                    'last_time_played', 'total_titles_played']
    
    # Convert multiple columns to int64
    data[['player_id', 'title_id']] = data[['player_id', 'title_id']].astype('int64')
    data['last_time_played'] = data['last_time_played'].astype('datetime64')
    
    # Convert last time played to correct format
    data[last_time_played] = pd.to_datetime(data[last_time_played]).dt.strftime(date_format)
    data[last_time_played] = data[last_time_played].apply(lambda x: convert_to_est(x))
    return data



@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
    #assert (output['titleId'] == 2043073184).all(), "This dataframe is not filtered only to Halo Infinite"