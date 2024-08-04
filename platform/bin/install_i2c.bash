#! /usr/bin/env bash

# enable i2c - code loosely based on raspi-config
echo "Enabling I2C";

CONFIG="/boot/firmware/config.txt";
sed -i -e "s/.*dtparam=i2c_arm=.*/dtparam=i2c_arm=on/" "$CONFIG";
I2C_CONFIG=$(grep "dtparam=i2c_arm" "$CONFIG");
if [ -z "$I2C_CONFIG" ]; then
    echo "dtparam=i2c_arm=on" >> "$CONFIG";
fi;
dtparam i2c_arm=on

# this shouldn't be necessary
#sed -i -e "s/.*dtparam=ii2c_arm_baudrate=.*/dtparam=i2c_arm_baudrate=10000/" "$CONFIG";
#I2C_BAUD=$(grep "dtparam=i2c_arm_baudrate=10000" "$CONFIG");
#if [ -z "$I2C_BAUD" ]; then
#    echo "dtparam=i2c_arm_baudrate=10000" >> "$CONFIG";
#fi;
#dtparam i2c_arm_baudrate=10000

MODULES="/etc/modules";
sed -i -e "s/^#[[:space:]]*\(i2c[-_]dev\)/\1/" "$MODULES";
I2C_MODULES=$(grep -q "^i2c[-_]dev" "$MODULES");
if [ -z "$I2C_MODULES" ]; then
    echo "i2c-dev" >> "$MODULES"
fi;

modprobe i2c-dev
