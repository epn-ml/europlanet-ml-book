#!/bin/bash

python3 -m venv venv
source venv/bin/activate
pip3 install pipreqs
pip3 install -r requirements.txt

wget 'https://agupubs.onlinelibrary.wiley.com/action/downloadSupplement?doi=10.1029%2F2019JA027544&file=jgra55678-sup-0002-Table_SI-S01.xlsx' -O jgra55678-sup-0002-Table_SI-S01.xlsx

./01-mfield.sh
./02-heliocoord.py Mercury 2011-Mar-23Z00:00 2015-May-01Z00:00 1m > mercury-pos-min.txt
./03-checkout.sh > checkout.dat
./04-philpott.py
