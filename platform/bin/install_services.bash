#! /usr/bin/env bash

# setup our executing path
rpi_home_subdir=/usr/local/rpi_home;
platform_bin_subdir="$rpi_home_subdir/platform/bin";

# install (upgrade) the rpi_home modules
# modules_dir="$rpi_home_subdir/modules";
# subdirs=$(find "$modules_dir" -mindepth 1 -maxdepth 1 -type d -not -path '.' | sort);
module_dirs=(ha_tiny rpi_home);
for module_dir in "${module_dirs[@]}"; do
  # get the subsubdirectory name without the full path
  module_dir_name=$(basename "$module_dir");
  echo "module: $module_dir_name";
  $rpi_home_subdir/python3/bin/pip3 install --upgrade "$module_dir";
done

# iterate over each subdirectory of the services directory
services_dir="$rpi_home_subdir/platform/services";
service_dirs=$(find "$services_dir" -mindepth 1 -maxdepth 1 -type d -not -path '.');
for service_dir in $service_dirs; do
  # get the subsubdirectory name without the full path
  service_dir_name=$(basename "$service_dir");
  echo "service: $service_dir_name";
  $platform_bin_subdir/install_service.bash "$service_dir_name";
done
