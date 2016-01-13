# fill dag with neutrino xsec validation jobs

import msg
import re, os

nuPDG = {
  '1000' :  '14',
  '1100' :  '14',
  '1200' : '-14',
  '1300' : '-14',
  '2010' :  '14'}
  
targetPDG = { 
  '1000' : '1000000010',
  '1100' : '1000010010',
  '1200' : '1000000010',
  '1300' : '1000010010',
  '2010' : '1000060120'}

mcseed = "210921029"
nEvents = "100000"
energy = "0.1,120.0"  
generatorList = "Default"
flux = "-f '1/x'"

def fillDAG (tag, dag, jobsub, xsec_a_path, outEvent, outRep):
  fillDAG_GHEP (tag, dag, jobsub, xsec_a_path, outEvent)
  fillDAG_GST (dag, jobsub, outEvent)

def fillDAG_GHEP (tag, dag, jobsub, xsec_a_path, out):
  # check if job is done already
  if isDoneGHEP (out):
    msg.warning ("xsec validation ghep files found in " + out + " ... " + msg.BOLD + "skipping xsecval:fillDAG_GHEP\n")
    return
  msg.info ("\tAdding xsec validation (ghep) jobs\n")
  # fill dag file with gevgen jobs in parallel mode
  print >>dag, "<parallel>"
  # loop over keys and generate proper command
  for key in nuPDG.iterkeys():
    cmd = "gevgen -n " + nEvents + " -e " + energy + " -p " + nuPDG[key] + flux + " -t " + targetPDG[key] + \
          " -r " + key + " --seed " + mcseed + " --cross-sections input/gxspl-vA-" + tag + ".xml" + \
          " --event-generator-list " + generatorList
    cmd = re.sub (' ', "SPACE", cmd) # temporary solution as workaround for jobsub quotes issue
    print >>dag, jobsub + " -i " + xsec_a_path + " -o " + out + " -l gevgen_" + key + ".log -c " + cmd
  # done
  print >>dag, "</parallel>"

def fillDAG_GST (dag, jobsub, out):
  # check if job is done already
  if isDoneGST (out):
    msg.warning ("xsec validation gst files found in " + out + " ... " + msg.BOLD + "skipping xsecval:fillDAG_GST\n")
    return
  msg.info ("\tAdding xsec validation (gst) jobs\n")
  # fill dag file with gntpc jobs in parallel mode
  print >>dag, "<parallel>"
  # loop over keys and generate proper command
  for key in nuPDG.iterkeys():
    cmd = "gntpc -f gst -i input/gntp." + key + ".ghep.root"
    cmd = re.sub (' ', "SPACE", cmd) # temporary solution as workaround for jobsub quotes issue
    print >>dag, jobsub + " -i " + out + " -o " + out + " -l gntpc" + key + ".log -c " + cmd
  # done
  print >>dag, "</parallel>"

def isDoneGHEP (path):
  # check if given path contains all ghep files
  for key in nuPDG.iterkeys():
    if "gntp." + key + ".ghep.root" not in os.listdir (path): return False
  return True
  
def isDoneGST (path):
  # check if given path contains all gst files
  for key in nuPDG.iterkeys():
    if "gntp." + key + ".gst.root" not in os.listdir (path): return False
  return True
