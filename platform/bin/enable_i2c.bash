#! /usr/bin/env bash

# enable i2c - code adapted from raspi-config
BLACKLIST=/etc/modprobe.d/raspi-blacklist.conf;
if [ -e /boot/firmware/config.txt ] ; then
  FIRMWARE=/firmware;
else
  FIRMWARE=;
fi
CONFIG=/boot${FIRMWARE}/config.txt;

set_config_var() {
  lua - "$1" "$2" "$3" <<EOF > "$3.bak"
local key=assert(arg[1])
local value=assert(arg[2])
local fn=assert(arg[3])
local file=assert(io.open(fn))
local made_change=false
for line in file:lines() do
  if line:match("^#?%s*"..key.."=.*$") then
    line=key.."="..value
    made_change=true
  end
  print(line)
end

if not made_change then
  print(key.."="..value)
end
EOF
mv "$3.bak" "$3"
}


get_i2c() {
  if grep -q -E "^(device_tree_param|dtparam)=([^,]*,)*i2c(_arm)?(=(on|true|yes|1))?(,.*)?$" $CONFIG; then
    echo 1;
  else
    echo 0;
  fi;
}

enable_i2c() {
  if [ "$(get_i2c)" -eq 0 ]; then
    echo "enabling i2c...";
    set_config_var dtparam=i2c_arm on $CONFIG;
    if ! [ -e $BLACKLIST ]; then
      touch $BLACKLIST
    fi;
    sed $BLACKLIST -i -e "s/^\(blacklist[[:space:]]*i2c[-_]bcm2708\)/#\1/";
    sed /etc/modules -i -e "s/^#[[:space:]]*\(i2c[-_]dev\)/\1/";
    if ! grep -q "^i2c[-_]dev" /etc/modules; then
      printf "i2c-dev\n" >> /etc/modules;
    fi;
    dtparam i2c_arm=on;
    modprobe i2c-dev;
  else
    echo "i2c is enabled";
  fi;
}

enable_i2c;
