# community-clusters

Currently, only contains a bootstrap ETL and the generated parquet file of 114438 records from a single WARC file.

To inspect the parquet file, open up Pyspark shell and run:

```python
df = sqlContext.read.parquet("spark-warehouse/test")
df.show()
df.count()
```

Sample:
```
In [3]: df.count()
Out[3]: 114438

In [4]: df.show(100)
+--------------------+----------------+--------------------+--------------------+
|              parent|       parentTLD|            childTLD|               child|
+--------------------+----------------+--------------------+--------------------+
|http://100balov.info|   100balov.info|    www.facebook.com|https://www.faceb...|
|http://100balov.info|   100balov.info|              vk.com|http://vk.com/sto...|
|http://100balov.info|   100balov.info|         twitter.com|https://twitter.c...|
|http://100balov.info|   100balov.info|               ok.ru|http://ok.ru/prof...|
|http://100balov.info|   100balov.info|      svitppt.com.ua|http://svitppt.co...|
|http://100balov.info|   100balov.info|        arnit.com.ua|http://arnit.com.ua/|
|http://100balov.info|   100balov.info|              vk.com|http://vk.com/sto...|
|http://100balov.info|   100balov.info|    www.facebook.com|https://www.faceb...|
|http://100balov.info|   100balov.info|              vk.com|http://vk.com/sto...|
|http://100balov.info|   100balov.info|         twitter.com|https://twitter.c...|
|http://100balov.info|   100balov.info|               ok.ru|http://ok.ru/prof...|
|http://100balov.info|   100balov.info|      svitppt.com.ua|http://svitppt.co...|
|http://100balov.info|   100balov.info|        arnit.com.ua|http://arnit.com.ua/|
|http://100balov.info|   100balov.info|              vk.com|http://vk.com/sto...|
|http://11210.peta...|  11210.peta2.jp|        bbs.peta2.jp|http://bbs.peta2.jp/|
|     http://1337x.to|        1337x.to|        bitsnoop.com|https://bitsnoop.com|
|     http://1337x.to|        1337x.to| www.limetorrents.cc|https://www.limet...|
|     http://1337x.to|        1337x.to| www.torrentfunk.com|https://www.torre...|
|     http://1337x.to|        1337x.to|  www.torrentbit.net|http://www.torren...|
|     http://1337x.to|        1337x.to|     www.torlock.com|https://www.torlo...|
|     http://1337x.to|        1337x.to|   torrentproject.se|https://torrentpr...|
|     http://1337x.to|        1337x.to|       itorrents.org|http://itorrents....|
|     http://1337x.to|        1337x.to|        torrage.info|http://torrage.in...|
|     http://1337x.to|        1337x.to|          btcache.me|http://btcache.me...|
|     http://1337x.to|        1337x.to|        bitsnoop.com|https://bitsnoop.com|
|     http://1337x.to|        1337x.to| www.limetorrents.cc|https://www.limet...|
|     http://1337x.to|        1337x.to| www.torrentfunk.com|https://www.torre...|
|     http://1337x.to|        1337x.to|  www.torrentbit.net|http://www.torren...|
|     http://1337x.to|        1337x.to|     www.torlock.com|https://www.torlo...|
|     http://1337x.to|        1337x.to|   torrentproject.se|https://torrentpr...|
|     http://1337x.to|        1337x.to|       itorrents.org|http://itorrents....|
|     http://1337x.to|        1337x.to|        torrage.info|http://torrage.in...|
|     http://1337x.to|        1337x.to|          btcache.me|http://btcache.me...|
|     http://1337x.to|        1337x.to|        bitsnoop.com|https://bitsnoop.com|
|     http://1337x.to|        1337x.to| www.limetorrents.cc|https://www.limet...|
|     http://1337x.to|        1337x.to| www.torrentfunk.com|https://www.torre...|
|     http://1337x.to|        1337x.to|  www.torrentbit.net|http://www.torren...|
|     http://1337x.to|        1337x.to|     www.torlock.com|https://www.torlo...|
|     http://1337x.to|        1337x.to|   torrentproject.se|https://torrentpr...|
|     http://1337x.to|        1337x.to|       itorrents.org|http://itorrents....|
|     http://1337x.to|        1337x.to|        torrage.info|http://torrage.in...|
|     http://1337x.to|        1337x.to|          btcache.me|http://btcache.me...|
|     http://1337x.to|        1337x.to| www.sparrowpics.com|https://www.sparr...|
|     http://1337x.to|        1337x.to| www.sparrowpics.com|https://www.sparr...|
|     http://1337x.to|        1337x.to| www.sparrowpics.com|https://www.sparr...|
|     http://1337x.to|        1337x.to| www.sparrowpics.com|https://www.sparr...|
|     http://1337x.to|        1337x.to| www.sparrowpics.com|https://www.sparr...|
|     http://1337x.to|        1337x.to| www.sparrowpics.com|https://www.sparr...|
|     http://1337x.to|        1337x.to|        bitsnoop.com|https://bitsnoop.com|
|     http://1337x.to|        1337x.to| www.limetorrents.cc|https://www.limet...|
|     http://1337x.to|        1337x.to| www.torrentfunk.com|https://www.torre...|
|     http://1337x.to|        1337x.to|  www.torrentbit.net|http://www.torren...|
|     http://1337x.to|        1337x.to|     www.torlock.com|https://www.torlo...|
|     http://1337x.to|        1337x.to|   torrentproject.se|https://torrentpr...|
|     http://1337x.to|        1337x.to|       itorrents.org|http://itorrents....|
|     http://1337x.to|        1337x.to|        torrage.info|http://torrage.in...|
|     http://1337x.to|        1337x.to|          btcache.me|http://btcache.me...|
|     http://1337x.to|        1337x.to|        bitsnoop.com|https://bitsnoop.com|
|     http://1337x.to|        1337x.to| www.limetorrents.cc|https://www.limet...|
|     http://1337x.to|        1337x.to| www.torrentfunk.com|https://www.torre...|
|     http://1337x.to|        1337x.to|  www.torrentbit.net|http://www.torren...|
|     http://1337x.to|        1337x.to|     www.torlock.com|https://www.torlo...|
|     http://1337x.to|        1337x.to|   torrentproject.se|https://torrentpr...|
|     http://1337x.to|        1337x.to|       itorrents.org|http://itorrents....|
|     http://1337x.to|        1337x.to|        torrage.info|http://torrage.in...|
|     http://1337x.to|        1337x.to|          btcache.me|http://btcache.me...|
|http://150currenc...| 150currency.com|www.centralbank.g...|http://www.centra...|
|http://150currenc...| 150currency.com|    en.wikipedia.org|http://en.wikiped...|
|http://150currenc...| 150currency.com|www.centralbank.g...|http://www.centra...|
|http://150currenc...| 150currency.com|     www.nbrm.gov.mk|http://www.nbrm.g...|
|http://150currenc...| 150currency.com|    en.wikipedia.org|http://en.wikiped...|
|http://150currenc...| 150currency.com|     www.nbrm.gov.mk|http://www.nbrm.g...|
|http://150currenc...| 150currency.com| extremetracking.com|http://extremetra...|
|http://182.93.172.45|   182.93.172.45|      202.143.173.44|http://202.143.17...|
|http://182.93.172.45|   182.93.172.45|      202.143.173.44|http://202.143.17...|
|http://182.93.172.45|   182.93.172.45|      202.143.173.44|http://202.143.17...|
|http://182.93.172.45|   182.93.172.45|      202.143.173.44|http://202.143.17...|
|http://182.93.172.45|   182.93.172.45|      202.143.173.44|http://202.143.17...|
|http://182.93.172.45|   182.93.172.45|      202.143.173.44|http://202.143.17...|
|http://182.93.172.45|   182.93.172.45|      202.143.173.44|http://202.143.17...|
|http://182.93.172.45|   182.93.172.45|      202.143.173.44|http://202.143.17...|
|http://182.93.172.45|   182.93.172.45|      202.143.173.44|http://202.143.17...|
|http://182.93.172.45|   182.93.172.45|      202.143.173.44|http://202.143.17...|
|http://182.93.172.45|   182.93.172.45|      202.143.173.44|http://202.143.17...|
|http://182.93.172.45|   182.93.172.45|      202.143.173.44|http://202.143.17...|
|http://182.93.172.45|   182.93.172.45|      202.143.173.44|http://202.143.17...|
|http://182.93.172.45|   182.93.172.45|      202.143.173.44|http://202.143.17...|
|http://182.93.172.45|   182.93.172.45|      202.143.173.44|http://202.143.17...|
|http://182.93.172.45|   182.93.172.45|      202.143.173.44|http://202.143.17...|
|http://182.93.172.45|   182.93.172.45|      202.143.173.44|http://202.143.17...|
|http://182.93.172.45|   182.93.172.45|      202.143.173.44|http://202.143.17...|
|http://182.93.172.45|   182.93.172.45|      202.143.173.44|http://202.143.17...|
|http://182.93.172.45|   182.93.172.45|      202.143.173.44|http://202.143.17...|
|http://182.93.172.45|   182.93.172.45|    drive.google.com|https://drive.goo...|
|http://18teenmovi...|18teenmovies.com|www.virginteenles...|http://www.virgin...|
|http://18yearsold...|  18yearsold.com|images.galleries....|http://images.gal...|
|http://18yearsold...|  18yearsold.com|images.galleries....|http://images.gal...|
|http://18yearsold...|  18yearsold.com|images.galleries....|http://images.gal...|
|http://18yearsold...|  18yearsold.com|images.galleries....|http://images.gal...|
|http://18yearsold...|  18yearsold.com|images.galleries....|http://images.gal...|
+--------------------+----------------+--------------------+--------------------+
only showing top 100 rows
```

bootstrap reads from your local files in parallel.

TODO:
- [ ] Extend `process_warcs` to S3
- [ ] Add `requirements.txt`
