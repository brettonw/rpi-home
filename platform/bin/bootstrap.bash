#!/usr/bin/env bash

COMMANDS=$(cat <<'ENDSSH'
# just keep the visual clutter to a minimum
echo > ~/.hushlogin

echo "updating package lists...";
sudo apt-get update;

echo "upgrading installed packages...";
sudo apt-get upgrade -y;

echo "installing git...";
sudo apt-get install -y git;

# create a .ssh key for github
echo "creating ssh key...";
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -q -N "";

# clone the rpi_home repository
echo "cloning rpi_home...";
git clone git@github.com:brettonw/rpi_home.git;

# move it to the final destination
echo "installing rpi_home to /usr/local/...";
sudo mv rpi_home /usr/local/;

echo "bootstrap complete. installing rpi_home...";
/usr/local/rpi_home/platform/bin/install.bash;

# reboot
echo "rebooting...";
sudo reboot now;
ENDSSH
);

# go to the target machine and run the commands from above
ssh $1 "${COMMANDS}";
