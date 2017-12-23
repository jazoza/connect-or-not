#!/bin/bash
while true
do
    if pgrep -fl "react.py" &>/dev/null; then
      echo "it is already running"
      sleep 60
    else
      echo "not running"
      python react.py&
    fi
done
