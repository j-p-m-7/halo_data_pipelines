from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from os import path
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


def add_foreign_keys_to_all_tables(postgres_loader, table_list):
    for table_name in table_list:
        query = f"""
        ALTER TABLE grunt.{table_name}
        ADD CONSTRAINT fk_match_det
        FOREIGN KEY (_dlt_root_id) REFERENCES grunt.match_det(_dlt_id)
        ON DELETE CASCADE;
        """
        try:
            postgres_loader.execute_query_raw(query)
        except Exception as e:
            print(f"Failed to add foreign key to {table_name}: {e}")



@data_exporter
def export_data(table_name_mapping, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """

    tables = list(table_name_mapping.values())[1:]
    print(tables)

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    
    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        for table in tables:
            try:
                loader.execute_query_raw(
                    query = f"""
                    ALTER TABLE grunt_staging.{table}
                    ADD CONSTRAINT fk_match_det
                    FOREIGN KEY (_dlt_root_id) REFERENCES grunt_staging.match_det(_dlt_id)
                    ON DELETE CASCADE
                    """
                    )
            except:
                print(f"\nForeign key already exists for {table}")
        #add_foreign_keys_to_all_tables(loader, tables)
    




