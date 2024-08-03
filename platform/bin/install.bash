#! /usr/bin/env bash

# setup our executing path
rpi_home_dir=/usr/local/rpi_home;
platform_bin_dir="$rpi_home_dir/platform/bin";

# install git
sudo apt-get install -y git;

# XXX update the config and cmdline
# cgroup_enable=cpuset cgroup_memory=1 cgroup_enable=memory
# headless, ethernet only
#dtoverlay=disable-wifi
#dtoverlay=disable-bt

# echo > .hushlogin
# install bashrc and .ssh

# if the target is in the wrong place, move it
# XXX can we do this?

# install the applications needed by the device at runtime
sudo apt-get install -y sysstat lshw apache2 python3 python3-pip python3-venv;

# create the python venv we'll be using
if [ ! -d "$rpi_home_dir/python3" ]; then
  python3 -m venv "$rpi_home_dir/python3";
fi;

# set the locale to what we need for sysstat - might need to run raspi-config to set the locale.
# XXX is there a better way?
if [ ! -f "/etc/default/locale" ]; then
  sudo raspi-config;
fi;
echo "LANG=C.UTF-8" | sudo tee "/etc/default/locale";

# set up the target directory
rpi_home_www_dir="/var/www/html";
if [ -L "$rpi_home_www_dir" ]; then
  sudo rm -f "$rpi_home_www_dir";
fi;
if [ -d "$rpi_home_www_dir" ]; then
  sudo mv "$rpi_home_www_dir" "$rpi_home_www_dir.old";
fi;
sudo ln -s "$rpi_home_dir/platform/www" "$rpi_home_www_dir";
echo "linked rpi_home dir ($rpi_home_www_dir).";

# drop the system report in the rpi_home directory, convert it to json, clean up after ourselves
sudo lshw > "$rpi_home_www_dir/lshw.txt";
"$platform_bin_dir/lshw-json.py" "$rpi_home_www_dir/lshw.txt" "$rpi_home_www_dir/platform.json";
rm -f "$rpi_home_www_dir/lshw.txt";

# install the services
$platform_bin_dir/install_sevices.bash;
