#!/bin/bash

docker run --name=appdaemon -d -p 5050:5050 \
  --restart=always \
  -e HA_URL="http://10.0.0.6:8123" \
  -e DASH_URL="http://$HOSTNAME:5050" \
  -v /home/pi/appdaemon:/conf \
  acockburn/appdaemon:latest