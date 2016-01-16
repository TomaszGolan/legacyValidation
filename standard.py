# fill dag with standard neutrino event generation jobs 

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

def fillDAG (jobsub, tag, paths):
  fillDAG_GHEP (jobsub, tag, paths['xsec_A'], paths['mctest'])
  fillDAG_GST (jobsub, paths['mctest'])
  fillDAG_sanity (jobsub, paths['mctest'], paths['sanity'])
  
def fillDAG_GHEP (jobsub, tag, xsec_a_path, out):
  # check if job is done already
  if isDoneGHEP (out):
    msg.warning ("Standard mctest ghep files found in " + out + " ... " + msg.BOLD + "skipping standard:fillDAG_GHEP\n", 1)
    return
  # not done, add jobs to dag
  msg.info ("\tAdding standard mctest (ghep) jobs\n")
  # in parallel mode
  jobsub.add ("<parallel>")
  inputFile = "gxspl-vA-" + tag + ".xml"
  options = " --seed " + mcseed + " --cross-sections input/" + inputFile
  # loop over keys and generate gevgen command
  for key in nuPDG.iterkeys():
    cmd = "gevgen -n " + nEvents[key] + " -e " + energy[key] + " -p " + nuPDG[key] + " -t " + targetPDG[key] + \
          " -r " + key + " --event-generator-list " + generatorList[key] + options
    logFile = "gevgen_" + key + ".log"
    jobsub.addJob (xsec_a_path + "/" + inputFile, out, logFile, cmd)
  # done
  jobsub.add ("</parallel>")

def fillDAG_GST (jobsub, out):
  # check if job is done already
  if isDoneGST (out):
    msg.warning ("Standard mctest gst files found in " + out + " ... " + msg.BOLD + "skipping standard:fillDAG_GST\n", 1)
    return
  # not done, add jobs to dag
  msg.info ("\tAdding standard mctest (gst) jobs\n")
  # in parallel mode
  jobsub.add ("<parallel>")
  # loop over keys and generate proper command
  for key in nuPDG.iterkeys():
    inputFile = "gntp." + key + ".ghep.root"
    cmd = "gntpc -f gst -i input/" + inputFile
    logFile = "gntpc" + key + ".log"
    jobsub.addJob (out + "/" + inputFile, out, logFile, cmd)
  # done
  jobsub.add ("</parallel>")

def fillDAG_sanity (jobsub, events, out):
  # check if job is done already
  if isDoneSanity (out):
    msg.warning ("Standard mctest sanity checks log files found in " + out + " ... " + msg.BOLD + \
                 "skipping standard:fillDAG_sanity\n", 1)
    return
  # not done, add jobs to dag
  msg.info ("\tAdding mctest sanity checks jobs\n")
  # in parallel mode
  jobsub.add ("<parallel>")
  options = " --add-event-printout-in-error-log --event-record-print-level 2 --max-num-of-errors-shown 10 " + \
            " --check-energy-momentum-conservation " + \
            " --check-charge-conservation " + \
            " --check-for-pseudoparticles-in-final-state " + \
            " --check-for-off-mass-shell-particles-in-final-state " + \
            " --check-for-num-of-final-state-nucleons-inconsistent-with-target " + \
            " --check-vertex-distribution " + \
            " --check-decayer-consistency"
  # loop over keys and generate gvld_sample_scan command
  for key in nuPDG.iterkeys():
    inputFile = "gntp." + key + ".ghep.root"
    output = "gntp." + key + ".ghep.root.sanity.log"
    cmd = "gvld_sample_scan -f input/" + inputFile + " -o " + output + options
    logFile = "gvld_sample_scan." + key + ".log"
    jobsub.addJob (events + "/" + inputFile, out, logFile, cmd)
  # done
  jobsub.add ("</parallel>")

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

def isDoneSanity (path):
  # check if given path contains all log files
  for key in nuPDG.iterkeys():
    if "gntp." + key + ".ghep.root.sanity.log" not in os.listdir (path): return False
  return True
