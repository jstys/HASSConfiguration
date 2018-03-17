#!/bin/bash

{
    rm -rf ./gittmp
    mkdir ./gittmp
    cd gittmp
    git clone https://github.com/jstys/HASSConfiguration.git
    cp -R ./HASSConfiguration/hass/* ../
    cd ..
    rm -rf gittmp
}