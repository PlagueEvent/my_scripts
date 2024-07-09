#!/bin/bash
set -eu
for ((i=1; i<10;i++))
do
	 patern=demo_$i
	 echo "$patern"
	 output=$(sed  "s/demo/$patern/g" /home/eugen/demo_big.sql >> demo_$i.sql)
	 #echo "Выполняется команда: '$output'"
done

#for ((i=1; i<10;i++))
#do 
#	output=$( pg_restore -U postgres -h 192.168.122.69  -f demo_$i.sql )
#	echo "$output"
#done
	 
