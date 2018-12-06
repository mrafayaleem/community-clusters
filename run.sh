#!/usr/bin/env bash

plot_communities()
{
    python3 plot_communities.py
}

perform_analysis()
{
    ${SPARK_HOME}/bin/spark-submit --packages graphframes:graphframes:0.6.0-spark2.3-s_2.11 analysis.py
}

run_etl(){
    cd bootstrap
    rm -r temp/
    python run_etl.py "$1" "$2" "$3" "$4" "$5"
    cd ..
}


if [ "$1" == "etl" ]; then
    run_etl "$2" "$3" "$4" "$5" "$6"
elif [ "$1" == "analyze" ]; then
    perform_analysis
elif [ "$1" == "plot-communities" ]; then
    plot_communities
elif [ "$1" == "server" ]; then
    python3 -m http.server
else
    echo "Unrecognized command"
fi
