TOP=../..

include $(TOP)/configure/CONFIG

# -------------------------------
# Build an Diamond Support Module
# -------------------------------

LIBRARY_IOC += lakeshore340

# xxxRecord.h will be created from xxxRecord.dbd
#DBDINC += xxx.h

# lakeshore340.dbd will be installed into <top>/dbd
DBD += lakeshore340.dbd

# lakeshore340.dbd will be created from these files
lakeshore340_DBD += base.dbd
lakeshore340_DBD += asyn.dbd
lakeshore340_DBD += drvVxi11.dbd
ifdef CALC
lakeshore340_DBD += sCalcoutRecord.dbd
lakeshore340_DBD += calc.dbd
endif
lakeshore340_DBD += stream.dbd

#Include files
#INC += xxx.h

# The following are compiled and added to the support library
#xxx_SRCS += xxxCodeA.c
#xxx_SRCS += xxxCodeB.c

# We need to link against the EPICS Base libraries
lakeshore340_LIBS += $(EPICS_BASE_IOC_LIBS)


# The following adds object code from base/src/vxWorks
currAmp_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary


include $(TOP)/configure/RULES
