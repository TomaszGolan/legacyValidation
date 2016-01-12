# command line parser for legacy validation @ FERMILAB

import argparse

def getArgs():
  parser = argparse.ArgumentParser (description = "GENIE Legacy Validation @ FERMILAB",
                                    usage = "./runLegacyValidation.py <options>")

  parser.add_argument ("--build_date", action = "store", dest = "build_date", metavar = "[YYYY-MM-DD]",
                       help = "if not defined the most recent build will be used")
  parser.add_argument ("--resource", action = "store", dest = "resource", metavar = "[GRID RESOURCE]",
                       default = "DEDICATED,OPPORTUNISTIC",
                       help = "DEDICATED,OPPORTUNISTIC [default] or DEDICATED,OPPORTUNISTIC,OFFSITE")
  parser.add_argument ("--group", action = "store", dest = "group", metavar = "[GROUP]", default = "genie",
                       help = "default = genie")

  required = parser.add_argument_group ("required arguments")
  required.add_argument ("--genie_tag", action = "store", dest = "tag", metavar = "[GENIE VERSION]", required = True)
  required.add_argument ("--run_path", action = "store", dest = "run", metavar = "[PATH TO RUNGENIE]", required = True)
  required.add_argument ("--builds", action = "store", dest = "builds", metavar = "[PATH TO BUILDS]", required = True)
  required.add_argument ("--output", action = "store", dest = "output", metavar = ["PATH FOR OUTPUT]"], required = True)

  # giving up this idea for now, script will look for previous results automatically 
  #~ previous = parser.add_argument_group ("previous results (will skip steps if provided)")
  #~ previous.add_argument ("--nucleon_splines", action = "store", dest = "xsec_n", metavar = "[PATH]",
                         #~ help = "path to nu-N splines")
  #~ previous.add_argument ("--nucleus_splines", action = "store", dest = "xsec_a", metavar = "[PATH]",
                         #~ help = "path to nu-A splines")
  #~ previous.add_argument ("--mctest", action = "store", dest = "mctest", metavar = "[PATH]",
                         #~ help = "path to standard mctest output")
  #~ previous.add_argument ("--sanity", action = "store", dest = "sanity", metavar = "[PATH]",
                         #~ help = "path to standard mctest sanity logs")

  return parser.parse_args()
