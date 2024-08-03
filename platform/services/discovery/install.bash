#! /usr/bin/env bash

# get the path where we are executing from
executing_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

service_name="discovery_registration.service";

# stop the service if it is already installed
if [ -f "/lib/systemd/system/$service_name" ]; then
  echo "stopping \"$service_name\"...";
  sudo systemctl stop "$service_name";
fi

# rewrite the service file and copy it to the lib directory
echo "installing \"$service_name\"...";
perl -pe "s/\Q{user}\E/$USER/g" "$executing_dir/$service_name" > "$executing_dir/$service_name.tmp";
sudo cp "$executing_dir/$service_name.tmp" "/lib/systemd/system/$service_name"
rm -f "$executing_dir/$service_name.tmp";

# enable the service
echo "enabling \"$service_name\"...";
sudo systemctl enable "$service_name";

# start the service
echo "starting \"$service_name\"...";
sudo systemctl start "$service_name";
