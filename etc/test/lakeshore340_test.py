#!/dls_sw/tools/bin/python2.4

# Test suite to use with pyUnit

from pkg_resources import require
require('dls.autotestframework')
from dls.autotestframework import *

from cases import *
import pyclbr

################################################
# Test suite for the lakeshore340 temperature controller.
    
class ls340TestSuite(TestSuite):

   def loadCasePlugins(self):
      classes = pyclbr.readmodule("cases")
      for c in classes:
         if not (c.endswith("Base")):
            classobj = eval(c)
            classinstance = classobj(self)
         

   
   def createTests(self):
      # Define the targets for this test suite
      Target("simulation", self,
             iocDirectory="iocs/example_sim",
             iocBootCmd="bin/linux-x86/stexample_sim.boot",
             epicsDbFiles="db/example_sim.db",
             simDevices=[SimDevice("controller1", 9001)],
             environment=[('EPICS_CA_REPEATER_PORT','6065'),('EPICS_CA_SERVER_PORT','6064')],
             guiCmds=['edm -m "lakeshore340=mp49:ls340sim" -x data/lakeshore340.edl'])

      self.loadCasePlugins()
      
     


################################################
# Main entry point

if __name__ == "__main__":
   # Create and run the test sequence
   ls340TestSuite()
