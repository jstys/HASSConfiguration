sudo hassbian-config install appdaemon
sudo su -s /bin/bash homeassistant
source /srv/appdaemon/bin/activate
pip install -r /home/homeassistant/appdaemon/requirements.txt