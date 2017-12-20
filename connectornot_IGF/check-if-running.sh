while true
do
    if pgrep -f "python test-py.py" &>/dev/null; then
      echo "it is already running"
      sleep 60
    else
      echo "not running"
      python test-py.py&
    fi
done
