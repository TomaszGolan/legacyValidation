# run sanity checks on standard mctest output files

import msg, standard
import re, os

def fillDAG (dag, jobsub, mctest_path, out):
  # check if job is done already
  if isDone (out):
    msg.warning ("Standard mctest sanity checks log files found in " + out + " ... " + msg.BOLD + "skipping sanity:fillDAG\n")
    return
  msg.info ("\tAdding mctest sanity checks jobs\n")
  # fill dag file with sanity check jobs in parallel mode
  print >>dag, "<parallel>"
  # loop over keys and generate proper command
  for key in standard.nuPDG.iterkeys():
    cmd = "gvld_sample_scan -f input/gntp." + key + ".ghep.root -o gntp." + key + ".ghep.root.sanity.log " + \
          "--add-event-printout-in-error-log --event-record-print-level 2 --max-num-of-errors-shown 10 " + \
          "--check-energy-momentum-conservation " + \
          "--check-charge-conservation " + \
          "--check-for-pseudoparticles-in-final-state " + \
          "--check-for-off-mass-shell-particles-in-final-state " + \
          "--check-for-num-of-final-state-nucleons-inconsistent-with-target " + \
          "--check-vertex-distribution " + \
          "--check-decayer-consistency"
    cmd = re.sub (' ', "SPACE", cmd) # temporary solution as workaround for jobsub quotes issue
    print >>dag, jobsub + " -i " + mctest_path + " -o " + out + " -l gvld_sample_scan." + key + ".log -c " + cmd
  # done
  print >>dag, "</parallel>"

def isDone (path):
  # check if given path contains all log files
  for key in standard.nuPDG.iterkeys():
    if "gntp." + key + ".ghep.root.sanity.log" not in os.listdir (path): return False
  return True
