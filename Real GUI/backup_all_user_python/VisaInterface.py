import visa

rm = visa.ResourceManager()

def ConnectToGPIBInstrument(ControllerID="0", GPIBAddress="5"):
    Instrument=None
    try:
        #Instrument = visa.instrument("GPIB"+ControllerID+"::"+GPIBAddress)
        Instrument = rm.open_resource('GPIB' + ControllerID + '::' + GPIBAddress + "::INSTR")

        #Instrument = VISAHandel.ConnectToLocalLANInstrument(ControllerID="0", TCPIPAddress=TCPIPAddress)



    except visa.VisaIOError:
        print('No Instrument detected on GPIB controllerID='+str(ControllerID)+' GPIBAddress='+str(GPIBAddress))
        Instrument = -1
    finally:
        if Instrument==None:
            print('No Instrument detected on GPIB controllerID='+str(ControllerID)+' GPIBAddress='+str(GPIBAddress))
            Instrument = -1
        return Instrument

def ConnectToLocalLANInstrument(ControllerID="0", TCPIPAddress=""):
    """
    'TCPIP0::10.99.10.200::inst0::INSTR'
    :param ControllerID:
    :param TCPIPAddress:
    :return:
    """
    Instrument=None
    try:
        #Instrument = visa.instrument("TCPIP"+ControllerID+"::"+TCPIPAddress)
        if type(ControllerID)!=str:
            ControllerID=str(ControllerID)
        Instrument=rm.open_resource('TCPIP'+ControllerID+'::'+TCPIPAddress+"::inst"+ControllerID+"::INSTR")
    except visa.VisaIOError:
        print('No Instrument detected on LAN controllerID='+str(ControllerID)+' TCPIPAddress='+str(TCPIPAddress))
        Instrument = -1
    finally:
        if Instrument==None:
            print('No Instrument detected on LAN controllerID='+str(ControllerID)+' TCPIPAddress='+str(TCPIPAddress))
            Instrument = -1
        return Instrument
    return Instrument

def ConnectToLANInstrument(ControllerID="0", TCPIPAddress="10.12.214.137"):
    Instrument=None
    try:
        Instrument = visa.instrument("TCPIP"+ControllerID+"::"+TCPIPAddress)
    except visa.VisaIOError:
        print('No Instrument detected on LAN controllerID='+str(ControllerID)+' TCPIPAddress='+str(TCPIPAddress))
        Instrument = -1
    finally:
        if Instrument==None:
            print('No Instrument detected on LAN controllerID='+str(ControllerID)+' TCPIPAddress='+str(TCPIPAddress))
            Instrument = -1
        return Instrument


def TermChars(Instrument, Chars=""):
    Status = None
    try:
        Status = Instrument.term_chars=Chars
    except AttributeError:
        Status = 'No Instrument'
        print(Status)
    finally:
        return Status

def WriteSCPICmd(Instrument, SCIPICmd):
    Status = None
    try:
        Status = Instrument.write(SCIPICmd)
    except AttributeError:
        Status = 'No Instrument'
        print(Status)
    finally:
        return Status

def ReadResult(Instrument):
    Status = None
    try:
        Status = Instrument.read()
    except AttributeError:
        Status = 'No Instrument'
        print(Status)
    finally:
        return Status

def ReadStatusByte(Instrument):
    Status = None
    try:
        Status = Instrument.stb
    except AttributeError:
        Status = 'No Instrument'
        print (Status)
    finally:
        return Status

def QuerySCPICmd(Instrument, SCIPICmd):
    Status=None
    try:
        Status = Instrument.query(SCIPICmd)#Instrument.ask(SCIPICmd)
    except AttributeError:
        Status = 'No Instrument'
        print (Status)
    finally:
        return Status

def IDNInstrument(Instrument):
    Status = None
    try:
        Status = QuerySCPICmd(Instrument, "*IDN?")
    except AttributeError:
        Status = 'No Instrument'
        print (Status)
    finally:
        return Status



