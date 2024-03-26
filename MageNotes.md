## 2.2.4 ETL: API to GCS
### Methodology
Data will be written to cloud bc storage is much cheaper and can accept semi-structured data much better than traditional RDB

From there, workflows involve staging, cleaning, and writing to analytical source. Or using data lake solution in cloud

#

### Coding Tips
Can drag and drop old data loaders/transformers. Be sure to link them together in tree view

### Data Engineering Principles
For large datasets, should we write to a single parquet file?

No!

We will partition by date so we can create even distribution for taxi rides
