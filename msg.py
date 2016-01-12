VIOLET    = '\033[95m'
BLUE      = '\033[94m'
GREEN     = '\033[92m'
YELLOW    = '\033[93m'
RED       = '\033[91m'
BOLD      = '\033[1m'
UNDERLINE = '\033[4m'
END       = '\033[0m'

def warning (text):
  print YELLOW + "WARNING: " + text + END
  
def error (text):
  print RED + "ERROR: " + text + END
  
def info (text):
  print VIOLET + text + END
