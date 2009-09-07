#!/bin/env python2.4

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
   """

   def __init__(self):
      pass

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
      serial_device.__init__(self,protocolBranches = ["blah1", "blah2", "blah3", "blah4"], power=True)
      print "Initialising ls340 simulator, V1.0"
      self.temperature1 = 0.0
      self.temperature2 = 0.0
      self.temperature3 = 0.0
      self.temperature4 = 0.0

      self.__ls340data = ls340data()

      self.__channels = ["1","2","3","4"]
        
      return



   def reply(self, command):
      '''This function must be defined. It is called by the serial_sim system
      whenever an asyn command is send down the line. Must return a string
      with a response to the command or None.'''

      result = None
      
      if self.diagnosticLevel() > 0:
         print "ls340::reply. command: " + command

      if (command == "*IDN?"):
         result = self.__ls340data.getIDN()

      elif (command == "HTR?"):
         result = self.__ls340data.getHTR()

      elif (command == "SETP? 1"):
         result = self.__ls340data.getSETP()

      elif (command.startswith("KRDG?")):
         chan = command.split(" ")[1]
         if (self.isChannelNumberOK(chan)):
            result = None
         else:
            result = self.__ls340data.getKRDG()

      elif (command.startswith("SRDG?")):
         chan = command.split(" ")[1]
         if (self.isChannelNumberOK(chan)):
            result = None
         else:
            result = self.__ls340data.getSRDG()

      elif (command == "RANGE?"):
         result = self.__ls340data.getRANGE()

      elif (command == "RAMP?"):
         result = self.__ls340data.getRAMP()

      else:
         #Return nothing in the case of a syntax error.
         result = None
         if self.diagnosticLevel() > 0:
            print "ls340::reply. Command not supported by simulation."

      
        
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





