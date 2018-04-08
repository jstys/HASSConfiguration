#!/bin/bash

{
    rm -rf ./gittmp
    mkdir ./gittmp
    cd gittmp
    git clone https://github.com/jstys/HASSConfiguration.git
    if [ -f ../appdaemon.yaml ]; then
        cp ../appdaemon.yaml ../appdaemon.yaml.bak
    fi
    cp -R ./HASSConfiguration/appdaemon/* ../
    cd ..
    rm -rf gittmp
}