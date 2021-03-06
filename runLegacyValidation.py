#!/usr/bin/env python

# GENIE Legacy Validation based on src/scripts/production/batch

from jobsub import Jobsub
import parser, jenkins, msg, nun, nua, standard, reptest, xsecval, hadronization
import os, datetime

def initMessage (args):
  print msg.BLUE
  print '*' * 80
  print '*', ' ' * 76, '*'
  print "*\tGENIE Legacy Validation based on src/scripts/production/batch", ' ' * 8, '*'
  print '*', ' ' * 76, '*'
  print '*' * 80
  print msg.GREEN
  print "Configuration:\n"
  print "\tGENIE version:\t", args.tag
  print "\tBuild on:\t", args.build_date
  print "\tLocated at:\t", args.builds
  print "\n\tResults folder:", args.output
  print msg.END

def preparePaths (path):
  # create a dictionary for output paths
  paths = {}
  paths['top'] = path
  # splines
  paths['xsec']   = path + "/xsec"
  paths['xsec_N'] = path + "/xsec/nuN"
  paths['xsec_A'] = path + "/xsec/nuA"
  # events
  paths['events']  = path + "/events"
  paths['mctest']  = path + "/events/mctest"
  paths['reptest'] = path + "/events/repeatability"
  paths['xsecval'] = path + "/events/xsec_validation"
  paths['hadron']  = path + "/events/hadronization"
  # reports
  paths['reports'] = path + "/reports"
  paths['sanity']  = path + "/reports/sanity_mctest"
  paths['replog']  = path + "/reports/repeatability_test"
  paths['xseclog'] = path + "/reports/xsec_validation"
  paths['xsecsng'] = path + "/reports/xsec_validation/single_comparisons_with_errors"
  paths['hadrep']  = path + "/reports/hadronization_test"
  # create all directiories
  for p in paths.values():
    if not os.path.exists (p): os.makedirs (p)
  # return paths dictionary
  return paths
    
if __name__ == "__main__":
  # parse command line arguments
  args = parser.getArgs()
  # find most recent build if date was not defined
  if args.build_date is None: args.build_date = jenkins.findLast (args.tag)
  # print configuration summary
  initMessage (args)
  # get build
  msg.info ("Getting GENIE from jenkins...\n")
  args.buildName = jenkins.getBuild (args.tag, args.build_date, args.builds)
  # preapre folder structure for output
  args.paths = preparePaths (args.output + "/" + args.tag + "/" + args.build_date)
  # initialize jobsub
  jobsub = Jobsub (args)
  # fill dag files with jobs
  msg.info ("Adding jobs to dag file: " + jobsub.dagFile + "\n")
  # nucleon cross sections
  nun.fillDAG (jobsub, args.tag, args.paths)
  # nucleus cross sections
  nua.fillDAG (jobsub, args.tag, args.paths)
  # standard mctest sanity
  standard.fillDAG (jobsub, args.tag, args.paths)
  # repeatability test
  reptest.fillDAG (jobsub, args.tag, args.paths)
  # xsec validation
  xsecval.fillDAG (jobsub, args.tag, args.build_date, args.paths)
  # hadronization test
  hadronization.fillDAG (jobsub, args.tag, args.build_date, args.paths)
  # dag file done, submit jobs
  jobsub.submit()
