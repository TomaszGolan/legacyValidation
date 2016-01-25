# GENIE Legacy Validation

This is the translation of perl validation scripts (src/scripts/production/batch) from perl to python and from PBS batch system to jobsub client.

The main script, **runLegacyValidation.py**, handles other modules to prepare a proper dag file and submit it to the grid.

```
usage: ./runLegacyValidation.py <options>

GENIE Legacy Validation @ FERMILAB

optional arguments:
  -h, --help            show this help message and exit
  --build_date [YYYY-MM-DD]
                        if not defined the most recent build will be used
  --resource [GRID RESOURCE]
                        DEDICATED,OPPORTUNISTIC [default] or
                        DEDICATED,OPPORTUNISTIC,OFFSITE
  --group [GROUP]       default = genie
  --os [SYSTEM]         default = SL6
  --debug [false or true]
                        default = false

required arguments:
  --genie_tag [GENIE VERSION]
  --run_path [PATH TO RUNGENIE]
  --builds [PATH TO BUILDS]
  --output [PATH FOR OUTPUT]
```

The script prepares the configuration and output folders based on user options. It assumes the path to GENIE = *PATH TO BUILD / GENIE VERSION*.

User must provide the path to **runGENIE.sh** script, which is used to run custom GENIE command. It takes several arguments:

* -p [path to genie]
* -o [path for output files]
* -i [path to input files]
* -l [log file name]
* -d [true to run in debug mode]
* -c [command to run]

It handles all common steps of running GENIE on grid:

* set up ifdh client
* copy input files to **input** folder
* set up GENIE dependencies
* run given command
* copy output files to **PATH FOR OUTPUT** (somewhere in /pnfs)

