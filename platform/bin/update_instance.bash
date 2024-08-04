#! /usr/bin/env bash

# setup our executing path
rpi_home_dir=/usr/local/rpi_home;
platform_bin_dir="$rpi_home_dir/platform/bin";

# move to the target directory
cd $rpi_home_dir || exit;
git pull && "$platform_bin_dir/install_services.bash";
