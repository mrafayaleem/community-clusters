#!/usr/bin/python
import os
import argparse


TEMP_PATH = 'temp'


if not os.path.exists(TEMP_PATH):
    os.makedirs(TEMP_PATH)


def main():
    threshold = args.threshold

    with open(args.input) as fp:
        data = fp.readlines()

    tout = []
    count = 0
    for i, line in enumerate(data):
        tout.append(line)

        if (i + 1) % threshold == 0:
            count += 1
            with open(TEMP_PATH + '/t{0}'.format(count), 'w') as file_handler:
                for item in tout:
                    file_handler.write("{}".format(item))
            tout = []

        elif i == len(data) - 1:
            count += 1
            with open(TEMP_PATH + '/t{0}'.format(count), 'w') as file_handler:
                for item in tout:
                    file_handler.write("{}".format(item))
            tout = []

    command = """
    $SPARK_HOME/bin/spark-submit ./parent_child.py {input} {output} {file_type} {crawl_path}
    """

    for i, fname in enumerate(os.listdir(TEMP_PATH)):
        input = TEMP_PATH + '/t{0}'.format(i+1)
        os.system(command.format(
            input=input,
            output=args.output + str(i),
            file_type=args.file_type,
            crawl_path=args.crawl_path
        ))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Perform ETL in chunks')
    parser.add_argument('input', type=str, help='Input path')
    parser.add_argument('output', type=str, help='Output path')
    parser.add_argument('file_type', type=str, help='file or s3')
    parser.add_argument('crawl_path', type=str, help='file path or bucket name in case of s3')
    parser.add_argument('threshold', type=int, help='batch size')

    args = parser.parse_args()

    main()
