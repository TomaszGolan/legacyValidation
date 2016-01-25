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
* in debug mode the whole output is copied to the log file (otherwise only errors)

In the first step, proper GENIE version (given by **GENIE VERSION TAG**) is downloaded from buildmaster to **PATH TO BUILDS** (unless given build already exists), using **jenkins.py**. If user does not provide the date of build the most recent is used. 

**jobsub.py** is initialized according to user options. It handles a dag file and provides an easy way to add new jobs. Because of quotes issue in jobsub client (it eats all quotes), all spaces in the command are replaced by SPACE. **runGENIE.sh** replace SPACE back to ' '.

The rest of modules are dedicated for different validation tests. Each one has similar structure - fill dag file with proper GENIE command using **jobsub.py** (unless results already exist - then skip the step).

* nun.py - neutrino-nucleon cross section splines
* nua.py - neutrino-nucleus cross section splines
* standard.py - basic sanity checks (conservation laws etc)
* reptest.py - repeatability test
* xsecval.py - compare GENIE predictions with data
* hadronization.py - hadronization test (comparing with data)


