import sys
import os
import re

from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext, functions
from pyspark.sql.types import StructField, StringType, StructType

from warcio import ArchiveIterator
from warcio.recordloader import ArchiveLoadFailed
from bs4 import BeautifulSoup
from urllib.parse import urlparse

import tldextract
import boto3
import botocore
from io import BytesIO
from tempfile import TemporaryFile


schema = StructType([
    StructField('parent', StringType()),
    StructField('parentTLD', StringType()),
    StructField('childTLD', StringType()),
    StructField('child', StringType())
])


@functions.udf(returnType=StringType())
def url_to_domain(url):
    return tldextract.extract(url).domain


def process_warcs(i_, iterator):
    # Currently, this function is processing from files in parallel across partitions.
    # We can extend this same function easily for S3

    s3pattern = re.compile('^s3://([^/]+)/(.+)')
    base_dir = os.path.abspath(os.path.dirname(__file__))

    no_sign_request = botocore.client.Config(
        signature_version=botocore.UNSIGNED)
    s3client = boto3.client('s3', config=no_sign_request)

    for uri in iterator:
        if uri.startswith('s3://'):
            s3match = s3pattern.match(uri)
            bucketname = s3match.group(1)
            path = s3match.group(2)
            warctemp = TemporaryFile(mode='w+b')
            
            try:
                s3client.download_fileobj(bucketname, path, warctemp)
            except botocore.client.ClientError as exception:
                print('Failed to download from s3')
                warctemp.close()
                continue
            warctemp.seek(0)
            stream = warctemp

        elif uri.startswith('file:'):
            uri = uri[5:]
            uri = os.path.join(base_dir, uri)
            try:
                stream = open(uri, 'rb')
            except IOError as exception:
                print("Failed to read data from local")
                continue
        else:
            print("Unknowm file system")

        try:
            for record in ArchiveIterator(stream):
                processed = process_record(record)
                if processed:
                    yield processed
                continue
        except ArchiveLoadFailed as exception:
            print('Invalid WARC')
        finally:
            stream.close()


def process_record(record):
    if record.rec_type == 'response' and record.http_headers.get_header('Content-Type') == 'text/html':
        target_uri = record.rec_headers.get_header('WARC-Target-URI')
        html = record.content_stream().read()

        parsed = urlparse(target_uri)
        parent = parsed.scheme + '://' + parsed.netloc
        parentTLD = rec.sub('', parsed.netloc).strip()

        return get_external_links(html, parentTLD, parent)
    else:
        return


def get_external_links(html_content, parentTLD, parent):
    """
    Extract links from the HTML
    """
    link_list = []
    unique_map = {}
    parser = BeautifulSoup(html_content, features="html.parser", from_encoding="iso-8859-1")

    # Find all hrefs under the 'a' html tag
    links = parser.find_all('a')

    if links:
        for link in links:
            href = link.attrs.get("href")
            # If relevant hrefs are found, store it in a list
            if href:
                href_parsed = urlparse(href)
                get_domain = href_parsed.netloc

                try:
                    parents_children = unique_map[parentTLD]
                except KeyError:
                    unique_map[parentTLD] = {}
                    parents_children = unique_map[parentTLD]

                parent_domain = rec.sub('', parentTLD).strip().split('.')[0]
                child_domain = rec.sub('', get_domain).strip().split('.')[0]

                if parent_domain != child_domain:
                    if (href.startswith("http") or href.startswith("http")) and href not in parents_children:
                    # if get_domain not in link_list and href.startswith("http"):
                        childTLD = rec.sub('', get_domain).strip()
                        child = href
                        link_list.append((parent, parentTLD, childTLD, child))
                        parents_children[href] = None

    return link_list


def main(input_file, output_file, file_system, to_crawl_data, sample):
    warcPaths = sc.textFile(input_file)
    #print('INDATA', input_data.collect())
    input_data = sc.parallelize(warcPaths.takeSample(False, sample))

    if(file_system=="s3"):
        input_data = input_data.map(lambda p: "s3://" + to_crawl_data + "/" + p)
    elif(file_system=="file"):
        input_data = input_data.map(lambda p: "file:" + to_crawl_data + "/" + p)
    else:
        print("file system not found.")

    partition_mapped = input_data.mapPartitionsWithIndex(process_warcs)
    mapped = partition_mapped.flatMap(lambda x: x)

    df = spark.createDataFrame(mapped, schema=schema).distinct()

    # Extract child and parent domains so we can easily use asin filtering
    df = df.select(
        '*', url_to_domain('childTLD').alias('childDomain'), url_to_domain('parentTLD').alias('parentDomain'))

    df.write.format("parquet").saveAsTable(output_file)

    #print('OUTDATA', mapped.take(5))


if __name__ == '__main__':
    conf = SparkConf().setAll((
        ("spark.task.maxFailures", "10"),
        ("spark.locality.wait", "20s"),
        ("spark.serializer", "org.apache.spark.serializer.KryoSerializer"),
    ))
    rec = re.compile(r"(https?://)?(www\.)?")  # Regex to clean parent/child links
    sc = SparkContext(appName='etl', conf=conf)
    spark = SQLContext(sparkContext=sc)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    file_system = sys.argv[3]
    to_crawl_data = sys.argv[4]
    sample = int(sys.argv[5])

    main(input_file, output_file, file_system, to_crawl_data, sample)
