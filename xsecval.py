# fill dag with neutrino xsec validation (comparisons with data) jobs

import msg
import os

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
flux = "1/x"

comparisons = ["numuCC_all", "numubarCC_all", "numuCC_lowE", "numubarCC_lowE", "numuCC_highE", "numubarCC_highE", 
               "numuCC_minos", "numubarCC_minos", "numuCC_sciboone", "r_minos", "numuCCQE_all", "numuCCQE_deuterium", 
               "numuCCQE_heavy_target", "numuCCQE_nomad_nucleon", "numuCCQE_nomad_nuclear", 
               "numuCCQE_miniboone_nuclear", "numuCCQE_all_12C_nuclear", "numubarCCQE_all", "numubarCCQE_deuterium", 
               "numubarCCQE_heavy_target", "numubarCCQE_nomad_nucleon", "numubarCCQE_nomad_nuclear", "numuCCppip", 
               "numuCCnpip", "numuCCppi0", "numuCCn2pip",  "numuCCppippi0",  "numuCCppippim", "numuCCpi0_numuCCQE_k2k", 
               "numuNCcohpi0_Ne20", "numuCCcohpip_Ne20", "numubarCCcohpim_Ne20", "numuNCcohpi0_Al27",
               "numuNCcohpi0_Si30", "numuCCcohpip_Si30", "numubarCCcohpim_Si30", "numuCC_dilepton_ratio_worldavg", 
               "numubarCC_dilepton_ratio_worldavg", "numuCC_charm_ratio_worldavg", "numuCC_dilepton_cdhs", 
               "numuCC_dilepton_nomad", "numuCC_dilepton_e744_e770", "numuCC_dilepton_e744", "numuCC_dilepton_fnal15ft",
               "numuCC_dilepton_gargamelle"]

def fillDAG (jobsub, tag, date, paths):
  fillDAG_GHEP (jobsub, tag, paths['xsec_A'], paths['xsecval'])
  fillDAG_GST (jobsub, paths['xsecval'])
  createFileList (tag, date, paths['xsec_A'], paths['xsecval'], paths['xseclog'])
  fillDAG_data (jobsub, tag, date, paths['xsec_A'], paths['xsecval'], paths['xseclog'], paths['xsecsng'])

def fillDAG_GHEP (jobsub, tag, xsec_a_path, out):
  # check if job is done already
  if isDoneGHEP (out):
    msg.warning ("xsec validation ghep files found in " + out + " ... " + msg.BOLD + "skipping xsecval:fillDAG_GHEP\n", 1)
    return
  #not done, add jobs to dag
  msg.info ("\tAdding xsec validation (ghep) jobs\n")
  # in parallel mode
  jobsub.add ("<parallel>")
  # common configuration
  inputFile = "gxspl-vA-" + tag + ".xml"
  options   = " -n " + nEvents + " -e " + energy + " -f " + flux + " --seed " + mcseed + \
              " --cross-sections input/" + inputFile + " --event-generator-list " + generatorList
  # loop over keys and generate gevgen command
  for key in nuPDG.iterkeys():
    cmd = "gevgen " + options + " -p " + nuPDG[key] + " -t " + targetPDG[key] + " -r " + key
    logFile = "gevgen_" + key + ".log"
    jobsub.addJob (xsec_a_path + "/" + inputFile, out, logFile, cmd)
  # done
  jobsub.add ("</parallel>")

def fillDAG_GST (jobsub, out):
  # check if job is done already
  if isDoneGST (out):
    msg.warning ("xsec validation gst files found in " + out + " ... " + msg.BOLD + "skipping xsecval:fillDAG_GST\n", 1)
    return
  # not done, add jobs to dag
  msg.info ("\tAdding xsec validation (gst) jobs\n")
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

def fillDAG_data (jobsub, tag, date, xsec_a_path, outEvents, outRep, outRepSng):
  # check if job is done already
  if isDoneData (tag, date, outRep, outRepSng):
    msg.warning ("xsec validation plots found in " + outRep + " ... " + msg.BOLD + "skipping xsecval:fillDAG_data\n", 1)
    return
  # not done, add jobs to dag
  msg.info ("\tAdding xsec validation (data) jobs\n")    
  # in parallel mode
  jobsub.add ("<parallel>")
  # one job for all comparisons without errors
  inFile  = "file_list-" + tag + "-" + date + ".xml"
  outFile = "genie_" + tag + "-" + date + "-world_nu_xsec_data_comp-all-withref"
  cmd = "gvld_nu_xsec -g input/" + inFile + " -o " + outFile
  # add the command to dag
  inputs = outRep + "/" + inFile + " " + xsec_a_path + "/xsec-vA-" + tag + ".root " + outEvents + "/*.ghep.root"
  logFile = "gvld_nu_xsec_all.log"
  jobsub.addJob (inputs, outRep, logFile, cmd)
  # job per comparison with error
  for comp in comparisons:
    outFile = "genie_" + tag + "-" + date + "-world_nu_xsec_data_comp-" + comp
    cmd = "gvld_nu_xsec -e -g input/" + inFile + " -o " + outFile + " -c " + comp
    logFile = "gvld_nu_xsec_" + comp + ".log"
    jobsub.addJob (inputs, outRepSng, logFile, cmd)
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
  
def isDoneData (tag, date, path, path2):
  # check if given path contains all plots
  if "genie_" + tag + "-" + date + "-world_nu_xsec_data_comp-all-withref.ps" not in os.listdir (path): return False
  for comp in comparisons:
    if "genie_" + tag + "-" + date + "-world_nu_xsec_data_comp-" + comp + ".ps" not in os.listdir (path2): return False
  return True
  
def createFileList (tag, date, xsec_a_path, outEvent, outRep):
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
  print >>xml, '\t\t<xsec_file> input/xsec-vA-' + tag + '.root </xsec_file>'
  print >>xml, '\t</model>'
  print >>xml, '</genie_simulation_outputs>'
  xml.close()
