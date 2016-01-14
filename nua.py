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
          
def fillDAG (tag, dag, jobsub, xsec_n_path, out):
  fillDAGPart (tag, dag, jobsub, xsec_n_path, out)
  fillDAGMerge (tag, dag, jobsub, out)
  
def fillDAGPart (tag, dag, jobsub, xsec_n_path, out):
  # check if job is done already
  if isDonePart (tag, out):
    msg.warning ("Nucleus splines found in " + out + " ... " + msg.BOLD + "skipping nua:fillDAGPart\n", 1)
    return
  msg.info ("\tAdding nucleus splines (part) jobs\n")
  # fill dag file with xsec-nucleus jobs in parallel mode
  print >>dag, "<parallel>"
  # loop over targets and generate proper command
  for t in targets:
    cmd = "gmkspl -p " + nuPDG + " -t " + t + " -n " + nKnots + " -e " + maxEnergy + \
          " --input-cross-sections input/gxspl-vN-" + tag + ".xml --output-cross-sections gxspl_" + t + ".xml"
    cmd = re.sub (' ', "SPACE", cmd) # temporary solution as workaround for jobsub quotes issue
    print >>dag, jobsub + " -x " + xsec_n_path + " -o " + out + " -l gxspl_" + t + ".xml.log -c " + cmd
  # done
  print >>dag, "</parallel>"
  
def fillDAGMerge (tag, dag, jobsub, out):
  # check if job is done already
  if isDoneMerge (tag, out):
    msg.warning ("Nucleus merged splines found in " + out + " ... " + msg.BOLD + "skipping nua:fillDAGMerge\n", 1)
    return
  msg.info ("\tAdding nucleus splines (merge) jobs\n")
  # fill dag file with splines add and 2root jobs in serial mode
  print >>dag, "<serial>"
  # merge splines job
  cmd = "gspladd -d input -o gxspl-vA-" + tag + ".xml"  
  cmd = re.sub (' ', "SPACE", cmd) # temporary solution as workaround for jobsub quotes issue
  print >>dag, jobsub + " -x " + out + " -o " + out + " -l gspladd.log -c " + cmd
  # convert to root job
  cmd = "gspl2root -p " + nuPDG + " -t " + ",".join(targets) + " -o xsec-vA-" + tag + ".root " + \
        "-f input/gxspl-vA-" + tag + ".xml"
  cmd = re.sub (' ', "SPACE", cmd) # temporary solution as workaround for jobsub quotes issue
  print >>dag, jobsub + " -s " + out + "/gxspl-vA-" + tag + ".xml -o " + out + " -l gspladd.log -c " + cmd
  # done
  print >>dag, "</serial>"

def isDonePart (tag, path):
  # check if given path contains all splines
  for t in targets:
    if "gxspl_" + t + ".xml" not in os.listdir (path): return False
  return True

def isDoneMerge (tag, path):
  if "gxspl-vA-" + tag + ".xml" not in os.listdir (path): return False
  if "xsec-vA-" + tag + ".root" not in os.listdir (path): return False
  return True
