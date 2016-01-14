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

def fillDAG (tag, date, dag, jobsub, genie_path, xsec_a_path, outEvent, outRep, outRepPs):
  fillDAG_GHEP (tag, dag, jobsub, xsec_a_path, outEvent)
  fillDAG_GST (dag, jobsub, outEvent)
  createFileList (tag, date, xsec_a_path, outEvent, outRep)
  fillDAG_data (tag, date, dag, jobsub, xsec_a_path, outEvent, outRep, outRepPs)

def fillDAG_GHEP (tag, dag, jobsub, xsec_a_path, out):
  # check if job is done already
  if isDoneGHEP (out):
    msg.warning ("xsec validation ghep files found in " + out + " ... " + msg.BOLD + "skipping xsecval:fillDAG_GHEP\n", 1)
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
    msg.warning ("xsec validation gst files found in " + out + " ... " + msg.BOLD + "skipping xsecval:fillDAG_GST\n", 1)
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

def fillDAG_data (tag, date, dag, jobsub, xsec_a_path, outEvents, outRep, outRepPs):
  # check if job is done already
  if isDoneData (tag, date, outRep, outRepPs):
    msg.warning ("xsec validation plots found in " + outRep + " ... " + msg.BOLD + "skipping xsecval:fillDAG_data\n", 1)
    return
  msg.info ("\tAdding xsec validation (data) jobs\n")    
  # single job to generate all GENIE/data comparisons
  print >>dag, "<parallel>"
  # one job for all without errors
  cmd = "gvld_nu_xsec -g input/file_list-" + tag + "-" + date + ".xml " + \
        "-o genie_" + tag + "-" + date + "-world_nu_xsec_data_comp-all-withref"
  cmd = re.sub (' ', "SPACE", cmd)  # temporary solution as workaround for jobsub quotes issue
  print >>dag, jobsub + " -x " + outRep + " -j " + xsec_a_path + " -k " + outEvents + " -o " + outRep + \
               " -l gvld_nu_xsec_all.log -c " + cmd
  # job per comparison with error
  for comp in comparisons:
    cmd = "gvld_nu_xsec -e -g input/file_list-" + tag + "-" + date + ".xml " + \
        "-o genie_" + tag + "-" + date + "-world_nu_xsec_data_comp-" + comp + " -c " + comp
    cmd = re.sub (' ', "SPACE", cmd)  # temporary solution as workaround for jobsub quotes issue
    print >>dag, jobsub + " -x " + outRep + " -j " + xsec_a_path + " -k " + outEvents + " -o " + outRepPs + \
                 " -l gvld_nu_xsec_" + comp + ".log -c " + cmd
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
