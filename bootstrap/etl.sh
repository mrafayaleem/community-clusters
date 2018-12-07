#!/bin/bash

run_etl(){
    echo "$1" "$2" "$3" "$4" "$5"
    python run_etl.py "$1" "$2" "$3" "$4" "$5"
}


if [ "$1" == "execute" ]; then
    run_etl "$2" "$3" "$4" "$5" "$6"

    # Make month directory and move all monthly outputs to this directory
    mkdir -p spark-warehouse/"$3"
    echo $(mv spark-warehouse/$3*? spark-warehouse/$3)
else
    echo "Unrecognized command"
fi
