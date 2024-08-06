#! /usr/bin/env bash

# setup our executing path
rpi_home_subdir=/usr/local/rpi_home;
platform_bin_subdir="$rpi_home_subdir/platform/bin";

# install (upgrade) the rpi_home modules
modules_dir="$rpi_home_subdir/modules";
subdirs=$(find "$modules_dir" -mindepth 1 -maxdepth 1 -type d -not -path '.' | sort);
for subdir in $subdirs; do
  # get the subsubdirectory name without the full path
  subdir_name=$(basename "$subdir");
  if [ "$subdir_name" != "bin" ]; then
    echo "module: $subdir_name";
    $rpi_home_subdir/python3/bin/pip3 install --upgrade "$subdir";
  fi;
done

# iterate over each subsubdirectory of the services subdirectory
services_dir="$rpi_home_subdir/platform/services";
subdirs=$(find "$services_dir" -mindepth 1 -maxdepth 1 -type d -not -path '.');
for subdir in $subdirs; do
  # get the subsubdirectory name without the full path
  subdir_name=$(basename "$subdir");
  echo "service: $subdir_name";
  $platform_bin_subdir/install_service.bash "$subdir_name";
done
