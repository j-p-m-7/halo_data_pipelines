import os
import duckdb
import pandas as pd

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
       # connect to the database
       
    db_path = kwargs['db_path']
    pipeline_name = kwargs['pipeline_name']
    dataset_name = kwargs['dataset_name']

    # let's see the tables
    conn = duckdb.connect(db_path)
    conn.sql(f"SET search_path = '{dataset_name}'")
    print(' \nDuckDB tables: ')

    tables = conn.sql("show tables")
    tables_list = tables.df()['name'].to_list()

    for table in tables_list:
        print(table)

    print(conn.sql("SELECT * FROM _dlt_pipeline_state").df())

    # Close the connection
    conn.close()



@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    for key, value in dictionary.items():
        assert value == 0, f"Value for key '{key}' is not zero but {value}"

