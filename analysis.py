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

months = ['may', 'oct']

def read_parqet(month):
    # Read in parquet files
    data = sqlContext.read.parquet('./bootstrap/spark-warehouse/'+month+'/'+month+'*')
    focus = ['etsy', 'ebay', 'amazon']
    # Select focus shopping domains
    specified_domain = data.filter(data.childDomain.isin(focus))

    return specified_domain

def hashnode(x):
    # Return a unique hashkey for each entry
    return hashlib.sha1(x.encode("UTF-8")).hexdigest()[:8]

def renameFile(directory, newname, extension):
    # Rename filename as spark partitions file
    for root, dirs_list, files_list in os.walk(os.getcwd()+"/"+directory):
        for file_name in files_list:
            if os.path.splitext(file_name)[-1] == extension:
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

def create_graph(vertices, edges, month):
    # create GraphFrame
    graph = GraphFrame(vertices, edges)
    links = edges.coalesce(1).write.csv('links-'+month, mode='overwrite')
    renameFile('links-'+month, 'links-'+month+'.csv', '.csv')
    return graph

def run_LPA(graph,month,  maxiter=5):
    # Run LPA
    communities = graph.labelPropagation(maxIter=maxiter)
    communityCount = communities.select('label').distinct().count()

    labelCount = communities.groupBy("label").count().sort(desc("count")).limit(10)
    topLabels = labelCount.select('label').collect()
    top10List = [str(i.label) for i in topLabels]
    top10Communitites = communities.filter(communities.label.isin(top10List))

    top10Communitites.coalesce(1).write.csv('top10-'+month, mode='overwrite')
    renameFile('top10-'+month, 'top10-'+month+'.csv', '.csv')
    
    communities.coalesce(1).write.csv('communities-'+month, mode='overwrite')
    renameFile('communities-'+month, 'communities-'+month+'.csv', '.csv')
    return communities, communityCount

def run_pagerank(graph, communities, month, maxiter=10):
    # Run PageRank
    pageRank = graph.pageRank(resetProbability=0.15, maxIter=maxiter)
    # Organize communities based on page rankings and weights
    topTenRankings = pageRank.vertices.select("id", "pagerank").orderBy("pagerank", ascending=False).limit(10)
    topTenRankings = functions.broadcast(topTenRankings)
    getRankingInfo = communities.join(topTenRankings, communities.id == topTenRankings.id).drop(topTenRankings.id).orderBy("pagerank", ascending=False)
    getRankingInfo.coalesce(1).write.csv('rankings-'+month, mode='overwrite', header='true')
    renameFile('rankings-'+month, 'rankings-'+month+'.csv', '.csv')

    weightedRelationship = pageRank.edges.select("src", "dst", "weight").distinct().orderBy("weight", ascending=False).limit(10)

    return pageRank

def main():
    # Get Edges and Vertices 
    for m in months:
        df = read_parqet(m).cache()
        vertices, edges = get_edge_vertices(df)
        # Create GraphFrame
        graph = create_graph(vertices, edges, m).cache()
        # Analysis
        communities, count = run_LPA(graph, m, maxiter=5)
        communitiesNodeRanking = run_pagerank(graph, communities, m, maxiter=10)

if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Perform graph analysis on CommonCrawl data')
    # parser.add_argument('-d', '--dir', type=str, nargs='?', default='',  help='Input path to parquet files')
    # args = parser.parse_args()
    main()