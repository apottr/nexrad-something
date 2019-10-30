#!/bin/sh

if [ -z $1 ]; then
    echo "pass product as argv"
    exit 1
fi

if [ -z $PIPENV_ACTIVE ]
then
    echo "env not active, exiting"
    exit 1
else
    echo "env active, continuing"
fi

if [ ! "$(ls -A radars/)" ]; then
    python downloader.py 2019 10 2 1 13
    python downloader.py 2019 5 1 2 42
    python downloader.py 2018 4 25 5 26
    python downloader.py 2017 8 2 2 10
    python downloader.py 2017 2 8 23 38
    python downloader.py 2016 2 25 23 1
    python downloader.py 2015 8 19 3 3
fi

echo "clearing figures"
rm -r figures/*png

echo "execute plotter"

python plotter.py $1

echo "to pdf"

echo $1

convert figures/*.png "pdfs/$1.pdf"
