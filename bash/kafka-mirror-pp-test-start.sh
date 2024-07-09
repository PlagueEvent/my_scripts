#!/bin/bash
echo "mirror maker restarted Вт 09 июл 2024 17:44:45 MSK">>/opt/hadoop/kafka/logs/mirror-pp-test.log
cd /opt/hadoop/kafka/bin/
export KAFKA_HEAP_OPTS=-Xmx384M
./kafka-mirror-pp-test.sh --consumer.config ../config_local/consumer_mirror_pp-test.properties --producer.config ../config_local/producer_mirror_adh_cluster.properties --whitelist 'test' --num.streams 3 --offset.commit.interval.ms 6000 --abort.on.send.failure false
