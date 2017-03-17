#!/bin/bash
ERR='\033[0;31m'  # Green
WARN='\033[1;33m'  # Yellow
OK='\033[0;32m'    # Red
NC='\033[0m'      # No Color

echo -e "${WARN}$1${NC}"
response="$($1)"
echo "$response"
if [[ $response == *"HTTP/1.1 200 OK"* ]]; then
  echo -e "${OK}OK${NC}"
  date="$(date)"
  filename="$(dirname "$0")/history.txt"
  echo "$1 - $date" >> $filename
else
  echo -e "${ERR}Not OK!${NC}"
fi
