
Steps to run ETL process:

ETL process should be executed from the bootstrap directory.

`etl.sh` takes 5 arguments as follows:
1. Input path containing warc paths
2. Output name (Usually month for which the ETL is executed)
3. Type of input (specifies if warc files should be loaded from local drive or s3). Options are:
    * s3
    * file
4. Craw path. Should be file path of your crawl data if type of input is file. Should be bucket (commoncrawl) in case of s3.
5. Batch size. Specifies how may batches of warc files to process in a single run.

For file:
```bash
cd  bootstrap
./etl.sh execute input_paths/may.warc.paths may file /Users/rafay/datalab/community-clusters/bootstrap 1
```

For S3:
```bash
cd  bootstrap
./etl.sh execute input_paths/may.warc.paths may s3 commoncrawl 10
```
