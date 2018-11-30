import pyspark
from pyspark import SparkContext
from pyspark.sql import SQLContext, functions
from pyspark.sql.functions import udf
from graphframes import *
import hashlib
import os

cwd = os.getcwd()

sc = SparkContext(appName="Community Clustering") 
sqlContext = SQLContext(sc)

df = sqlContext.read.parquet("./bootstrap/spark-warehouse/test")
distinct_df = df.distinct().limit(10000)

# Select set of parents and children TLDs (nodes) to assign id for each node.
assignID = distinct_df.select("parentTLD","childTLD").rdd.flatMap(lambda x: x).distinct()

def hashnode(x):
    return hashlib.sha1(x.encode("UTF-8")).hexdigest()[:8]

# Rename filename as spark partitions file
def renameFile(directory, newname):
    for root, dirs_list, files_list in os.walk(cwd+"/"+directory):
        for file_name in files_list:
            if os.path.splitext(file_name)[-1] == '.csv':
                old_file = os.path.join(directory, file_name)
                new_file = os.path.join(directory, newname)
                os.rename(old_file,new_file)
                return 'done'

hashnode_udf = udf(hashnode)
vertices = assignID.map(lambda x: (hashnode(x), x)).toDF(["id","name"])
edges = distinct_df.select("parentTLD","childTLD")\
    .withColumn("src", hashnode_udf("parentTLD"))\
    .withColumn("dst", hashnode_udf("childTLD"))\
    .select("src","dst")

# create GraphFrame
graph = GraphFrame(vertices, edges)
links = edges.coalesce(1).write.csv('links')
renameFile('links', 'links.csv')

# Run LPA
communities = graph.labelPropagation(maxIter=5).cache()
# communityCount = communities.select('label').distinct().count()

# Run PageRank
pageRank = graph.pageRank(resetProbability=0.01, maxIter=20)
pageRankings = pageRank.vertices.select("id", "pagerank")

pageRankings = functions.broadcast(pageRankings)
communitiesNodeRanking = communities.join(pageRankings, communities.id == pageRankings.id).drop(pageRankings.id).orderBy("pagerank", ascending=False)
communitiesNodeRanking.coalesce(1).write.csv('communities')
renameFile('communities', 'rankings.csv')

# Run TriangleCount
# triangleCount = graph.triangleCount()
# triangleCount.where(triangleCount["count"] > 0).show()


