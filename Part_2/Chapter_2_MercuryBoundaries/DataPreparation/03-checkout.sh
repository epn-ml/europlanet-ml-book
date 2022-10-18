#!/bin/bash

wget https://pds-ppi.igpp.ucla.edu/ditdos/download?id=pds://PPI/MESS-E_V_H_SW-MAG-4-SUMM-CALIBRATED-V1.0/CATALOG/MESS_MAGRDR_DS.CAT -O MESS_MAGRDR_DS.CAT
sed -i 's/&nbsp;//g' MESS_MAGRDR_DS.CAT
grep SCI MESS_MAGRDR_DS.CAT | egrep '201[1-5]' | sed -e s/MOI//g -e s/OB[1-5]//g | grep '(' | awk '{ print $1 $2 $3 $4 $5 $6 $7 $8}' | sed 's/1Apr2005/01Apr2005/g' | sed 's/9Aug2005/09Apr2005/g' | sed 's/29Feb2013/28Feb2013/g'
rm MESS_MAGRDR_DS.CAT
