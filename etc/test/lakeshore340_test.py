#!/dls_sw/tools/bin/python2.4

# Test suite to use with pyUnit

from pkg_resources import require
require('dls.autotestframework')
from dls.autotestframework import *

from ls340cases import *
import pyclbr

################################################
# Test suite for the lakeshore340 temperature controller.

class ls340TestSuite(TestSuite):

   def loadCasePlugins(self, testclasses):
      classes = pyclbr.readmodule("ls340cases")
      for c in classes:
         if not (c.endswith("Base")):
            classobj = eval(c)
            if (issubclass(classobj, TestCase)):
               if not (classobj == TestCase):
                  testclasses.append(classobj)

   def createTests(self):
      # Define the targets for this test suite
      # Rename 'dev' to be 'simulation' when the database has been fixed so that the tests work.
      Target("dev", self,
             iocDirectory="iocs/example_sim",
             iocBootCmd="bin/linux-x86/stexample_sim.boot",
             epicsDbFiles="db/example_sim.db",
             simDevices=[SimDevice("controller1", 9001)],
             guiCmds=['edm -m "lakeshore340=mp49:ls340sim" -x data/lakeshore340.edl'])

      testclasses = []
      self.loadCasePlugins(testclasses)
      for testclass in testclasses:
         testclass(self)



################################################
# Main entry point

if __name__ == "__main__":
   # Create and run the test sequence
   ls340TestSuite()
