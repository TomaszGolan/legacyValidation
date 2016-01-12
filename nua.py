# fill dag file with neutrino-nucleus cross section splines jobs

import msg
import re, os

nKnots    = "1000" # no. of knots for gmkspl
maxEnergy = "150"  # maximum energy for gmkspl

nuPDG = "12,-12,14,-14" # pdg of neutrinos to process

# targets to process
targets = ['1000060120',  # C12
           '1000080160',  # O16
           '1000100200',  # Ne20
           '1000130270',  # Al27
           '1000140300',  # Si30
           '1000180380',  # Ar38
           '1000260560'   # Fe56
          ];

def fillDAG (tag, dag, jobsub, xsec_n_path, out):
  # check if job is done already
  if isDone (tag, out):
    msg.warning ("Nucleus splines found in " + out + " ... " + msg.BOLD + "skipping nua:fillDAG\n")
    return
  # fill dag file with xsec-nucleus jobs in parallel mode
  print >>dag, "<parallel>"
  # loop over targets and generate proper command
  for t in targets:
    cmd = "gmkspl -p " + nuPDG + " -t " + t + " -n " + nKnots + " -e " + maxEnergy + \
          " --input-cross-sections input/gxspl-vN-" + tag + ".xml --output-cross-sections gxspl_" + t + ".xml"
    cmd = re.sub (' ', "SPACE", cmd) # temporary solution as workaround for jobsub quotes issue
    print >>dag, jobsub + " -i " + xsec_n_path + " -o " + out + " -l gxspl_" + t + ".xml.log -c " + cmd
  # done
  print >>dag, "</parallel>"
  # fill dag file with splines add job
  print >>dag, "<serial>"
  cmd = "gspladd -d input -o gxspl-vA-" + tag + ".xml"  
  cmd = re.sub (' ', "SPACE", cmd) # temporary solution as workaround for jobsub quotes issue
  print >>dag, jobsub + " -i " + out + " -o " + out + " -l gspladd.log -c " + cmd
  print >>dag, "</serial>"
  # done

def isDone (tag, path):
  # check if given path contains all splines
  for t in targets:
    if "gxspl_" + t + ".xml" not in os.listdir (path): return False
  return True
