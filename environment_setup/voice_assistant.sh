git clone https://github.com/google/aiyprojects-raspbian.git
cd aiyprojects-raspbian
git checkout master
./scripts/install-deps.sh
sudo ./scripts/install-alsa-config.sh
sudo ./scripts/install-services.sh
sudo ./scripts/configure-driver.sh
sudo reboot now
source ./env/bin/activate
./checkpoints/check_audio.py