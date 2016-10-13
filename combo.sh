#!/bin/sh

./rm.sh && \
./launch.sh && \
sleep 1 && \
./check.sh && \
sleep 1 && \
./benchmark.sh START
