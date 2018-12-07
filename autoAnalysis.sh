#!/usr/bin/env bash
  
for file in data/ETLout/test/*; do
	echo "reading file $file"
	IFS='/ ' read -r -a array <<< $file
	month=${array[3]}
	echo `spark-submit --packages graphframes:graphframes:0.6.0-spark2.3-s_2.11 analysis.py --inputs $file/*/  --outputs $month --path data/AnalysisOut/$1 --focus amazon`
done

#echo "id,name,label,pagerank" | cat - tnew
