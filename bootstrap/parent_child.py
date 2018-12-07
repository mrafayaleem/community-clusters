#!/usr/bin/env python3
import os
import re
import argparse

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
    try:

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
                    print('Failed to download from s3', exception)
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
                    print("Failed to read data from local", exception)
                    continue
            else:
                print("Unknown file system")

            try:
                for record in ArchiveIterator(stream):
                    processed = process_record(record)
                    if processed:
                        yield processed
                    continue
            except ArchiveLoadFailed as exception:
                print('Invalid WARC', exception)
            finally:
                stream.close()
    except: 
        print("URL invalid")


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

                parent_domain = tldextract.extract(parentTLD).domain
                child_domain = tldextract.extract(get_domain).domain

                if parent_domain != child_domain:
                    if (href.startswith("http") or href.startswith("http")) and href not in parents_children:
                        childTLD = rec.sub('', get_domain).strip()
                        child = href
                        link_list.append((parent, parentTLD, childTLD, child))
                        parents_children[href] = None

    return link_list


def main(input_file, output_file, file_system, to_crawl_data):
    input_data = sc.textFile(input_file)

    if file_system == "s3":
        input_data = input_data.map(lambda p: "s3://" + to_crawl_data + "/" + p)
    elif file_system == "file":
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


if __name__ == '__main__':
    conf = SparkConf().setAll((
        ("spark.task.maxFailures", "10"),
        ("spark.locality.wait", "20s"),
        ("spark.serializer", "org.apache.spark.serializer.KryoSerializer"),
    ))
    rec = re.compile(r"(https?://)?(www\.)?")  # Regex to clean parent/child links
    sc = SparkContext(appName='etl-common-crawl', conf=conf)
    spark = SQLContext(sparkContext=sc)

    parser = argparse.ArgumentParser(description='Perform ETL on CommonCrawl')
    parser.add_argument('input', type=str,  help='Input path')
    parser.add_argument('output', type=str, help='Output path')
    parser.add_argument('file_type', type=str, help='file or s3')
    parser.add_argument('crawl_path', type=str, help='file path or bucket name in case of s3')

    args = parser.parse_args()

    main(args.input, args.output, args.file_type, args.crawl_path)
