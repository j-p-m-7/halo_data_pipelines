from mage_ai.data_cleaner.transformer_actions.base import BaseAction
from mage_ai.data_cleaner.transformer_actions.constants import ActionType, Axis
from mage_ai.data_cleaner.transformer_actions.utils import build_transformer_action
from pandas import DataFrame

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def execute_transformer_action(df: DataFrame, *args, **kwargs) -> DataFrame:
    """
    Execute Transformer Action: ActionType.CLEAN_COLUMN_NAME

    Docs: https://docs.mage.ai/guides/transformer-blocks#clean-column-names
    """

    cols = df.columns
    print(cols)
    renamed_cols = [col.removeprefix("match_info__") if "match_info" in col else col for col in cols]
    print(renamed_cols)

    df.columns = renamed_cols
    #return df
    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
