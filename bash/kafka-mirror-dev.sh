#!/bin/bash 
echo "Имя сервиса:"
read servicename

echo "топик кафки/список топиков(список передавать в виде topic1|topic2|topic3):"
read topic

echo "Откуда и куда читаем:"
echo "-------------------------------------"
echo "[1] kkd-kafka01t   ->  udrvs-ad-kafka"
echo "[2] kkd-dmz-kfk    ->  udrvs-ad-kafka"
echo "[3] udrvs-ad-kafka ->  kkd-kafka01t"
echo "[4] udrvs-ad-kafka ->  kkd-dmz-kfk"

read kafkaread

case "$kafkaread" in
	1) 
		bootstrap="10.207.33.197:9092"
		prefix=pp
		producer=producer_mirror_adh_cluster.properties 
		consumer=consumer-mirror-$prefix-$servicename.properties 
		;;
	2)	
		bootstrap="10.207.33.132:9092,10.207.33.133:9092,10.207.33.134:9092"
		prefix=pr
  	producer=producer_mirror_adh_cluster.properties 
		consumer=consumer-mirror-$prefix-$servicename.properties 

		;;
  3) 
		bootstrap="10.207.33.197:9092"
		prefix=pp
	  producer=consumer-mirror-$prefix-$servicename.properties 
		consumer=producer_mirror_adh_nt_cluster.properties 

		;;
	4)	
		bootstrap="10.207.33.132:9092,10.207.33.133:9092,10.207.33.134:9092"
		prefix=pr
	  producer=consumer-mirror-$prefix-$servicename.properties 
		consumer=producer_mirror_adh_nt_cluster.properties 

		;;

esac

#пилим демона
#cat << EOF | tee kafka-mirror-$prefix-$servicename.service
cat << EOF | tee kafka-mirror-$prefix-$servicename.service
[Unit]
Description=KafkaMirror Daemon 
Documentation=https://kafka.apache.org/documentation/
Requires=network.target
After=network.target

[Service]
User=local_kafka
Group=local_kafka
ExecStart=/opt/hadoop/kafka-mirror-$prefix-$servicename-start.sh
ExecStop=/opt/hadoop/kafka-mirror-$prefix-$servicename-stop.sh
TimeoutSec=60
Restart=on-failure

[Install]
WantedBy=default.target
EOF

#echo "add new-$prefix-$servicename.sh to $bootstrap servier(s)"
#пилим файлы /opt/hadoop/ если топиков в задаче больше одного, то затем можно их добавить в whitelist
#start.sh
cat << EOF | tee kafka-mirror-$prefix-$servicename-start.sh
#!/bin/bash
echo "mirror maker restarted \$(date)">>/opt/hadoop/kafka/logs/mirror-$prefix-$servicename.log
cd /opt/hadoop/kafka/bin/
export KAFKA_HEAP_OPTS=-Xmx384M
./kafka-mirror-$prefix-$servicename.sh \
--consumer.config ../config_local/$consumer \
--producer.config ../config_local/$producer \
--whitelist '$topic' \
--num.streams 3 \
--offset.commit.interval.ms 6000 \
--abort.on.send.failure false
EOF

#stop.sh
cat << EOF | tee kafka-mirror-$prefix-$servicename-stop.sh
#cat << EOF | tee kafka-mirror-$prefix-$servicename-stop.sh
#!/bin/sh
SIGNAL=\${SIGNAL:-TERM}
PIDS=\$(ps ax | grep -i "consumer-mirror-$prefix-$servicename*" | grep java | grep -v grep | awk '{print $1}') 
if [ -z "\$PIDS" ]; then
  echo "No mirrormaker service to stop"
  echo "No mirrormaker service to stop" >> /opt/hadoop/kafka/logs/mirror-$prefix-$servicename.log
  exit 1
else
  kill -s \$SIGNAL \$PIDS
  echo "stopped mirrormaker service"
  echo "stopped mirrormaker service \$date" >> /opt/hadoop/kafka/logs/mirror-$prefix-$servicename.log
fi
EOF

#файл /opt/hadoop/kafka/config_local/*.properties
#cat << EOF | tee kafka-mirror-$prefix-$servicename.properties 
cat << EOF | tee consumer-mirror-$prefix-$servicename.properties
bootstrap.servers=$bootstrap
group.id=udrvs_adh_cluster_pr_ern
partition.assignment.strategy=org.apache.kafka.clients.consumer.RoundRobinAssignor
sasl.mechanism=PLAIN
security.protocol=SASL_PLAINTEXT
sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required username="sys_udrvs_prod_kafka_mirror" password="kxZrqHKIA8eMcf9vJdlLGf7Y";
auto.offset.reset=earliest
max.partition.fetch.bytes = 26428700
EOF

# /opt/hadoop/kafka/bin/ 
#cat << EOF | tee kafka-mirror-$prefix-$servicename.sh
cat << EOF | tee kafka-mirror-$prefix-$servicename.sh
#!/bin/bash
exec \$(dirname $0)/kafka-run-$prefix-$servicename-class.sh kafka.tools.MirrorMaker "\$@"
EOF

#последний этап
#cp /opt/hadoop/kafka/bin/kafka-run-class.sh -va /opt/hadoop/kafka/bin/kafka-run-$prefix-$servicename-class.sh

#chown -R local_kafka:local_kafka /opt/hadoop/
#chmod 755  kafka-run-$prefix-$servicename-class.sh
chmod 755  kafka-mirror-$prefix-$servicename.sh
chmod 755  kafka-mirror-$prefix-$servicename-start.sh
chmod 755  kafka-mirror-$prefix-$servicename-stop.sh

echo "---------------------------------------"
echo "kafka-mirror-$prefix-$servicename.service"

#/usr/bin/systemctl daemon-reload
#systetmctl enable --now kafka-mirror-$prefix-$servicename.service
#/usr/bin/systemctl status networking.service

