#!/bin/bash

FIRMWARE_BASE_URL="https://github.com/Koenkk/Z-Stack-firmware/releases/download"
FIRMWARE_FILE="Z-Stack_3.x.0_coordinator_20240710/CC1352P2_CC2652P_launchpad_coordinator_20240710.zip"
FIRMWARE_PATH="$FIRMWARE_BASE_URL/$FIRMWARE_FILE"
SERIAL_DEV="/dev/ttyUSB0"

docker run --rm \
    --device $SERIAL_DEV:$SERIAL_DEV \
    -e FIRMWARE_URL=$FIRMWARE_PATH \
    ckware/ti-cc-tool -ewv -p $SERIAL_DEV --bootloader-sonoff-usb