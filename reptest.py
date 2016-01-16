# fill dag with repeatability test

import msg, standard
import re, os

runs = ['100', '101', '102']

def fillDAG (jobsub, tag, paths):
  fillDAGEv (jobsub, tag, paths['xsec_A'], paths['reptest'])
  fillDAGTest (jobsub, paths['reptest'], paths['replog'])

def fillDAGEv (jobsub, tag, xsec_a_path, out):
  # check if job is done already
  if isDoneEv (out):
    msg.warning ("Repeatability test events found in " + out + " ... " + msg.BOLD + "skipping reptest:fillDAGEv\n", 1)
    return
  # not done, add jobs to dag
  msg.info ("\tAdding repeatability test (gevgen) jobs\n")
  # in parallel mode
  jobsub.add ("<parallel>")
  # loop over runs and generate gevgen command
  inputFile = "gxspl-vA-" + tag + ".xml"
  options = " -p 14 -t 1000260560 -e 0.1,50 -f '1/x' --seed 123456 --cross-sections input/" + inputFile
  for run in runs:
    cmd = "gevgen " + options + " -r " + run
    logFile = "gevgen_" + run + ".log"
    jobsub.addJob (xsec_a_path + "/" + inputFile, out, logFile, cmd)
  # done
  jobsub.add ("</parallel>")
  
def fillDAGTest (jobsub, events, out):
  # check if job is done already
  if isDoneTest (out):
    msg.warning ("Repeatability test logs found in " + out + " ... " + msg.BOLD + "skipping reptest:fillDAGTest\n", 1)
    return
  # not done, add jobs to dag
  msg.info ("\tAdding repeatability test (gvld) jobs\n")
  # in parallel mode
  jobsub.add ("<parallel>")
  # loop over runs and generate proper command
  options = " --add-event-printout-in-error-log --max-num-of-errors-shown 10 "
  input1 = "gntp." + runs[0] + ".ghep.root" 
  for run in runs[1:]:
    input2 = "gntp." + run + ".ghep.root"
    output = "reptest_runs" + runs[0] + "vs" + run + ".log"
    logFile = "gvld_repeatability_test_" + runs[0] + "vs" + run + ".log"
    cmd = "gvld_repeatability_test --first-sample input/" + input1 + \
          " --second-sample input/" + input2 + options + " -o " + output
    jobsub.addJob (events + "/*.ghep.root", out, logFile, cmd)
  # done  
  jobsub.add ("</parallel>")

def isDoneEv (path):
  # check if given path contains all root files
  for run in runs:
    if "gntp." + run + ".ghep.root" not in os.listdir (path): return False
  return True

def isDoneTest (path):
  return True # gvld_repeatability_test is missing, skip this step for now
  # check if given path contains all log files
  for run in runs[1:]:
    if "reptest_runs" + runs[0] + "vs" + run + ".log"  not in os.listdir (path): return False
  return True
