#! /usr/bin/env bash

# enable spi - code adapted from raspi-config
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

get_spi() {
  if grep -q -E "^(device_tree_param|dtparam)=([^,]*,)*spi(=(on|true|yes|1))?(,.*)?$" $CONFIG; then
    echo 1;
  else
    echo 0;
  fi;
}

enable_spi() {
  if [ "$(get_spi)" -eq 0 ]; then
    echo "enabling spi...";
    set_config_var dtparam=spi on $CONFIG;
    if ! [ -e $BLACKLIST ]; then
      touch $BLACKLIST
    fi;
    sed $BLACKLIST -i -e "s/^\(blacklist[[:space:]]*spi[-_]bcm2708\)/#\1/"
    dtparam spi=on
  else
    echo "spi is enabled";
  fi;
}

enable_spi;
