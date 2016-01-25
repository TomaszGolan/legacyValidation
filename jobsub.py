import msg
import os, re, subprocess

class Jobsub:
  # handle jobsub command for runGENIE.sh in dag file  
  def __init__ (self, args):
    # init a proper jobsub command for dag
    # -n option is mandatory for jobsub (otherwise jobs will be run twice...)
    self.basecmd = "jobsub -n --OS=%s --resource-provides=usage_model=%s -G %s file://%s -p %s -d %s" % \
                   (args.os, args.resource, args.group, args.run, args.builds + "/" + args.buildName, args.debug)
    # create dag file
    self.dagFile = args.paths['top'] + "/legacyValidation-" + args.tag + "-" + args.build_date + ".dag"
    # remove is the file exists
    try: os.remove (self.dagFile)
    except OSError: pass
    # open dag file tp write
    self.dag = open (self.dagFile, 'w')
    # prepare submit commands
    self.setup = "source /cvmfs/fermilab.opensciencegrid.org/products/common/etc/setups.sh; setup jobsub_client; "
    self.subdag = "jobsub_submit_dag -G " + args.group + " file://" + self.dagFile
  
  # close and submit dag
  def submit(self):
    self.dag.close()
    msg.info ("Done with dag file. Ready to submit.\n")
    # check if run is not empty
    if os.stat(self.dagFile).st_size == 0:
      msg.warning ("Dag file: " + self.dagFile + " is empty. " + msg.RED + msg.BOLD + "NO JOBS TO RUN!!!\n")
      exit (0)
    # submit dag
    msg.info ("Submitting: " + self.dagFile + "\n")
    subprocess.Popen (self.setup + self.subdag, shell=True, executable="/bin/bash")

  # print given command with given options to dag file (input files to copy, path for output, logfilename, command)
  def addJob (self, inputs, output, logfile, cmd):
    cmd = re.sub (' ', "SPACE", cmd)   # temporary solution as workaround for jobsub quotes issue
    inputs = re.sub (' ', "SPACE", inputs) # temporary solution as workaround for jobsub quotes issue
    # write full jobsub command to dag file
    print >>self.dag, self.basecmd + \
                      " -i " + inputs + \
                      " -o " + output + \
                      " -l " + logfile + \
                      " -c " + cmd
                      
  # print custom text to dag
  def add (self, text):
    print >>self.dag, text
    
