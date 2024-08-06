#! /usr/bin/env bash

echo "installing rpi_home..."

# setup our executing path
rpi_home_dir=/usr/local/rpi_home;
platform_bin_dir="$rpi_home_dir/platform/bin";

# the config file
CONFIG="/boot/firmware/config.txt";

# disable bluetooth almost always
sudo bash <<EOF
sed -i -e "s/.*dtoverlay=disable-bt/dtoverlay=disable-bt/" "$CONFIG";
BT_CONFIG=$(grep "dtoverlay=disable-bt" "$CONFIG");
if [ -z "$BT_CONFIG" ]; then
    echo "dtoverlay=disable-bt" >> "$CONFIG";
fi;
echo "  bluetooth disabled!"
EOF

# determine if this is a wifi-only device (a raspberry pi zero or zero 0)
is_not_raspberry_pi_zero() {
  local hw_revision;
  hw_revision=$(grep Revision /proc/cpuinfo | awk '{print $3}');
  case $hw_revision in
      "900092" | "900093" | "920093" | "902120")
          return 1;
          ;;
      *)
          return 0;
          ;;
  esac
}

# disable wifi - probably, if there is an eth0 interface on the device
if is_not_raspberry_pi_zero; then
sudo bash <<EOF
    sed -i -e "s/.*dtoverlay=disable-wifi/dtoverlay=disable-wifi/" "$CONFIG";
    BT_CONFIG=$(grep "dtoverlay=disable-wifi" "$CONFIG");
    if [ -z "$BT_CONFIG" ]; then
        echo "dtoverlay=disable-wifi" >> "$CONFIG";
    fi;
    echo "  wifi disabled!"
EOF
fi;

# the command line file
CMDLINE="/boot/firmware/cmdline.txt";

# update the cmdline to support docker controls we want
CGROUP_ENABLED=$(grep "cgroup_enable=cpuset cgroup_memory=1 cgroup_enable=memory" "$CMDLINE");
if [ -z "$CGROUP_ENABLED" ]; then
    sudo bash <<EOF
    echo " cgroup_enable=cpuset cgroup_memory=1 cgroup_enable=memory" | tee -a "$CMDLINE";
EOF
fi;

# install the applications needed by the device at runtime
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y sysstat lshw apache2 python3 python3-pip python3-venv;

# create the python venv we'll be using
if [ ! -d "$rpi_home_dir/python3" ]; then
  python3 -m venv "$rpi_home_dir/python3";
fi;

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
sudo lshw | tee "$rpi_home_www_dir/lshw.txt";
"$platform_bin_dir/lshw-json.py" "$rpi_home_www_dir/lshw.txt" "$rpi_home_www_dir/platform.json";
rm -f "$rpi_home_www_dir/lshw.txt";
echo "exported platform.json.";

# install the services
$platform_bin_dir/install_services.bash;
