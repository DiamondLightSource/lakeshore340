#!/dls_sw/tools/bin/python2.4

# Test suite to use with pyUnit

from pkg_resources import require
require('dls.autotestframework')
from dls.autotestframework import *

################################################
# Test suite for the lakeshore340 temperature controller.
    
class ls340TestSuite(TestSuite):
   
   def createTests(self):
      # Define the targets for this test suite
      Target("simulation", self,
             iocDirectory="iocs/example_sim",
             iocBootCmd="bin/linux-x86/stexample_sim.boot",
             epicsDbFiles="db/example_sim.db",
             environment=[('EPICS_CA_REPEATER_PORT','6065'),('EPICS_CA_SERVER_PORT','6064')],
             guiCmds=['edm -m "lakeshore340=mp49:ls340sim" -x data/lakeshore340.edl'])
      
      # The tests
      ls340CaseGetID(self)
      
      
       
################################################
# Intermediate test case class that provides some utility functions
# for this suite


class ls340CaseBase(TestCase):
   
   def __init__(self, A):
      TestCase.__init__(self, A)
      self.__pvbase = "mp49:ls340sim"

   def getPVBase(self):
      return self.__pvbase
      


################################################
# Test cases


class ls340CaseGetID(ls340CaseBase):
   
   def runTest(self):
      '''Read the IDN string.'''
      
      pv = self.getPVBase() + ":ID"
      print "pv is: " + pv
      
      id = self.getPv(pv)
      
      print "id is: " + id
      


################################################
# Main entry point

if __name__ == "__main__":
   # Create and run the test sequence
   ls340TestSuite()
