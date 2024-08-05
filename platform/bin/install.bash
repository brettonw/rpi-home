#! /usr/bin/env bash

# setup our executing path
rpi_home_dir=/usr/local/rpi_home;
platform_bin_dir="$rpi_home_dir/platform/bin";

# function to ask for user confirmation with a default option (chatgpt, reviewed by bsw)
ask_user() {
    local prompt default reply

    # determine the prompt format based on the default value
    if [[ "$2" =~ ^[Yy]$ ]]; then
        prompt="Y/n"
        default=Y
    elif [[ "$2" =~ ^[Nn]$ ]]; then
        prompt="y/N"
        default=N
    else
        echo "invalid default option: $2"
        return 1
    fi

    while true; do
        # prompt the user with the formatted question
        read -p "$1 ($prompt): " reply
        # f no reply is given, use the default
        if [[ -z "$reply" ]]; then
            reply=$default
        fi
        case $reply in
            [Yy]* ) return 0;;  # return 0 for "yes"
            [Nn]* ) return 1;;  # return 1 for "no"
            * ) echo "please answer yes or no.";;  # shouldn't happen
        esac
    done
}

# the config file
CONFIG="/boot/firmware/config.txt";

# disable bluetooth almost always
if ask_user "would you like to disable bluetooth?" "y"; then
  sed -i -e "s/.*dtoverlay=disable-bt/dtoverlay=disable-bt/" "$CONFIG";
  BT_CONFIG=$(grep "dtoverlay=disable-bt" "$CONFIG");
  if [ -z "$BT_CONFIG" ]; then
      echo "dtoverlay=disable-bt" >> "$CONFIG";
  fi;
  echo "  bluetooth disabled!"
fi;

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
  if ask_user "would you like to disable wifi?" "y"; then
    sed -i -e "s/.*dtoverlay=disable-wifi/dtoverlay=disable-wifi/" "$CONFIG";
    BT_CONFIG=$(grep "dtoverlay=disable-wifi" "$CONFIG");
    if [ -z "$BT_CONFIG" ]; then
        echo "dtoverlay=disable-wifi" >> "$CONFIG";
    fi;
    echo "  wifi disabled!"
  fi;
fi;

the command line file
CMDLINE="/boot/firmware/cmdline.txt";

# update the cmdline to support docker controls we want
CGROUP_ENABLED=$(grep "cgroup_enable=cpuset cgroup_memory=1 cgroup_enable=memory" "$CMDLINE");
if [ -z "$CGROUP_ENABLED" ]; then
    echo " cgroup_enable=cpuset cgroup_memory=1 cgroup_enable=memory" >> "$CMDLINE";
fi;

# install the applications needed by the device at runtime
sudo apt-get install -y sysstat lshw apache2 python3 python3-pip python3-venv;

# create the python venv we'll be using
if [ ! -d "$rpi_home_dir/python3" ]; then
  python3 -m venv "$rpi_home_dir/python3";
fi;

# set the locale to what we need for sysstat - based off the raspi-config script
sudo bash <<EOF
echo "C.UTF-8 UTF-8" > /etc/locale.gen;
echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen;
update-locale --no-checks LANG=C.UTF-8;
dpkg-reconfigure -f noninteractive locales;
EOF

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

# install the services
$platform_bin_dir/install_sevices.bash;
