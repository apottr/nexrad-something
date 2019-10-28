#!/bin/sh

if [ -z $PIPENV_ACTIVE ]
then
    echo "env not active, exiting"
    exit 1
else
    echo "env active, continuing"
fi

python downloader.py 2019 10 2 1 13
python downloader.py 2019 5 1 2 42
python downloader.py 2018 4 25 5 26
python downloader.py 2017 8 2 2 10
python downloader.py 2017 2 8 23 38