#! /usr/bin/env bash

# copy the setup.cfg file from the template
SETUP_CFG_FILE="setup.cfg";
cp template_setup.cfg $SETUP_CFG_FILE;

# read the build number
BUILD_NUMBER_FILE="build_number.txt";
BUILD_NUMBER=$(< $BUILD_NUMBER_FILE);

# edit the setup.cfg file to include the build number
perl -pi -e "s/%BUILD_NUMBER%/$BUILD_NUMBER/" "$SETUP_CFG_FILE";

# increment the version for the next run
BUILD_NUMBER=$(($BUILD_NUMBER + 1));
echo $BUILD_NUMBER > $BUILD_NUMBER_FILE;
git commit -m "build number increment" $BUILD_NUMBER_FILE;

# build, upload, and clean up (because the python build tools don't)
python3 -m build
python3 -m twine upload dist/*
rm -rf build dist setup.cfg
find . -type d -iname *.egg-info -print0 | xargs -0 -I {} rm -rf "{}"
