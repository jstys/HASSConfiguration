#!/bin/bash

read -p "IP-based device? " IP_DEV

if ! test -f backup.txt; then
    echo "Missing backup.txt"
    exit 1
fi

if [[ "$IP_DEV" == "y" ]]; then
    read -p "Enter address: " IP_ADDR
    docker-compose run --rm bellows_ip -d $IP_ADDR info
    docker-compose run --rm bellows_ip -d $IP_ADDR restore -f --i-understand-i-can-update-eui64-only-once-and-i-still-want-to-do-it -B /tmp/backup.txt
else
    read -p "Enter tty port: " TTY_PORT
    if ! test -c $TTY_PORT; then
        echo "Invalid tty port"
        exit 1
    fi
    
    TTY_PORT=$TTY_PORT docker-compose run --rm bellows_tty -d $TTY_PORT info
    TTY_PORT=$TTY_PORT docker-compose run --rm bellows_tty -d $TTY_PORT restore --i-understand-i-can-update-eui64-only-once-and-i-still-want-to-do-it -B /tmp/backup.txt
fi