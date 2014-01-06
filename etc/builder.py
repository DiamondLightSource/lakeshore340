from iocbuilder import AutoSubstitution
from iocbuilder.modules.streamDevice import AutoProtocol

class lakeshore340(AutoSubstitution, AutoProtocol):
    # Substitution attributes
    TemplateFile = 'lakeshore340.template'

    # AutoProtocol attributes
    ProtocolFiles = ['lakeshore340.proto']


