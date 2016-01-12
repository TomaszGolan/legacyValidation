# fill dag with standard neutrino event generation jobs for GENIE release validation

import msg
import re, os

mcseed = '210921029'

# number of events to generate for each job
nEvents = { 
  '1000' : '100000',
  '1001' : '100000',
  '1002' : '100000',
  '1003' : '100000',
  '1101' : '100000',
  '1102' : '100000',
  '1103' : '100000',
  '2001' : '100000',
  '2002' : '100000',
  '2003' : '100000',
  '2101' : '100000',
  '2102' : '100000',
  '2103' : '100000',
  '9001' : '100000',
  '9002' : '100000',
  '9101' : '100000',
  '9201' :  '50000',
  '9202' :  '50000',
  '9203' :  '50000',  
  '9204' :  '50000'}

# neutrino pdg for each job
nuPDG = { 
  '1000' :  '14',
  '1001' :  '14',
  '1002' :  '14',
  '1003' :  '14',
  '1101' : '-14',
  '1102' : '-14',
  '1103' : '-14',
  '2001' :  '14',
  '2002' :  '14',
  '2003' :  '14',
  '2101' : '-14',
  '2102' : '-14',
  '2103' : '-14',
  '9001' :  '14',
  '9002' :  '14',
  '9101' :  '14',
  '9201' :  '12',
  '9202' :  '14',
  '9203' :  '14',  
  '9204' :  '-12'}

# target pdf for each job
targetPDG = { 
  '1000' : '1000000010',
  '1001' : '1000000010',
  '1002' : '1000000010',
  '1003' : '1000000010',
  '1101' : '1000010010',
  '1102' : '1000010010',
  '1103' : '1000010010',
  '2001' : '1000260560',
  '2002' : '1000260560',
  '2003' : '1000260560',
  '2101' : '1000260560',
  '2102' : '1000260560',
  '2103' : '1000260560',
  '9001' : '1000260560',
  '9002' : '1000260560',
  '9101' : '1000260560',
  '9201' : '1000260560',
  '9202' : '1000260560',
  '9203' : '1000260560', 
  '9204' : '1000260560'}

# neutrino energy for each job
energy = { 
  '1000' :  '0.5',
  '1001' :  '1.0',
  '1002' :  '5.0',
  '1003' : '50.0',
  '1101' :  '1.0',
  '1102' :  '5.0',
  '1103' : '50.0',
  '2001' :  '1.0',
  '2002' :  '5.0',
  '2003' : '50.0',
  '2101' :  '1.0',
  '2102' :  '5.0',
  '2103' : '50.0',
  '9001' :  '5.0',
  '9002' :  '5.0',
  '9101' :  '2.0',
  '9201' :  '1.0',
  '9202' :  '1.0',
  '9203' : '20.0',
  '9204' : '20.0'}

# event generator list for each job
generatorList = { 
  '1000' : 'Default',
  '1001' : 'Default',
  '1002' : 'Default',
  '1003' : 'Default',
  '1101' : 'Default',
  '1102' : 'Default',
  '1103' : 'Default',
  '2001' : 'Default',
  '2002' : 'Default',
  '2003' : 'Default',
  '2101' : 'Default',
  '2102' : 'Default',
  '2103' : 'Default',
  '9001' : 'CharmCCDIS',
  '9002' : 'CharmCCQE',
  '9101' : 'COH',
  '9201' : 'NuEElastic',
  '9202' : 'NuEElastic',
  '9203' : 'IMD',
  '9204' : 'IMD'}

def fillDAG (tag, dag, jobsub, xsec_a_path, out):
  # check if job is done already
  if isDone (out):
    msg.warning ("Standard mctest root files found in " + out + " ... " + msg.BOLD + "skipping standard:fillDAG\n")
    return
  msg.info ("\tAdding standard mctest jobs\n")
  # fill dag file with gevgen jobs in parallel mode
  print >>dag, "<parallel>"
  # loop over keys and generate proper command
  for key in nuPDG.iterkeys():
    cmd = "gevgen -n " + nEvents[key] + " -e " + energy[key] + " -p " + nuPDG[key] + " -t " + targetPDG[key] + \
          " -r " + key + " --seed " + mcseed + " --cross-sections input/gxspl-vA-" + tag + ".xml" + \
          " --event-generator-list " + generatorList[key]
    cmd = re.sub (' ', "SPACE", cmd) # temporary solution as workaround for jobsub quotes issue
    print >>dag, jobsub + " -i " + xsec_a_path + " -o " + out + " -l gevgen_" + key + ".log -c " + cmd
  # done
  print >>dag, "</parallel>"
  # fill dag file with gntps jobs in parallel mode
  print >>dag, "<parallel>"
  # loop over keys and generate proper command
  for key in nuPDG.iterkeys():
    cmd = "gntpc -f gst -i input/gntp." + key + ".ghep.root"
    cmd = re.sub (' ', "SPACE", cmd) # temporary solution as workaround for jobsub quotes issue
    print >>dag, jobsub + " -i " + out + " -o " + out + " -l gntpc" + key + ".log -c " + cmd
  # done
  print >>dag, "</parallel>"

def isDone (path):
  # check if given path contains all root files
  for key in nuPDG.iterkeys():
    if "gntp." + key + ".ghep.root" not in os.listdir (path): return False
    if "gntp." + key + ".gst.root" not in os.listdir (path): return False
  return True