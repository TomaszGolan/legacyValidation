# command line parser for legacy validation (compare) @ FERMILAB

import argparse

def getArgs():
  parser = argparse.ArgumentParser (description = "GENIE Legacy Validation Comparisons @ FERMILAB",
                                    usage = "./compare.py <options>")

  required = parser.add_argument_group ("required arguments")
  required.add_argument ("--builds", action = "store", dest = "builds", metavar = "[PATH TO BUILDS]", required = True)
  required.add_argument ("--genie_tags", action = "store", dest = "tags", metavar = "['TAG1 TAG2...'']", required = True, help = "genie tags to compare")
  required.add_argument ("--genie_dates", action = "store", dest = "dates", metavar = "['DATE1 DATE2...']", required = True, help = "corresponding build dates")
  required.add_argument ("--top_dir", action = "store", dest = "topdir", metavar = "[PATH FOR LV RESULTS TOPDIR]", required = True)
  required.add_argument ("--comp_path", action = "store", dest = "run", metavar = "[PATH TO RUNCOMPARE]", required = True)

  return parser.parse_args()
