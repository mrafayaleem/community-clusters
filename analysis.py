"""
Perform graph analysis on a subset of Common Crawl Data using PySpark

Usage: spark-submit analysis.py --dir <path_to_parquets>  --focus twitter google facebook
We can sequentially add as many domain names as arguments to --focus and the argparser will append them to a list
"""
import argparse
import pyspark
from pyspark import SparkContext
from pyspark.sql import SQLContext,SparkSession, functions
from pyspark.sql.functions import udf, col, desc
from graphframes import *
import hashlib
import os

sc = SparkContext()
spark = SparkSession.builder.appName('Community Clustering').getOrCreate()
assert spark.version >= '2.3' # make sure we have Spark 2.3+
sqlContext = SQLContext(sc)

def read_parqet(inputs, focus):
    # Read in parquet files
    data = sqlContext.read.parquet(inputs)
    # Select focus domains
    if focus:
        data = data.filter(data.childDomain.isin(focus))
    return data

def hashnode(x):
    # Return a unique hashkey for each entry
    return hashlib.sha1(x.encode("UTF-8")).hexdigest()[:8]          

def get_edge_vertices(df):
    hashnode_udf = functions.udf(hashnode)
    # Returns the set of edges and vertices for our graph
    # First, select a set of parents and children TLDs (nodes) to assign id for each node.
    assignID = df.select("parentTLD","childTLD").rdd.flatMap(lambda x: x).distinct()
    # Assign hashids to each vertex
    vertices = assignID.map(lambda x: (hashnode(x), x)).toDF(["id","name"])
    edges = df.select("parentTLD","childTLD")\
        .withColumn("src", hashnode_udf("parentTLD"))\
        .withColumn("dst", hashnode_udf("childTLD"))\
        .select("src","dst").distinct()
    return vertices, edges

def create_graph(vertices, edges, outputs, path):
    # create GraphFrame
    graph = GraphFrame(vertices, edges)
    links = edges.write.csv(path+'/links-'+outputs, mode='overwrite')
    return graph

def run_LPA(graph, outputs, path, maxiter=5):
    # Run LPA
    communities = graph.labelPropagation(maxIter=maxiter)
    communityCount = communities.select('label').distinct().count()
    communities.write.csv(path+'/communities-'+outputs, mode='overwrite')
    return communities, communityCount

def run_pagerank(graph, communities, outputs, path, maxiter=10):
    # Run PageRank
    pageRank = graph.pageRank(resetProbability=0.15, maxIter=maxiter)
    # Organize communities based on page rankings and weights
    topTenRankings = pageRank.vertices.select("id", "pagerank").orderBy("pagerank", ascending=False).limit(10)
    topTenRankings = functions.broadcast(topTenRankings)
    getRankingInfo = communities.join(topTenRankings, communities.id == topTenRankings.id).drop(topTenRankings.id).orderBy("pagerank", ascending=False)
    getRankingInfo.write.csv(path+'/rankings-'+outputs, mode='overwrite')
    return pageRank

def main(inputs, outputs, path, focus):
    # Get Edges and Vertices 
    df = read_parqet(inputs, focus).cache()
    vertices, edges = get_edge_vertices(df)
    # Create GraphFrame
    graph = create_graph(vertices, edges, outputs, path).cache()
    # Analysis
    communities, count = run_LPA(graph, outputs, path, maxiter=5)
    communitiesNodeRanking = run_pagerank(graph, communities, outputs, path, maxiter=10)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Perform graph analysis on CommonCrawl data')
    parser.add_argument('-i', '--inputs', type=str, nargs='?', default='./bootstrap/spark-warehouse/oct/oct*',  help='Input path to parquet files')
    parser.add_argument('-o', '--outputs', type=str, nargs='?', help='Output name for files generated')
    parser.add_argument('-p', '--path', type=str, nargs='?', help='Output directory path name for focus domains')
    parser.add_argument('-f', '--focus', type=str, nargs='*', help='List of items we want to focus on')
    args = parser.parse_args()
    main(args.inputs, args.outputs, args.path, args.focus)