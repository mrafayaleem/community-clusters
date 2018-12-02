#!/usr/bin/env python3
"""
Perform graph analysis on a subset of Common Crawl Data using PySpark

Usage: spark-submit analysis.py --dir <path_to_parquets> --limiter <max_no_items> --focus twitter google facebook
We can sequentially add as many domain names as arguments to --focus and the argparser will append them to a list
"""
import argparse
import pyspark
from pyspark import SparkContext
from pyspark.sql import SQLContext,SparkSession, functions
from graphframes import *
import hashlib
import os

sc = SparkContext() 
spark = SparkSession.builder.appName('Community Clustering').getOrCreate()
assert spark.version >= '2.3' # make sure we have Spark 2.3+
sqlContext = SQLContext(sc)

def read_parqet(dir, lim, focus):
    # Read in parquet and limit the entries for quicker analysis
    df = sqlContext.read.parquet(dir)
    df = df.distinct().limit(lim)
    
    # Filter domains for more specific inquiry
    if focus: 
        df = df.filter(df.childDomain.isin(focus))
    return df

def hashnode(x):
    # Return a unique hashkey for each entry
    return hashlib.sha1(x.encode("UTF-8")).hexdigest()[:8]

def renameFile(directory, newname):
    # Rename filename as spark partitions file
    for root, dirs_list, files_list in os.walk(os.getcwd()+"/"+directory):
        for file_name in files_list:
            if os.path.splitext(file_name)[-1] == '.csv':
                old_file = os.path.join(directory, file_name)
                new_file = os.path.join(directory, newname)
                os.rename(old_file,new_file)           

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
        .select("src","dst")
    return vertices, edges

def create_graph(vertices, edges):
    # create GraphFrame
    graph = GraphFrame(vertices, edges)
    links = edges.coalesce(1).write.csv('links', mode='overwrite')
    renameFile('links', 'links.csv')
    return graph

def run_LPA(graph, maxiter=5):
    # Run LPA
    communities = graph.labelPropagation(maxIter=maxiter)
    return communities

def run_pagerank(graph, communities, maxiter=20):
    # Run PageRank
    pageRank = graph.pageRank(resetProbability=0.01, maxIter=maxiter)
    pageRankings = pageRank.vertices.select("id", "pagerank")
    # Organize communities based on page rankings and 
    pageRankings = functions.broadcast(pageRankings)
    communitiesNodeRanking = communities.join(pageRankings, communities.id == pageRankings.id).drop(pageRankings.id).orderBy("pagerank", ascending=False)
    communitiesNodeRanking.coalesce(1).write.csv('communities', mode='overwrite')
    renameFile('communities', 'rankings.csv')
    return communitiesNodeRanking

def run_trianglecount(graph, mincount=0):
    # Run TriangleCount and store only those rows with values above mincount
    triangleCount = graph.triangleCount()
    triangleCount = triangleCount.where(triangleCount["count"] > mincount)
    return triangleCount

def main(dir, limiter, focus_list):
    df = read_parqet(dir, lim=limiter, focus=focus_list)
    # Get edges and Vertices
    vertices, edges = get_edge_vertices(df)
    # Create GraphFrame
    graph = create_graph(vertices, edges)
    # Analysis
    communities = run_LPA(graph, maxiter=5)
    communitiesNodeRanking = run_pagerank(graph, communities, maxiter=20)
    # triangleCount = run_trianglecount(graph, mincount=0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Perform graph analysis on CommonCrawl')
    parser.add_argument('-d', '--dir', type=str, nargs='?', default='./bootstrap/spark-warehouse/output',  help='Input path to parquet files')
    parser.add_argument('-l', '--limiter', type=int, nargs='?', default=10000, help='Max number of items (int) we want to analyze')
    parser.add_argument('-f', '--focus', type=str, nargs='*', help='List of items we want to focus on')

    args = parser.parse_args()
    main(args.dir, args.limiter, args.focus)