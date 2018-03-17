#!/bin/bash

{
    rm -rf ./gittmp
    mkdir ./gittmp
    cd gittmp
    git clone https://github.com/jstys/HASSConfiguration.git
    cp -R ./HASSConfiguration/appdaemon/* ../
    cd ..
    rm -rf gittmp
}