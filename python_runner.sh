#!/bin/bash --login

pip install -r requirements.txt
python scrap_finviz_mac.py
python column.py
python delete_duplicates.py
