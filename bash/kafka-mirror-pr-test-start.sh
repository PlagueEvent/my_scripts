#!/bin/bash
echo "mirror maker restarted $(date)">>/opt/hadoop/kafka/logs/mirror-pr-test.log
cd /opt/hadoop/kafka/bin/
export KAFKA_HEAP_OPTS=-Xmx384M
./kafka-mirror-pr-test.sh --consumer.config ../config_local/consumer_mirror_pr-test.properties --producer.config ../config_local/producer_mirror_adh_cluster.properties --whitelist 'test' --num.streams 3 --offset.commit.interval.ms 6000 --abort.on.send.failure false
