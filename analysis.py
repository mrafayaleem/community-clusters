import pyspark
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.functions import udf
from graphframes import *
import hashlib

sc = SparkContext(appName="Community Clustering") 
sqlContext = SQLContext(sc)

df = sqlContext.read.parquet("./bootstrap/spark-warehouse/test")
distinct_df = df.distinct().limit(10000)

# Select set of parents and children TLDs (nodes) to assign id for each node.
assignID = distinct_df.select("parentTLD","childTLD").rdd.flatMap(lambda x: x).distinct()

def hashnode(x):
    return hashlib.sha1(x.encode("UTF-8")).hexdigest()[:8]

hashnode_udf = udf(hashnode)
vertices = assignID.map(lambda x: (hashnode(x), x)).toDF(["id","name"])
edges = distinct_df.select("parentTLD","childTLD")\
    .withColumn("src", hashnode_udf("parentTLD"))\
    .withColumn("dst", hashnode_udf("childTLD"))\
    .select("src","dst")

# create GraphFrame
graph = GraphFrame(vertices, edges)
links = edges.coalesce(1).write.csv('links')

# Run LPA
communities = graph.labelPropagation(maxIter=5)
groups = communities.coalesce(1).write.csv('groups')
communityCount = communities.select('label').distinct().count()
print(communityCount, "communities in sample graph.")

# Run PageRank
results = graph.pageRank(resetProbability=0.01, maxIter=20)
results.vertices.select("id", "pagerank")\
    .join(vertices, on="id").orderBy("pagerank", ascending=False)\
    .show(10)