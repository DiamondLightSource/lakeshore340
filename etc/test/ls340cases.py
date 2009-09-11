#!/dls_sw/tools/bin/python2.4

from pkg_resources import require
require('dls.autotestframework')
from dls.autotestframework import TestCase

import re

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


class ls340CaseHTR(ls340CaseBase):
   """
   Test case to read HTR value.
   Checks that it is in valid range of (0-100)
   """

   def runTest(self):
      pv = self.getPVBase() + ":HTR"
      self.verifyPvInRange(pv, 0, 100)


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
      #More puts to check it still works
      self.putPv(pvSet, -10)
      self.putPv(pvSet, 100)
      self.putPv(pvSet, 350)
      self.putPv(pvSet, 20)

class ls340CaseKRDG(ls340CaseBase):
   """
   Test case to read the temperature PVs.
   The test just reads the PVs.
   """

   def runTest(self):
      for i in range(0,4):
         pv = self.getPVBase() + ":KRDG" + str(i)
         print pv
         self.getPv(pv)

      
