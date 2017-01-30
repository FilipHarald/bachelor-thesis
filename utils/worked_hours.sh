#!/bin/bash
echo 'Filip:'
cat log.md |  awk -F "|" '{print $3, $4}' | grep 'X' | awk -F " " '{print $1}' | awk '{s+=$1} END {print s}'
echo 'Teddy:'
cat log.md |  awk -F "|" '{print $3, $5}' | grep 'X' | awk -F " " '{print $1}' | awk '{s+=$1} END {print s}'
echo 'sum:'
cat log.md |  awk -F "|" '{print $3}' | grep -E -w '[0-9]+' | awk '{s+=$1} END {print s}'
