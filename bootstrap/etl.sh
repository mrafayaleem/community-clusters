#!/bin/bash

run_etl(){
    echo "$1" "$2" "$3" "$4" "$5"
    python run_etl.py "$1" "$2" "$3" "$4" "$5"
}


if [ "$1" == "execute" ]; then

    # Remove temp dir
    rm -r temp/

    run_etl "$2" "$3" "$4" "$5" "$6"

    # Make month directory and move all monthly
    # outputs to this directory
    mkdir -p ../data/ETLout/"$3"
    echo $(mv ../data/ETLout/$3*? ../data/ETLout/$3)

else
    echo "Unrecognized command"
fi
