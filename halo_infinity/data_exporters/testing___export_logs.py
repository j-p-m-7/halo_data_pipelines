from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from pandas import DataFrame
from os import path
import duckdb

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_postgres(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to a PostgreSQL database.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#postgresql
    """
    schema_name = 'spartan_dlt_logs'  # Specify the name of the schema to export data to
    pipeline_name = kwargs['pipeline_name']
    dataset_name = kwargs['dataset_name']
    
    # connect to the database
    conn = duckdb.connect(f"{pipeline_name}.duckdb")

    # let's see the tables
    conn.sql(f"SET search_path = '{dataset_name}'")

    print('Loaded tables: ')
    tables_list = conn.sql("show tables")
    print(tables_list)
    tables_list = tables_list.df()['name'].to_list()


    tables_list = [name for name in tables_list if name.startswith('_dlt')]

    # Dictionary of tables and their primary key columns
    tables_and_pks = {
        '_dlt_loads': 'load_id',
        '_dlt_pipeline_state': 'created_at',
        '_dlt_version': 'inserted_at'
    }

    # Display the tables and set primary keys using the dictionary
    for table in tables_list:
        if table in tables_and_pks:
            pk = tables_and_pks[table]
        
        df = conn.sql(f"SELECT * FROM {table}").df()

        if not df.empty:

            table_name = table  # Specify the name of the table to export data to
            config_path = path.join(get_repo_path(), 'io_config.yaml')
            config_profile = 'dev'

            with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
                loader.export(
                    df,
                    schema_name,
                    table_name,
                    index=False,  # Specifies whether to include index in exported table
                    if_exists='append',  # Specify resolution policy if table name already exists
                    unique_conflict_method="UPDATE",
                    unique_constraints=[pk]
                )

    return "Success"
