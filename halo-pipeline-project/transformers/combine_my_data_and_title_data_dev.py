import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(friends_data, friends_title_data, *args, **kwargs):
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

    player_data = pd.merge(friends_data, friends_title_data, on='player_id', how='inner')
    assert len(player_data.columns) == len(friends_data.columns) + len(friends_title_data.columns) - 1, "Not all columns were added"


    player_data = player_data.rename(columns={'gamerscore': 'total_gamerscore'})


    columns_order = [
    'player_id',
    'gamertag',
    'modern_gamertag_suffix',
    'unique_modern_gamertag',
    'account_tier',
    'years_with_xbox_gold',
    'real_name',
    'real_name_override',
    'location',
    'bio',
    'xbox_one_rep',
    'is_quarantined',
    'is_sponsored_user',
    'total_gamerscore',
    'total_titles_played',
    'title_id',
    'game',
    'last_time_played',
    'game_achievements',
    'game_gamerscore',
    'game_max_gamerscore',
    'game_achievements_progress'
    ]

    player_data = player_data[columns_order]

    return player_data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
