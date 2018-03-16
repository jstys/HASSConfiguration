#!/bin/bash

if [ -d .git ]; then
    git pull
else
    git clone https://github.com/jstys/HASSConfiguration/tree/master/appdaemon
fi