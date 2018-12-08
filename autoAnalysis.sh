#!/usr/bin/env bash

#$1:shopping
#$2:'amazon ebay'
#$3:may
  
echo "Running analysis.py"

month=$3
category=$1
${SPARK_HOME}/bin/spark-submit --packages graphframes:graphframes:0.6.0-spark2.3-s_2.11 analysis.py --inputs data/ETLout/$month --outputs $month --path data/AnalysisOut/$1 --focus $2 
#echo `spark-submit --packages graphframes:graphframes:0.6.0-spark2.3-s_2.11 analysis.py --inputs data/ETLout/test/$month --outputs $month --path data/AnalysisOut/$1 --focus $2`
wait $!

echo "Concatenating for D3"

echo `cat data/AnalysisOut/$category/rankings-$month/part-* > data/htmlInput/rankings-$category-$month.csv`
printf '%s\n' "id,name,label,pagerank" | cat - data/htmlInput/rankings-$category-$month.csv > data/htmlInput/rankings-$category-$month.csv
rm data/htmlInput/$category-$month.csv

mkdir -p data/D3Input/$category
echo `cat data/AnalysisOut/$category/links-$month/part-* > data/D3Input/$category/links-$month.csv`

echo `cat data/AnalysisOut/$category/communities-$month/part-* >  data/D3Input/$category/communities-$month.csv`

echo "Running plot_communities.py"

echo `python3 plot_communities.py --outputs $month --path $category`

sed "s/%%MONTH%%/$month/; s/%%CATEGORY%%/$category/" index-template.html > public/index-$category-$month.html
