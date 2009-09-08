TOP=../..

include $(TOP)/configure/CONFIG



PROD_IOC = example_sim

# example_sim.dbd will be installed into <top>/dbd
DBD += example_sim.dbd

# example_sim.dbd will be created from these files
example_sim_DBD += base.dbd
example_sim_DBD += asyn.dbd
example_sim_DBD += drvVxi11.dbd
example_sim_DBD += stream.dbd
example_sim_DBD += drvAsynSerialPort.dbd
example_sim_DBD += drvAsynIPPort.dbd
example_sim_DBD += lakeshore340.dbd
example_sim_DBD += pyDrv.dbd
#example_sim_DBD += xxx.dbd

# example_sim_registerRecordDeviceDriver.cpp will be created
# example_sim.dbd
example_sim_SRCS += example_sim_registerRecordDeviceDriver.cpp

# These two lines are needed for non-vxWorks builds, such as Linux
example_sim_SRCS_DEFAULT += example_simMain.cpp
example_sim_SRCS_vxWorks += -nil-

# Add locally compiled object code
#example_sim_SRCS +=

# The following adds object code from base/src/vxWorks
example_sim_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# This line says that this IOC Application depends on the
# xxx Support Module
#example_sim_LIBS += xxx
example_sim_LIBS += asyn
example_sim_LIBS += stream
example_sim_LIBS += pyDrv


# We need to link this IOC Application against the EPICS Base libraries
example_sim_LIBS += $(EPICS_BASE_IOC_LIBS)


include $(TOP)/configure/RULES
