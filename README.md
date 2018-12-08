# Community Clusters in Web Graphs using PySpark

Contains a bootstrap ETL to generate a parquet file of records from a single WARC file of common crawl web data.

## Install modules
All code in this repository uses Python 3.6+ and PySpark 2.3+.  First, install dependencies:
  
    pip3 install -r requirements.txt

## Directory information

-  ```bootstrap```: Contains ETL code and the condensed parquet files with URL information
-  ```data```: Contains results of graph analysis
-  ```public```: Contains D3 visualizations of web graph clusters

## ETL, Analysis and Visualization:
Use commands in [RUNNING.md](https://github.com/mrafayaleem/community-clusters/blob/master/RUNNING.md) to perform analysis and generate results that are visualized in D3. 

Example dataframe created by reading parquet files:

    >>> sqlContext = SQLContext(sc)
    >>> df = sqlContext.read.parquet("./bootstrap/spark-warehouse/<your-directory>*")

    +--------------------+--------------------+-----------+--------------------+-----------+------------+
    |              parent|           parentTLD|   childTLD|               child|childDomain|parentDomain|
    +--------------------+--------------------+-----------+--------------------+-----------+------------+
    |http://1separable...|1separable-43v3r....|twitter.com|http://twitter.co...|    twitter|     skyrock|
    |      http://3msk.ru|             3msk.ru|    k--k.ru|http://k--k.ru/85...|       k--k|        3msk|
    |      http://3msk.ru|             3msk.ru|    com9.ru|http://com9.ru/85...|       com9|        3msk|
    |      http://3msk.ru|             3msk.ru|    com9.ru|http://com9.ru/85...|       com9|        3msk|
    |      http://3msk.ru|             3msk.ru| top.vy3.ru|http://top.vy3.ru...|        vy3|        3msk|
    +--------------------+--------------------+-----------+--------------------+-----------+------------+
    only showing top 5 rows

## Interactive Analysis:
To develop a workflow and make intuitive visualizations, use the Jupyter notebook ```graph_mining.ipynb``` to interactively query the data in PySpark. Requires the PySpark 
environment to be configured on the system:

    export SPARK_HOME=/home/<user>/spark-2.3.1-bin-hadoop2.7/
    export PYSPARK_PYTHON=python3
    
Open and run the ```graph_mining.ipynb``` notebook in a shell that used the above commands, so that the shell knows wher eto find PySpark on your system. 
