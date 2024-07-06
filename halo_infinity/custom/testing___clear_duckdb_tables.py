import os
import duckdb
import pandas as pd

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

deleted_rows_count = {}

# Function to delete all data in a table and count rows
def delete_data_in_table(conn, table_name):
    # Get the initial row count
    initial_count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    # Delete all rows
    conn.execute(f"DELETE FROM {table_name}")
    # Store the initial count in the dictionary
    deleted_rows_count[table_name] = initial_count

# Function to verify that a table is empty
def verify_table_empty(conn, table_name):
    result = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()
    assert result[0] == 0, f"Table {table_name} is not empty!"


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
    wal_path = db_path + '.wal'

    # Delete the DuckDB database file
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"{db_path} has been deleted.")
    else:
        print(f"{db_path} does not exist.")

    # Delete the WAL file if it exists
    if os.path.exists(wal_path):
        os.remove(wal_path)
        print(f"{wal_path} has been deleted.")
    else:
        print(f"{wal_path} does not exist.")

    pipeline_name = kwargs['pipeline_name']
    dataset_name = kwargs['dataset_name']

    db_path = f"{pipeline_name}.duckdb"
    wal_path = db_path + ".wal"
    conn = duckdb.connect(db_path)

    # let's see the tables
    conn.sql(f"SET search_path = '{dataset_name}'")
    print(' \nCleared DuckDB tables: ')

    tables = conn.sql("show tables")
    tables_list = tables.df()['name'].to_list()

    for table in tables_list:
        print(table)
        delete_data_in_table(conn, table)
        verify_table_empty(conn, table)

    # Close the connection
    conn.close()


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    for key, value in dictionary.items():
        assert value == 0, f"Value for key '{key}' is not zero but {value}"

