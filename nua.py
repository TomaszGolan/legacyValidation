# fill dag file with neutrino-nucleus cross section splines jobs

import msg
import re, os

nKnots    = "1000" # no. of knots for gmkspl
maxEnergy = "150"  # maximum energy for gmkspl

nuPDG = "12,-12,14,-14" # pdg of neutrinos to process

# targets to process
targets = ['1000010010',  # H1
           '1000000010',  # n
           '1000060120',  # C12
           '1000080160',  # O16
           '1000100200',  # Ne20
           '1000130270',  # Al27
           '1000140300',  # Si30
           '1000180380',  # Ar38
           '1000260560'   # Fe56
          ];
          
def fillDAG (jobsub, tag, paths):
  fillDAGPart (jobsub, tag, paths['xsec_N'], paths['xsec_A'])
  fillDAGMerge (jobsub, tag, paths['xsec_A'])
  
def fillDAGPart (jobsub, tag, xsec_n_path, out):
  # check if job is done already
  if isDonePart (tag, out):
    msg.warning ("Nucleus splines found in " + out + " ... " + msg.BOLD + "skipping nua:fillDAGPart\n", 1)
    return
  # not done, add jobs to dag
  msg.info ("\tAdding nucleus splines (part) jobs\n")
  # in parallel mode
  jobsub.add ("<parallel>")
  # common options
  inputFile = "gxspl-vN-" + tag + ".xml"
  inputs = xsec_n_path + "/*.xml"
  options = " --input-cross-sections input/" + inputFile
  # loop over targets and generate proper command
  for t in targets:
    outputFile = "gxspl_" + t + ".xml"
    cmd = "gmkspl -p " + nuPDG + " -t " + t + " -n " + nKnots + " -e " + maxEnergy + options + \
          " --output-cross-sections " + outputFile
    logFile = "gxspl_" + t + ".xml.log"
    jobsub.addJob (inputs, out, logFile, cmd)
  # done
  jobsub.add ("</parallel>")
  
def fillDAGMerge (jobsub, tag, out):
  # check if job is done already
  if isDoneMerge (tag, out):
    msg.warning ("Nucleus merged splines found in " + out + " ... " + msg.BOLD + "skipping nua:fillDAGMerge\n", 1)
    return
  # not done, add jobs to dag
  msg.info ("\tAdding nucleus splines (merge) jobs\n")
  # in serial mode
  jobsub.add ("<serial>")
  # common options
  xmlFile = "gxspl-vA-" + tag + ".xml"
  # merge splines job
  cmd = "gspladd -d input -o " + xmlFile
  inputs = out + "/*.xml"
  logFile = "gspladd.log"
  jobsub.addJob (inputs, out, logFile, cmd)
  # convert to root job
  rootFile = "xsec-vA-" + tag + ".root"
  cmd = "gspl2root -p " + nuPDG + " -t " + ",".join(targets) + " -o " + rootFile + " -f input/" + xmlFile
  inputs = out + "/" + xmlFile
  logFile = "gspl2root.log"
  jobsub.addJob (inputs, out, logFile, cmd)
  # done
  jobsub.add ("</serial>")

def isDonePart (tag, path):
  # check if given path contains all splines
  for t in targets:
    if "gxspl_" + t + ".xml" not in os.listdir (path): return False
  return True

def isDoneMerge (tag, path):
  if "gxspl-vA-" + tag + ".xml" not in os.listdir (path): return False
  if "xsec-vA-" + tag + ".root" not in os.listdir (path): return False
  return True
