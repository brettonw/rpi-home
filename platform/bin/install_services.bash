#! /usr/bin/env bash

# setup our executing path
rpi_home_dir=/usr/local/rpi_home;
platform_bin_dir="$rpi_home_dir/platform/bin";
services_dir="$rpi_home_dir/platform/services";

# install (upgrade) the rpi_home module
$rpi_home_dir/python3/bin/pip3 install --upgrade "$rpi_home_dir/pip/";

# iterate over each subdirectory of the services directory
subdirs=$(find "$services_dir" -mindepth 1 -maxdepth 1 -type d -not -path '.');
for dir in $subdirs; do
  # get the subdirectory name without the full path
  subdir_name=$(basename "$dir");
  echo "service: $subdir_name";
  $platform_bin_dir/install_service.bash "$subdir_name";
done
