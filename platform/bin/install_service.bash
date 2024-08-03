#! /usr/bin/env bash

# setup our executing path
rpi_home_dir=/usr/local/rpi_home;
services_dir="$rpi_home_dir/platform/services";

# accumulate the service specification
service_dir=$1;
source_dir="$services_dir/$service_dir";
service_name="rpi_home_$service_dir.service";
systemd_dir="/lib/systemd/system";

# stop the service if it is already installed
if [ -f "$systemd_dir/$service_name" ]; then
  echo "  stopping existing \"$service_name\"...";
  sudo systemctl stop "$service_name";
fi

# rewrite the service file and copy it to the lib directory
echo "  installing \"$service_name\"...";
perl -pe "s/\Q{user}\E/$USER/g" "$source_dir/$service_name" > "$source_dir/$service_name.tmp";
sudo cp "$source_dir/$service_name.tmp" "$systemd_dir/$service_name"
rm -f "$source_dir/$service_name.tmp";

# enable the service
echo "  enabling \"$service_name\"...";
sudo systemctl enable "$service_name";

# start the service
echo "  starting \"$service_name\"...";
sudo systemctl start "$service_name";

echo "  finished installing \"$service_name\"";
