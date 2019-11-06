#!/bin/sh

if [ -z $1 ]; then
    echo "pass product as argv"
    exit 1
fi

if [ -z $2 ]; then
    FNAME=$1
else
    FNAME=$2
fi

if [ -z $PIPENV_ACTIVE ]
then
    echo "env not active, exiting"
    exit 1
else
    echo "env active, continuing"
fi

arr[0]=$(echo "2019 10 2 1 13" | base64)
arr[1]=$(echo "2019 5 1 2 42" | base64)
arr[2]=$(echo "2018 4 25 5 26" | base64)
arr[3]=$(echo "2017 8 2 2 10" | base64)
arr[4]=$(echo "2017 2 8 23 38" | base64)
arr[5]=$(echo "2016 2 25 23 1" | base64)
arr[6]=$(echo "2015 8 19 3 3" | base64)
if [ ! "$(ls -A radars/*_V06*)" ]; then
    for r in ${arr[*]}; do
        python downloader.py KVBX $r
    done
fi

echo "clearing figures"
rm -r figures/*png

echo "execute plotter"

python plotter.py $1 

echo "to pdf"

echo $1

convert figures/*.png "pdfs/$FNAME.pdf"
