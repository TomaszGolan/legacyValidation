# fill dag with hadronization test jobs

import msg
import os

nuPDG = {
  '1000' :  '14',
  '1100' :  '14',
  '1200' : '-14',
  '1300' : '-14'}
  
targetPDG = { 
  '1000' : '1000000010',
  '1100' : '1000010010',
  '1200' : '1000000010',
  '1300' : '1000010010'}

mcseed = "210921029"
nEvents = "100000"
energy = "0.5,80.0"  
generatorList = "HadronizationTest"
flux = "1/x"

def fillDAG (jobsub, tag, date, paths):
  fillDAG_GHEP (jobsub, tag, paths['xsec_N'], paths['hadron'])
  fillDAG_GST (jobsub, paths['hadron'])
  createFileList (tag, date, paths['xsec_N'], paths['hadron'], paths['hadrep'])
  fillDAG_data (jobsub, tag, date, paths['xsec_N'], paths['hadron'], paths['hadrep'])

def fillDAG_GHEP (jobsub, tag, xsec_n_path, out):
  # check if job is done already
  if isDoneGHEP (out):
    msg.warning ("hadornization test ghep files found in " + out + " ... " + msg.BOLD + "skipping hadronization:fillDAG_GHEP\n", 1)
    return
  #not done, add jobs to dag
  msg.info ("\tAdding hadronization test (ghep) jobs\n")
  # in parallel mode
  jobsub.add ("<parallel>")
  # common configuration
  inputFile = "gxspl-vN-" + tag + ".xml"
  options   = " -n " + nEvents + " -e " + energy + " -f " + flux + " --seed " + mcseed + \
              " --cross-sections input/" + inputFile + " --event-generator-list " + generatorList
  # loop over keys and generate gevgen command
  for key in nuPDG.iterkeys():
    cmd = "gevgen " + options + " -p " + nuPDG[key] + " -t " + targetPDG[key] + " -r " + key
    logFile = "gevgen_" + key + ".log"
    jobsub.addJob (xsec_n_path + "/" + inputFile, out, logFile, cmd)
  # done
  jobsub.add ("</parallel>")

def fillDAG_GST (jobsub, out):
  # check if job is done already
  if isDoneGST (out):
    msg.warning ("hadronization test gst files found in " + out + " ... " + msg.BOLD + "skipping hadronization:fillDAG_GST\n", 1)
    return
  # not done, add jobs to dag
  msg.info ("\tAdding hadronization test (gst) jobs\n")
  # in parallel mode
  jobsub.add ("<parallel>")
  # loop over keys and generate gntpc command
  for key in nuPDG.iterkeys():
    inputFile = "gntp." + key + ".ghep.root"
    logFile = "gntpc" + key + ".log"
    cmd = "gntpc -f gst -i input/" + inputFile
    jobsub.addJob (out + "/" + inputFile, out, logFile, cmd)
  # done
  jobsub.add ("</parallel>")

def fillDAG_data (jobsub, tag, date, xsec_n_path, outEvents, outRep):
  # check if job is done already
  if isDoneData (tag, date, outRep):
    msg.warning ("hadronization test plots found in " + outRep + " ... " + msg.BOLD + "skipping hadronization:fillDAG_data\n", 1)
    return
  # not done, add jobs to dag
  msg.info ("\tAdding hadronization test (plots) jobs\n")    
  # in serial mode
  jobsub.add ("<serial>")
  inFile  = "file_list-" + tag + "-" + date + ".xml"
  outFile = "genie_" + tag + "-hadronization_test.ps"
  cmd = "gvld_hadronz_test -g input/" + inFile + " -o " + outFile
  # add the command to dag
  inputs = outRep + "/" + inFile + " " + xsec_n_path + "/xsec-vN-" + tag + ".root " + outEvents + "/*.ghep.root"
  logFile = "gvld_hadronz_test.log"
  jobsub.addJob (inputs, outRep, logFile, cmd)
  # done
  jobsub.add ("</serial>")
  
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
  
def isDoneData (tag, date, path):
  # check if given path contains the plots
  if "genie_" + tag + "-hadronization_test.ps" not in os.listdir (path): return False
  return True
  
def createFileList (tag, date, xsec_n_path, outEvent, outRep):
  # create xml file with the file list in the format as src/scripts/production/misc/make_genie_sim_file_list.pl
  xmlFile = outRep + "/file_list-" + tag + "-" + date + ".xml"
  try: os.remove (xmlFile)
  except OSError: pass
  xml = open (xmlFile, 'w');
  print >>xml, '<?xml version="1.0" encoding="ISO-8859-1"?>'
  print >>xml, '<genie_simulation_outputs>'
  print >>xml, '\t<model name="' + tag + '-' + date + '">'
  for key in nuPDG.iterkeys():
    print >>xml, '\t\t<evt_file format="ghep"> input/gntp.' + key + '.ghep.root </evt_file>'
  print >>xml, '\t\t<xsec_file> input/xsec-vN-' + tag + '.root </xsec_file>'
  print >>xml, '\t</model>'
  print >>xml, '</genie_simulation_outputs>'
  xml.close()

