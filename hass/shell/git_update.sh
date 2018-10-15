#!/bin/bash

{
    rm -rf ./gittmp ./zhanewtmp
    mkdir ./gittmp ./zhanewtmp

    cd gittmp
    git clone https://github.com/jstys/HASSConfiguration.git
    cp -R ./HASSConfiguration/hass/* ../
    cd ..
    rm -rf gittmp

    cd zhanewtmp
    git clone https://github.com/Yoda-x/ha-zha-new.git
    rsync -avh ./ha-zha-new/custom_components/* ../custom_components
    cd ..
    rm -rf zhanewtmp
}