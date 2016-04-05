# create proper xml filelist to do xsec comparisons between models

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

def createFileList (args):
  # create xml file with the file list in the format as src/scripts/production/misc/make_genie_sim_file_list.pl
  xmlFile = args.out + "/xsec_list-"
  for i in range(len(args.tags)):
    xmlFile += args.tags[i] + "_" + args.dates[i]
    if i + 1 != len(args.tags): xmlFile += "_vs_"
  xmlFile += ".xml"
  try: os.remove (xmlFile)
  except OSError: pass
  xml = open (xmlFile, 'w');
  print >>xml, '<?xml version="1.0" encoding="ISO-8859-1"?>'
  print >>xml, '<genie_simulation_outputs>'

  for i in range(len(args.tags)):
    print >>xml, '\t<model name="' + args.tags[i] + '-' + args.dates[i] + '">'
    ghepPath = args.topdir + "/" + args.tags[i] + "/" + args.dates[i] + "/events/xsec_validation"
    xsecPath = args.topdir + "/" + args.tags[i] + "/" + args.dates[i] + "/xsec/nuA"
    for key in nuPDG.iterkeys():
      print >>xml, '\t\t<evt_file format="ghep"> ' + ghepPath + '/gntp.' + key + '.ghep.root </evt_file>'
    print >>xml, '\t\t<xsec_file> ' + xsecPath + '/xsec-vA-' + args.tags[i] + '.root </xsec_file>'
    print >>xml, '\t</model>'

  print >>xml, '</genie_simulation_outputs>'
  xml.close()
  return xmlFile
