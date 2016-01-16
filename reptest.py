# fill dag with repeatability test

import msg, standard
import re, os

runs = ['100', '101', '102']

def fillDAG (tag, dag, jobsub, xsec_a_path, outEv, outTest):
  fillDAGEv (tag, dag, jobsub, xsec_a_path, outEv)
  fillDAGTest (dag, jobsub, outEv, outTest)

def fillDAGEv (tag, dag, jobsub, xsec_a_path, out):
  # check if job is done already
  if isDoneEv (out):
    msg.warning ("Repeatability test events found in " + out + " ... " + msg.BOLD + "skipping reptest:fillDAGEv\n", 1)
    return
  msg.info ("\tAdding repeatability test (gevgen) jobs\n")
  # fill dag file with the same jobs with different run number in parallel mode
  print >>dag, "<parallel>"
  # loop over runs and generate proper command
  for run in runs:
    cmd = "gevgen -p 14 -t 1000260560 -e 0.1,50 -f '1/x' --seed 123456 -r " + run + \
          " --cross-sections input/gxspl-vA-" + tag + ".xml"
    cmd = re.sub (' ', "SPACE", cmd) # temporary solution as workaround for jobsub quotes issue
    cmd = re.sub ("\'", "SQUOTE", cmd) # temporary solution as workaround for jobsub quotes issue
    print >>dag, jobsub + " -i " + xsec_a_path + "/gxspl-vA-" + tag + ".xml -o " + out + \
                 " -l gevgen_" + run + ".log -c " + cmd
  # done
  print >>dag, "</parallel>"
  
def fillDAGTest (dag, jobsub, events, out):
  # check if job is done already
  if isDoneTest (out):
    msg.warning ("Repeatability test logs found in " + out + " ... " + msg.BOLD + "skipping reptest:fillDAGTest\n", 1)
    return
  msg.info ("\tAdding repeatability test (gvld) jobs\n")
  # fill dag file with repeatability test jobs in parallel mode
  print >>dag, "<parallel>"
  # loop over runs and generate proper command
  for run in runs[1:]:
    cmd = "gvld_repeatability_test --first-sample input/gntp." + runs[0] + ".ghep.root " + \
          " --second-sample input/gntp." + run + ".ghep.root " + \
          " --add-event-printout-in-error-log --max-num-of-errors-shown 10 " + \
          " -o reptest_runs" + runs[0] + "vs" + run + ".log"
    cmd = re.sub (' ', "SPACE", cmd) # temporary solution as workaround for jobsub quotes issue
    print >>dag, jobsub + " -i " + events + "/*.ghep.root -o " + out + \
                          " -l gvld_repeatability_test_" + runs[0] + "vs" + run + ".log -c " + cmd
  # done  
  print >>dag, "</parallel>"

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
