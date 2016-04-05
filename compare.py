#!/usr/bin/env python

# GENIE Legacy Validation Comparisons based on src/scripts/production/batch

import parser_comp, msg, xsec_comp, had_comp
import os, sys, datetime, subprocess

def check (args):
  args.tags = args.tags.split()
  args.dates = args.dates.split()
  args.path = args.builds + "/genie_" + args.tags[0] + "_buildmaster_" + args.dates[0]
  args.out = "./comparisons/"

  if len(args.tags) != len(args.dates):
    print msg.RED
    print "ERROR: #tags != #dates"
    print msg.END
    sys.exit(1)

def initMessage (args):
  print msg.BLUE
  print '*' * 92
  print '*', ' ' * 88, '*'
  print "*\tGENIE Legacy Validation Comparisons based on src/scripts/production/batch", ' ' * 8, '*'
  print '*', ' ' * 88, '*'
  print '*' * 92
  print msg.GREEN
  check(args)
  print "Configuration:\n"
  print "\tGENIE results to compare:"
  for i in range(len(args.tags)):
    print "\t\t", args.tags[i], "(", args.dates[i], ")"
    print "\t\tfrom:", args.topdir + "/" + args.tags[i] + "/" + args.dates[i], "\n"
  print "\tValidation apps will be called from:", args.path
  print "\tResults will be saved in:", args.out
  print msg.END

if __name__ == "__main__":
  # parse command line arguments
  args = parser_comp.getArgs()
  # print configuration summary
  initMessage (args)
  # create directory for output
  if not os.path.exists (args.out): os.makedirs (args.out)
  # create filelist for xsec comparisons
  xsec_list = xsec_comp.createFileList(args)
  xsec_output = args.out + "/xsec_comp-"
  for i in range(len(args.tags)):
    xsec_output += args.tags[i] + "_" + args.dates[i]
    if i + 1 != len(args.tags): xsec_output += "_vs_"
  command = "bash " + args.run + " -c gvld_nu_xsec -p " + args.path + " -f " + xsec_list + " -o " + xsec_output
  subprocess.Popen (command, shell=True, executable="/bin/bash")
  # create hadronization comparisons
  had_list = had_comp.createFileList(args)
  had_output = args.out + "/xsec_comp-"
  for i in range(len(args.tags)):
    had_output += args.tags[i] + "_" + args.dates[i]
    if i + 1 != len(args.tags): had_output += "_vs_"
  command = "bash " + args.run + " -c gvld_hadronz_test -p " + args.path + " -f " + had_list + " -o " + had_output
  subprocess.Popen (command, shell=True, executable="/bin/bash")
