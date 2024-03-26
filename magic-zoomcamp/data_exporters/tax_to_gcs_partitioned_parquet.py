import pyarrow as pa
import pyarrow.parquet as pq
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

# Tell pyarrow where credentials are
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'home/src/dtc-dez-417003-d2a8b12f96f7.json'
# File location mounted in docker

# Define bucket name
bucket_name = 'mage_zoomcamp_j-p-m-7'

#Define name
project_id = 'dtc-dez-417003'

table_name = 'nyc_taxi_data'

# From here, pyarrow will handle partitioning

@data_exporter
def export_data(data, *args, **kwargs):
    # Specify your data exporting logic here
    


