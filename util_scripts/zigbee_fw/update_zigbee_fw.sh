#!/bin/bash

FIRMWARE_FILE="$(pwd)/CC1352P2_CC2652P_launchpad_coordinator_20240710.hex"
SERIAL_DEV="/dev/ttyUSB0"

docker run --rm \
    --device $SERIAL_DEV:$SERIAL_DEV \
    -e FIRMWARE_FILE=/firmware.hex \
    -v $FIRMWARE_FILE:/firmware.hex \
    ckware/ti-cc-tool -ewv -p $SERIAL_DEV --bootloader-sonoff-usb