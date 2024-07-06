from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from pandas import DataFrame
from os import path
import duckdb
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter



@data_exporter
def export_data_to_postgres(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to a PostgreSQL database.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#postgresql
    """
    schema_name = 'spartan'  # Specify the name of the schema to export data to
    pipeline_name = kwargs['pipeline_name']
    dataset_name = kwargs['dataset_name']
    
    # connect to the database
    conn = duckdb.connect(f"{pipeline_name}.duckdb")
    conn.sql(f"SET search_path = '{dataset_name}'")

    print('Loaded tables: ')
    tables_list = conn.sql("show tables")
    print(tables_list)
    tables_list = tables_list.df()['name'].to_list()

    tables_list = [name for name in tables_list if not name.startswith('_dlt')]
    #tables_list = ['match_details']
    tables_added = []

    table_name_mapping = {
    "match_details": "match_det",
    "match_details__players": "match_det_players",
    "match_details__players__player_team_stats": "match_det_players_team_stats",
    "match_details__players__player_team_stats__stats__core_stats__medals": "match_det_players_team_stats_medals",
    "match_details__players__player_team_stats__stats__core_stats__personal_scores": "match_det_players_team_stats_scores",
    "match_details__teams": "match_det_teams",
    "match_details__teams__stats__core_stats__medals": "match_det_teams_stats_medals",
    "match_details__teams__stats__core_stats__personal_scores": "match_det_teams_stats_scores"
    }

    # Display the tables and set primary keys using the dictionary
    for table, postgres_table in table_name_mapping.items():
        #print(table)
        if 1==1:
        #try:
            df = conn.sql(f"SELECT * FROM {table}").df()
            table_name = postgres_table  # Specify the name of the table to export data to
            config_path = path.join(get_repo_path(), 'io_config.yaml')
            config_profile = 'dev'

            with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
                loader.export(
                    df,
                    schema_name,
                    table_name,
                    index=False,  # Specifies whether to include index in exported table
                    if_exists='append', # Specify resolution policy if table name already exists
                    unique_conflict_method='UPDATE',
                    unique_constraints=['_dlt_id']
                )
            tables_added.append(table)
        # except:
        #     unique_violation = 'True'
        #     continue

    print("Records added to PostgreSQL")

    # if unique_violation:
    #     return_statement = 'UniqueViolation: Records were not added but DuckDB instance was cleared'

    return table_name_mapping