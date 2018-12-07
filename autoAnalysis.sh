#!/usr/bin/env bash

#$1:shopping
#$2:amazon ebay
#$3:month to run plot_communities on
  
echo "Running analysis.py"

for file in data/ETLout/*; do
	echo "reading file $file"
	IFS='/ ' read -r -a array <<< $file
	month=${array[3]}
	echo `spark-submit --packages graphframes:graphframes:0.6.0-spark2.3-s_2.11 analysis.py --inputs $file/*/  --outputs $month --path data/AnalysisOut/$1 --focus $2`
done

echo "Concatenating for D3"

for file in data/AnalysisOut/$1/rankings-*; do

	IFS='/ ' read -r -a array1 <<< $file
	IFS='- ' read -r -a array2 <<< ${array1[3]}
	month=${array2[1]}

	echo `cat $file/part-* > data/htmlInput/$month.csv`
	printf '%s\n' "id,name,label,pagerank" | cat - data/htmlInput/$month.csv > data/htmlInput/rankings-$month.csv
	rm data/htmlInput/$month.csv
done

mkdir -p data/D3Input/$1
for file in data/AnalysisOut/$1/links-*; do 
	IFS='/ ' read -r -a array1 <<< $file
        IFS='- ' read -r -a array2 <<< ${array1[3]}
        month=${array2[1]}
	echo `cat $file/part-* > data/D3Input/$1/links-$month.csv`
done

for file in data/AnalysisOut/$1/communities-*; do
	IFS='/ ' read -r -a array1 <<< $file
        IFS='- ' read -r -a array2 <<< ${array1[3]}
        month=${array2[1]}
	echo `cat $file/part-* >  data/D3Input/$1/communities-$month.csv`
done

echo "Running plot_communities.py"

echo `python3 plot_communities.py --outputs $3 --path $1`

