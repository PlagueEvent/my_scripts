#!/bin/bash
echo "Имя топика:"
read topicname

echo "Откуда читаем:"
echo "--------------"
echo "   [0]kkd-kafka01t"
echo "   [1]kkd-dmz-kfk "

read kafkaread

case "$kafkaread" in
	0) 
		bootstrap="10.207.33.197:9092"
		prefix=pr
		;;
	1)	
		bootstrap="10.207.33.132:9092,10.207.33.133:9092,10.207.33.134:9092"
		prefix=pp
		;;
esac

echo "add new-$prefix-$topicname.sh to $bootstrap servier(s)"


