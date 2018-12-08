
# ETL for data extraction and cleaning:

ETL process should be executed from the bootstrap directory.

`etl.sh` takes 5 arguments as follows:
1. Input path containing warc paths
2. Output name (Usually month for which the ETL is executed)
3. Type of input (specifies if warc files should be loaded from local drive or S3). Options are:
    * S3: use this if you want to access the crawl data through S3 buckets (does not need S3 credentials) 
    * file: use this if you want to work on WARC data that exists on your local machine
4. Crawl path. Should be file path of your crawl data if type of input is file. Should be bucket (commoncrawl) in case of S3.
5. Batch size. Specifies how may batches of warc files to process in a single run.

Note that if you are running ETL from local drive, you will need to download sample crawl data using the following command. This might take a couple of hours.
```
cd  bootstrap
./get-data.sh
```

## To run ETL from S3 (For the month of may):
```bash
cd  bootstrap
./etl.sh execute input_paths/may.warc.paths may S3 commoncrawl 10
```

## To run ETL from the file:
```bash
cd  bootstrap
./etl.sh execute input_paths/may.warc.paths may file /Users/rafay/datalab/community-clusters/bootstrap 1
```

# Analysis and Visualiztion:

This process should be executed from the root directory.

`autoAnalysis.sh` takes 3 arguments as follows:
1. Category of focus e.g. shopping
2. Focus Domains e.g. 'etsy ebay amazon'
3. Month e.g may

## Run analysis and generate visualization files:
```
./autoAnalysis.sh shopping  'etsy ebay amazon' may
```

## View results in browser:
```
python3 -m http.server 8080
```

Then navigate to `public/index-` + category + `-` + month + `.html` on your browser
e.g.

    localhost:8080/public/index-shopping-may.html