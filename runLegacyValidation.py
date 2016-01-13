#!/usr/bin/env python

# GENIE Legacy Validation based on src/scripts/production/batch

import parser, jenkins, msg, nun, nua, standard, reptest, xsecval
import os, datetime, subprocess

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
  # reports
  paths['reports']  = path + "/reports"
  paths['sanity']   = path + "/reports/sanity_mctest"
  paths['replog']   = path + "/reports/repeatability_test"
  paths['xseclog']  = path + "/reports/xsec_validation"
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
  buildName = jenkins.getBuild (args.tag, args.build_date, args.builds)
  # preapre folder structure for output
  paths = preparePaths (args.output + "/" + args.tag + "/" + args.build_date)
  # dag file
  dagFile = paths['top'] + "/legacyValidation-" + args.tag + "-" + args.build_date + ".dag"
  try: os.remove (dagFile)
  except OSError: pass
  dag = open (dagFile, 'w');
  # common jobsub command
  jobsub = "jobsub --OS=SL6 --resource-provides=usage_model=" + args.resource + " -G " + args.group + " file://" \
           + args.run + " -p " + args.builds + "/" + buildName
  # fill dag files with jobs
  msg.info ("Adding jobs to dag file: " + dagFile + "\n")
  nun.fillDAG (args.tag, dag, jobsub, paths['xsec_N'])                  # nucleon cross sections
  nua.fillDAG (args.tag, dag, jobsub, paths['xsec_N'], paths['xsec_A']) # nucleus cross sections
  standard.fillDAG (args.tag, dag, jobsub, paths['xsec_A'], paths['mctest'], paths['sanity'])  # standard mctest sanity
  reptest.fillDAG (args.tag, dag, jobsub, paths['xsec_A'], paths['reptest'], paths['replog'])  # repeatability test
  xsecval.fillDAG (args.tag, args.build_date, dag, jobsub, args.builds + "/" + buildName, paths['xsec_A'], paths['xsecval'], paths['xseclog']) # xsec validation
  # dag file done
  dag.close()
  msg.info ("Done with dag file. Ready to submit.\n")
  # run DAG
  if os.stat(dagFile).st_size == 0:
    msg.warning ("Dag file: " + dagFile + " is empty. " + msg.RED + msg.BOLD + "NO JOBS TO RUN!!!\n")
    exit (0)
  msg.info ("Submitting: " + dagFile + "\n")
  subprocess.Popen ("source /cvmfs/fermilab.opensciencegrid.org/products/common/etc/setups.sh; setup jobsub_client; " +
                    "jobsub_submit_dag -G " + args.group + " file://" + dagFile, shell=True, executable="/bin/bash")
