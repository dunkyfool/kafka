#!/bin/bash

total=$(ls /proc|grep ^[0-9]*$|wc -l)
total=$((total-1))
index=1
for i in `ls /proc|grep ^[0-9]*$`;
do
	echo "################### $index/$total ########################"
	echo "PID=$i"
	prtstat $i
	echo "################################################"
	echo " "
	index=$((index+1))
done
