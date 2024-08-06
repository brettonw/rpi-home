#! /usr/bin/env bash

# setup our executing path
rpi_home_dir=/usr/local/rpi_home;
platform_bin_subdir="$rpi_home_dir/platform/bin";

# install (upgrade) the rpi_home modules
modules_dir="$rpi_home_dir/modules";
module_dirs=(ha_tiny rpi_home);
for module_dir in "${module_dirs[@]}"; do
  echo "module: $module_dir";
  $rpi_home_dir/python3/bin/pip3 install --upgrade "$modules_dir/$module_dir";
done

# iterate over each subdirectory of the services directory
services_dir="$rpi_home_dir/platform/services";
service_dirs=$(find "$services_dir" -mindepth 1 -maxdepth 1 -type d -not -path '.');
for service_dir in $service_dirs; do
  # get the subsubdirectory name without the full path
  service_dir_name=$(basename "$service_dir");
  echo "service: $service_dir_name";
  $platform_bin_subdir/install_service.bash "$service_dir_name";
done
