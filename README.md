# Community Clusters in Web Graphs using PySpark

Contains a bootstrap ETL to generate a parquet file of records from a single WARC file of common crawl web data.

Example command to generate the parquet files to ```test/``` from the common crawl data:

    $ spark-submit parent_child.py input/test_warc.txt output s3 commoncrawl 2 

To inspect the parquet file, open up Pyspark shell and run:

```
$ pyspark
>>> df = sqlContext.read.parquet("spark-warehouse/test")
```

Sample:
```
In [3]: df.count()
Out[3]: 5673

In [4]: df.show(10)
+--------------------+--------------+-------------------+--------------------+
|              parent|     parentTLD|           childTLD|               child|
+--------------------+--------------+-------------------+--------------------+
|http://100balov.info| 100balov.info|       facebook.com|https://www.faceb...|
|http://100balov.info| 100balov.info|             vk.com|http://vk.com/sto...|
|http://100balov.info| 100balov.info|        twitter.com|https://twitter.c...|
|http://100balov.info| 100balov.info|              ok.ru|http://ok.ru/prof...|
|http://100balov.info| 100balov.info|     svitppt.com.ua|http://svitppt.co...|
|http://100balov.info| 100balov.info|forum.100balov.info|http://forum.100b...|
|http://100balov.info| 100balov.info|       arnit.com.ua|http://arnit.com.ua/|
|http://11210.peta...|11210.peta2.jp|       bbs.peta2.jp|http://bbs.peta2.jp/|
|     http://1337x.to|      1337x.to|      chat.1337x.to|https://chat.1337...|
|     http://1337x.to|      1337x.to|       bitsnoop.com|https://bitsnoop.com|
+--------------------+--------------+-------------------+--------------------+
only showing top 10 rows

```
Once we have the dataframe of all the parent/child links as above, we can proceed 
to perform graph analysis using PySpark graphframes. 

To run analysis on the Spark shell with the GraphFrames package, specify the below optional arguments (using facebook, twitter and google, and max of 10,000 items as as an example):
    
    `$ spark-submit --packages graphframes:graphframes:0.6.0-spark2.3-s_2.11 analysis.py --dir bootstrap/spark-warehouse/6warcs --focus twitter google facebook`

To plot community clusters after analysis"

    `$ python3 plot_communities.py`

To view communities detected on a browser:

    `$ python3 -m http.server 8000`  OR
    `$ python3 -m SimpleHTTPServer 8000`

Then open:
`localhost:8000/public/index.html` in the browser
TODO:

- [x] Extend `process_warcs` to S3
- [x] Add `requirements.txt`
- [x] use distinct in parent/child domains for analysis
- [x] analyse the popularity of these domains
- [x] analysis around the paths of the popular domains
- [x] visualize the popularity 