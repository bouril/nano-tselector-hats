#!/usr/bin/env bash

# Use an LCG release for ROOT+python 3: http://lcginfo.cern.ch/release/94python3/
source /cvmfs/sft.cern.ch/lcg/views/LCG_94python3/x86_64-slc6-gcc62-opt/setup.sh

# forward all arguments to the driver script
./driver.py $@
