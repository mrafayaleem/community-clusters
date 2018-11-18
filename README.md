# community-clusters

Currently, only contains a bootstrap ETL and the generated parquet file of 114438 records from a single WARC file.

To inspect the parquet file, open up Pyspark shell and run:

```python
df = sqlContext.read.parquet("spark-warehouse/test")
df.show()
df.count()
```

bootstrap reads from your local files in parallel.

TODO:
- [ ] Extend `process_warcs` to S3
- [ ] Add `requirements.txt`
