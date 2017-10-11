#!/bin/sh


set -e
set -u

SNIPS_CONFIG_PATH="/opt/snips/config"
SNIPS_INSTALL_PATH="/usr/bin"
SNIPS_BINARY="${SNIPS_INSTALL_PATH}/snips"
SNIPS_UPDATE_PLATFORM_BINARY="${SNIPS_INSTALL_PATH}/snips-update-platform"
SNIPS_INSTALL_ASSISTANT_BINARY="${SNIPS_INSTALL_PATH}/snips-install-assistant"
SNIPS_WATCH_BINARY="${SNIPS_INSTALL_PATH}/snips-watch"

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# See which `echo` command to use to output colors, depending on the shell
echo_cmd="echo"
_echo_tmp=`echo -e ""`
if [ -z $_echo_tmp ]; then
    echo_cmd="echo -e"
fi

say () {
    $echo_cmd "${1}"
}

err () {
    $echo_cmd "${RED}${1}${NC}" >&2
    exit 1
}

command_exists () {
	command -v "$@" > /dev/null 2>&1
}

need_cmd () {
    if ! command_exists "$1"
    then
        err "need '$1' (install it using apt-get)"
    fi
}

say "Snips platform installation script"
say "${GREEN}WARNING${NC}: for troubleshooting, refer to the documentation on ${GREEN}https://github.com/snipsco/snips-platform-documentation/wiki${NC}"

# This script is meant to be run on a raspi
uname -a | grep -E "armv(7|6)" > /dev/null || err "You should run the Snips platform installation on a Raspberry Pi device"

user="$(id -un 2>/dev/null || true)"
sh_c='sh -c'
if [ "$user" != 'root' ]; then
	if command_exists sudo; then
		sh_c='sudo -E sh -c'
	elif command_exists su; then
		sh_c='su -c'
	else
		cat >&2 <<-'EOF'
		Error: this installer needs the ability to run commands as root.
		We are unable to find either "sudo" or "su" available to make this happen.
EOF
		exit 1
	fi
fi

say " - the Snips config path is ${SNIPS_CONFIG_PATH}"

# Create platform config dir
$sh_c "mkdir -p '${SNIPS_CONFIG_PATH}'"

say " - ensuring Docker is installed"

# Make sure Docker is available
if ! command -v docker > /dev/null 2>&1
then
    say " - ${RED}WARNING${NC}: command 'docker' not found"
    say "Do you want to install docker? (Y/n)"
    read a </dev/tty || a="y" # if the tty is not available, force installation
    if [ "$a" = "" -o "$a" = "y" -o "$a" = "Y" ] ; then
        need_cmd curl
        say " - running 'docker_install.sh'"
        sh ./docker_install.sh || err "Could not install Docker"
    else
        err "Docker is required to run the Snips platform"
    fi

    $sh_c 'usermod -aG docker pi'
    $sh_c 'systemctl enable docker'
    $sh_c 'systemctl start docker'
    if [ $(id -gn) != docker ]; then
        exec sg docker "curl https://install.snips.ai -sSf | sh"
    fi

fi

# Enable docker
say " - enabling Docker"
$sh_c 'systemctl enable docker'
$sh_c 'systemctl start docker'
$sh_c 'usermod -aG docker pi'

say " - ensuring the audio input is correctly setup"
# Make sure there is a .asoundrc
if [ -f ${HOME}/.asoundrc ]; then
    say "   - ${GREEN}Found ${HOME}/.asoundrc${NC}"
else
    say "   - ${RED}WARNING${NC}: no ${HOME}/.asoundrc found, creating a file with default parameters (if this does not work, see )"
    say "   - ${RED}WARNING${NC}: using default parameters of hw:0,0 for audio output and hw:1,0 for audio input, you can test those settings using 'arecord' and 'aplay' to ensure they work, see ${GREEN}https://github.com/snipsco/snips-platform-documentation/wiki/1.-Setup-the-Snips-Voice-Platform-on-your-Raspberry-Pi#configuring-the-audio${NC} for troubleshooting"
    cat >| ${HOME}/.asoundrc <<EOS
pcm.!default {
  type asym
   playback.pcm {
     type plug
     slave.pcm "hw:0,0"
   }
   capture.pcm {
     type plug
     slave.pcm "hw:1,0"
   }
}

ctl.!default {
  type hw
  card 1
}
EOS
fi

# Require mktemp to create files
need_cmd mktemp
# Require unzip for the snips-install-assistant command
need_cmd unzip

say " - installing ${GREEN}snips${NC} to ${SNIPS_INSTALL_PATH}"

out_file=`mktemp`
cat > ${out_file} <<EOF
#!/bin/sh
set -e

echo "Running Snips"

# Removing any running container
(docker stop snips > /dev/null 2>&1) || true

# Making sure a microphone is detected
(LC_ALL=C arecord -l | grep card > /dev/null) || (echo "No microphone found, make sure you connect a microphone to your Raspberry Pi and it is visible with 'arecord -l'" >&2 ; exit 1)

# Making sure there is an assistant
[ -f '${SNIPS_CONFIG_PATH}/assistant/assistant.json' ] || (echo "No assistant found, make sure you install an assistant using 'snips-install-assistant assistant.zip' before starting the platform" >&2 ; exit 1)

# Start the Snips container
docker run -t --rm --name snips \
    --privileged \
    --log-driver none \
    -p 9898:1883 \
    -v ${HOME}/.asoundrc:/root/.asoundrc \
    -v ${SNIPS_CONFIG_PATH}:/opt/snips/config \
    -v /dev/snd:/dev/snd \
    snipsdocker/platform
EOF
$sh_c "mv -f ${out_file} ${SNIPS_BINARY}"
$sh_c "chmod a+x '${SNIPS_BINARY}'"

say " - installing ${GREEN}snips-platform-update${NC} to ${SNIPS_INSTALL_PATH}"

out_file=`mktemp`
sudo cat > ${out_file} <<EOF
#!/bin/sh
set -e

echo "Updating Snips platform"
docker pull snipsdocker/platform
EOF
$sh_c "mv -f ${out_file} ${SNIPS_UPDATE_PLATFORM_BINARY}"
$sh_c "chmod a+x '${SNIPS_UPDATE_PLATFORM_BINARY}'"

say " - installing ${GREEN}snips-install-assistant${NC} to ${SNIPS_INSTALL_PATH}"

out_file=`mktemp`
sudo cat > ${out_file} <<EOF
#!/bin/sh
set -e

if [ -z \$1 ]; then
    echo "Usage: \$0 assistant.zip"
    echo "where assistant.zip is the assistant archive downloaded from https://console.snips.ai"
    exit 1
fi

if [ ! -f \$1 ]; then
    echo "File \$1 not found"
    exit 1
fi

echo "Installing Snips assistant \$1 in /opt/snips/config/assistant"
sudo rm -rf ${SNIPS_CONFIG_PATH}/assistant
sudo unzip \$1 -d ${SNIPS_CONFIG_PATH}
EOF
$sh_c "mv -f ${out_file} ${SNIPS_INSTALL_ASSISTANT_BINARY}"
$sh_c "chmod a+x '${SNIPS_INSTALL_ASSISTANT_BINARY}'"

say " - installing ${GREEN}snips-watch${NC} to ${SNIPS_WATCH_BINARY}"

out_file=`mktemp`
sudo cat > ${out_file} <<EOF
#!/usr/bin/env python
#encoding: utf-8

try:
    import paho.mqtt.client as mqtt
except:
    raise Exception("Please install paho-mqtt: pip install paho-mqtt")
    import sys
    sys.exit(1)

try:
    import simplejson as json
except:
    raise Exception("Please install simplejson: pip install simplejson")
    import sys
    sys.exit(1)

import datetime

def time_now():
    return datetime.datetime.now().strftime('%H:%M:%S.%f')

# MQTT client to connect to the bus
mqtt_client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    # subscribe to all messages
    mqtt_client.subscribe('#')


# Process a message as it arrives
def on_message(client, userdata, msg):
        print('[{}] - {}'.format(time_now(), msg.topic))

        if len(msg.payload) > 0:
            json_payload = json.loads(msg.payload)
            if msg.topic == 'hermes/audioServer/playBytes' and json_payload['wavBytes'] is not None:
                json_payload['wavBytes'] = json_payload['wavBytes'][:42] + (json_payload['wavBytes'][42:] and '...')

            print(json.dumps(json_payload, indent=2, sort_keys=True, ensure_ascii=False, encoding="utf-8"))

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect('localhost', 9898)
mqtt_client.loop_forever()
EOF
$sh_c "mv -f ${out_file} ${SNIPS_WATCH_BINARY}"
$sh_c "chmod a+x '${SNIPS_WATCH_BINARY}'"

# Warn the user if Python or pip is not installed
if ! ( command -v python && command -v pip ) > /dev/null 2>&1
then
    say "${RED}WARNING${NC}: python and pip are required to run snips-watch but were not found on the system"
    say "Do you want to install Python and pip? (Y/n)"
    read a </dev/tty || a="y" # if the tty is not available, force installation
    if [ "$a" = "" -o "$a" = "y" -o "$a" = "Y" ] ; then
        say " - installing ${GREEN}python${NC} and ${GREEN}pip${NC}"
        sudo apt-get install -y python python-pip
    else
        say "${RED}You can use 'apt-get install python python-pip && pip install --upgrade paho-mqtt simplejson'${NC}"
    fi
fi

if command -v pip > /dev/null 2>&1
then
    say " - installing ${GREEN}paho-mqtt${NC} and ${GREEN}simplejson${NC} as a requirement for snips-watch"
    sudo pip install --upgrade paho-mqtt simplejson
fi

# Do the update to download the Snips platform
say " - Downloading the Snips platform"
${SNIPS_UPDATE_PLATFORM_BINARY} || {
    say "Could not install the Snips platform\n"
    say "${RED}If the Docker image could not be downloaded because of a permission denied error, you might want to log out and log in again, and run the script again${NC}\n"
    say "see ${GREEN}https://github.com/snipsco/snips-platform-documentation/wiki/1.-Setup-the-Snips-Voice-Platform-on-your-Raspberry-Pi#step-4-download-snips-platform-docker-image${NC} for troubleshooting"
    err "Error while downloading the Docker image"
}

say "${GREEN}Done!${NC}"
say ""
say "Installed binaries:"
say ""
say " - ${GREEN}snips${NC}: start the Snips platform"
say " - ${GREEN}snips-install-assistant${NC} assistant.zip: install an assistant from a .zip archive downloaded from the console"
say " - ${GREEN}snips-update-platform${NC}: update the platform to the latest version"
say " - ${GREEN}snips-watch${NC}: display the messages sent on the bus"
say ""
say "${GREEN}WARNING${NC}: you might want to adjust your audio settings using 'alsamixer' to make sure the audio input and output gain have correct values"
say ""
say "${GREEN}WARNING${NC}: make sure your audio output and input are correctly configured using 'arecord' to record a wav and 'aplay' to play it, see ${GREEN}https://github.com/snipsco/snips-platform-documentation/wiki/1.-Setup-the-Snips-Voice-Platform-on-your-Raspberry-Pi#configuring-the-audio${NC} for audio troubleshooting"
say ""
say "Finish the installation by following the tutorial at ${GREEN}https://github.com/snipsco/snips-platform-documentation/wiki/1.-Setup-the-Snips-Voice-Platform-on-your-Raspberry-Pi${NC} and create your first assistant!"
