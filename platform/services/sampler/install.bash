#! /usr/bin/env bash

# get the path where we are executing from
executing_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

service_name="rpi_home_sampler.service";

# stop the service if it is already installed
if [ -f "/lib/systemd/system/$service_name" ]; then
  echo "stopping \"$service_name\"...";
  sudo systemctl stop "$service_name";
fi

# copy the service file to the lib directory
echo "installing \"$service_name\"...";
sudo cp "$executing_dir/$service_name" "/lib/systemd/system/"

# enable the service
echo "enabling \"$service_name\"...";
sudo systemctl enable "$service_name";

# start the service
echo "starting \"$service_name\"...";
sudo systemctl start "$service_name";
