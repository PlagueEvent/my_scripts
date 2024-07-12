#!/bin/bash 
echo "Имя сервиса:"
read servicename

#echo "топик кафки/список топиков(список передавать в виде topic1|topic2|topic3):"
#read topic

echo "Откуда и куда читаем:"
echo "-------------------------------------"
echo "[1] kkd-kafka01t   ->  udrvs-ad-kafka"
echo "[2] kkd-dmz-kfk    ->  udrvs-ad-kafka"
echo "[3] udrvs-ad-kafka ->  kkd-kafka01t"
echo "[4] udrvs-ad-kafka ->  kkd-dmz-kfk"

read kafkaread

case "$kafkaread" in
	0) 
		bootstrap="10.207.33.197:9092"
		prefix=pp
		;;
	1)	
		bootstrap="10.207.33.132:9092,10.207.33.133:9092,10.207.33.134:9092"
		prefix=pr

		;;
  3) 
		bootstrap="10.207.33.197:9092"
		prefix=pp

		;;
	4)	
		bootstrap="10.207.33.132:9092,10.207.33.133:9092,10.207.33.134:9092"
		prefix=pr

		;;

esac

echo $prefix
echo  $kafkaread 
if (( $kafkaread < 3 ))
  then	
		echo $prefix
	  echo "producer=producer_mirror_adh_cluster.properties"
    echo "consumer=consumer-mirror-$prefix-$servicename.properties"
  else
		echo $prefix  
    echo "producer=consumer-mirror-$prefix-$servicename.properties"
		echo "consumer=producer_mirror_adh_nt_cluster.properties" 
fi 







