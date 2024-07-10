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

#пилим демона
#cat << EOF | tee kafka-mirror-$prefix-$topicname.service
cat << EOF | tee /etc/systemd/system/kafka-mirror-$prefix-$topicname.service
[Unit]
Description=KafkaMirror Daemon 
Documentation=https://kafka.apache.org/documentation/
Requires=network.target
After=network.target

[Service]
User=local_kafka
Group=local_kafka
ExecStart=/opt/hadoop/kafka-mirror-$prefix-$topicname-start.sh
ExecStop=/opt/hadoop/kafka-mirror-$prefix-$topicname-stop.sh
TimeoutSec=60
Restart=on-failure

[Install]
WantedBy=default.target
EOF

#echo "add new-$prefix-$topicname.sh to $bootstrap servier(s)"
#пилим файлы /opt/hadoop/ если топиков в задаче больше одного, то затем можно их добавить в whitelist
#start.sh
#cat << EOF | tee kafka-mirror-$prefix-$topicname-start.sh
cat << EOF | tee /opt/hadoop/kafka-mirror-$prefix-$topicname-start.sh
#!/bin/bash
echo "mirror maker restarted \$(date)">>/opt/hadoop/kafka/logs/mirror-$prefix-$topicname.log
cd /opt/hadoop/kafka/bin/
export KAFKA_HEAP_OPTS=-Xmx384M
./kafka-mirror-$prefix-$topicname.sh \
--consumer.config ../config_local/consumer-mirror-$prefix-$topicname.properties \
--producer.config ../config_local/producer_mirror_adh_cluster.properties \
--whitelist '$topicname' \
--num.streams 3 \
--offset.commit.interval.ms 6000 \
--abort.on.send.failure false
EOF
#stop.sh
cat << EOF | tee /opt/hadoop/kafka-mirror-$prefix-$topicname-start.sh
#cat << EOF | tee kafka-mirror-$prefix-$topicname-stop.sh
#!/bin/sh
SIGNAL=\${SIGNAL:-TERM}
PIDS=\$(ps ax | grep -i "consumer-mirror-$prefix-$topicname*" | grep java | grep -v grep | awk '{print $1}') 
if [ -z "\$PIDS" ]; then
  echo "No mirrormaker service to stop"
  echo "No mirrormaker service to stop" >> /opt/hadoop/kafka/logs/mirror-$prefix-$topicname.log
  exit 1
else
  kill -s \$SIGNAL \$PIDS
  echo "stopped mirrormaker service"
  echo "stopped mirrormaker service \$date" >> /opt/hadoop/kafka/logs/mirror-$prefix-$topicname.log
fi
EOF

#файл /opt/hadoop/kafka/config_local/*.properties
#cat << EOF | tee kafka-mirror-$prefix-$topicname.properties 
cat << EOF | tee /opt/hadoop/kafka/config_local/kafka-mirror-$prefix-$topicname.properties
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
#cat << EOF | tee kafka-mirror-$prefix-$topicname.sh
cat << EOF | tee /opt/hadoop/kafka/bin/kafka-mirror-$prefix-$topicname.sh
#!/bin/bash
exec \$(dirname $0)/kafka-run-$prefix-$topicname-class.sh kafka.tools.MirrorMaker "\$@"
EOF

#последний этап
cp /opt/hadoop/kafka/bin/kafka-run-class.sh -va /opt/hadoop/kafka/bin/kafka-run-$prefix-$topicname-class.sh

chown -R local_kafka:local_kafka /opt/hadoop/
chmod 755  /opt/hadoop/kafka/bin/kafka-run-$prefix-$topicname-class.sh
chmod 755  /opt/hadoop/kafka/bin/kafka-mirror-$prefix-$topicname.sh
chmod 644  /opt/hadoop/kafka/config_local/kafka-mirror-$prefix-$topicname.properties
chmod 755  /opt/hadoop/kafka-mirror-$prefix-$topicname-start.sh
chmod 755  /opt/hadoop/kafka-mirror-$prefix-$topicname-stop.sh

systemctl daemon-reload
systetmctl enable --now kafka-mirror-$prefix-$topicname.service
systemctl status kafka-mirror-$prefix-$topicname.service

