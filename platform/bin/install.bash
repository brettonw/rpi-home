#! /usr/bin/env bash

# get the path where we are executing from
executing_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
rpi_root_dir=/usr/local/rpi_home;

# if the target is in the wrong place, move it
# XXX can we do this?

# install the applications needed by the device at runtime
sudo apt-get install -y sysstat lshw apache2 python3 python3-pip python3-venv;

# create the python venv we'll be using
if [ ! -d "$rpi_root_dir/python3" ]; then
  python3 -m venv "$rpi_root_dir/python3";
fi;

# set the locale to what we need for sysstat - might need to run raspi-config to set the locale.
# XXX is there a better way?
if [ ! -f "/etc/default/locale" ]; then
  sudo raspi-config;
fi;
echo "LANG=C.UTF-8" | sudo tee "/etc/default/locale";

# set up the target directory
rpi_home_www_dir="/var/www/html/rpi_home";
if [ -L "$rpi_home_www_dir" ]; then
  sudo rm -f "$rpi_home_www_dir";
fi;
sudo ln -s "$rpi_root_dir/platform/www" "$rpi_home_www_dir";
echo "Linked rpi_home dir ($rpi_home_www_dir).";

# drop the system report in the rpi_home directory, convert it to json, clean up after ourselves
sudo lshw > "$rpi_home_www_dir/lshw.txt";
"$executing_dir/lshw-json.py" "$rpi_home_www_dir/lshw.txt" "$rpi_home_www_dir/platform.json";
rm -f "$rpi_home_www_dir/lshw.txt";

# install (upgrade) the rpi_home module
$rpi_root_dir/python3/bin/pip3 install --upgrade "$rpi_root_dir/pip/rpi_home";

# install the discovery listener service
$rpi_root_dir/platform/services/discovery/install.bash;

# install the sampler service
$rpi_root_dir/platform/services/sampler/install.bash;
