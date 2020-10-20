#!/bin/bash

stock_list=`python blah2.py`
# stock_list=`python blah2.py`
echo $stock_list
arr=($stock_list)

stock0=`echo ${arr[0]} | tr -dc "[:alnum:]\n\r"`
stock1=`echo ${arr[1]} | tr -dc "[:alnum:]\n\r"`
stock2=`echo ${arr[2]} | tr -dc "[:alnum:]\n\r"`
stock3=`echo ${arr[3]} | tr -dc "[:alnum:]\n\r"`
stock4=`echo ${arr[4]} | tr -dc "[:alnum:]\n\r"`
stock5=`echo ${arr[5]} | tr -dc "[:alnum:]\n\r"`
stock6=`echo ${arr[6]} | tr -dc "[:alnum:]\n\r"`
stock7=`echo ${arr[7]} | tr -dc "[:alnum:]\n\r"`
stock8=`echo ${arr[8]} | tr -dc "[:alnum:]\n\r"`
stock9=`echo ${arr[9]} | tr -dc "[:alnum:]\n\r"`

python jarvis.py $stock0 &
python jarvis.py $stock1 & 
python jarvis.py $stock2 & 
python jarvis.py $stock3 & 
python jarvis.py $stock4 & 
python jarvis.py $stock5 & 
python jarvis.py $stock6 & 
python jarvis.py $stock7 & 
python jarvis.py $stock8 & 
python jarvis.py $stock9 &

wait
echo "Trading day done"