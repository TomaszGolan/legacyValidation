#!/bin/bash

while getopts p:f:o:c: OPT
do
  case ${OPT} in
    p) # path to genie top dir
      export GENIE=$OPTARG
      ;;
    f) # xml filelist
      xml=$OPTARG
      ;;
    o) # output
      out=$OPTARG
      ;;
    c) # command to run
      com=$OPTARG
      ;;
  esac
done

### setup externals and paths ###

export GUPSBASE=/cvmfs/fermilab.opensciencegrid.org/

source $GUPSBASE/products/genie/externals/setup

setup root v5_34_25a -q debug:e7:nu
setup lhapdf v5_9_1b -q debug:e7
setup log4cpp v1_1_1b -q debug:e7

export LD_LIBRARY_PATH=$GENIE/lib:$LD_LIBRARY_PATH
export PATH=$GENIE/bin:$PATH

$com -g $xml -o $out
