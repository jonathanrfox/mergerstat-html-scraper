#!/bin/bash

# args:
# $1 is pattern to match
# $2 is file
# Examples:
# ./helper Merger* fakemain.py
# ./helper Facebook* main.py

findFiles() {
    find ./inputs -maxdepth 1 -type f -name ${1} -print0
}

if [ "${2}" == "main.py" ]; then
    findFiles ${1} | xargs -0 -n1 python ${2}
else
    findFiles ${1} | xargs -0 -n1 python ${2} | sort
fi
