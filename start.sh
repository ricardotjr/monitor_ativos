#!/bin/bash

if [ -d "venv" ];
then
	. venv/bin/activate
else
	python3 -m venv venv
	. venv/bin/activate
pip install pandas_datareader rich yahoo_fin pyfiglet
fi
python monitor.py
