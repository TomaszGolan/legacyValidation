# handle jenkins artifacts

import ast, urllib, sys, msg, os, tarfile

url = "https://buildmaster.fnal.gov/view/GENIE/job/jenkinsTest/lastSuccessfulBuild/"

def getBuildList():
  # check available artifacts at jenkins
  artifacts = []
  # url/api/python['artifacts'] returns the list of dictionaries for artifacts, we just need files names
  for artifact in ast.literal_eval (urllib.urlopen(url + "/api/python").read())['artifacts']:
    artifacts.append (artifact['fileName'])
  return artifacts  

def getTagList (tag):
  # check available artifacts with given tag at jenkins
  artifacts = []
  # url/api/python['artifacts'] returns the list of dictionaries for artifacts, we just need files names
  for artifact in ast.literal_eval (urllib.urlopen(url + "/api/python").read())['artifacts']:
    if tag in artifact['fileName']: artifacts.append (artifact['fileName'])
  return artifacts 
  
def findLast (tag):
  # find the most recent build for given tag
  if getTagList(tag): return sorted(getTagList(tag))[-1][-14:-4]
  else: return "[no build for " + tag + "]"
  
def getBuild (tag, date, path):
  # get build with defined tag and date and save in path 
  buildName = "genie_" + tag + "_buildmaster_" + date
  # check if build aready exists
  if os.path.isdir (path + "/" + buildName):
    msg.warning (path + "/" + buildName + " already exists ... " + msg.BOLD + "skipping jenkins:getBuild\n")
    return buildName
  # no build
  tarball = buildName + ".tgz"
  # check it build available
  if tarball not in getBuildList():
    msg.error ("There is no artifact for " + msg.BOLD + tarball + "\n")
    print "Available artifacts:\n"
    for artifact in getBuildList(): print "\t" + artifact + "\n"
    sys.exit (1)
  # download build
  msg.info ("Downloading " + msg.BOLD + tarball)
  urllib.urlretrieve (url + "/artifact/genie_builds/" + tarball, path + "/" + tarball)
  # extract the build
  msg.info ("Extracting to " + msg.BOLD + path + "/" + buildName + "\n")
  tarfile.open(path + "/" + tarball, 'r').extractall(path + "/" + buildName)
  # return buildName
  return buildName
