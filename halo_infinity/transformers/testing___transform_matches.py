import dlt
import duckdb
import pandas as pd
from mage_ai.data_preparation.variable_manager import set_global_variable

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
    mage_pipeline_name = kwargs['mage_pipeline_name']
    table = "match_history"
    set_global_variable('testing___get_matches', key='table', value=table)

    # create a pipeline and set dataset name
    pipeline = dlt.pipeline(destination='duckdb', dataset_name='halo_test')
    set_global_variable('testing___get_matches', key='pipeline_name', value=pipeline.pipeline_name)
    set_global_variable('testing___get_matches', key='dataset_name', value=pipeline.dataset_name)
    

    # run the pipeline
    info = pipeline.run(data,
                        table_name=table,
                        write_disposition="merge",
                        primary_key="MatchId")

    # print the pipeline information
    print("Pipeline name: ",pipeline.pipeline_name)
    print("Dataset name: ",pipeline.dataset_name)
    print("Table name: ",table,'\n')

    # connect to the database
    conn = duckdb.connect(f"{pipeline.pipeline_name}.duckdb")

    # let's see the tables
    conn.sql(f"SET search_path = '{pipeline.dataset_name}'")
    print(' \n\n\nLoaded tables: ')
    print(conn.sql("show tables"))
    #tables_list = conn.sql("show tables").df()['name'].to_list()

    df = conn.sql(f"SELECT * FROM {table}").df()
    print("df columns", df.columns)

    print(" \n\n\nLoaded matches:")
    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
