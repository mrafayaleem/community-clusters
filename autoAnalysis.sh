#!/usr/bin/env bash
  
echo "Running analysis.py"

for file in data/ETLout/test/*; do
	echo "reading file $file"
	IFS='/ ' read -r -a array <<< $file
	month=${array[3]}
	#echo `spark-submit --packages graphframes:graphframes:0.6.0-spark2.3-s_2.11 analysis.py --inputs $file/*/  --outputs $month --path data/AnalysisOut/$1 --focus amazon`
done

echo "Concatenating for D3"

for file in data/AnalysisOut/$1/links-*; do

	IFS='/ ' read -r -a array1 <<< $file
	IFS='- ' read -r -a array2 <<< ${array1[3]}
	month=${array2[1]}

	echo `cat $file/part-* > data/D3Input/$month.csv`
	printf '%s\n' "id,name,label,pagerank" | cat - data/D3Input/$month.csv > data/D3Input/links-$month.csv
	rm data/D3Input/$month.csv
done

