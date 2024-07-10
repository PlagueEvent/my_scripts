#!/bin/sh
SIGNAL=${SIGNAL:-TERM}
PIDS=$(ps ax | grep -i "consumer_mirror_pr-test*" | grep java | grep -v grep | awk '{print }') 
if [ -z "$PIDS" ]; then
  echo "No mirrormaker service to stop"
  echo "No mirrormaker service to stop" >> /opt/hadoop/kafka/logs/mirror-pr-test.log
  exit 1
else
  kill -s $SIGNAL $PIDS
  echo "stopped mirrormaker service"
  echo "stopped mirrormaker service $date" >> /opt/hadoop/kafka/logs/mirror-pr-test.log
fi
