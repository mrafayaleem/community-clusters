#!/usr/bin/env bash
  
for file in data/ETLout/*; do
    	#echo `spark-submit analysis.py --inputs $file/*/  --outputs AnalysisOut/ twitter google facebook $file`
	IFS='/ ' read -r -a array <<< $file
	month=${array[2]}
	echo "$month"	
	echo "$file/*/"
done

#echo "id,name,label,pagerank" | cat - tnew
