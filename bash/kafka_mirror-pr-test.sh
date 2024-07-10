#!/bin/bash
exec $(dirname ./kafka-mirror.sh)/kafka-run-pr-test-class.sh kafka.tools.MirrorMaker "$@"
