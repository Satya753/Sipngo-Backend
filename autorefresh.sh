#!/bin/bash

flask_server="app.py"

pid=$(ps aux | grep "$flask_server" | grep -v grep | awk '{print $2}')
echo "$pid"

if [ -z "$pid" ]; then
    echo "Process '$process_name' not found."
else
	kill -9 "$pid"
fi
nohup python3.9 /test/sipngo/app.py > /dev/null 2>&1 &

