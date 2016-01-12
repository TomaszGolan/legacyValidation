#!/bin/bash

while getopts p:o:i:l:c: OPT
do
  case ${OPT} in
    p) # path to genie top dir
      export GENIE=$OPTARG
      ;;
    o) # output directory
      out=$OPTARG
      ;;
    i) # input files dir
      input=$OPTARG
      ;;
    l) # logfile name
      log=$OPTARG
      ;;
    c) # command to run
      cmd=`echo $OPTARG | sed 's/SPACE/ /g'`
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

source /cvmfs/fermilab.opensciencegrid.org/products/common/etc/setups.sh
setup ifdhc

### load input (if defined) ###

if [ -n "$input" ]; then ifdh cp -r $input input; fi

### run the command ###

$cmd 1>/dev/null 2>log

### copy results to scratch

mkdir scratch
mv *.root scratch
mv *.xml scratch
mv *.log scratch

### copy everything from scratch to output 

ifdh cp -r scratch $out

# example (problems with " eaten by jobsub...)
# jobsub_submit -G genie -M --OS=SL6 --resource-provides=usage_model=DEDICATED,OPPORTUNISTIC file://runGENIE.sh -p /grid/fermiapp/genie/builds/genie_R-2_9_0_buildmaster_2015-10-27/ -o /pnfs/genie/scratch/users/goran/ -c "gmkspl -p 12 -t 1000010010 -n 500 -e 500 -o scratch/pgxspl-qel.xml --event-generator-list QE"
# temporary solution: use SPACE instead of spaces
# jobsub_submit -G genie -M --OS=SL6 --resource-provides=usage_model=DEDICATED,OPPORTUNISTIC file://runGENIE.sh -p /grid/fermiapp/genie/builds/genie_R-2_9_0_buildmaster_2015-10-27/ -o /pnfs/genie/scratch/users/goran/ -c "gmksplSPACE-pSPACE12SPACE-tSPACE1000010010SPACE-nSPACE500SPACE-eSPACE500SPACE-oSPACEscratch/pgxspl-qel.xmlSPACE--event-generator-listSPACEQE"
