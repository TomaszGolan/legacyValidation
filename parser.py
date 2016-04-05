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
  parser.add_argument ("--os", action = "store", dest = "os", metavar = "[SYSTEM]", default = "SL6",
                       help = "default = SL6")
  parser.add_argument ("--debug", action = "store", dest = "debug", metavar = "[false or true]", default = "false",
                       help = "default = false")

  required = parser.add_argument_group ("required arguments")
  required.add_argument ("--genie_tag", action = "store", dest = "tag", metavar = "[GENIE VERSION]", required = True)
  required.add_argument ("--run_path", action = "store", dest = "run", metavar = "[PATH TO RUNGENIE]", required = True)
  required.add_argument ("--builds", action = "store", dest = "builds", metavar = "[PATH TO BUILDS]", required = True)
  required.add_argument ("--output", action = "store", dest = "output", metavar = ["PATH FOR OUTPUT]"], required = True)

  return parser.parse_args()
