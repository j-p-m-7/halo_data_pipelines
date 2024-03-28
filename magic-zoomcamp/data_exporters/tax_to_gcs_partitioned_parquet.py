import pyarrow as pa
import pyarrow.parquet as pq
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

# Tell pyarrow where credentials are
# File location mounted in docker
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/src/dtc-dez-417003-d2a8b12f96f7.json"

# Define bucket name
bucket_name = 'mage_zoomcamp_j-p-m-7'

project_id = 'dtc-dez-417003'

table_name = "nyc_taxi_data"

root_path = f'{bucket_name}/{table_name}'


# From here, pyarrow will handle partitioning 


@data_exporter
def export_data(data, *args, **kwargs):
    # Specify your data exporting logic here
    # Create date column 
    # Datetime column should give us date in string format
    data['tpep_pickup_date'] = data['tpep_pickup_datetime'].dt.date

    # Pyarrow table 
    table = pa.Table.from_pandas(data)

    # Google Cloud Storage Object in pyarrow filesystem
    # Authorizes usage of env variable automatically
    gcs = pa.fs.GcsFileSystem()

    #
    pq.write_to_dataset(
        table,
        root_path,
        partition_cols=['tpep_pickup_date'],
        filesystem=gcs
    )


