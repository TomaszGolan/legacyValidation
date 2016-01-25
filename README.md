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
  --output ['PATH FOR OUTPUT]']
```
