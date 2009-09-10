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
             simDevices=[SimDevice("controller1", 9001)],
             environment=[('EPICS_CA_REPEATER_PORT','6065'),('EPICS_CA_SERVER_PORT','6064')],
             guiCmds=['edm -m "lakeshore340=mp49:ls340sim" -x data/lakeshore340.edl'])
      
      # The tests
      ls340CaseGetID(self)
      ls340CaseSETP(self)
      
      
       
################################################
# Intermediate test case class that provides some utility functions
# for this suite


class ls340CaseBase(TestCase):
   """
   Base class for all lakeshore340 test cases.
   This is where the base PV is hardcoded to be 'mp49:ls340sim'
   """
   
   def __init__(self, A):
      TestCase.__init__(self, A)
      self.__pvbase = "mp49:ls340sim"

   def getPVBase(self):
      return self.__pvbase
      


################################################
# Test cases


class ls340CaseGetID(ls340CaseBase):
   """
   Test case to read the ID string.
   The test just checks that the string is in the correct format.
   """
   
   def runTest(self):
      
      pv = self.getPVBase() + ":ID"
      
      val = self.getPv(pv)

      regex = re.compile('^LSCI,MODEL340,.{6},.{8}')
      if (not(regex.match(val))):
         self.fail(str("ID string did not match expected format. Got: " + val))

      
class ls340CaseSETP(ls340CaseBase):
   """
   Test case to set and read the SETP PV.
   It does not check that the readback is correct (don't know what range to check..)
   """

   def runTest(self):
      pv = self.getPVBase() + ":SETP"
      pvSet = pv + "_S"

      self.putPv(pvSet, 23)
      val = self.getPv(pv)
      #Couple more puts to check it still works
      self.putPv(pvSet, 0)
      self.putPv(pvSet, 100)
   




################################################
# Main entry point

if __name__ == "__main__":
   # Create and run the test sequence
   ls340TestSuite()
