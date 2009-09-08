#!/dls_sw/tools/bin/python2.4

from pkg_resources import require
require('dls_serial_sim==1.7')
from dls_serial_sim import serial_device
import re, os

from random import randrange
from random import random


class ls340data(object):
   """
   Class to deal with return data for the lakeshore 340 simulation.
   For each command, this class generates an appropriate response.
   The class can also hold state.

   At the moment setting parameter has no effect on what is read back.
   The numbers read back are all random numbers.
   """

   def __init__(self):
      self.__setp = 0.0
      self.__range = 0
      self.__ramponoff = 0
      self.__ramprate = 0.0
      self.__mout = 0.0
      self.__p = 0.0
      self.__i = 0.0
      self.__d = 0.0
      self.__cmode = 1

   def setSETP(self, val):
      self.__setp = float(val)

   def setRANGE(self, val):
      ival = int(val)
      if ((ival >= 0) and (ival <= 5)):
         self.__range = ival

   def setRAMP(self, onoff, val):
      ionoff = int(onoff)
      fval = float(val)
      if ((ionoff == 0) or (ionoff == 1)):
         self.__ramponoff = ionoff
         self.__ramprate = fval

   def setMOUT(self, val):
      fval = float(val)
      if ((fval >= 0) and (fval <=100.0)):
         self.__mout = fval

   def setPID(self, p, i, d):
      self.__p = float(p)
      if (i != None):
         self.__i = float(i)
      if (d != None):
         self.__d = float(d)

   def setCMODE(self, cmode):
      icmode = int(cmode)
      if ((icmode > 0) and (icmode < 7)):
         self.__cmode = icmode

   def getIDN(self):
      return "LSCI,MODEL340,123456,02032001"

   def getHTR(self):
      return self.returnRateTypeString()

   def getSETP(self):
      return self.returnTempTypeString()

   def getKRDG(self):
      return self.returnTempTypeString()

   def getSRDG(self):
      return self.returnTempTypeString()

   def getRANGE(self):
      return str(randrange(0, 6, 1))

   def getRAMP(self):
      rand1 = randrange(0, 2, 1)
      return str(rand1) + "," + self.returnRateTypeString()

   def getMOUT(self):
      return self.returnRateTypeString()

   def getPID(self):
      rand1 = randrange(0, 1001, 1)
      rand2 = randrange(0, 10, 1)
      rand3 = randrange(0, 1001, 1)
      rand4 = randrange(0, 10, 1)
      rand5 = randrange(0, 1001, 1)
      
      if (rand1 == 1000):
         rand2 = 0

      if (rand3 == 1000):
         rand4 = 0
      
      return str(rand1) + "." + str(rand2) + "," + str(rand3) + "." + str(rand4) + "," + str(rand5)

   def getCMODE(self):
      rand1 = randrange(1, 7, 1)
      return str(rand1)

   def getTUNEST(self):
      rand1 = randrange(0, 2, 1)
      return str(rand1)

   def returnRateTypeString(self):
      """
      Returns a string random number in this format: 000.0
      """
      rand1 = randrange(0, 101, 1)
      rand2 = randrange(0, 10, 1)
      if (rand1 == 100):
         rand2 = 0
         
      strrand1 = str(rand1)
      strrand2 = str(rand2)
      
      return strrand1 + "." + strrand2

   

   def returnTempTypeString(self):
      """
      Returns a string in this format: +000.000E+0
      The signs are random.
      All numbers are random.
      """
      rand1 = randrange(0, 101, 1)
      rand2 = randrange(0, 101, 1)
      rand3 = randrange(0, 10, 1)

      sign = random()
      signstr1 = "-"
      if (sign < 0.5):
         signstr1 = "+"

      sign = random()
      signstr2 = "-"
      if (sign < 0.5):
         signstr2 = "+"
      
      return signstr1 + str(rand1) + "." + str(rand2) + "E" + signstr2 + str(rand3)


   

class ls340(serial_device):
   Terminator = "\r\n"
    
   def __init__(self):
      '''Constructor.  Remember to call the base class constructor.'''

      protocolBranches = ["*IDN?", "HTR?", "SETP?", "KRDG?", "SRDG?", "RANGE?", "RAMP?", "MOUT?", "PID?",
                          "CMODE?", "TUNEST?", "SETP", "RANGE", "RAMP", "MOUT", "PID_P", "PID_I", "PID_D", "CMODE"]
      
      serial_device.__init__(self, protocolBranches, power=True)
      print "Initialising ls340 simulator, V1.0"

      self.__ls340data = ls340data()

      #Valid channel numbers
      self.__channels = ["0","1","2","3"]
        
      return



   def reply(self, command):
      '''This function must be defined. It is called by the serial_sim system
      whenever an asyn command is send down the line. Must return a string
      with a response to the command or None.'''

      result = None
      
      if self.diagnosticLevel() > 0:
         print "ls340::reply. command: " + repr(command)

      if (command == "*IDN?"):
         result = self.__ls340data.getIDN()
         self.covered("*IDN?")

      elif (command == "HTR?"):
         result = self.__ls340data.getHTR()
         self.covered("HTR?")

      elif (command == "SETP? 1"):
         result = self.__ls340data.getSETP()
         self.covered("SETP?")

      elif (command.startswith("KRDG?")):
         chan = command.split(" ")[1]
         if (self.isChannelNumberOK(chan)):
            result = None
         else:
            result = self.__ls340data.getKRDG()
         self.covered("KRDG?")

      elif (command.startswith("SRDG?")):
         chan = command.split(" ")[1]
         if (self.isChannelNumberOK(chan)):
            result = None
         else:
            result = self.__ls340data.getSRDG()
         self.covered("SRDG?")

      elif (command == "RANGE?"):
         result = self.__ls340data.getRANGE()
         self.covered("RANGE?")

      elif (command == "RAMP? 1"):
         result = self.__ls340data.getRAMP()
         self.covered("RAMP?")

      elif (command == "MOUT? 1"):
         result = self.__ls340data.getMOUT()
         self.covered("MOUT?")

      elif (command == "PID? 1"):
         result = self.__ls340data.getPID()
         self.covered("PID?")

      elif (command == "CMODE? 1"):
         result = self.__ls340data.getCMODE()
         self.covered("CMODE?")

      elif (command == "TUNEST?"):
         result = self.__ls340data.getTUNEST()
         self.covered("TUNEST?")

      #Set functions

      elif (command.startswith("SETP 1,")):
         val = command.split(",")[1]
         self.__ls340data.setSETP(val)
         self.covered("SETP")

      elif (command.startswith("RANGE ")):
         val = command.split(" ")[1]
         self.__ls340data.setRANGE(val)
         self.covered("RANGE")

      elif (command.startswith("RAMP 1")):
         val_onoff = command.split(",")[1]
         val_rate = command.split(",")[2]
         self.__ls340data.setRAMP(val_onoff, val_rate)
         self.covered("RAMP")

      elif (command.startswith("MOUT 1")):
         val = command.split(",")[1]
         self.__ls340data.setMOUT(val)
         self.covered("MOUT")

      elif (command.startswith("PID 1")):
         vals = command.split(",")
         val_p = vals[1]
         val_i = None
         val_d = None
         if (len(vals) > 2):
            val_i = vals[2]
         if (len(vals) > 3):
            val_d = vals[3]
         self.__ls340data.setPID(val_p, val_i, val_d)
         self.covered("PID_P")
         if (val_i != None):
            self.covered("PID_I")
         if (val_d != None):
            self.covered("PID_D")

      elif (command.startswith("CMODE 1")):
         val = command.split(",")[1]
         self.__ls340data.setCMODE(val)
         self.covered("CMODE")

      else:
         #Return nothing in the case of a syntax error (that's what the lakeshore does)
         result = None
         if self.diagnosticLevel() > 0:
            print "ls340::reply. Command not supported by simulation."

      if self.diagnosticLevel() > 0:
         print "ls340::reply. result: " + repr(command)
        
      return result

   def isChannelNumberOK(self, channel):
      """
      Check that the channel number is in the __channels list
      Returns True (channel is valid) or False (channel is not valid).
      """
      chanError = 0
      for c in self.__channels:
         if (channel != c):
            chanError = chanError+1
      if (chanError == 4):
         return True
      else:
         return False



   def initialise(self):
      '''Called by the framework when the power is switched on.'''
      print "ls340::initialise. Power on."

        

if __name__ == "__main__":
    # little test function that runs only when you run this file
    dev = ls340()
    dev.start_ip(9015)
    dev.start_debug(9016)
    # do a raw_input() to stop the program exiting immediately
    raw_input()





