#!/bin/bash

BASE_URL='https://pds-ppi.igpp.ucla.edu/ditdos/download?id='
PDS_ID='pds://PPI/MESS-E_V_H_SW-MAG-4-SUMM-CALIBRATED-V1.0/DATA/MSO'
years=$(seq 2011 2015)

mkdir -p full/{01,05,10,60,source} orbit

for y in $years; do
  wget "${BASE_URL}${PDS_ID}/${y}" -O full/source/${y}.zip
done

for y in $years; do
  unzip -o -d full/source full/source/${y}.zip
done

find full/source/ -iname '*_01_V08.TAB' -exec mv {} full/01/ \;
find full/source/ -iname '*_05_V08.TAB' -exec mv {} full/05/ \;
find full/source/ -iname '*_10_V08.TAB' -exec mv {} full/10/ \;
find full/source/ -iname '*_60_V08.TAB' -exec mv {} full/60/ \;
