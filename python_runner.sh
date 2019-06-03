#!/bin/bash --login

pip install -r requirements.txt
python scrap_finviz_aws.py
python column.py
