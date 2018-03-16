#!/bin/bash

if [ -d .git ]; then
    git pull
else
    git clone https://github.com/jstys/HASSConfiguration/tree/master/hass
fi

curl -X POST http://localhost:8123/api/services/homeassistant/restart