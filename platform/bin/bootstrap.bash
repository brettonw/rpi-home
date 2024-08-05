#!/usr/bin/env bash

COMMANDS=$(cat <<'ENDSSH'
# just keep the visual clutter to a minimum
echo > ~/.hushlogin

# set the locale to what we need - based off the raspi-config script
echo "setting locale...";
sudo bash <<EOF
echo "C.UTF-8 UTF-8" > /etc/locale.gen;
echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen;
update-locale --no-checks LANG=C.UTF-8;
dpkg-reconfigure -f noninteractive locales;
EOF

# update the system
echo "updating package lists and upgrading installed packages...";
sudo apt-get update && apt-get upgrade -y;

# install git
echo "installing git...";
sudo apt-get install -y git;

# clone the rpi_home repository
echo "cloning rpi_home...";
git clone https://github.com/brettonw/rpi_home.git;

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
