if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


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
    data = data.drop('hostId', axis=1)

    data.columns = ['player_id', 'is_sponsored_user', 'gamertag', 'gamerscore', 'account_tier', 
                    'years_with_xbox_gold','xbox_one_rep', 'location', 'bio', 'real_name', 
                    'real_name_override', 'modern_gamertag_suffix', 'unique_modern_gamertag',
                    'is_quarantined', 'display_linked_accounts']

    # Convert multiple columns to int64
    columns_to_type_convert_to_int = ['player_id',
                               'gamerscore',
                               'years_with_xbox_gold']
    data[columns_to_type_convert_to_int] = data[columns_to_type_convert_to_int].astype('int64')

    # Convert to boolean values
    data['is_quarantined'] = data['is_quarantined'].apply(lambda x: True if x == 0 else False)

    # Conver to bool
    columns_to_type_convert_to_bool = ['is_quarantined','is_sponsored_user']
    data[columns_to_type_convert_to_bool] = data[columns_to_type_convert_to_bool].astype('bool')

    return data

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
